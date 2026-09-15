#!/usr/bin/env python3
"""
pipeline/run_chronaeon.py
Analytical wrapper for ChronAeon.
Runs AutoClock multi-rate community deconvolution, extracts Studentized LOOCV triage residuals,
and projects continuous alluvial streamline coordinates (t, y, w, k).
"""

import argparse
import csv
import json
import os
import subprocess
import sys
from typing import Any, Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.utils.serialization import write_json_payload

COLOR_PALETTE = [
    "#3b82f6",  # Sapphire Blue
    "#10b981",  # Emerald Green
    "#f59e0b",  # Amber / Gold
    "#ec4899",  # Rose Pink
    "#8b5cf6",  # Violet
    "#06b6d4",  # Cyan
    "#f97316",  # Orange
    "#84cc16",  # Lime
]


def run_chronaeon_pipeline(
    pathogen_id: str,
    alignment_path: str,
    metadata_path: str,
    output_dir: str,
    max_k: int = 4,
) -> Dict[str, Any]:
    """Execute ChronAeon AutoClock and triage deconvolution."""
    print("=" * 70)
    print(f"ChronAeon Analytical Engine: Deconvolving '{pathogen_id}'")
    print("=" * 70)

    work_dir = os.path.join(output_dir, "chronaeon_work")
    os.makedirs(work_dir, exist_ok=True)
    autoclock_json = os.path.join(work_dir, "autoclock.json")
    classified_csv = os.path.join(work_dir, "classified.csv")

    cmd = [
        "chronaeon",
        "autoclock",
        "-a", alignment_path,
        "-d", metadata_path,
        "--date-col", "date",
        "--strain-col", "strain",
        "--manifold", "distance",
        "-k", str(max_k),
        "--output-dir", work_dir,
        "-o", autoclock_json,
        "-c", classified_csv,
        "--quiet",
    ]

    print(f"Executing: {' '.join(cmd)}")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"[Warning] chronaeon stderr: {proc.stderr}")

    if not os.path.exists(autoclock_json):
        raise RuntimeError(f"ChronAeon failed to produce {autoclock_json}. Stderr: {proc.stderr}")

    with open(autoclock_json, "r", encoding="utf-8") as f:
        ac_data = json.load(f)

    # 1. Format Communities Metadata
    communities_raw = ac_data.get("communities", {})
    community_metas = []
    
    # Handle dict or list format
    if isinstance(communities_raw, dict):
        com_items = sorted(communities_raw.items(), key=lambda x: int(x[0]))
    else:
        com_items = [(str(i), c) for i, c in enumerate(communities_raw)]

    for idx, (cid, cinfo) in enumerate(com_items):
        cid_int = int(cid)
        color = COLOR_PALETTE[cid_int % len(COLOR_PALETTE)]
        cal_rate = cinfo.get("calibrated_rate", 1.0e-3)
        if cal_rate is None or cal_rate <= 0:
            cal_rate = 1.0e-3
        
        cal_tmrca = cinfo.get("calibrated_tmrca")
        if cal_tmrca is None:
            cal_tmrca = 2020.0

        community_metas.append({
            "id": cid_int,
            "rate": float(f"{cal_rate:.6f}"),
            "r2": float(f"{cinfo.get('r2', 0.85):.4f}"),
            "tmrca": float(f"{cal_tmrca:.4f}"),
            "taxa_count": cinfo.get("taxa_count", 0),
            "color": color,
            "timespan": cinfo.get("timespan", [2020.0, 2026.5]),
        })

    # 2. Extract LOOCV Triage Outliers
    triage_csv = os.path.join(work_dir, "autoclock_sequence_triage.csv")
    outliers = []
    if os.path.exists(triage_csv):
        with open(triage_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    z_score = float(row.get("studentized_residual", 0.0))
                    is_sus = row.get("is_sus", "False").lower() == "true" or abs(z_score) >= 3.0
                    
                    if is_sus or abs(z_score) >= 2.5:
                        reasons = []
                        if abs(z_score) >= 3.5:
                            reasons.append(f"Extreme molecular clock departure (|Z|={abs(z_score):.2f} >= 3.5)")
                            classification = "sequencing_artifact"
                        else:
                            reasons.append(f"Statistically significant clock deviation (|Z|={abs(z_score):.2f})")
                            classification = "genuine_saltation"

                        outliers.append({
                            "strain": row.get("strain", "unknown"),
                            "date": float(f"{float(row.get('date', 2024.0)):.4f}"),
                            "community": int(row.get("clock_community", 0)),
                            "divergence": float(f"{float(row.get('divergence', 0.0)):.6f}"),
                            "residual": float(f"{float(row.get('residual', 0.0)):.6f}"),
                            "studentized_residual": float(f"{z_score:.4f}"),
                            "is_sus": is_sus,
                            "classification": classification,
                            "reasons": reasons,
                        })
                except (ValueError, TypeError):
                    continue

    # 3. Generate Continuous Alluvial Streamline Coordinates (t, y, w, k)
    # Read classified metadata to place each community along continuous ribbons
    classified_path = os.path.join(work_dir, "classified.csv")
    samples_by_community = {c["id"]: [] for c in community_metas}
    
    if os.path.exists(classified_path):
        with open(classified_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    cid = int(row.get("clock_community", 0))
                    d = float(row.get("date", 2024.0))
                    div = float(row.get("divergence", 0.0))
                    n_obs = int(row.get("n_obs", 1))
                    if cid in samples_by_community:
                        samples_by_community[cid].append({"date": d, "divergence": div, "n_obs": n_obs})
                except (ValueError, TypeError):
                    continue

    ribbons = []
    all_dates = []
    all_divs = []

    for c in community_metas:
        cid = c["id"]
        samples = sorted(samples_by_community.get(cid, []), key=lambda s: s["date"])
        if not samples:
            continue

        dates = [s["date"] for s in samples]
        divs = [s["divergence"] for s in samples]
        all_dates.extend(dates)
        all_divs.extend(divs)

        # Build 15-20 spline knots across timespan for continuous ribbon
        t_start = max(min(dates), c["tmrca"])
        t_end = max(dates)
        n_knots = 16
        knots = []
        dt = (t_end - t_start) / max(n_knots - 1, 1)

        for step in range(n_knots):
            t_k = t_start + step * dt
            # Manifold divergence along AutoClock slope
            y_base = c["rate"] * max(0.0, t_k - c["tmrca"]) * 1000.0 + (cid * 0.8)
            # Active volume in window [t_k - 0.25, t_k + 0.25]
            window_obs = sum(s["n_obs"] for s in samples if abs(s["date"] - t_k) <= 0.35)
            # Non-linear expansion width
            w_k = max(0.5, (window_obs ** 0.5) * 0.4)

            knots.append({
                "t": float(f"{t_k:.4f}"),
                "y": float(f"{y_base:.4f}"),
                "w": float(f"{w_k:.4f}"),
                "community": cid,
                "n_obs": window_obs,
            })

        ribbons.append({
            "lineage_id": f"community_{cid}",
            "community": cid,
            "knots": knots,
        })

    time_range = [
        float(f"{min(all_dates):.2f}") if all_dates else 2020.0,
        float(f"{max(all_dates):.2f}") if all_dates else 2026.5,
    ]
    div_range = [
        float(f"{min(all_divs):.4f}") if all_divs else 0.0,
        float(f"{max(all_divs):.4f}") if all_divs else 0.05,
    ]

    # 4. Save Static Payloads
    static_dir = os.path.join("static", "data", pathogen_id)
    os.makedirs(static_dir, exist_ok=True)

    streamline_payload = {
        "pathogen_id": pathogen_id,
        "name": pathogen_id.replace("-", " ").title(),
        "time_range": time_range,
        "divergence_range": div_range,
        "communities": community_metas,
        "ribbons": ribbons,
    }
    streamline_file = os.path.join(static_dir, "manifold_streamlines.json")
    write_json_payload(streamline_payload, streamline_file)

    triage_payload = {
        "pathogen_id": pathogen_id,
        "optimal_k": len(community_metas),
        "communities": community_metas,
        "outliers": outliers,
    }
    triage_file = os.path.join(static_dir, "autoclock_triage.json")
    write_json_payload(triage_payload, triage_file)

    print(f"\n[✓] ChronAeon Execution Complete:")
    print(f"   Clock Communities: {len(community_metas)}")
    print(f"   Streamline Ribbons: {len(ribbons)}")
    print(f"   Quarantined Outliers: {len(outliers)}")
    print(f"   Saved Streamlines: {streamline_file}")
    print(f"   Saved Triage: {triage_file}")
    print("=" * 70)

    return {
        "streamlines": streamline_payload,
        "triage": triage_payload,
    }


def main():
    parser = argparse.ArgumentParser(description="ChronAeon Manifold & Triage Wrapper")
    parser.add_argument("-p", "--pathogen", default="sars-cov-2")
    parser.add_argument("-a", "--alignment", default="data/sars-cov-2/spike_alignment.fasta")
    parser.add_argument("-d", "--metadata", default="data/sars-cov-2/collapsed_metadata.tsv")
    parser.add_argument("-o", "--output-dir", default="data/sars-cov-2")
    parser.add_argument("-k", "--max-k", type=int, default=4)

    args = parser.parse_args()
    run_chronaeon_pipeline(
        pathogen_id=args.pathogen,
        alignment_path=args.alignment,
        metadata_path=args.metadata,
        output_dir=args.output_dir,
        max_k=args.max_k,
    )


if __name__ == "__main__":
    main()
