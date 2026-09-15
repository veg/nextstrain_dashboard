#!/usr/bin/env python3
"""
pipeline/sync_pathogen.py
Downloader, ETag validator, and in-frame codon haplotype deduplicator.
Ingests raw sequence and metadata files for targeted pathogens,
pruning identical sequences while preserving temporal and geographic footprints.
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, Optional

# Add parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.utils.fasta_parser import collapse_haplotypes
from pipeline.utils.s3_client import download_s3_file, get_s3_metadata, list_s3_keys

REGISTRY_DATA = "static/data/registry.json"
REGISTRY_CONFIG = "config/pathogen_registry.json"
DEFAULT_DATA_DIR = "data"


def resolve_pathogen_sources(pathogen_id: str, gene: Optional[str] = None) -> Dict[str, Any]:
    """Find upstream S3 keys for sequences, metadata, and tree."""
    if os.path.exists(REGISTRY_CONFIG):
        with open(REGISTRY_CONFIG, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            for p in cfg.get("pathogens", []):
                if p["id"] == pathogen_id:
                    pathogen_info = p
                    break
            else:
                pathogen_info = {"id": pathogen_id, "s3_workflow_prefix": f"files/workflows/{pathogen_id}/"}
    else:
        pathogen_info = {"id": pathogen_id, "s3_workflow_prefix": f"files/workflows/{pathogen_id}/"}

    prefix = pathogen_info.get("s3_workflow_prefix", "")
    target_gene = gene or pathogen_info.get("default_gene", "")

    # For SARS-CoV-2, use files/ncov/open/africa/ or files/ncov/open/global/ or files/ncov/open/100k/
    if pathogen_id == "sars-cov-2":
        # Check files/ncov/open/africa/ (very fast, clean dataset ~1.5k genomes) or 100k
        return {
            "fasta_key": "files/ncov/open/africa/aligned.fasta.xz",
            "meta_key": "files/ncov/open/africa/metadata.tsv.xz",
            "name": "SARS-CoV-2",
            "gene": target_gene,
        }

    # For H5N1, use files/workflows/avian-flu/h5n1/ha/
    if pathogen_id == "avian-flu-h5n1":
        gene_name = target_gene.lower() if target_gene else "ha"
        return {
            "fasta_key": f"files/workflows/avian-flu/h5n1/{gene_name}/sequences.fasta.zst",
            "meta_key": "files/workflows/avian-flu/h5n1/metadata.tsv.zst",
            "name": "Avian Influenza A/H5N1",
            "gene": gene_name,
        }

    # For Seasonal Flu H3N2
    if pathogen_id == "influenza-h3n2":
        gene_name = target_gene.lower() if target_gene else "ha"
        return {
            "fasta_key": f"files/workflows/seasonal-flu/h3n2/{gene_name}/sequences.fasta.zst",
            "meta_key": "files/workflows/seasonal-flu/h3n2/metadata.tsv.zst",
            "name": "Influenza A/H3N2",
            "gene": gene_name,
        }

    # For Seasonal Flu H1N1pdm
    if pathogen_id == "influenza-h1n1pdm":
        gene_name = target_gene.lower() if target_gene else "ha"
        return {
            "fasta_key": f"files/workflows/seasonal-flu/h1n1pdm/{gene_name}/sequences.fasta.zst",
            "meta_key": "files/workflows/seasonal-flu/h1n1pdm/metadata.tsv.zst",
            "name": "Influenza A/H1N1pdm",
            "gene": gene_name,
        }

    # For Seasonal Flu B (Victoria)
    if pathogen_id == "influenza-b":
        gene_name = target_gene.lower() if target_gene else "ha"
        return {
            "fasta_key": f"files/workflows/seasonal-flu/vic/{gene_name}/sequences.fasta.zst",
            "meta_key": "files/workflows/seasonal-flu/vic/metadata.tsv.zst",
            "name": "Influenza B (Victoria)",
            "gene": gene_name,
        }

    # For RSV A
    if pathogen_id == "rsv":
        return {
            "fasta_key": "files/workflows/rsv/a/sequences.fasta.xz",
            "meta_key": "files/workflows/rsv/a/metadata.tsv.gz",
            "name": "RSV A & B",
            "gene": target_gene or "F",
        }

    # Generic discovery
    keys = list_s3_keys(prefix, max_keys=50)
    fasta_key = None
    meta_key = None

    for k in keys:
        k_name = k["key"]
        if (target_gene.lower() in k_name.lower() or not fasta_key) and any(
            k_name.endswith(ext) for ext in [".fasta", ".fasta.xz", ".fasta.zst", ".fasta.gz"]
        ):
            fasta_key = k_name
        if any(k_name.endswith(ext) for ext in ["metadata.tsv", "metadata.tsv.xz", "metadata.tsv.zst", "metadata.tsv.gz"]):
            meta_key = k_name

    return {
        "fasta_key": fasta_key,
        "meta_key": meta_key,
        "name": pathogen_info.get("name", pathogen_id),
        "gene": target_gene,
    }


def sync_pathogen(
    pathogen_id: str,
    gene: Optional[str] = None,
    data_dir: str = DEFAULT_DATA_DIR,
    max_taxa: Optional[int] = None,
    force: bool = False,
) -> Dict[str, Any]:
    """Execute download and haplotype collapsing for specified pathogen."""
    print("=" * 70)
    print(f"NextGen Surveillance: Ingesting Pathogen '{pathogen_id}'")
    print("=" * 70)

    sources = resolve_pathogen_sources(pathogen_id, gene)
    fasta_key = sources["fasta_key"]
    meta_key = sources["meta_key"]

    if not fasta_key:
        raise RuntimeError(f"Could not locate FASTA sequence key for pathogen {pathogen_id}")

    target_dir = os.path.join(data_dir, pathogen_id)
    raw_dir = os.path.join(target_dir, "raw")
    os.makedirs(raw_dir, exist_ok=True)

    # 1. Download Sequence FASTA
    raw_fasta_filename = os.path.basename(fasta_key)
    raw_fasta_dest = os.path.join(raw_dir, raw_fasta_filename)
    decompressed_fasta, fasta_downloaded = download_s3_file(
        fasta_key, raw_fasta_dest, decompress=True, force=force
    )

    # 2. Download Metadata TSV
    decompressed_meta = None
    if meta_key:
        raw_meta_filename = os.path.basename(meta_key)
        raw_meta_dest = os.path.join(raw_dir, raw_meta_filename)
        decompressed_meta, meta_downloaded = download_s3_file(
            meta_key, raw_meta_dest, decompress=True, force=force
        )

    # 3. Collapse Haplotypes
    collapsed_fasta = os.path.join(target_dir, "collapsed_alignment.fasta")
    collapsed_metadata = os.path.join(target_dir, "collapsed_metadata.tsv")

    print(f"\nCollapsing identical haplotypes from {decompressed_fasta}...")
    stats = collapse_haplotypes(
        fasta_path=decompressed_fasta,
        metadata_path=decompressed_meta,
        strain_col="strain",
        date_col="date",
        output_fasta=collapsed_fasta,
        output_metadata=collapsed_metadata,
        max_taxa=max_taxa,
    )

    print(f"Haplotype collapsing complete:")
    print(f"   Raw sequences:        {stats['raw_count']}")
    print(f"   Unique haplotypes:    {stats['unique_haplotypes']}")
    print(f"   Redundancy reduction: {stats['compression_ratio']}%")
    print(f"   Temporal span:        {stats['t_min']} - {stats['t_max']}")
    print(f"   Output FASTA:         {collapsed_fasta}")
    print(f"   Output Metadata:      {collapsed_metadata}")
    print("=" * 70)

    stats["pathogen_id"] = pathogen_id
    stats["collapsed_fasta"] = collapsed_fasta
    stats["collapsed_metadata"] = collapsed_metadata
    return stats


def main():
    parser = argparse.ArgumentParser(description="NextGen Pathogen Data Ingestion and Haplotype Deduplicator")
    parser.add_argument("-p", "--pathogen", default="avian-flu-h5n1", help="Pathogen ID (default: avian-flu-h5n1)")
    parser.add_argument("-g", "--gene", default=None, help="Target gene (e.g. ha, S)")
    parser.add_argument("-m", "--max-taxa", type=int, default=None, help="Optional taxa subsampling cap")
    parser.add_argument("-f", "--force", action="store_true", help="Force re-download even if cache matches")
    parser.add_argument("-d", "--data-dir", default=DEFAULT_DATA_DIR, help="Base data directory")

    args = parser.parse_args()
    sync_pathogen(
        pathogen_id=args.pathogen,
        gene=args.gene,
        data_dir=args.data_dir,
        max_taxa=args.max_taxa,
        force=args.force,
    )


if __name__ == "__main__":
    main()
