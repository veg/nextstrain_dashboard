#!/usr/bin/env python3
"""
pipeline/broadcast/notify_slack.py
Slack webhook integration generating interactive Block Kit alert cards
for newly confirmed sweeps, velocity accelerations, and quarantined outliers.
"""

import argparse
import json
import os
import sys
import urllib.request
from typing import Any, Dict, Optional

DASHBOARD_BASE_URL = os.environ.get("DASHBOARD_BASE_URL", "https://surveillance.veg.org")
REPO_BASE_URL = os.environ.get("REPO_BASE_URL", "https://github.com/veg/pathogen-intelligence")


def build_slack_blocks(
    delta_report: Dict[str, Any],
    dispatch_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Compile Slack Block Kit payload."""
    pathogen_id = delta_report.get("pathogen_id", "pathogen")
    pathogen_title = pathogen_id.replace("-", " ").title()
    date_str = delta_report.get("date", "Today")
    alert_level = delta_report.get("alert_level", "Nominal")

    # Icon by alert level
    if "Tier-1" in alert_level:
        header_icon = "🚨"
    elif "Tier-2" in alert_level:
        header_icon = "⚠️"
    else:
        header_icon = "ℹ️"

    # Format fields
    active_codons = ", ".join(delta_report.get("active_codons_summary", ["None"])) or "None"
    communities = delta_report.get("new_clock_communities", [])
    rate_str = f"{communities[0].get('rate', 0.0):.2e}" if communities else "Standard"
    outliers_count = len(delta_report.get("new_quarantined_outliers", []))

    # URLs
    focal_codon = ""
    if delta_report.get("newly_confirmed_sweeps"):
        focal_codon = f"&codon={delta_report['newly_confirmed_sweeps'][0]['codon']}"
    dashboard_url = f"{DASHBOARD_BASE_URL}/{pathogen_id}?t={date_str}{focal_codon}"
    
    if dispatch_path and os.path.exists(dispatch_path):
        rel_dispatch = os.path.basename(dispatch_path)
        dispatch_url = f"{REPO_BASE_URL}/blob/main/dispatches/{rel_dispatch}"
    else:
        dispatch_url = f"{REPO_BASE_URL}/tree/main/dispatches"

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{header_icon} Pathogen Intelligence Alert: {pathogen_title} ({date_str})",
                "emoji": True,
            },
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Alert Level:* {alert_level}"},
                {"type": "mrkdwn", "text": f"*Active Codons:* {active_codons}"},
                {"type": "mrkdwn", "text": f"*AutoClock Rate:* {rate_str} subs/site/yr"},
                {"type": "mrkdwn", "text": f"*Quarantined Outliers:* {outliers_count} isolate(s) (|Z| > 3.0)"},
            ],
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"> *Executive Summary:*\n{delta_report.get('executive_summary', 'No summary available.')}",
            },
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Open Interactive Dashboard"},
                    "style": "primary",
                    "url": dashboard_url,
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Read Full Dispatch"},
                    "url": dispatch_url,
                },
            ],
        },
    ]

    return {"blocks": blocks}


def send_slack_notification(
    delta_file: str,
    dispatch_file: Optional[str] = None,
    webhook_url: Optional[str] = None,
    dry_run: bool = False,
) -> bool:
    """Send or print Slack notification."""
    with open(delta_file, "r", encoding="utf-8") as f:
        delta_data = json.load(f)

    payload = build_slack_blocks(delta_data, dispatch_file)
    url = webhook_url or os.environ.get("SLACK_WEBHOOK_URL")

    if dry_run or not url:
        print("[Slack Broadcast: Dry Run Preview]")
        print(json.dumps(payload, indent=2))
        return True

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status == 200


def main():
    parser = argparse.ArgumentParser(description="Slack Notification Publisher")
    parser.add_argument("-d", "--delta", required=True, help="Path to delta_report.json")
    parser.add_argument("-m", "--dispatch", default=None, help="Path to markdown dispatch")
    parser.add_argument("--dry-run", action="store_true", help="Print Block Kit JSON without sending")
    args = parser.parse_args()

    send_slack_notification(args.delta, args.dispatch, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
