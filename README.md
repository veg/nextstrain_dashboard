# NextGen Real-Time Pathogen Surveillance & Autonomous Agent Intelligence Cockpit

[![Daily Surveillance Pipeline](https://github.com/veg/pathogen-intelligence/actions/workflows/daily_surveillance_pipeline.yml/badge.svg)](https://github.com/veg/pathogen-intelligence/actions/workflows/daily_surveillance_pipeline.yml)
[![Deploy Dashboard](https://github.com/veg/pathogen-intelligence/actions/workflows/deploy_dashboard.yml/badge.svg)](https://github.com/veg/pathogen-intelligence/actions/workflows/deploy_dashboard.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An ultra-modern, real-time molecular epidemiology surveillance platform and autonomous AI intelligence system developed at the **Pond / Temple / VEG Lab**.

Designed to supersede legacy cladogram viewers (Nextstrain / Auspice) by replacing dense cladograms with **continuous manifold dynamics (ChronAeon)**, estimating **instantaneous positive sweep velocities (HyphAeon)** without post-fixation dilution, and closing the loop with an **autonomous AI intelligence agent** that drafts daily epidemiological dispatches across GitHub, Slack, and Email.

---

## Architecture Overview

```
+--------------------------------------------------------------------------------------------------+
|                             NEXTGEN SURVEILLANCE & AGENT PLATFORM                                |
+--------------------------------------------------------------------------------------------------+
|   DATA INGESTION (Daily Cron)         ANALYTICAL ENGINE                   FRONTEND & BROADCAST   |
|                                                                                                  |
|   +-----------------------+           +----------------------+              +----------------+   |
|   | NEXTSTRAIN S3 / REG   | --------> | CHRONAEON            | -----------> | SVELTEKIT 2.0  |   |
|   | All Pathogen Manifests|           | - Manifold Alluvial  |              | - WebGPU Paths |   |
|   +-----------+-----------+           | - AutoClock Multi    |              | - 3D Mol* Sync |   |
|               |                       | - LOOCV Triage       |              | - Epistasis    |   |
|               v                       +----------+-----------+              +--------+-------+   |
|   +-----------------------+                      |                                   |           |
|   | GITHUB ACTIONS CI/CD  |                      |                                   |           |
|   | Dedicated Repo Runner | --------> +----------------------+                       |           |
|   +-----------+-----------+           | HYPHAEON             | ----------------------+           |
|               |                       | - Sweep Velocity     |                                   |
|               |                       | - 2-Stage Filter     |                                   |
|               v                       | - Axial Epistasis    |                                   |
|   +-----------------------+           +----------+-----------+                                   |
|   | DELTA COMPUTATION     |                      |                                               |
|   | New sweeps, clusters, | -------->            v                                               |
|   | rate jumps, anomalies |           +----------------------+                                   |
|   +-----------------------+           | AUTONOMOUS AGENT     |                                   |
|                                       | (Antigravity Engine) |                                   |
|                                       +----------+-----------+                                   |
|                                                  |                                               |
|                                                  v                                               |
|                                       +----------------------+                                   |
|                                       | MULTI-CHANNEL DISPATCH|                                  |
|                                       | - GitHub PR / Commit |                                   |
|                                       | - Slack Block Kit    |                                   |
|                                       | - HTML Email Digest  |                                   |
|                                       +----------------------+                                   |
+--------------------------------------------------------------------------------------------------+
```

---

## Key Capabilities

### 1. Five Synchronized Interactive Viewports
- **Viewport A: Alluvial Manifold Phylogeny (WebGPU / Deck.gl):** Replaces static bifurcating cladograms with continuous flowing river corridors along calendar time. Width dynamically scales with lineage observation volume ($N_{\text{obs}}$) while vertical axis maps genealogical divergence.
- **Viewport B: Instantaneous Sweep Velocity Waterfall:** Continuous codon-level selection velocity heatmap:
  $$v_s(t) = \max\left(0, \frac{d}{dt}\hat{a}_s(t)\right)$$
  Bypasses post-fixation dilution and captures acute selective inflection points months before peak population prevalence. Toggle between Stage-2 confirmed sweeps and rescued sweeps.
- **Viewport C: 3D Macromolecular Dynamics (Mol* / Three.js):** Real-time 3D protein overpaint (SARS-CoV-2 Spike `7KRR`, Avian Flu HA `4HMG`). Structural residues dynamically pulse and glow based on their active sweep velocity at the cursor date.
- **Viewport D: Autonomous Agent Intelligence Hub:** Publication-grade markdown briefings authored by the Antigravity Agent. Features interactive deep-link tokens (e.g. `[t=2024.8, codon=456]`) that synchronize all other viewports on click.
- **Viewport E: 3D Epistatic Co-Selection Network:** Force-directed network of Composite Epistatic Selection Index ($\text{CESI} \ge 1.5$) couplings, uncovering functional sectors that link antibody escape mutations to receptor affinity-restoring partners.
- **Auxiliary: AutoClock Regimes & LOOCV Outlier Quarantine Tray:** Polar clock community metrics ($\mu_k, R_k^2, t_{\text{MRCA},k}$) and closed-form studentized residual outlier audit ($|Z| \ge 3.0$), distinguishing sequencing artifacts from genuine saltations.

---

## Pipeline Execution

### 1. Dynamic Registry Discovery
```bash
# Crawl data.nextstrain.org public S3 bucket across Tier 1, 2, and 3 targets
python pipeline/sync_registry.py
```

### 2. Ingest and Deduplicate Sequences
```bash
# Download and collapse identical haplotypes with ETag / SHA-256 caching
python pipeline/sync_pathogen.py --pathogen sars-cov-2
python pipeline/sync_pathogen.py --pathogen avian-flu-h5n1
```

### 3. Run ChronAeon (Manifold & AutoClock)
```bash
python pipeline/run_chronaeon.py \
  --pathogen sars-cov-2 \
  -a data/sars-cov-2/spike_alignment.fasta \
  -d data/sars-cov-2/collapsed_metadata.tsv \
  -o data/sars-cov-2
```

### 4. Run HyphAeon (Selection Velocity & Epistasis)
```bash
python pipeline/run_hyphaeon.py \
  --pathogen sars-cov-2 \
  -a data/sars-cov-2/spike_alignment.fasta \
  -d data/sars-cov-2/chronaeon_work/classified.csv \
  -o data/sars-cov-2
```

### 5. Delta Engine & Multi-Channel Broadcast
```bash
# Extract daily changes and alert tiers
python pipeline/compute_delta.py --pathogen sars-cov-2

# Compile agent prompt context
python pipeline/build_agent_prompt.py --pathogen sars-cov-2 -o pipeline/agent_prompts/latest.md

# Publish Slack Block Kit alert cards
python pipeline/broadcast/notify_slack.py --delta static/data/sars-cov-2/delta_report.json

# Send responsive HTML email digest
python pipeline/broadcast/notify_email.py --delta static/data/sars-cov-2/delta_report.json --output preview.html
```

---

## Frontend Web Development

The dashboard is built with **SvelteKit 2.0** utilizing **Svelte 5 runes** (`$state`, `$derived`, `$effect`) for fine-grained 60 FPS viewport synchronization without virtual DOM overhead.

```bash
# Install dependencies
npm install

# Start local hot-reloading development server
npm run dev

# Build static SSG site (ready for GitHub Pages or Cloudflare Pages)
npm run build

# Preview production build locally
npm run preview
```

---

## License
MIT License. Developed by Sergei L. Kosakovsky Pond & the VEG Lab team.
