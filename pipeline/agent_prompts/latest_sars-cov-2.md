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
Execute the daily epidemiological intelligence review for SARS-COV-2 (sars-cov-2) on 2026-09-14.

Input Data Context:
- Current Surveillance Target: sars-cov-2 (Spike Glycoprotein)
- Daily Delta Summary:
{
  "date": "2026-09-14",
  "pathogen_id": "sars-cov-2",
  "alert_level": "Tier-1 High Velocity Sweep",
  "newly_confirmed_sweeps": [
    {
      "codon": 3,
      "peak_velocity": 0.0106,
      "peak_date": 2022.1174,
      "auc": 0.0049,
      "p_perm": 0.0476,
      "r2_wave": 0.5848
    },
    {
      "codon": 22,
      "peak_velocity": 0.0092,
      "peak_date": 2024.8349,
      "auc": 0.0046,
      "p_perm": 0.0476,
      "r2_wave": 0.1583
    },
    {
      "codon": 52,
      "peak_velocity": 0.0266,
      "peak_date": 2023.7026,
      "auc": 0.0123,
      "p_perm": 0.0476,
      "r2_wave": 0.1228
    },
    {
      "codon": 59,
      "peak_velocity": 0.0104,
      "peak_date": 2024.8349,
      "auc": 0.0048,
      "p_perm": 0.0476,
      "r2_wave": 0.1378
    },
    {
      "codon": 83,
      "peak_velocity": 0.0241,
      "peak_date": 2023.0232,
      "auc": 0.0121,
      "p_perm": 0.0476,
      "r2_wave": 0.1582
    },
    {
      "codon": 146,
      "peak_velocity": 0.0193,
      "peak_date": 2023.0232,
      "auc": 0.0092,
      "p_perm": 0.0476,
      "r2_wave": 0.1387
    },
    {
      "codon": 176,
      "peak_velocity": 0.0351,
      "peak_date": 2024.8349,
      "auc": 0.0154,
      "p_perm": 0.0476,
      "r2_wave": 0.1366
    },
    {
      "codon": 183,
      "peak_velocity": 0.0146,
      "peak_date": 2023.0232,
      "auc": 0.0068,
      "p_perm": 0.0476,
      "r2_wave": 0.1461
    },
    {
      "codon": 184,
      "peak_velocity": 0.0134,
      "peak_date": 2024.8349,
      "auc": 0.0061,
      "p_perm": 0.0476,
      "r2_wave": 0.1373
    },
    {
      "codon": 186,
      "peak_velocity": 0.02,
      "peak_date": 2025.2878,
      "auc": 0.009,
      "p_perm": 0.0476,
      "r2_wave": 0.0301
    },
    {
      "codon": 213,
      "peak_velocity": 0.0156,
      "peak_date": 2023.0232,
      "auc": 0.0108,
      "p_perm": 0.0476,
      "r2_wave": 0.2167
    },
    {
      "codon": 339,
      "peak_velocity": 0.0062,
      "peak_date": 2021.8909,
      "auc": 0.0066,
      "p_perm": 0.0476,
      "r2_wave": 0.7159
    },
    {
      "codon": 346,
      "peak_velocity": 0.0103,
      "peak_date": 2021.8909,
      "auc": 0.0122,
      "p_perm": 0.0476,
      "r2_wave": 0.1422
    },
    {
      "codon": 455,
      "peak_velocity": 0.0139,
      "peak_date": 2023.7026,
      "auc": 0.0075,
      "p_perm": 0.0476,
      "r2_wave": 0.281
    },
    {
      "codon": 456,
      "peak_velocity": 0.0047,
      "peak_date": 2024.6085,
      "auc": 0.0044,
      "p_perm": 0.0476,
      "r2_wave": 0.4404
    },
    {
      "codon": 475,
      "peak_velocity": 0.0083,
      "peak_date": 2025.2878,
      "auc": 0.0053,
      "p_perm": 0.0476,
      "r2_wave": 0.0981
    },
    {
      "codon": 478,
      "peak_velocity": 0.0109,
      "peak_date": 2023.2497,
      "auc": 0.013,
      "p_perm": 0.0476,
      "r2_wave": 0.2142
    },
    {
      "codon": 486,
      "peak_velocity": 0.0088,
      "peak_date": 2022.3438,
      "auc": 0.0056,
      "p_perm": 0.0476,
      "r2_wave": 0.5551
    },
    {
      "codon": 519,
      "peak_velocity": 0.0092,
      "peak_date": 2022.5703,
      "auc": 0.0041,
      "p_perm": 0.0476,
      "r2_wave": 0.1066
    },
    {
      "codon": 529,
      "peak_velocity": 0.0167,
      "peak_date": 2024.8349,
      "auc": 0.0073,
      "p_perm": 0.0476,
      "r2_wave": 0.138
    },
    {
      "codon": 658,
      "peak_velocity": 0.0075,
      "peak_date": 2022.5703,
      "auc": 0.0038,
      "p_perm": 0.0476,
      "r2_wave": 0.0721
    },
    {
      "codon": 940,
      "peak_velocity": 0.0051,
      "peak_date": 2022.5703,
      "auc": 0.0023,
      "p_perm": 0.0476,
      "r2_wave": 0.1066
    },
    {
      "codon": 950,
      "peak_velocity": 0.0127,
      "peak_date": 2021.438,
      "auc": 0.0068,
      "p_perm": 0.0476,
      "r2_wave": 0.127
    },
    {
      "codon": 1086,
      "peak_velocity": 0.0232,
      "peak_date": 2024.1555,
      "auc": 0.0182,
      "p_perm": 0.0476,
      "r2_wave": 0.2864
    },
    {
      "codon": 1091,
      "peak_velocity": 0.0203,
      "peak_date": 2020.0792,
      "auc": 0.0064,
      "p_perm": 0.0476,
      "r2_wave": 0.0336
    },
    {
      "codon": 1104,
      "peak_velocity": 0.0089,
      "peak_date": 2024.1555,
      "auc": 0.0104,
      "p_perm": 0.0476,
      "r2_wave": 0.1102
    },
    {
      "codon": 1150,
      "peak_velocity": 0.0374,
      "peak_date": 2023.9291,
      "auc": 0.0187,
      "p_perm": 0.0476,
      "r2_wave": 0.4059
    }
  ],
  "accelerations": [],
  "new_clock_communities": [
    {
      "id": 0,
      "rate": 0.001,
      "r2": 0.0206,
      "tmrca": NaN,
      "taxa_count": 130,
      "color": "#3b82f6",
      "timespan": [
        2023.5699,
        2026.6466
      ]
    },
    {
      "id": 1,
      "rate": 0.001,
      "r2": 0.7606,
      "tmrca": NaN,
      "taxa_count": 38,
      "color": "#10b981",
      "timespan": [
        2021.8904,
        2026.5918
      ]
    },
    {
      "id": 2,
      "rate": 0.0033,
      "r2": 0.8037,
      "tmrca": NaN,
      "taxa_count": 132,
      "color": "#f59e0b",
      "timespan": [
        2020.0792,
        2023.8685
      ]
    }
  ],
  "new_quarantined_outliers": [
    {
      "strain": "ZAF/Wuhan-Hu-1/2024",
      "date": 2024.2077,
      "community": 1,
      "divergence": 0.0106,
      "residual": 0.0062,
      "studentized_residual": 3.5322,
      "is_sus": true,
      "classification": "sequencing_artifact",
      "reasons": [
        "Extreme molecular clock departure (|Z|=3.53 >= 3.5)"
      ]
    },
    {
      "strain": "OZ536347",
      "date": 2026.5918,
      "community": 1,
      "divergence": 0.0082,
      "residual": 0.0071,
      "studentized_residual": 3.9666,
      "is_sus": true,
      "classification": "sequencing_artifact",
      "reasons": [
        "Extreme molecular clock departure (|Z|=3.97 >= 3.5)"
      ]
    },
    {
      "strain": "EGY/OmicronVaccinepassage5/2022",
      "date": 2022.7863,
      "community": 2,
      "divergence": 0.0021,
      "residual": -0.0049,
      "studentized_residual": -3.4871,
      "is_sus": true,
      "classification": "genuine_saltation",
      "reasons": [
        "Statistically significant clock deviation (|Z|=3.49)"
      ]
    },
    {
      "strain": "NGA/AKS009/2022",
      "date": 2022.375,
      "community": 2,
      "divergence": 0.0016,
      "residual": -0.0041,
      "studentized_residual": -2.8966,
      "is_sus": false,
      "classification": "genuine_saltation",
      "reasons": [
        "Statistically significant clock deviation (|Z|=2.90)"
      ]
    }
  ],
  "active_codons_summary": [
    "Spike Glycoprotein 3",
    "Spike Glycoprotein 22",
    "Spike Glycoprotein 52",
    "Spike Glycoprotein 59",
    "Spike Glycoprotein 83",
    "Spike Glycoprotein 146",
    "Spike Glycoprotein 176",
    "Spike Glycoprotein 183",
    "Spike Glycoprotein 184",
    "Spike Glycoprotein 186",
    "Spike Glycoprotein 213",
    "Spike Glycoprotein 339",
    "Spike Glycoprotein 346",
    "Spike Glycoprotein 455",
    "Spike Glycoprotein 456",
    "Spike Glycoprotein 475",
    "Spike Glycoprotein 478",
    "Spike Glycoprotein 486",
    "Spike Glycoprotein 519",
    "Spike Glycoprotein 529",
    "Spike Glycoprotein 658",
    "Spike Glycoprotein 940",
    "Spike Glycoprotein 950",
    "Spike Glycoprotein 1086",
    "Spike Glycoprotein 1091",
    "Spike Glycoprotein 1104",
    "Spike Glycoprotein 1150"
  ],
  "executive_summary": "Active positive sweep velocity acceleration detected at Spike Glycoprotein codons [3, 22, 52]. Instantaneous selection intensity reached 0.0374 subs/site/yr with 4 quarantined LOOCV outlier(s)."
}

- AutoClock Rate Communities:
[
  {
    "id": 0,
    "rate": 0.001,
    "r2": 0.0206,
    "tmrca": NaN,
    "taxa_count": 130,
    "color": "#3b82f6",
    "timespan": [
      2023.5699,
      2026.6466
    ]
  },
  {
    "id": 1,
    "rate": 0.001,
    "r2": 0.7606,
    "tmrca": NaN,
    "taxa_count": 38,
    "color": "#10b981",
    "timespan": [
      2021.8904,
      2026.5918
    ]
  },
  {
    "id": 2,
    "rate": 0.0033,
    "r2": 0.8037,
    "tmrca": NaN,
    "taxa_count": 132,
    "color": "#f59e0b",
    "timespan": [
      2020.0792,
      2023.8685
    ]
  }
]

- Top Emergent Sweeps (Instantaneous Positive Velocity vs Diluted Static):
[
  {
    "codon": 3,
    "peak_velocity": 0.0106,
    "peak_date": 2022.1174,
    "auc": 0.0049,
    "p_perm": 0.0476,
    "r2_wave": 0.5848
  },
  {
    "codon": 22,
    "peak_velocity": 0.0092,
    "peak_date": 2024.8349,
    "auc": 0.0046,
    "p_perm": 0.0476,
    "r2_wave": 0.1583
  },
  {
    "codon": 52,
    "peak_velocity": 0.0266,
    "peak_date": 2023.7026,
    "auc": 0.0123,
    "p_perm": 0.0476,
    "r2_wave": 0.1228
  },
  {
    "codon": 59,
    "peak_velocity": 0.0104,
    "peak_date": 2024.8349,
    "auc": 0.0048,
    "p_perm": 0.0476,
    "r2_wave": 0.1378
  },
  {
    "codon": 83,
    "peak_velocity": 0.0241,
    "peak_date": 2023.0232,
    "auc": 0.0121,
    "p_perm": 0.0476,
    "r2_wave": 0.1582
  },
  {
    "codon": 146,
    "peak_velocity": 0.0193,
    "peak_date": 2023.0232,
    "auc": 0.0092,
    "p_perm": 0.0476,
    "r2_wave": 0.1387
  },
  {
    "codon": 176,
    "peak_velocity": 0.0351,
    "peak_date": 2024.8349,
    "auc": 0.0154,
    "p_perm": 0.0476,
    "r2_wave": 0.1366
  },
  {
    "codon": 183,
    "peak_velocity": 0.0146,
    "peak_date": 2023.0232,
    "auc": 0.0068,
    "p_perm": 0.0476,
    "r2_wave": 0.1461
  },
  {
    "codon": 184,
    "peak_velocity": 0.0134,
    "peak_date": 2024.8349,
    "auc": 0.0061,
    "p_perm": 0.0476,
    "r2_wave": 0.1373
  },
  {
    "codon": 186,
    "peak_velocity": 0.02,
    "peak_date": 2025.2878,
    "auc": 0.009,
    "p_perm": 0.0476,
    "r2_wave": 0.0301
  }
]

- Epistatic Co-Selection Pairs (Composite Epistatic Selection Index CESI >= 1.5):
[
  {
    "source": 264,
    "target": 455,
    "cesi": 17.4099,
    "sim": 0.8362,
    "shared_branches": 112
  },
  {
    "source": 450,
    "target": 455,
    "cesi": 14.7414,
    "sim": 0.8688,
    "shared_branches": 112
  },
  {
    "source": 50,
    "target": 455,
    "cesi": 14.2973,
    "sim": 0.8211,
    "shared_branches": 104
  },
  {
    "source": 127,
    "target": 455,
    "cesi": 13.893,
    "sim": 0.8045,
    "shared_branches": 106
  },
  {
    "source": 216,
    "target": 455,
    "cesi": 13.5043,
    "sim": 0.8295,
    "shared_branches": 112
  },
  {
    "source": 455,
    "target": 1143,
    "cesi": 12.7027,
    "sim": 0.8287,
    "shared_branches": 111
  },
  {
    "source": 127,
    "target": 264,
    "cesi": 12.5449,
    "sim": 0.967,
    "shared_branches": 117
  },
  {
    "source": 264,
    "target": 450,
    "cesi": 12.1607,
    "sim": 0.954,
    "shared_branches": 113
  },
  {
    "source": 50,
    "target": 264,
    "cesi": 12.1418,
    "sim": 0.9282,
    "shared_branches": 108
  },
  {
    "source": 216,
    "target": 264,
    "cesi": 12.1314,
    "sim": 0.9919,
    "shared_branches": 123
  },
  {
    "source": 264,
    "target": 1143,
    "cesi": 11.3265,
    "sim": 0.9837,
    "shared_branches": 121
  },
  {
    "source": 187,
    "target": 795,
    "cesi": 11.2434,
    "sim": 0.931,
    "shared_branches": 27
  },
  {
    "source": 22,
    "target": 455,
    "cesi": 11.0861,
    "sim": 0.7617,
    "shared_branches": 92
  },
  {
    "source": 455,
    "target": 487,
    "cesi": 10.758,
    "sim": 0.6575,
    "shared_branches": 65
  },
  {
    "source": 688,
    "target": 795,
    "cesi": 10.621,
    "sim": 0.8352,
    "shared_branches": 28
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
