"""
Serialization and payload optimization utility for the NextGen surveillance dashboard.
Quantizes float values and handles brotli/gzip compression for static client-side loading.
"""

import gzip
import json
import os
from typing import Any, Dict, List, Union


def round_floats(obj: Any, precision: int = 4) -> Any:
    """Recursively round floats in nested dictionaries/lists to minimize payload bytes."""
    if isinstance(obj, float):
        return round(obj, precision)
    elif isinstance(obj, dict):
        return {k: round_floats(v, precision) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [round_floats(x, precision) for x in obj]
    return obj


def write_json_payload(
    data: Union[Dict, List],
    output_path: str,
    compress_gzip: bool = True,
    precision: int = 4,
) -> int:
    """
    Writes data as formatted JSON and optionally generates .gz companion file.
    Returns size in bytes of the written file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    optimized_data = round_floats(data, precision=precision)

    json_str = json.dumps(optimized_data, separators=(",", ":"))
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json_str)

    raw_size = os.path.getsize(output_path)

    if compress_gzip:
        gz_path = output_path + ".gz"
        with gzip.open(gz_path, "wt", encoding="utf-8", compresslevel=9) as fgz:
            fgz.write(json_str)

    return raw_size
