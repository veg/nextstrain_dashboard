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
Execute the daily epidemiological intelligence review for INFLUENZA-B (influenza-b) on 2026-09-14.

Input Data Context:
- Current Surveillance Target: influenza-b (Hemagglutinin (HA))
- Daily Delta Summary:
{
  "date": "2026-09-14",
  "pathogen_id": "influenza-b",
  "alert_level": "Tier-2 Moderate Velocity",
  "newly_confirmed_sweeps": [],
  "accelerations": [],
  "new_clock_communities": [],
  "new_quarantined_outliers": [],
  "active_codons_summary": [],
  "executive_summary": "Active positive sweep velocity acceleration detected at Hemagglutinin (HA) codons [536, 538, 539]. Current instantaneous selection intensity reached 0.0039 subs/site/yr with 0 quarantined LOOCV outlier(s)."
}

- AutoClock Rate Communities:
[
  {
    "id": 0,
    "rate": 0.0009,
    "r2": 0.1277,
    "tmrca": 2018.1008,
    "taxa_count": 49,
    "color": "#3b82f6",
    "timespan": [
      2021.0384,
      2024.0519
    ]
  },
  {
    "id": 1,
    "rate": 0.0042,
    "r2": 0.0447,
    "tmrca": 2021.4385,
    "taxa_count": 14,
    "color": "#10b981",
    "timespan": [
      2023.1616,
      2024.0519
    ]
  },
  {
    "id": 2,
    "rate": 0.001,
    "r2": 0.1211,
    "tmrca": 2020.0,
    "taxa_count": 10,
    "color": "#f59e0b",
    "timespan": [
      2021.0384,
      2023.1616
    ]
  }
]

- Top Emergent Sweeps (Instantaneous Positive Velocity vs Diluted Static):
[
  {
    "codon": 143,
    "peak_velocity": 0.0475,
    "peak_date": 2022.5838,
    "auc": 0.01,
    "p_perm": 0.0323,
    "r2_wave": 1.0
  },
  {
    "codon": 198,
    "peak_velocity": 0.0617,
    "peak_date": 2022.5838,
    "auc": 0.0129,
    "p_perm": 0.0323,
    "r2_wave": 1.0
  },
  {
    "codon": 536,
    "peak_velocity": 0.4355,
    "peak_date": 2023.7428,
    "auc": 0.0989,
    "p_perm": 0.0323,
    "r2_wave": 1.0
  },
  {
    "codon": 538,
    "peak_velocity": 0.3651,
    "peak_date": 2023.7428,
    "auc": 0.0829,
    "p_perm": 0.0323,
    "r2_wave": 1.0
  },
  {
    "codon": 539,
    "peak_velocity": 0.2894,
    "peak_date": 2023.7428,
    "auc": 0.0657,
    "p_perm": 0.0323,
    "r2_wave": 1.0
  },
  {
    "codon": 541,
    "peak_velocity": 0.3264,
    "peak_date": 2023.7428,
    "auc": 0.0765,
    "p_perm": 0.0323,
    "r2_wave": 1.0
  },
  {
    "codon": 544,
    "peak_velocity": 0.4162,
    "peak_date": 2023.7428,
    "auc": 0.0945,
    "p_perm": 0.0323,
    "r2_wave": 1.0
  }
]

- Epistatic Co-Selection Pairs (Composite Epistatic Selection Index CESI >= 1.5):
[
  {
    "source": 9,
    "target": 198,
    "cesi": 5.1481,
    "sim": 0.6569,
    "shared_branches": 9
  },
  {
    "source": 95,
    "target": 256,
    "cesi": 3.7381,
    "sim": 0.8187,
    "shared_branches": 10
  },
  {
    "source": 143,
    "target": 198,
    "cesi": 3.6902,
    "sim": 1.0,
    "shared_branches": 14
  },
  {
    "source": 95,
    "target": 218,
    "cesi": 2.9904,
    "sim": 1.0,
    "shared_branches": 10
  },
  {
    "source": 8,
    "target": 198,
    "cesi": 2.9179,
    "sim": 0.5708,
    "shared_branches": 14
  },
  {
    "source": 9,
    "target": 200,
    "cesi": 2.5827,
    "sim": 0.5588,
    "shared_branches": 4
  },
  {
    "source": 95,
    "target": 159,
    "cesi": 2.5629,
    "sim": 1.0,
    "shared_branches": 10
  },
  {
    "source": 198,
    "target": 200,
    "cesi": 2.5259,
    "sim": 0.5323,
    "shared_branches": 4
  },
  {
    "source": 81,
    "target": 259,
    "cesi": 2.4128,
    "sim": 0.7861,
    "shared_branches": 2
  },
  {
    "source": 9,
    "target": 143,
    "cesi": 2.3616,
    "sim": 0.6571,
    "shared_branches": 9
  },
  {
    "source": 200,
    "target": 259,
    "cesi": 2.248,
    "sim": 0.682,
    "shared_branches": 2
  },
  {
    "source": 95,
    "target": 235,
    "cesi": 2.2366,
    "sim": 0.8449,
    "shared_branches": 10
  },
  {
    "source": 151,
    "target": 259,
    "cesi": 2.2223,
    "sim": 0.7878,
    "shared_branches": 2
  },
  {
    "source": 9,
    "target": 116,
    "cesi": 2.2146,
    "sim": 0.7467,
    "shared_branches": 7
  },
  {
    "source": 9,
    "target": 81,
    "cesi": 2.155,
    "sim": 0.5008,
    "shared_branches": 3
  }
]

- Historical Context (2026-09-14):
# Pathogen Intelligence Briefing: Seasonal Influenza B (Victoria Lineage)
**Date:** 2026-09-14 | **Surveillance Target:** Influenza B (`influenza-b`) | **Alert Level:** Tier-2 Moderate Velocity

---

### 1. Executive Summary & Surveillance Status
Longitudinal phylodynamic tracking of Influenza B Victoria lineage Hemagglutinin (HA) reveals ongoing antigenic renewal across subclade V1A.3a.2. Instantaneous selection velocity modeling identifies moderate positive selection bursts at HA1 globular head residues [133, 197, 199] in recent isolates ($t \ge 2024.5$). Current surveillance alert level is ...

Generate an Intelligence Dispatch in markdown adhering to the 5-part structure:
1. Executive Alert (1 concise paragraph highlighting new VOC/VOI risks or transmission jumps).
2. Molecular Acceleration Analysis (detailed breakdown of active sweeps, comparing sweep velocity to empirical prevalence).
3. Structural & Epistatic Synthesis (domain mapping, binding affinity, and compensatory partners).
4. Molecular Clock & Triage Audit (AutoClock emergence horizons, local rate accelerations, and LOOCV outlier quarantine log).
5. Forward Surveillance Recommendations (targeted diagnostic, vaccine, and sequencing priorities).

Use inline deep-link tokens where appropriate, e.g. [t=2024.4, codon=456].
