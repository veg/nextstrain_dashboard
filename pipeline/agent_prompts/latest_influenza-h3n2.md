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
Execute the daily epidemiological intelligence review for INFLUENZA-H3N2 (influenza-h3n2) on 2026-09-14.

Input Data Context:
- Current Surveillance Target: influenza-h3n2 (Hemagglutinin (HA))
- Daily Delta Summary:
{
  "date": "2026-09-14",
  "pathogen_id": "influenza-h3n2",
  "alert_level": "Nominal",
  "newly_confirmed_sweeps": [],
  "accelerations": [],
  "new_clock_communities": [],
  "new_quarantined_outliers": [],
  "active_codons_summary": [],
  "executive_summary": "Nominal evolutionary trajectory maintained across 2 AutoClock communities (t=2026.47). Historical adaptive sweeps (e.g. L455F/JN.1 at t=2023.78) have transitioned to post-sweep fixation/quiescence. Current instantaneous selection velocities across all sites remain baseline (max v_s = 0.0033 subs/site/yr)."
}

- AutoClock Rate Communities:
[
  {
    "id": 0,
    "rate": 0.0037,
    "r2": 0.6762,
    "tmrca": 2020.0,
    "taxa_count": 158,
    "color": "#3b82f6",
    "timespan": [
      2022.8356,
      2026.4658
    ]
  },
  {
    "id": 1,
    "rate": 0.001,
    "r2": 0.106,
    "tmrca": 2020.0,
    "taxa_count": 89,
    "color": "#10b981",
    "timespan": [
      2020.0,
      2023.9534
    ]
  }
]

- Top Emergent Sweeps (Instantaneous Positive Velocity vs Diluted Static):
[
  {
    "codon": 11,
    "peak_velocity": 0.138,
    "peak_date": 2020.4974,
    "auc": 0.0467,
    "p_perm": 0.0323,
    "r2_wave": 0.9992
  },
  {
    "codon": 14,
    "peak_velocity": 0.0763,
    "peak_date": 2020.4974,
    "auc": 0.0329,
    "p_perm": 0.0323,
    "r2_wave": 0.971
  },
  {
    "codon": 15,
    "peak_velocity": 0.0501,
    "peak_date": 2020.4974,
    "auc": 0.017,
    "p_perm": 0.0323,
    "r2_wave": 0.9992
  },
  {
    "codon": 16,
    "peak_velocity": 0.0782,
    "peak_date": 2020.4974,
    "auc": 0.0297,
    "p_perm": 0.0323,
    "r2_wave": 0.9959
  },
  {
    "codon": 18,
    "peak_velocity": 0.0803,
    "peak_date": 2020.4974,
    "auc": 0.0332,
    "p_perm": 0.0323,
    "r2_wave": 0.9917
  },
  {
    "codon": 19,
    "peak_velocity": 0.0283,
    "peak_date": 2020.4974,
    "auc": 0.01,
    "p_perm": 0.0323,
    "r2_wave": 0.9986
  },
  {
    "codon": 41,
    "peak_velocity": 0.0459,
    "peak_date": 2020.4974,
    "auc": 0.0203,
    "p_perm": 0.0323,
    "r2_wave": 0.9264
  },
  {
    "codon": 47,
    "peak_velocity": 0.1027,
    "peak_date": 2020.4974,
    "auc": 0.0348,
    "p_perm": 0.0323,
    "r2_wave": 0.9992
  },
  {
    "codon": 61,
    "peak_velocity": 0.1108,
    "peak_date": 2020.4974,
    "auc": 0.0375,
    "p_perm": 0.0323,
    "r2_wave": 0.9992
  },
  {
    "codon": 64,
    "peak_velocity": 0.0421,
    "peak_date": 2020.4974,
    "auc": 0.0206,
    "p_perm": 0.0323,
    "r2_wave": 0.9371
  }
]

- Epistatic Co-Selection Pairs (Composite Epistatic Selection Index CESI >= 1.5):
[
  {
    "source": 138,
    "target": 292,
    "cesi": 12.707,
    "sim": 0.9394,
    "shared_branches": 104
  },
  {
    "source": 99,
    "target": 292,
    "cesi": 9.3224,
    "sim": 0.6394,
    "shared_branches": 12
  },
  {
    "source": 151,
    "target": 205,
    "cesi": 8.8847,
    "sim": 0.7822,
    "shared_branches": 66
  },
  {
    "source": 151,
    "target": 292,
    "cesi": 8.7711,
    "sim": 0.6118,
    "shared_branches": 20
  },
  {
    "source": 99,
    "target": 151,
    "cesi": 8.4791,
    "sim": 0.6628,
    "shared_branches": 10
  },
  {
    "source": 99,
    "target": 153,
    "cesi": 8.1402,
    "sim": 0.9099,
    "shared_branches": 9
  },
  {
    "source": 69,
    "target": 292,
    "cesi": 7.8557,
    "sim": 0.5952,
    "shared_branches": 81
  },
  {
    "source": 66,
    "target": 69,
    "cesi": 7.7197,
    "sim": 0.6969,
    "shared_branches": 45
  },
  {
    "source": 99,
    "target": 138,
    "cesi": 7.4786,
    "sim": 0.6195,
    "shared_branches": 11
  },
  {
    "source": 69,
    "target": 138,
    "cesi": 7.3469,
    "sim": 0.6724,
    "shared_branches": 80
  },
  {
    "source": 138,
    "target": 151,
    "cesi": 6.9918,
    "sim": 0.5891,
    "shared_branches": 20
  },
  {
    "source": 66,
    "target": 292,
    "cesi": 6.8119,
    "sim": 0.4968,
    "shared_branches": 51
  },
  {
    "source": 153,
    "target": 292,
    "cesi": 6.7803,
    "sim": 0.6764,
    "shared_branches": 9
  },
  {
    "source": 151,
    "target": 153,
    "cesi": 6.3816,
    "sim": 0.7255,
    "shared_branches": 9
  },
  {
    "source": 172,
    "target": 292,
    "cesi": 6.2433,
    "sim": 0.7886,
    "shared_branches": 49
  }
]

- Historical Context (2026-09-14):
# Pathogen Intelligence Briefing: Seasonal Influenza A/H3N2 Hemagglutinin
**Date:** 2026-09-14 | **Surveillance Target:** Influenza A/H3N2 (`influenza-h3n2`) | **Alert Level:** Nominal (Clade Equilibrium / Baseline Drift)

---

### 1. Executive Summary & Surveillance Status
Longitudinal surveillance of Influenza A/H3N2 Hemagglutinin (HA) across 2020–2026 reveals that **contemporary selection velocities remain at nominal drift levels** ($t = 2026.47$). The major adaptive antigenic transitions that defined recent Northern and Southern Hemisphere seasons—most notably selective bursts across clade...

Generate an Intelligence Dispatch in markdown adhering to the 5-part structure:
1. Executive Alert (1 concise paragraph highlighting new VOC/VOI risks or transmission jumps).
2. Molecular Acceleration Analysis (detailed breakdown of active sweeps, comparing sweep velocity to empirical prevalence).
3. Structural & Epistatic Synthesis (domain mapping, binding affinity, and compensatory partners).
4. Molecular Clock & Triage Audit (AutoClock emergence horizons, local rate accelerations, and LOOCV outlier quarantine log).
5. Forward Surveillance Recommendations (targeted diagnostic, vaccine, and sequencing priorities).

Use inline deep-link tokens where appropriate, e.g. [t=2024.4, codon=456].
