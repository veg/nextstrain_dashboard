"""
Fast FASTA streaming parser and haplotype deduplicator.
Collapses identical sequences to save computation in ChronAeon and HyphAeon,
tracking observational frequency (N_obs) and temporal intervals.
"""

import csv
import datetime
import hashlib
import os
import re
from typing import Dict, Generator, List, Optional, Tuple


def parse_fasta_stream(file_path: str) -> Generator[Tuple[str, str], None, None]:
    """Memory-efficient streaming FASTA generator."""
    current_header = None
    current_seq_chunks = []

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_header is not None:
                    yield current_header, "".join(current_seq_chunks).upper()
                current_header = line[1:].strip()
                current_seq_chunks = []
            else:
                current_seq_chunks.append(line)

        if current_header is not None:
            yield current_header, "".join(current_seq_chunks).upper()


def parse_date_to_decimal(date_str: str) -> Optional[float]:
    """Convert YYYY-MM-DD or partial date string to decimal calendar year."""
    if not date_str or date_str in ("?", "unknown", "None"):
        return None

    # Already decimal float
    try:
        val = float(date_str)
        if 1900 <= val <= 2100:
            return val
    except ValueError:
        pass

    # Standard YYYY-MM-DD
    match = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", date_str)
    if match:
        year, month, day = map(int, match.groups())
        try:
            d = datetime.date(year, month, day)
            start_year = datetime.date(year, 1, 1)
            end_year = datetime.date(year + 1, 1, 1)
            return year + (d - start_year).days / (end_year - start_year).days
        except ValueError:
            return float(year)

    # YYYY-MM
    match = re.match(r"^(\d{4})-(\d{2})$", date_str)
    if match:
        year, month = map(int, match.groups())
        return year + (month - 0.5) / 12.0

    # Just YYYY
    match = re.match(r"^(\d{4})$", date_str)
    if match:
        return float(match.group(1)) + 0.5

    return None


def collapse_haplotypes(
    fasta_path: str,
    metadata_path: Optional[str] = None,
    strain_col: str = "strain",
    date_col: str = "date",
    output_fasta: Optional[str] = None,
    output_metadata: Optional[str] = None,
    max_taxa: Optional[int] = None,
) -> Dict[str, any]:
    """
    Collapse identical sequences into unique haplotypes.
    Retains sample count N_obs, earliest & latest collection dates.
    """
    # Load metadata if present
    meta_by_strain = {}
    if metadata_path and os.path.exists(metadata_path):
        with open(metadata_path, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                strain = row.get(strain_col) or row.get("Strain") or row.get("name")
                if strain:
                    meta_by_strain[strain] = row

    # Determine dominant in-frame target length if sequences vary
    length_counter = {}
    sample_count = 0
    for header, seq in parse_fasta_stream(fasta_path):
        sample_count += 1
        seq_len = len(seq)
        weight = 5 if (seq.startswith("ATG") and seq_len % 3 == 0) else 1
        length_counter[seq_len] = length_counter.get(seq_len, 0) + weight
        if sample_count >= 1000:
            break

    target_length = None
    if length_counter:
        target_length = max(length_counter.keys(), key=lambda l: length_counter[l])

    # Hash sequences
    haplotypes = {}  # seq_hash -> dict with representative, count, dates, members
    raw_count = 0

    for header, seq in parse_fasta_stream(fasta_path):
        # Filter for uniform length alignment
        if target_length and len(seq) != target_length:
            continue

        raw_count += 1
        strain = header.split()[0]

        # Extract date from metadata or header
        date_val = None
        if strain in meta_by_strain:
            date_raw = meta_by_strain[strain].get(date_col) or meta_by_strain[strain].get("date")
            date_val = parse_date_to_decimal(date_raw)
        
        # Fallback date extraction from header (e.g., strain|2024-03-12)
        if date_val is None:
            parts = header.split("|")
            for part in parts:
                parsed = parse_date_to_decimal(part.strip())
                if parsed:
                    date_val = parsed
                    break

        seq_hash = hashlib.md5(seq.encode("utf-8")).hexdigest()

        if seq_hash not in haplotypes:
            haplotypes[seq_hash] = {
                "rep_strain": strain,
                "sequence": seq,
                "count": 1,
                "members": [strain],
                "dates": [date_val] if date_val else [],
                "meta": meta_by_strain.get(strain, {}),
            }
        else:
            haplotypes[seq_hash]["count"] += 1
            haplotypes[seq_hash]["members"].append(strain)
            if date_val:
                haplotypes[seq_hash]["dates"].append(date_val)

        if max_taxa and raw_count >= max_taxa:
            break

    # Subsample / sort haplotypes
    sorted_haplos = sorted(haplotypes.values(), key=lambda h: h["count"], reverse=True)

    # Determine date intervals
    all_dates = []
    collapsed_rows = []

    for h in sorted_haplos:
        dates = h["dates"]
        if dates:
            min_d = min(dates)
            max_d = max(dates)
            mean_d = sum(dates) / len(dates)
            all_dates.extend(dates)
        else:
            min_d = max_d = mean_d = 2024.0

        row = {
            "strain": h["rep_strain"],
            "date": f"{mean_d:.4f}",
            "date_min": f"{min_d:.4f}",
            "date_max": f"{max_d:.4f}",
            "n_obs": h["count"],
            "members": ";".join(h["members"][:10]),
        }
        # Copy other metadata attributes
        for k, v in h["meta"].items():
            if k not in row:
                row[k] = v
        collapsed_rows.append(row)

    # Write output files if paths provided
    if output_fasta:
        os.makedirs(os.path.dirname(output_fasta), exist_ok=True)
        with open(output_fasta, "w", encoding="utf-8") as f:
            for h in sorted_haplos:
                f.write(f">{h['rep_strain']}\n{h['sequence']}\n")

    if output_metadata:
        os.makedirs(os.path.dirname(output_metadata), exist_ok=True)
        if collapsed_rows:
            fieldnames = list(collapsed_rows[0].keys())
            with open(output_metadata, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
                writer.writeheader()
                writer.writerows(collapsed_rows)

    stats = {
        "raw_count": raw_count,
        "unique_haplotypes": len(sorted_haplos),
        "compression_ratio": float(f"{(1.0 - len(sorted_haplos) / max(raw_count, 1)) * 100:.2f}"),
        "t_min": float(f"{min(all_dates):.4f}") if all_dates else 2020.0,
        "t_max": float(f"{max(all_dates):.4f}") if all_dates else 2026.0,
    }
    return stats
