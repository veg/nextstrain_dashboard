#!/usr/bin/env python3
"""
pipeline/compute_delta.py
Quantitative delta and anomaly extraction engine.
Diffs current ChronAeon and HyphAeon outputs against historical baseline,
flagging newly confirmed sweeps, velocity accelerations (>= 2x), AutoClock community shifts,
and quarantined outliers to trigger autonomous agent dispatches.
"""

import argparse
import datetime
import json
import os
import sys
from typing import Any, Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.utils.serialization import write_json_payload

STATE_DIR = "state"
STATIC_DATA_DIR = "static/data"


def compute_pathogen_delta(pathogen_id: str) -> Dict[str, Any]:
    """Compute surveillance deltas for pathogen."""
    print("=" * 70)
    print(f"Surveillance Delta Engine: Auditing Changes for '{pathogen_id}'")
    print("=" * 70)

    data_dir = os.path.join(STATIC_DATA_DIR, pathogen_id)
    velocity_file = os.path.join(data_dir, "sweep_velocity.json")
    triage_file = os.path.join(data_dir, "autoclock_triage.json")
    epistasis_file = os.path.join(data_dir, "epistasis_cesi.json")

    if not os.path.exists(velocity_file) or not os.path.exists(triage_file):
        raise FileNotFoundError(f"Missing required analytical payloads in {data_dir}")

    with open(velocity_file, "r", encoding="utf-8") as f:
        v_data = json.load(f)
    with open(triage_file, "r", encoding="utf-8") as f:
        t_data = json.load(f)
    
    epi_data = {}
    if os.path.exists(epistasis_file):
        with open(epistasis_file, "r", encoding="utf-8") as f:
            epi_data = json.load(f)

    # Load previous run state if exists
    os.makedirs(STATE_DIR, exist_ok=True)
    prev_state_file = os.path.join(STATE_DIR, f"{pathogen_id}_state.json")
    prev_state = {}
    if os.path.exists(prev_state_file):
        try:
            with open(prev_state_file, "r", encoding="utf-8") as f:
                prev_state = json.load(f)
        except Exception:
            prev_state = {}

    prev_confirmed = set(prev_state.get("confirmed_codons", []))
    prev_velocities = prev_state.get("codon_velocities", {})

    # 1. Newly Confirmed Sweeps
    curr_confirmed = v_data.get("confirmed_sweeps", [])
    newly_confirmed = []
    active_codons = []

    for sweep in curr_confirmed:
        codon = sweep["codon"]
        active_codons.append(f"{v_data.get('protein', 'Protein')} {codon}")
        if codon not in prev_confirmed:
            newly_confirmed.append(sweep)

    # If first run and newly_confirmed is empty, seed with top sweeps
    if not prev_confirmed and curr_confirmed:
        newly_confirmed = curr_confirmed

    # 2. Velocity Accelerations (>= 2.0x increase in recent time points)
    matrix = v_data.get("matrix", [])
    codons = v_data.get("codons", [])
    time_points = v_data.get("time_points", [])
    accelerations = []
    current_velocities = {}

    if matrix and len(time_points) >= 4:
        for idx, codon in enumerate(codons):
            curve = matrix[idx]
            v_now = curve[-1]
            v_prev_local = curve[-3] if len(curve) >= 3 else curve[0]
            current_velocities[str(codon)] = v_now

            # Compare against previous run or recent curve inflection
            v_hist = prev_velocities.get(str(codon), v_prev_local)
            if v_now >= 0.005 and v_hist > 0:
                factor = v_now / v_hist
                if factor >= 2.0:
                    accelerations.append({
                        "codon": codon,
                        "previous_velocity": float(f"{v_hist:.5f}"),
                        "current_velocity": float(f"{v_now:.5f}"),
                        "acceleration_factor": float(f"{factor:.2f}"),
                    })
                    active_codons.append(f"{v_data.get('protein', 'Protein')} {codon} (Accel {factor:.1f}x)")

    # 3. AutoClock Community Shifts
    curr_communities = t_data.get("communities", [])
    prev_community_ids = set(prev_state.get("community_ids", []))
    new_communities = [c for c in curr_communities if c["id"] not in prev_community_ids]
    if not prev_community_ids:
        new_communities = curr_communities

    # 4. Quarantined Outliers
    outliers = t_data.get("outliers", [])
    prev_outlier_strains = set(prev_state.get("outlier_strains", []))
    new_outliers = [o for o in outliers if o["strain"] not in prev_outlier_strains]
    if not prev_outlier_strains:
        new_outliers = outliers

    # 5. Alert Level Assessment
    # Tier-1: High velocity sweep (>= 0.02) or >= 2x acceleration in surveillance codons
    surv_codons = set(v_data.get("surveillance_codons", []))
    surv_accelerated = any(a["codon"] in surv_codons for a in accelerations)
    max_v = max([s.get("peak_velocity", 0.0) for s in curr_confirmed] + [0.0])

    if max_v >= 0.02 or surv_accelerated or len(accelerations) >= 3:
        alert_level = "Tier-1 High Velocity Sweep"
    elif newly_confirmed or len(new_communities) > 0:
        alert_level = "Tier-2 Moderate Velocity"
    else:
        alert_level = "Nominal"

    today_str = datetime.date.today().isoformat()

    # Formulate Executive Summary
    if newly_confirmed or accelerations:
        focus_sites = ", ".join([str(s["codon"]) for s in newly_confirmed[:3]]) or ", ".join([str(a["codon"]) for a in accelerations[:3]])
        exec_summary = (
            f"Active positive sweep velocity acceleration detected at {v_data.get('protein', 'protein')} codons [{focus_sites}]. "
            f"Instantaneous selection intensity reached {max_v:.4f} subs/site/yr with {len(new_outliers)} quarantined LOOCV outlier(s)."
        )
    else:
        exec_summary = (
            f"Nominal evolutionary trajectory maintained across {len(curr_communities)} AutoClock communities. "
            f"No acute positive sweep velocity inflections detected in current surveillance horizon."
        )

    delta_report = {
        "date": today_str,
        "pathogen_id": pathogen_id,
        "alert_level": alert_level,
        "newly_confirmed_sweeps": newly_confirmed,
        "accelerations": accelerations,
        "new_clock_communities": new_communities,
        "new_quarantined_outliers": new_outliers,
        "active_codons_summary": list(dict.fromkeys(active_codons)),
        "executive_summary": exec_summary,
    }

    # Save delta report
    out_file = os.path.join(data_dir, "delta_report.json")
    write_json_payload(delta_report, out_file)

    # Update state
    updated_state = {
        "last_run": today_str,
        "confirmed_codons": [s["codon"] for s in curr_confirmed],
        "codon_velocities": current_velocities,
        "community_ids": [c["id"] for c in curr_communities],
        "outlier_strains": [o["strain"] for o in outliers],
    }
    with open(prev_state_file, "w", encoding="utf-8") as f:
        json.dump(updated_state, f, indent=2)

    print(f"\n[✓] Delta Computation Complete:")
    print(f"   Alert Level:              {alert_level}")
    print(f"   Newly Confirmed Sweeps:   {len(newly_confirmed)}")
    print(f"   Velocity Accelerations:   {len(accelerations)}")
    print(f"   New Clock Communities:   {len(new_communities)}")
    print(f"   New Quarantined Outliers: {len(new_outliers)}")
    print(f"   Saved Delta Report:       {out_file}")
    print("=" * 70)

    return delta_report


def main():
    parser = argparse.ArgumentParser(description="Surveillance Delta and Anomaly Extraction Engine")
    parser.add_argument("-p", "--pathogen", default="sars-cov-2")
    args = parser.parse_args()
    compute_pathogen_delta(args.pathogen)


if __name__ == "__main__":
    main()
