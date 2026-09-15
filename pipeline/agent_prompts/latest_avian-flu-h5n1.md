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
Execute the daily epidemiological intelligence review for AVIAN-FLU-H5N1 (avian-flu-h5n1) on 2026-09-14.

Input Data Context:
- Current Surveillance Target: avian-flu-h5n1 (Spike Glycoprotein)
- Daily Delta Summary:
{
  "date": "2026-09-14",
  "pathogen_id": "avian-flu-h5n1",
  "alert_level": "Tier-2 Moderate Velocity",
  "newly_confirmed_sweeps": [
    {
      "codon": 3,
      "peak_velocity": 0.0005,
      "peak_date": 2024.0219,
      "auc": 0.0001,
      "p_perm": 0.0476,
      "r2_wave": 1.0
    },
    {
      "codon": 143,
      "peak_velocity": 0.0041,
      "peak_date": 2024.2678,
      "auc": 0.0009,
      "p_perm": 0.0476,
      "r2_wave": 1.0
    },
    {
      "codon": 325,
      "peak_velocity": 0.0003,
      "peak_date": 2024.0219,
      "auc": 0.0,
      "p_perm": 0.0476,
      "r2_wave": 1.0
    }
  ],
  "accelerations": [],
  "new_clock_communities": [
    {
      "id": 0,
      "rate": 0.001,
      "r2": 0.3252,
      "tmrca": NaN,
      "taxa_count": 56,
      "color": "#3b82f6",
      "timespan": [
        2024.0792,
        2024.2678
      ]
    },
    {
      "id": 1,
      "rate": 0.001,
      "r2": 0.3978,
      "tmrca": NaN,
      "taxa_count": 38,
      "color": "#10b981",
      "timespan": [
        2024.0219,
        2024.2486
      ]
    }
  ],
  "new_quarantined_outliers": [
    {
      "strain": "A/canadagoose/NewMexico/24-005749-001/2024",
      "date": 2024.123,
      "community": 0,
      "divergence": 0.0053,
      "residual": 0.0023,
      "studentized_residual": 2.6555,
      "is_sus": false,
      "classification": "genuine_saltation",
      "reasons": [
        "Statistically significant clock deviation (|Z|=2.66)"
      ]
    },
    {
      "strain": "A/mallard/Minnesota/24-006961-018/2024",
      "date": 2024.1585,
      "community": 0,
      "divergence": 0.0059,
      "residual": 0.0036,
      "studentized_residual": 3.9074,
      "is_sus": true,
      "classification": "sequencing_artifact",
      "reasons": [
        "Extreme molecular clock departure (|Z|=3.91 >= 3.5)"
      ]
    },
    {
      "strain": "A/mountain_lion/Montana/24-005908-001/2024",
      "date": 2024.0792,
      "community": 0,
      "divergence": 0.0018,
      "residual": -0.002,
      "studentized_residual": -2.5159,
      "is_sus": false,
      "classification": "genuine_saltation",
      "reasons": [
        "Statistically significant clock deviation (|Z|=2.52)"
      ]
    },
    {
      "strain": "A/snow_goose/California/24-004881-004/2024",
      "date": 2024.0464,
      "community": 1,
      "divergence": 0.0113,
      "residual": 0.0052,
      "studentized_residual": 3.4098,
      "is_sus": true,
      "classification": "genuine_saltation",
      "reasons": [
        "Statistically significant clock deviation (|Z|=3.41)"
      ]
    },
    {
      "strain": "A/red-tailedhawk/SouthCarolina/24-005993-001/2024",
      "date": 2024.0219,
      "community": 1,
      "divergence": 0.003,
      "residual": -0.0038,
      "studentized_residual": -2.5645,
      "is_sus": false,
      "classification": "genuine_saltation",
      "reasons": [
        "Statistically significant clock deviation (|Z|=2.56)"
      ]
    }
  ],
  "active_codons_summary": [
    "Spike Glycoprotein 3",
    "Spike Glycoprotein 143",
    "Spike Glycoprotein 325"
  ],
  "executive_summary": "Active positive sweep velocity acceleration detected at Spike Glycoprotein codons [3, 143, 325]. Instantaneous selection intensity reached 0.0041 subs/site/yr with 5 quarantined LOOCV outlier(s)."
}

- AutoClock Rate Communities:
[
  {
    "id": 0,
    "rate": 0.001,
    "r2": 0.3252,
    "tmrca": NaN,
    "taxa_count": 56,
    "color": "#3b82f6",
    "timespan": [
      2024.0792,
      2024.2678
    ]
  },
  {
    "id": 1,
    "rate": 0.001,
    "r2": 0.3978,
    "tmrca": NaN,
    "taxa_count": 38,
    "color": "#10b981",
    "timespan": [
      2024.0219,
      2024.2486
    ]
  }
]

- Top Emergent Sweeps (Instantaneous Positive Velocity vs Diluted Static):
[
  {
    "codon": 3,
    "peak_velocity": 0.0005,
    "peak_date": 2024.0219,
    "auc": 0.0001,
    "p_perm": 0.0476,
    "r2_wave": 1.0
  },
  {
    "codon": 143,
    "peak_velocity": 0.0041,
    "peak_date": 2024.2678,
    "auc": 0.0009,
    "p_perm": 0.0476,
    "r2_wave": 1.0
  },
  {
    "codon": 325,
    "peak_velocity": 0.0003,
    "peak_date": 2024.0219,
    "auc": 0.0,
    "p_perm": 0.0476,
    "r2_wave": 1.0
  }
]

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
