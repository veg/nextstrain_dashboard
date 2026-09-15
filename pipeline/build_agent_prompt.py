#!/usr/bin/env python3
"""
pipeline/build_agent_prompt.py
Compiles high-dimensional phylodynamic outputs (ChronAeon clocks, HyphAeon sweep velocities,
CESI epistasis matrix, structural domains, and previous briefings) into standardized prompt context
for the Antigravity Autonomous Intelligence Agent.
"""

import argparse
import datetime
import glob
import json
import os
import sys
from typing import Any, Dict, Optional

SYSTEM_DIRECTIVE = """You are the Chief Epidemiological Intelligence Agent for the NextGen Pathogen Surveillance Platform.
Your mission is to synthesize high-dimensional phylodynamic outputs (ChronAeon manifold clocks and HyphAeon sweep velocities) into concise, publication-grade genomic intelligence briefings for public health leaders, vaccine developers, and molecular epidemiologists.

Key principles:
1. Rigorously separate population frequency (lagging metric) from positive sweep velocity (leading indicator of instantaneous adaptive advantage).
2. Contextualize structural biology: explain receptor-binding alterations, neutralizing antibody escape, and compensatory epistatic partners.
3. Audit molecular clock regimes: interpret AutoClock rate shifts and evaluate quarantined isolates (distinguishing sequencing/primer artifacts from genuine saltations).
4. Provide actionable guidance: identify specific clades requiring targeted PCR/sequencing, vaccine composition updates, or therapeutic vulnerability concerns.
5. Maintain multi-turn intellectual continuity with previous dispatches."""


def get_latest_previous_dispatch(pathogen_id: str) -> tuple:
    """Find the most recent dispatch markdown file for this pathogen."""
    dispatch_files = sorted(glob.glob(f"dispatches/*-{pathogen_id}.md"))
    if not dispatch_files:
        return "None", "No previous dispatches recorded. This is the baseline surveillance briefing."
    latest_file = dispatch_files[-1]
    filename = os.path.basename(latest_file)
    date_part = filename.split(f"-{pathogen_id}")[0]
    with open(latest_file, "r", encoding="utf-8") as f:
        content = f.read()
    # Return first 600 chars as snippet
    return date_part, content[:600] + "..."


def build_prompt_context(
    pathogen_id: str,
    output_prompt_path: Optional[str] = None,
) -> Dict[str, str]:
    """Build full prompt text and metadata for the agent."""
    data_dir = os.path.join("static", "data", pathogen_id)
    delta_file = os.path.join(data_dir, "delta_report.json")
    triage_file = os.path.join(data_dir, "autoclock_triage.json")
    velocity_file = os.path.join(data_dir, "sweep_velocity.json")
    epistasis_file = os.path.join(data_dir, "epistasis_cesi.json")

    # Load data files
    delta_data = {}
    if os.path.exists(delta_file):
        with open(delta_file, "r", encoding="utf-8") as f:
            delta_data = json.load(f)

    triage_data = {}
    if os.path.exists(triage_file):
        with open(triage_file, "r", encoding="utf-8") as f:
            triage_data = json.load(f)

    velocity_data = {}
    if os.path.exists(velocity_file):
        with open(velocity_file, "r", encoding="utf-8") as f:
            velocity_data = json.load(f)

    epistasis_data = {}
    if os.path.exists(epistasis_file):
        with open(epistasis_file, "r", encoding="utf-8") as f:
            epistasis_data = json.load(f)

    today_str = datetime.date.today().isoformat()
    prev_date, prev_snippet = get_latest_previous_dispatch(pathogen_id)

    # Format summaries
    clock_summary = json.dumps(triage_data.get("communities", []), indent=2)
    sweeps_summary = json.dumps(velocity_data.get("confirmed_sweeps", [])[:10], indent=2)
    edges_summary = json.dumps(epistasis_data.get("edges", [])[:15], indent=2)
    delta_summary = json.dumps(delta_data, indent=2)

    user_prompt = f"""Execute the daily epidemiological intelligence review for {pathogen_id.upper()} ({pathogen_id}) on {today_str}.

Input Data Context:
- Current Surveillance Target: {pathogen_id} ({velocity_data.get('protein', 'Primary Target')})
- Daily Delta Summary:
{delta_summary}

- AutoClock Rate Communities:
{clock_summary}

- Top Emergent Sweeps (Instantaneous Positive Velocity vs Diluted Static):
{sweeps_summary}

- Epistatic Co-Selection Pairs (Composite Epistatic Selection Index CESI >= 1.5):
{edges_summary}

- Historical Context ({prev_date}):
{prev_snippet}

Generate an Intelligence Dispatch in markdown adhering to the 5-part structure:
1. Executive Alert (1 concise paragraph highlighting new VOC/VOI risks or transmission jumps).
2. Molecular Acceleration Analysis (detailed breakdown of active sweeps, comparing sweep velocity to empirical prevalence).
3. Structural & Epistatic Synthesis (domain mapping, binding affinity, and compensatory partners).
4. Molecular Clock & Triage Audit (AutoClock emergence horizons, local rate accelerations, and LOOCV outlier quarantine log).
5. Forward Surveillance Recommendations (targeted diagnostic, vaccine, and sequencing priorities).

Use inline deep-link tokens where appropriate, e.g. [t=2024.4, codon=456]."""

    if output_prompt_path:
        os.makedirs(os.path.dirname(output_prompt_path), exist_ok=True)
        with open(output_prompt_path, "w", encoding="utf-8") as f:
            f.write(f"# SYSTEM DIRECTIVE\n{SYSTEM_DIRECTIVE}\n\n# USER PROMPT\n{user_prompt}\n")
        print(f"Saved compiled agent prompt to {output_prompt_path}")

    return {
        "system_directive": SYSTEM_DIRECTIVE,
        "user_prompt": user_prompt,
    }


def main():
    parser = argparse.ArgumentParser(description="Autonomous Agent Prompt Compiler")
    parser.add_argument("-p", "--pathogen", default="sars-cov-2")
    parser.add_argument("-o", "--output", default="pipeline/agent_prompts/latest_prompt.md")
    args = parser.parse_args()
    build_prompt_context(args.pathogen, args.output)


if __name__ == "__main__":
    main()
