#!/usr/bin/env python3
"""
pipeline/broadcast/notify_email.py
Compiles an editorial HTML intelligence digest for public health subscribers.
Renders Jinja2 template with deep-link CTA buttons and responsive metric ribbons.
"""

import argparse
import html
import json
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, Optional

from jinja2 import Environment, FileSystemLoader

DASHBOARD_BASE_URL = os.environ.get("DASHBOARD_BASE_URL", "https://surveillance.veg.org")
REPO_BASE_URL = os.environ.get("REPO_BASE_URL", "https://github.com/veg/pathogen-intelligence")
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


def render_markdown_simple(md_text: str) -> str:
    """Basic markdown to HTML converter for email without external deps."""
    lines = md_text.split("\n")
    html_lines = []
    in_list = False

    for line in lines:
        line_s = line.strip()
        if not line_s:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append("<br/>")
            continue

        # Headers
        if line_s.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h3 style='color: #38bdf8; font-size: 16px; margin: 20px 0 8px;'>{html.escape(line_s[4:])}</h3>")
        elif line_s.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h2 style='color: #ffffff; font-size: 18px; margin: 24px 0 10px; border-bottom: 1px solid #334155; padding-bottom: 6px;'>{html.escape(line_s[3:])}</h2>")
        elif line_s.startswith("# "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h1 style='color: #ffffff; font-size: 22px; margin: 24px 0 12px;'>{html.escape(line_s[2:])}</h1>")
        elif line_s.startswith("- ") or line_s.startswith("* "):
            if not in_list:
                html_lines.append("<ul style='padding-left: 20px; margin: 8px 0;'>")
                in_list = True
            html_lines.append(f"<li style='margin-bottom: 4px;'>{html.escape(line_s[2:])}</li>")
        elif line_s.startswith("> "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<blockquote style='border-left: 3px solid #38bdf8; padding-left: 12px; margin: 8px 0; color: #94a3b8;'>{html.escape(line_s[2:])}</blockquote>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<p style='margin: 8px 0;'>{html.escape(line_s)}</p>")

    if in_list:
        html_lines.append("</ul>")

    return "\n".join(html_lines)


def build_email_digest(
    delta_report: Dict[str, Any],
    dispatch_path: Optional[str] = None,
) -> str:
    """Compile responsive HTML email digest using Jinja2."""
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("email_digest.html.j2")

    pathogen_id = delta_report.get("pathogen_id", "sars-cov-2")
    pathogen_name = pathogen_id.replace("-", " ").title()

    sweeps = delta_report.get("newly_confirmed_sweeps", [])
    max_v = max([s.get("peak_velocity", 0.0) for s in sweeps] + [0.0])
    communities = delta_report.get("new_clock_communities", [])
    tmrca = communities[0].get("tmrca", 2024.0) if communities else 2024.0

    rendered_md = ""
    if dispatch_path and os.path.exists(dispatch_path):
        with open(dispatch_path, "r", encoding="utf-8") as f:
            raw_md = f.read()
        rendered_md = render_markdown_simple(raw_md)
    else:
        rendered_md = "<p>Real-time surveillance delta report generated from ChronAeon and HyphAeon analytical streams.</p>"

    dashboard_url = f"{DASHBOARD_BASE_URL}/{pathogen_id}?t={delta_report.get('date', '')}"

    html_content = template.render(
        pathogen_name=pathogen_name,
        date=delta_report.get("date", "Today"),
        alert_level=delta_report.get("alert_level", "Tier-1 High Velocity Sweep"),
        active_sweeps_count=len(sweeps),
        max_velocity=f"{max_v:.4f} subs/site/yr",
        tmrca_horizon=f"t_MRCA {tmrca:.2f}",
        executive_summary=delta_report.get("executive_summary", ""),
        rendered_markdown=rendered_md,
        dashboard_url=dashboard_url,
        repo_url=f"{REPO_BASE_URL}/blob/main/dispatches",
    )

    return html_content


def send_email_digest(
    delta_file: str,
    dispatch_file: Optional[str] = None,
    output_html: Optional[str] = None,
    dry_run: bool = True,
) -> str:
    """Generate and optionally dispatch email digest."""
    with open(delta_file, "r", encoding="utf-8") as f:
        delta_data = json.load(f)

    html_email = build_email_digest(delta_data, dispatch_file)

    if output_html:
        os.makedirs(os.path.dirname(output_html), exist_ok=True)
        with open(output_html, "w", encoding="utf-8") as f:
            f.write(html_email)
        print(f"[Email Preview Saved] -> {output_html}")

    smtp_host = os.environ.get("SMTP_HOST")
    if not dry_run and smtp_host:
        smtp_user = os.environ.get("SMTP_USER")
        smtp_pass = os.environ.get("SMTP_PASS")
        recipients = os.environ.get("ALERT_RECIPIENTS", "").split(",")

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🚨 Pathogen Intelligence Alert: {delta_data.get('pathogen_id', '').upper()} ({delta_data.get('date', '')})"
        msg["From"] = smtp_user
        msg["To"] = ", ".join(recipients)
        msg.attach(MIMEText(html_email, "html"))

        with smtplib.SMTP_SSL(smtp_host, 465) as server:
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, recipients, msg.as_string())
            print(f"[Email Digest Dispatched] -> {len(recipients)} subscriber(s)")

    return html_email


def main():
    parser = argparse.ArgumentParser(description="HTML Email Digest Generator")
    parser.add_argument("-d", "--delta", required=True, help="Path to delta_report.json")
    parser.add_argument("-m", "--dispatch", default=None, help="Path to markdown dispatch")
    parser.add_argument("-o", "--output", default="static/data/sars-cov-2/email_preview.html")
    parser.add_argument("--send", action="store_true", help="Send via SMTP using environment credentials")
    args = parser.parse_args()

    send_email_digest(
        delta_file=args.delta,
        dispatch_file=args.dispatch,
        output_html=args.output,
        dry_run=not args.send,
    )


if __name__ == "__main__":
    main()
