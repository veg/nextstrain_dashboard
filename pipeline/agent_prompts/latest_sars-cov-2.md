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
  "alert_level": "Nominal",
  "newly_confirmed_sweeps": [],
  "accelerations": [],
  "new_clock_communities": [],
  "new_quarantined_outliers": [],
  "active_codons_summary": [],
  "executive_summary": "Nominal evolutionary trajectory maintained across 3 AutoClock communities (t=2026.65). Historical adaptive sweeps (e.g. L455F/JN.1 at t=2023.78) have transitioned to post-sweep fixation/quiescence. Current instantaneous selection velocities across all sites remain baseline (max v_s = 0.0046 subs/site/yr)."
}

- AutoClock Rate Communities:
[
  {
    "id": 0,
    "rate": 0.001,
    "r2": 0.0206,
    "tmrca": 2020.0,
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
    "tmrca": 2020.0,
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
    "tmrca": 2020.0,
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
    "peak_velocity": 0.0121,
    "peak_date": 2022.2684,
    "auc": 0.005,
    "p_perm": 0.0323,
    "r2_wave": 0.5172
  },
  {
    "codon": 22,
    "peak_velocity": 0.0125,
    "peak_date": 2024.7943,
    "auc": 0.0048,
    "p_perm": 0.0323,
    "r2_wave": 0.1633
  },
  {
    "codon": 52,
    "peak_velocity": 0.0284,
    "peak_date": 2023.6155,
    "auc": 0.0141,
    "p_perm": 0.0323,
    "r2_wave": 0.1361
  },
  {
    "codon": 59,
    "peak_velocity": 0.0149,
    "peak_date": 2024.7943,
    "auc": 0.0049,
    "p_perm": 0.0323,
    "r2_wave": 0.1478
  },
  {
    "codon": 83,
    "peak_velocity": 0.0289,
    "peak_date": 2023.1103,
    "auc": 0.0123,
    "p_perm": 0.0323,
    "r2_wave": 0.1377
  },
  {
    "codon": 176,
    "peak_velocity": 0.0487,
    "peak_date": 2024.7943,
    "auc": 0.0161,
    "p_perm": 0.0323,
    "r2_wave": 0.1483
  },
  {
    "codon": 183,
    "peak_velocity": 0.0172,
    "peak_date": 2023.1103,
    "auc": 0.0069,
    "p_perm": 0.0323,
    "r2_wave": 0.1257
  },
  {
    "codon": 184,
    "peak_velocity": 0.019,
    "peak_date": 2024.7943,
    "auc": 0.0062,
    "p_perm": 0.0323,
    "r2_wave": 0.1476
  },
  {
    "codon": 186,
    "peak_velocity": 0.021,
    "peak_date": 2025.2995,
    "auc": 0.0113,
    "p_perm": 0.0323,
    "r2_wave": 0.0239
  },
  {
    "codon": 213,
    "peak_velocity": 0.0193,
    "peak_date": 2023.1103,
    "auc": 0.011,
    "p_perm": 0.0323,
    "r2_wave": 0.2026
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

- Historical Context (2026-09-14):
# Pathogen Intelligence Briefing: SARS-CoV-2 Spike Glycoprotein
**Date:** 2026-09-14 | **Surveillance Target:** SARS-CoV-2 (`sars-cov-2`) | **Alert Level:** Nominal (Post-Sweep Equilibrium / Baseline Drift)

---

### 1. Executive Summary & Surveillance Status
Continuous positive selection velocity $v_s(t)$ computed across the 6.5-year longitudinal alignment of SARS-CoV-2 Spike reveals that **no acute positive sweep velocity surges are currently active** in the contemporary surveillance horizon ($t = 2026.65$). The historical peak velocity events documented in the dataset—most notably at [t=202...

Generate an Intelligence Dispatch in markdown adhering to the 5-part structure:
1. Executive Alert (1 concise paragraph highlighting new VOC/VOI risks or transmission jumps).
2. Molecular Acceleration Analysis (detailed breakdown of active sweeps, comparing sweep velocity to empirical prevalence).
3. Structural & Epistatic Synthesis (domain mapping, binding affinity, and compensatory partners).
4. Molecular Clock & Triage Audit (AutoClock emergence horizons, local rate accelerations, and LOOCV outlier quarantine log).
5. Forward Surveillance Recommendations (targeted diagnostic, vaccine, and sequencing priorities).

Use inline deep-link tokens where appropriate, e.g. [t=2024.4, codon=456].
