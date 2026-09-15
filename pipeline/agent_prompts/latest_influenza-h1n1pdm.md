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
Execute the daily epidemiological intelligence review for INFLUENZA-H1N1PDM (influenza-h1n1pdm) on 2026-09-14.

Input Data Context:
- Current Surveillance Target: influenza-h1n1pdm (Hemagglutinin (HA))
- Daily Delta Summary:
{
  "date": "2026-09-14",
  "pathogen_id": "influenza-h1n1pdm",
  "alert_level": "Tier-1 High Velocity Sweep",
  "newly_confirmed_sweeps": [],
  "accelerations": [],
  "new_clock_communities": [],
  "new_quarantined_outliers": [],
  "active_codons_summary": [],
  "executive_summary": "Active positive sweep velocity acceleration detected at Hemagglutinin (HA) codons [53, 91, 47]. Current instantaneous selection intensity reached 0.0217 subs/site/yr with 0 quarantined LOOCV outlier(s)."
}

- AutoClock Rate Communities:
[
  {
    "id": 0,
    "rate": 0.004,
    "r2": 0.8521,
    "tmrca": 2022.6566,
    "taxa_count": 162,
    "color": "#3b82f6",
    "timespan": [
      2022.811,
      2026.3808
    ]
  },
  {
    "id": 1,
    "rate": 0.0022,
    "r2": 0.2298,
    "tmrca": 2016.3891,
    "taxa_count": 108,
    "color": "#10b981",
    "timespan": [
      2020.0027,
      2025.1918
    ]
  }
]

- Top Emergent Sweeps (Instantaneous Positive Velocity vs Diluted Static):
[
  {
    "codon": 2,
    "peak_velocity": 0.1017,
    "peak_date": 2020.6569,
    "auc": 0.0306,
    "p_perm": 0.0323,
    "r2_wave": 0.4934
  },
  {
    "codon": 3,
    "peak_velocity": 0.1158,
    "peak_date": 2020.6569,
    "auc": 0.0349,
    "p_perm": 0.0323,
    "r2_wave": 0.4934
  },
  {
    "codon": 13,
    "peak_velocity": 0.093,
    "peak_date": 2020.8204,
    "auc": 0.0479,
    "p_perm": 0.0323,
    "r2_wave": 0.957
  },
  {
    "codon": 91,
    "peak_velocity": 0.0582,
    "peak_date": 2020.8204,
    "auc": 0.036,
    "p_perm": 0.0323,
    "r2_wave": 0.9138
  },
  {
    "codon": 101,
    "peak_velocity": 0.0321,
    "peak_date": 2020.8204,
    "auc": 0.0175,
    "p_perm": 0.0323,
    "r2_wave": 0.9547
  },
  {
    "codon": 114,
    "peak_velocity": 0.0794,
    "peak_date": 2020.8204,
    "auc": 0.0409,
    "p_perm": 0.0323,
    "r2_wave": 0.957
  },
  {
    "codon": 142,
    "peak_velocity": 0.0908,
    "peak_date": 2020.8204,
    "auc": 0.0487,
    "p_perm": 0.0323,
    "r2_wave": 0.9553
  },
  {
    "codon": 143,
    "peak_velocity": 0.1233,
    "peak_date": 2020.8204,
    "auc": 0.0635,
    "p_perm": 0.0323,
    "r2_wave": 0.957
  },
  {
    "codon": 147,
    "peak_velocity": 0.0063,
    "peak_date": 2022.4558,
    "auc": 0.004,
    "p_perm": 0.0323,
    "r2_wave": 0.9305
  },
  {
    "codon": 158,
    "peak_velocity": 0.0424,
    "peak_date": 2020.8204,
    "auc": 0.0246,
    "p_perm": 0.0323,
    "r2_wave": 0.9197
  }
]

- Epistatic Co-Selection Pairs (Composite Epistatic Selection Index CESI >= 1.5):
[
  {
    "source": 391,
    "target": 402,
    "cesi": 5.8497,
    "sim": 0.7966,
    "shared_branches": 2
  },
  {
    "source": 204,
    "target": 267,
    "cesi": 5.5742,
    "sim": 0.5962,
    "shared_branches": 22
  },
  {
    "source": 381,
    "target": 391,
    "cesi": 5.4856,
    "sim": 0.9086,
    "shared_branches": 2
  },
  {
    "source": 130,
    "target": 300,
    "cesi": 5.3688,
    "sim": 0.5879,
    "shared_branches": 38
  },
  {
    "source": 204,
    "target": 276,
    "cesi": 4.1284,
    "sim": 0.4658,
    "shared_branches": 23
  },
  {
    "source": 276,
    "target": 325,
    "cesi": 3.9662,
    "sim": 0.9908,
    "shared_branches": 55
  },
  {
    "source": 267,
    "target": 276,
    "cesi": 3.845,
    "sim": 0.7475,
    "shared_branches": 31
  },
  {
    "source": 202,
    "target": 233,
    "cesi": 3.43,
    "sim": 0.8201,
    "shared_branches": 6
  },
  {
    "source": 204,
    "target": 325,
    "cesi": 3.3597,
    "sim": 0.4617,
    "shared_branches": 23
  },
  {
    "source": 276,
    "target": 435,
    "cesi": 3.3415,
    "sim": 0.9488,
    "shared_branches": 55
  },
  {
    "source": 159,
    "target": 276,
    "cesi": 3.2947,
    "sim": 0.7245,
    "shared_branches": 55
  },
  {
    "source": 300,
    "target": 319,
    "cesi": 3.231,
    "sim": 0.5619,
    "shared_branches": 38
  },
  {
    "source": 130,
    "target": 156,
    "cesi": 3.1383,
    "sim": 0.4132,
    "shared_branches": 38
  },
  {
    "source": 391,
    "target": 406,
    "cesi": 3.1314,
    "sim": 0.8261,
    "shared_branches": 2
  },
  {
    "source": 267,
    "target": 325,
    "cesi": 3.1278,
    "sim": 0.7406,
    "shared_branches": 31
  }
]

- Historical Context (2026-09-14):
# Pathogen Intelligence Briefing: Seasonal Influenza A/H1N1pdm Hemagglutinin
**Date:** 2026-09-14 | **Surveillance Target:** Influenza A/H1N1pdm (`influenza-h1n1pdm`) | **Alert Level:** Tier-1 High Velocity Sweep

---

### 1. Executive Alert: Active Velocity Acceleration
Genomic surveillance of Influenza A/H1N1pdm Hemagglutinin (HA) across 2020–2026 detects **acute contemporary positive selection velocity acceleration** concentrated at HA residues [53, 91, 47]. Contemporary instantaneous selection intensity reached $v_s(t) = 0.0206\text{ subs/site/yr}$ at the active surveillance horizon ($t = ...

Generate an Intelligence Dispatch in markdown adhering to the 5-part structure:
1. Executive Alert (1 concise paragraph highlighting new VOC/VOI risks or transmission jumps).
2. Molecular Acceleration Analysis (detailed breakdown of active sweeps, comparing sweep velocity to empirical prevalence).
3. Structural & Epistatic Synthesis (domain mapping, binding affinity, and compensatory partners).
4. Molecular Clock & Triage Audit (AutoClock emergence horizons, local rate accelerations, and LOOCV outlier quarantine log).
5. Forward Surveillance Recommendations (targeted diagnostic, vaccine, and sequencing priorities).

Use inline deep-link tokens where appropriate, e.g. [t=2024.4, codon=456].
