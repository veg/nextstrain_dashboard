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
Execute the daily epidemiological intelligence review for MPOX (mpox) on 2026-09-14.

Input Data Context:
- Current Surveillance Target: mpox (Envelope Protein A35R)
- Daily Delta Summary:
{
  "date": "2026-09-14",
  "pathogen_id": "mpox",
  "alert_level": "Tier-2 Moderate Velocity",
  "newly_confirmed_sweeps": [],
  "accelerations": [],
  "new_clock_communities": [
    {
      "id": 0,
      "rate": 0.001,
      "r2": 0.0,
      "tmrca": 2020.0,
      "taxa_count": 293,
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
      "taxa_count": 5,
      "color": "#10b981",
      "timespan": [
        2024.0,
        2024.0
      ]
    }
  ],
  "new_quarantined_outliers": [
    {
      "strain": "OR146323",
      "date": 2024.0,
      "community": 0,
      "divergence": 0.0018,
      "residual": 0.0018,
      "studentized_residual": 9.8151,
      "is_sus": true,
      "classification": "sequencing_artifact",
      "reasons": [
        "Extreme molecular clock departure (|Z|=9.82 >= 3.5)"
      ]
    },
    {
      "strain": "OR146324",
      "date": 2024.0,
      "community": 0,
      "divergence": 0.0018,
      "residual": 0.0018,
      "studentized_residual": 9.8151,
      "is_sus": true,
      "classification": "sequencing_artifact",
      "reasons": [
        "Extreme molecular clock departure (|Z|=9.82 >= 3.5)"
      ]
    },
    {
      "strain": "OR146440",
      "date": 2024.0,
      "community": 0,
      "divergence": 0.0018,
      "residual": 0.0018,
      "studentized_residual": 9.8151,
      "is_sus": true,
      "classification": "sequencing_artifact",
      "reasons": [
        "Extreme molecular clock departure (|Z|=9.82 >= 3.5)"
      ]
    }
  ],
  "active_codons_summary": [],
  "executive_summary": "Active positive sweep velocity acceleration detected at Envelope Protein A35R codons []. Current instantaneous selection intensity reached 0.0000 subs/site/yr with 3 quarantined LOOCV outlier(s)."
}

- AutoClock Rate Communities:
[
  {
    "id": 0,
    "rate": 0.001,
    "r2": 0.0,
    "tmrca": 2020.0,
    "taxa_count": 293,
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
    "taxa_count": 5,
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
[]

- Historical Context (None):
No previous dispatches recorded. This is the baseline surveillance briefing.

Generate an Intelligence Dispatch in markdown adhering to the 5-part structure:
1. Executive Alert (1 concise paragraph highlighting new VOC/VOI risks or transmission jumps).
2. Molecular Acceleration Analysis (detailed breakdown of active sweeps, comparing sweep velocity to empirical prevalence).
3. Structural & Epistatic Synthesis (domain mapping, binding affinity, and compensatory partners).
4. Molecular Clock & Triage Audit (AutoClock emergence horizons, local rate accelerations, and LOOCV outlier quarantine log).
5. Forward Surveillance Recommendations (targeted diagnostic, vaccine, and sequencing priorities).

Use inline deep-link tokens where appropriate, e.g. [t=2024.4, codon=456].
