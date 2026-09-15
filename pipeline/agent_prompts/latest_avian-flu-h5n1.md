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
- Current Surveillance Target: avian-flu-h5n1 (Hemagglutinin (HA))
- Daily Delta Summary:
{
  "date": "2026-09-14",
  "pathogen_id": "avian-flu-h5n1",
  "alert_level": "Nominal",
  "newly_confirmed_sweeps": [],
  "accelerations": [],
  "new_clock_communities": [],
  "new_quarantined_outliers": [],
  "active_codons_summary": [
    "Hemagglutinin (HA) 143"
  ],
  "executive_summary": "Nominal evolutionary trajectory maintained across 2 AutoClock communities. No acute positive sweep velocity inflections detected in current surveillance horizon."
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
    "codon": 143,
    "peak_velocity": 0.0041,
    "peak_date": 2024.2678,
    "auc": 0.0009,
    "p_perm": 0.0323,
    "r2_wave": 1.0
  }
]

- Epistatic Co-Selection Pairs (Composite Epistatic Selection Index CESI >= 1.5):
[]

- Historical Context (2026-09-13):
# Pathogen Intelligence Briefing: Avian Influenza A/H5N1 Clade 2.3.4.4b
**Date:** 2026-09-13 | **Surveillance Target:** Avian Influenza A/H5N1 (`avian-flu-h5n1`) | **Alert Level:** Tier-2 Moderate Velocity

---

### 1. Executive Alert
Genomic surveillance of H5N1 clade 2.3.4.4b reveals emerging selective acceleration across Hemagglutinin (HA) receptor-binding residues, focalized at [t=2024.1, codon=137] and [t=2024.2, codon=190]. While avian $\alpha2\text{-}3$ sialic acid specificity remains conserved across the wild bird reservoir, bovine and dairy spillover isolates (genotype B3.13) display ...

Generate an Intelligence Dispatch in markdown adhering to the 5-part structure:
1. Executive Alert (1 concise paragraph highlighting new VOC/VOI risks or transmission jumps).
2. Molecular Acceleration Analysis (detailed breakdown of active sweeps, comparing sweep velocity to empirical prevalence).
3. Structural & Epistatic Synthesis (domain mapping, binding affinity, and compensatory partners).
4. Molecular Clock & Triage Audit (AutoClock emergence horizons, local rate accelerations, and LOOCV outlier quarantine log).
5. Forward Surveillance Recommendations (targeted diagnostic, vaccine, and sequencing priorities).

Use inline deep-link tokens where appropriate, e.g. [t=2024.4, codon=456].
