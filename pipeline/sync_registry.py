#!/usr/bin/env python3
"""
pipeline/sync_registry.py
Dynamic crawler and discovery engine for Nextstrain S3 repository.
Scans data.nextstrain.org manifests across Tier 1, 2, and 3 pathogens.
"""

import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List

# Add parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.utils.s3_client import get_s3_metadata, list_s3_keys, load_cache_manifest
from pipeline.utils.serialization import write_json_payload

REGISTRY_CONFIG = "config/pathogen_registry.json"
OUTPUT_REGISTRY_DATA = "static/data/registry.json"


def inspect_pathogen_target(pathogen: Dict[str, Any]) -> Dict[str, Any]:
    """Inspect S3 files available for a given pathogen entry."""
    pid = pathogen["id"]
    prefix = pathogen["s3_workflow_prefix"]
    print(f"-> Inspecting {pathogen['name']} ({pid}) under s3://nextstrain-data/{prefix}...")

    # Query S3 listing
    keys = list_s3_keys(prefix, max_keys=50)

    # Find metadata and sequence files
    fasta_candidates = []
    metadata_candidates = []
    tree_candidates = []
    json_candidates = []

    for k in keys:
        key_name = k["key"]
        if any(ext in key_name for ext in [".fasta", ".fa", ".fna"]):
            fasta_candidates.append(k)
        elif any(ext in key_name for ext in ["metadata.tsv", "metadata.csv"]):
            metadata_candidates.append(k)
        elif any(ext in key_name for ext in [".nwk", "tree"]):
            tree_candidates.append(k)
        elif key_name.endswith(".json"):
            json_candidates.append(k)

    # Determine primary files
    primary_fasta = None
    if fasta_candidates:
        # Prefer default gene if available
        def_gene = pathogen.get("default_gene", "").lower()
        matched = [k for k in fasta_candidates if def_gene and f"/{def_gene}/" in k["key"].lower()]
        primary_fasta = matched[0] if matched else fasta_candidates[0]

    primary_meta = metadata_candidates[0] if metadata_candidates else None
    primary_tree = tree_candidates[0] if tree_candidates else None

    # Get latest update timestamp
    all_timestamps = [k["last_modified"] for k in keys if "last_modified" in k]
    latest_update = max(all_timestamps) if all_timestamps else datetime.utcnow().isoformat()

    return {
        "id": pid,
        "name": pathogen["name"],
        "tier": pathogen["tier"],
        "cadence": pathogen["cadence"],
        "focal_protein": pathogen.get("focal_protein", ""),
        "pdb_id": pathogen.get("pdb_id", ""),
        "active": pathogen.get("active", True),
        "total_files_discovered": len(keys),
        "primary_fasta": primary_fasta["key"] if primary_fasta else None,
        "primary_metadata": primary_meta["key"] if primary_meta else None,
        "primary_tree": primary_tree["key"] if primary_tree else None,
        "last_upstream_update": latest_update,
    }


def main():
    print("=" * 70)
    print("NextGen Surveillance Platform: Dynamic Registry Discovery Scanner")
    print("=" * 70)

    if not os.path.exists(REGISTRY_CONFIG):
        print(f"[Error] Missing registry config: {REGISTRY_CONFIG}")
        sys.exit(1)

    with open(REGISTRY_CONFIG, "r", encoding="utf-8") as f:
        config = json.load(f)

    pathogens = config.get("pathogens", [])
    print(f"Loaded {len(pathogens)} configured pathogen targets from {REGISTRY_CONFIG}\n")

    registry_report = []
    for p in pathogens:
        try:
            info = inspect_pathogen_target(p)
            registry_report.append(info)
            status_symbol = "✓" if info["primary_fasta"] and info["primary_metadata"] else "⚠"
            print(f"   {status_symbol} Discovered {info['total_files_discovered']} files | Fast: {bool(info['primary_fasta'])} | Meta: {bool(info['primary_metadata'])} | Updated: {info['last_upstream_update']}")
        except Exception as e:
            print(f"   ✗ Error scanning {p['id']}: {e}")

    # Write static output payload
    output_payload = {
        "scan_time": datetime.utcnow().isoformat() + "Z",
        "total_pathogens": len(registry_report),
        "pathogens": registry_report,
    }
    write_json_payload(output_payload, OUTPUT_REGISTRY_DATA)
    print(f"\nSaved dynamic registry to {OUTPUT_REGISTRY_DATA} ({len(registry_report)} entries).")
    print("=" * 70)


if __name__ == "__main__":
    main()
