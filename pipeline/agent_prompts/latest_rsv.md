# SYSTEM DIRECTIVE
You are the Chief Epidemiological Intelligence Agent for the NextGen Pathogen Surveillance Platform.
Your mission is to synthesize high-dimensional phylodynamic outputs (ChronAeon manifold clocks and HyphAeon sweep velocities) into concise, publication-grade genomic intelligence briefings for public health leaders, vaccine developers, and molecular epidemiologists.

Key principles:
1. Rigorously separate population frequency (lagging metric) from positive sweep velocity (leading indicator of instantaneous adaptive advantage).
2. Contextualize structural biology: explain receptor-binding alterations, neutralizing antibody escape, and compensatory epistatic partners.
3. Audit molecular clock regimes: interpret AutoClock rate shifts and evaluate quarantined isolates (distinguishing sequencing/primer artifacts from genuine saltations).
4. Provide actionable guidance: identify specific clades requiring targeted PCR/sequencing, vaccine composition updates, or therapeutic vulnerability concerns.
5. Maintain multi-turn intellectual continuity with previous dispatches.

# USER PROMPT
Execute the daily epidemiological intelligence review for RSV (rsv) on 2026-09-14.

Input Data Context:
- Current Surveillance Target: rsv (Fusion Glycoprotein (F))
- Daily Delta Summary:
{
  "date": "2026-09-14",
  "pathogen_id": "rsv",
  "alert_level": "Nominal",
  "newly_confirmed_sweeps": [],
  "accelerations": [],
  "new_clock_communities": [],
  "new_quarantined_outliers": [],
  "active_codons_summary": [],
  "executive_summary": "Nominal evolutionary trajectory maintained across 2 AutoClock communities (t=2026.00). Historical adaptive sweeps (e.g. L455F/JN.1 at t=2023.78) have transitioned to post-sweep fixation/quiescence. Current instantaneous selection velocities across all sites remain baseline (max v_s = 0.0000 subs/site/yr)."
}

- AutoClock Rate Communities:
[
  {
    "id": 0,
    "rate": 0.001,
    "r2": 0.0,
    "tmrca": 2020.0,
    "taxa_count": 182,
    "color": "#3b82f6",
    "timespan": [
      2024.0,
      2024.0
    ]
  },
  {
    "id": 1,
    "rate": 0.001,
    "r2": 0.0,
    "tmrca": 2020.0,
    "taxa_count": 118,
    "color": "#10b981",
    "timespan": [
      2024.0,
      2024.0
    ]
  }
]

- Top Emergent Sweeps (Instantaneous Positive Velocity vs Diluted Static):
[]

- Epistatic Co-Selection Pairs (Composite Epistatic Selection Index CESI >= 1.5):
[
  {
    "source": 7,
    "target": 111,
    "cesi": 7.4006,
    "sim": 0.6987,
    "shared_branches": 86
  },
  {
    "source": 14,
    "target": 111,
    "cesi": 5.9777,
    "sim": 0.5042,
    "shared_branches": 93
  },
  {
    "source": 7,
    "target": 14,
    "cesi": 5.2971,
    "sim": 0.4018,
    "shared_branches": 89
  },
  {
    "source": 21,
    "target": 106,
    "cesi": 3.6473,
    "sim": 0.5834,
    "shared_branches": 4
  },
  {
    "source": 31,
    "target": 111,
    "cesi": 2.9531,
    "sim": 0.8919,
    "shared_branches": 77
  },
  {
    "source": 65,
    "target": 106,
    "cesi": 2.6452,
    "sim": 0.5336,
    "shared_branches": 4
  },
  {
    "source": 21,
    "target": 65,
    "cesi": 2.6293,
    "sim": 0.7257,
    "shared_branches": 4
  },
  {
    "source": 14,
    "target": 24,
    "cesi": 2.3932,
    "sim": 0.4396,
    "shared_branches": 14
  },
  {
    "source": 7,
    "target": 31,
    "cesi": 2.3495,
    "sim": 0.6382,
    "shared_branches": 72
  }
]

- Historical Context (None):
No previous dispatches recorded. This is the baseline surveillance briefing.

Generate an Intelligence Dispatch in markdown adhering to the 5-part structure:
1. Executive Alert (1 concise paragraph highlighting new VOC/VOI risks or transmission jumps).
2. Molecular Acceleration Analysis (detailed breakdown of active sweeps, comparing sweep velocity to empirical prevalence).
3. Structural & Epistatic Synthesis (domain mapping, binding affinity, and compensatory partners).
4. Molecular Clock & Triage Audit (AutoClock emergence horizons, local rate accelerations, and LOOCV outlier quarantine log).
5. Forward Surveillance Recommendations (targeted diagnostic, vaccine, and sequencing priorities).

Use inline deep-link tokens where appropriate, e.g. [t=2024.4, codon=456].
