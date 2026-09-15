#!/usr/bin/env python3
"""
pipeline/run_surveillance_and_deploy.py
Master End-to-End Surveillance Orchestrator.
Runs the complete analytical stack locally on your machine, synthesizes intelligence dispatches,
builds the static dashboard (build/), and pushes directly to GitHub Pages (gh-pages branch).
"""

import argparse
import datetime
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.broadcast.notify_email import send_email_digest
from pipeline.broadcast.notify_slack import send_slack_notification
from pipeline.build_agent_prompt import build_prompt_context
from pipeline.compute_delta import compute_pathogen_delta
from pipeline.run_chronaeon import run_chronaeon_pipeline
from pipeline.run_hyphaeon import run_hyphaeon_pipeline
from pipeline.sync_pathogen import sync_pathogen
from pipeline.sync_registry import inspect_pathogen_target, main as crawl_registry


def run_full_pipeline(
    pathogen_id: str = "sars-cov-2",
    gene: Optional[str] = None,
    max_taxa: int = 400,
    deploy: bool = True,
    broadcast: bool = False,
):
    # Lookup registry parameters if gene not explicitly passed
    reg_path = "config/pathogen_registry.json"
    focal_protein = "Spike Glycoprotein"
    if os.path.exists(reg_path):
        with open(reg_path, "r") as rf:
            reg_data = json.load(rf)
            for p in reg_data.get("pathogens", []):
                if p.get("id") == pathogen_id:
                    if not gene:
                        gene = p.get("default_gene", "S")
                    focal_protein = p.get("focal_protein", focal_protein)
                    break
    if not gene:
        gene = "S"

    print("=" * 80)
    print(f"NEXTGEN SURVEILLANCE: LOCAL INGESTION, ANALYSIS & STATIC DEPLOYMENT")
    print(f"Target Pathogen: {pathogen_id} (Gene: {gene}, Protein: {focal_protein})")
    print(f"Deploy to GH Pages: {deploy} | Live Broadcast: {broadcast}")
    print("=" * 80)

    # 1. Sync & Collapse Sequences
    print("\n[Step 1/6] Ingesting and deduplicating sequences from Nextstrain S3...")
    sync_stats = sync_pathogen(pathogen_id=pathogen_id, gene=gene, max_taxa=max_taxa)
    alignment_path = sync_stats["collapsed_fasta"]
    metadata_path = sync_stats["collapsed_metadata"]

    # Special handling for in-frame alignments if pre-computed
    if pathogen_id == "sars-cov-2" and os.path.exists("data/sars-cov-2/spike_alignment.fasta"):
        alignment_path = "data/sars-cov-2/spike_alignment.fasta"
    elif pathogen_id == "avian-flu-h5n1" and os.path.exists("data/avian-flu-h5n1/ha_inframe_alignment.fasta"):
        alignment_path = "data/avian-flu-h5n1/ha_inframe_alignment.fasta"
        metadata_path = "data/avian-flu-h5n1/ha_inframe_metadata.tsv"

    # 2. Run ChronAeon Manifold & LOOCV Triage
    print("\n[Step 2/6] Executing ChronAeon AutoClock and Manifold Deconvolution...")
    chron_res = run_chronaeon_pipeline(
        pathogen_id=pathogen_id,
        alignment_path=alignment_path,
        metadata_path=metadata_path,
        output_dir=f"data/{pathogen_id}",
        max_k=3,
    )

    # 3. Run HyphAeon Selection Velocity & Epistasis
    print("\n[Step 3/6] Executing HyphAeon Continuous Selection & Epistatic Sector Mining...")
    hyph_res = run_hyphaeon_pipeline(
        pathogen_id=pathogen_id,
        alignment_path=alignment_path,
        metadata_path=f"data/{pathogen_id}/chronaeon_work/classified.csv",
        output_dir=f"data/{pathogen_id}",
        gene=gene,
        protein_name=focal_protein,
        n_permutations=30,
        time_points=40,
    )

    # 4. Compute Surveillance Delta & Anomaly Report
    print("\n[Step 4/6] Computing Quantitative Delta & Outlier Triage...")
    delta_report = compute_pathogen_delta(pathogen_id=pathogen_id)

    # 5. Compile Agent Prompt & Copy Dispatches
    print("\n[Step 5/6] Formatting Agent Intelligence Context & Updating Dispatches...")
    prompt_file = f"pipeline/agent_prompts/latest_{pathogen_id}.md"
    build_prompt_context(pathogen_id=pathogen_id, output_prompt_path=prompt_file)

    os.makedirs("static/dispatches", exist_ok=True)
    subprocess.run("cp dispatches/*.md static/dispatches/ 2>/dev/null || true", shell=True)

    # 6. Optional Multi-Channel Broadcast
    if broadcast:
        print("\nPublishing Slack and Email alerts...")
        send_slack_notification(f"static/data/{pathogen_id}/delta_report.json")
        send_email_digest(
            f"static/data/{pathogen_id}/delta_report.json",
            output_html=f"static/data/{pathogen_id}/email_preview.html",
        )

    # 7. Build Static Pages and Push to GitHub Pages
    if deploy:
        print("\n[Step 6/6] Compiling Static SvelteKit Dashboard and Pushing to GitHub Pages...")
        subprocess.run(["bash", "pipeline/deploy_gh_pages.sh"], check=True)
    else:
        print("\n[Step 6/6] Static build skipped (pass --deploy to build and publish).")

    print("\n" + "=" * 80)
    print(f"SURVEILLANCE WORKFLOW COMPLETED SUCCESSFULLY FOR {pathogen_id}!")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Master Surveillance Orchestrator & Static Host Deployer")
    parser.add_argument("-p", "--pathogen", default="sars-cov-2", help="Target pathogen ID")
    parser.add_argument("-g", "--gene", default=None, help="Target gene identifier")
    parser.add_argument("-m", "--max-taxa", type=int, default=300, help="Taxa subsampling cap for fast runs")
    parser.add_argument("--all", action="store_true", help="Run surveillance across all active Tier-1 pathogens")
    parser.add_argument("--deploy", action="store_true", default=True, help="Build and push to gh-pages branch")
    parser.add_argument("--no-deploy", dest="deploy", action="store_false", help="Skip deployment push")
    parser.add_argument("--broadcast", action="store_true", help="Send live Slack and Email broadcasts")

    args = parser.parse_args()

    if args.all:
        targets = ["sars-cov-2", "avian-flu-h5n1"]
        for idx, target in enumerate(targets):
            is_last = idx == len(targets) - 1
            run_full_pipeline(
                pathogen_id=target,
                gene=None,
                max_taxa=args.max_taxa,
                deploy=args.deploy if is_last else False,
                broadcast=args.broadcast,
            )
    else:
        run_full_pipeline(
            pathogen_id=args.pathogen,
            gene=args.gene,
            max_taxa=args.max_taxa,
            deploy=args.deploy,
            broadcast=args.broadcast,
        )


if __name__ == "__main__":
    main()
