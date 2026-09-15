"""
S3 and HTTP client for downloading and streaming Nextstrain data assets.
Directly communicates with https://nextstrain-data.s3.amazonaws.com without requiring AWS credentials.
"""

import gzip
import json
import lzma
import os
import shutil
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Tuple

try:
    import zstandard as zstd
except ImportError:
    zstd = None

S3_BASE_URL = "https://nextstrain-data.s3.amazonaws.com"
DEFAULT_CACHE_FILE = "state/cache_manifest.json"


def get_s3_metadata(key: str) -> Optional[Dict[str, Any]]:
    """Retrieve object metadata via HEAD request."""
    clean_key = key.lstrip("/")
    url = f"{S3_BASE_URL}/{clean_key}"
    req = urllib.request.Request(url, method="HEAD")
    req.add_header("User-Agent", "NextGenSurveillance/1.0")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            headers = dict(resp.headers)
            return {
                "url": url,
                "key": clean_key,
                "etag": headers.get("ETag", "").strip('"'),
                "sha256": headers.get("x-amz-meta-sha256sum", ""),
                "last_modified": headers.get("Last-Modified", ""),
                "content_length": int(headers.get("Content-Length", 0)),
                "content_type": headers.get("Content-Type", ""),
            }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    except Exception as e:
        print(f"[Warning] Failed to fetch HEAD for {url}: {e}")
        return None


def list_s3_keys(prefix: str, max_keys: int = 100) -> List[Dict[str, Any]]:
    """List S3 keys matching prefix using the S3 REST XML API."""
    url = f"{S3_BASE_URL}/?prefix={prefix}&max-keys={max_keys}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "NextGenSurveillance/1.0")

    results = []
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            xml_content = resp.read()
            root = ET.fromstring(xml_content)
            ns = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
            for c in root.findall("s3:Contents", ns):
                key = c.find("s3:Key", ns).text
                size = int(c.find("s3:Size", ns).text)
                etag = c.find("s3:ETag", ns).text.strip('"')
                last_mod = c.find("s3:LastModified", ns).text
                results.append({
                    "key": key,
                    "size": size,
                    "etag": etag,
                    "last_modified": last_mod,
                })
    except Exception as e:
        print(f"[Error] Failed to list S3 keys for prefix '{prefix}': {e}")
    return results


def load_cache_manifest(cache_path: str = DEFAULT_CACHE_FILE) -> Dict[str, Any]:
    """Load local cache metadata file."""
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_cache_manifest(manifest: Dict[str, Any], cache_path: str = DEFAULT_CACHE_FILE) -> None:
    """Save local cache metadata file."""
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)


def decompress_stream(in_path: str, out_path: str) -> None:
    """Decompress .xz, .zst, or .gz file to out_path based on magic bytes."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(in_path, "rb") as f:
        magic = f.read(4)

    # Magic byte detection:
    # XZ: \xfd7zX (fd 37 7a 58)
    # GZIP: \x1f\x8b (1f 8b)
    # ZSTD: \x28\xb5\x2f\xfd (28 b5 2f fd)
    if magic.startswith(b"\xfd7zX") or in_path.endswith(".xz"):
        with lzma.open(in_path, "rb") as fin, open(out_path, "wb") as fout:
            shutil.copyfileobj(fin, fout)
    elif magic.startswith(b"\x1f\x8b") or in_path.endswith(".gz"):
        with gzip.open(in_path, "rb") as fin, open(out_path, "wb") as fout:
            shutil.copyfileobj(fin, fout)
    elif magic.startswith(b"(\xb5/\xfd") or in_path.endswith(".zst"):
        if zstd is None:
            raise RuntimeError("zstandard package is required to decompress .zst files")
        dctx = zstd.ZstdDecompressor()
        with open(in_path, "rb") as fin, open(out_path, "wb") as fout:
            dctx.copy_stream(fin, fout)
    else:
        # plain uncompressed copy
        shutil.copyfile(in_path, out_path)


def download_s3_file(
    key: str,
    dest_path: str,
    decompress: bool = True,
    force: bool = False,
    cache_path: str = DEFAULT_CACHE_FILE,
) -> Tuple[str, bool]:
    """
    Downloads an S3 file if remote differs from cache.
    Returns (local_file_path, downloaded_flag).
    """
    clean_key = key.lstrip("/")
    manifest = load_cache_manifest(cache_path)
    cached_info = manifest.get(clean_key, {})

    remote_meta = get_s3_metadata(clean_key)
    if not remote_meta:
        raise FileNotFoundError(f"Key '{clean_key}' not found on {S3_BASE_URL}")

    # Determine uncompressed destination path
    final_output = dest_path
    if decompress and any(clean_key.endswith(ext) for ext in [".xz", ".zst", ".gz"]):
        for ext in [".xz", ".zst", ".gz"]:
            if final_output.endswith(ext):
                final_output = final_output[:-len(ext)]
                break

    # Check cache match
    if not force and os.path.exists(final_output):
        if cached_info.get("etag") == remote_meta.get("etag") and cached_info.get("etag"):
            return final_output, False

    # Perform download
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    temp_download = dest_path + ".tmp"
    url = remote_meta["url"]

    print(f"Downloading {url} -> {dest_path}...")
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "NextGenSurveillance/1.0")

    with urllib.request.urlopen(req, timeout=120) as resp, open(temp_download, "wb") as fout:
        shutil.copyfileobj(resp, fout)

    if decompress and any(clean_key.endswith(ext) for ext in [".xz", ".zst", ".gz"]):
        decompress_stream(temp_download, final_output)
        os.remove(temp_download)
    else:
        os.rename(temp_download, dest_path)
        final_output = dest_path

    # Update cache manifest
    manifest[clean_key] = remote_meta
    save_cache_manifest(manifest, cache_path)

    return final_output, True
