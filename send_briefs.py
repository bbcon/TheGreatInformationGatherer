#!/usr/bin/env python3
"""
Send daily and weekly briefs via email with styled HTML templates.
"""
import os
import sys
import re
import argparse
import base64
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from src.email_sender import EmailSender

load_dotenv()

# Issue tracking file
ISSUE_FILE = Path('state/issue_number.txt')

def get_issue_number() -> int:
    """Get the current issue number."""
    if ISSUE_FILE.exists():
        return int(ISSUE_FILE.read_text().strip())
    return 1

def increment_issue_number() -> int:
    """Increment and return the new issue number."""
    current = get_issue_number()
    new_num = current + 1
    ISSUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    ISSUE_FILE.write_text(str(new_num))
    return new_num

def get_logo_html(size: int = 40) -> str:
    """Get the logo as inline HTML table (email-client compatible)."""
    # Create a simple M monogram using tables for maximum email compatibility
    scale = size / 40
    return f'''<table role="presentation" cellpadding="0" cellspacing="0" style="width: {size}px; height: {size}px; background-color: #1a1a2e; border-radius: {int(size/2)}px;">
        <tr>
            <td align="center" valign="middle" style="font-family: Georgia, serif; font-size: {int(22*scale)}px; font-weight: bold; color: #ffffff; line-height: 1;">
                M
            </td>
        </tr>
    </table>'''

def format_bold_text(text: str) -> str:
    """Convert **text** markdown to <strong>text</strong> HTML."""
    # Use regex to properly handle bold markers
    return re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

def estimate_reading_time(content: str) -> int:
    """Estimate reading time in minutes (average 200 words per minute)."""
    words = len(content.split())
    return max(1, round(words / 200))


def create_section_html(title: str, paragraphs: list) -> str:
    """Create HTML for a single section."""
    content = ""
    for i, p in enumerate(paragraphs):
        # Handle bullet points
        if p.startswith('- '):
            p = format_bold_text(p[2:])
            content += f'<p style="margin: 0 0 10px 0; font-size: 15px; line-height: 1.7; color: #333333; padding-left: 20px;">• {p}</p>'
        else:
            p = format_bold_text(p)
            margin = "0" if i == len(paragraphs) - 1 else "0 0 14px 0"
            content += f'<p style="margin: {margin}; font-size: 15px; line-height: 1.7; color: #333333;">{p}</p>'

    return f'''
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 32px;">
                <tr>
                    <td>
                        <h2 style="margin: 0 0 14px 0; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: #5597cb;">
                            {title}
                        </h2>
                        {content}
                    </td>
                </tr>
            </table>
'''

def create_daily_html(date_str: str, content: str, issue_num: int) -> str:
    """Create styled HTML email for daily brief."""
    # Parse date
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    date_display = date_obj.strftime('%B %d, %Y')
    day_name = date_obj.strftime('%A')

    # Get reading time
    reading_time = estimate_reading_time(content)

    # Get logo
    logo_html = get_logo_html(40)
    logo_html_small = get_logo_html(32)

    # Parse content into sections
    lines = content.strip().split('\n')

    # Skip the date header if present
    if lines[0].startswith('# '):
        lines = lines[1:]

    # Get the lead paragraph (first non-empty line)
    lead = ""
    content_start = 0
    for i, line in enumerate(lines):
        line = line.strip()
        if line and not line.startswith('**'):
            lead = line
            content_start = i + 1
            break
        elif line.startswith('**') and not line.endswith('**'):
            lead = line
            content_start = i + 1
            break

    # Format bold text in lead
    lead = format_bold_text(lead)

    # Parse sections
    sections_html = ""
    current_section = None
    current_content = []

    for line in lines[content_start:]:
        line = line.strip()
        if not line:
            continue

        if line.startswith('**') and line.endswith('**'):
            if current_section:
                sections_html += create_section_html(current_section, current_content)
            current_section = line.strip('*')
            current_content = []
        else:
            current_content.append(line)

    if current_section:
        sections_html += create_section_html(current_section, current_content)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Daily Macro & Market Brief | {date_display}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5;">
        <tr>
            <td align="center" style="padding: 40px 20px;">
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width: 680px; background-color: #ffffff; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                    <!-- Header -->
                    <tr>
                        <td style="background-color: #040505; padding: 32px 48px 28px 48px;">
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="width: 50px; vertical-align: top;">
                                        {logo_html}
                                    </td>
                                    <td style="padding-left: 16px; vertical-align: middle;">
                                        <p style="margin: 0 0 4px 0; font-size: 11px; letter-spacing: 3px; text-transform: uppercase; color: #5597cb; font-weight: 500;">
                                            The Daily Macro & Market Brief
                                        </p>
                                        <h1 style="margin: 0; font-size: 28px; font-weight: 300; color: #ffffff; line-height: 1.2; letter-spacing: -0.5px;">
                                            {date_display}
                                        </h1>
                                    </td>
                                    <td align="right" valign="top" style="padding-top: 4px;">
                                        <p style="margin: 0 0 4px 0; font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; color: #666666;">
                                            {day_name}
                                        </p>
                                        <p style="margin: 0; font-size: 10px; letter-spacing: 1px; color: #5597cb;">
                                            Issue #{issue_num}
                                        </p>
                                        <p style="margin: 4px 0 0 0; font-size: 10px; color: #666666;">
                                            {reading_time} min read
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- Accent Line -->
                    <tr>
                        <td style="background: linear-gradient(90deg, #5597cb 0%, #aac3e3 100%); height: 3px;"></td>
                    </tr>
                    <!-- Lead Section -->
                    <tr>
                        <td style="padding: 40px 48px 28px 48px; border-bottom: 1px solid #e8e8e8;">
                            <p style="margin: 0; font-size: 18px; line-height: 1.65; color: #1a1a1a; font-weight: 400;">
                                {lead}
                            </p>
                            <p style="margin: 20px 0 0 0; font-size: 12px; line-height: 1.5; color: #888888; font-style: italic; letter-spacing: 0.3px;">
                                What moved markets today, by order of importance.
                            </p>
                        </td>
                    </tr>
                    <!-- Content -->
                    <tr>
                        <td style="padding: 36px 48px;">
                            {sections_html}
                        </td>
                    </tr>
                    <!-- Forward CTA -->
                    <tr>
                        <td style="padding: 0 48px 36px 48px;">
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8f9fa; border-radius: 4px;">
                                <tr>
                                    <td style="padding: 20px 24px; text-align: center;">
                                        <p style="margin: 0 0 8px 0; font-size: 13px; color: #555555;">
                                            Know someone who'd find this useful?
                                        </p>
                                        <p style="margin: 0; font-size: 14px; font-weight: 600; color: #5597cb;">
                                            Forward this email to a colleague
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- Thanks -->
                    <tr>
                        <td style="padding: 0 48px 40px 48px; text-align: center;">
                            <p style="margin: 0; font-size: 14px; color: #888888; font-style: italic;">
                                Thanks for reading. See you tomorrow.
                            </p>
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #040505; padding: 36px 48px;">
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="width: 40px; vertical-align: top;">
                                        {logo_html_small}
                                    </td>
                                    <td style="padding-left: 14px;">
                                        <p style="margin: 0 0 4px 0; font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: #5597cb;">
                                            The Daily Macro & Market Brief
                                        </p>
                                        <p style="margin: 0; font-size: 12px; color: #666666; line-height: 1.5;">
                                            Cut through the noise. Get the macro story in 5 minutes.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>'''


def create_weekly_html(week_label: str, content: str, issue_num: int) -> str:
    """Create styled HTML email for weekly brief."""
    # Get reading time
    reading_time = estimate_reading_time(content)

    # Get logo
    logo_html = get_logo_html(40)
    logo_html_small = get_logo_html(32)

    # Parse content into sections
    lines = content.strip().split('\n')

    # Skip the week header if present
    if lines[0].startswith('# '):
        lines = lines[1:]

    # Get the lead paragraph(s) - everything before first section header
    lead_parts = []
    content_start = 0
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        if line.startswith('**') and line.endswith('**'):
            content_start = i
            break
        lead_parts.append(line)

    lead = format_bold_text(' '.join(lead_parts))

    # Parse sections
    sections_html = ""
    current_section = None
    current_content = []

    for line in lines[content_start:]:
        line = line.strip()
        if not line:
            continue

        if line.startswith('**') and line.endswith('**'):
            if current_section:
                sections_html += create_section_html(current_section, current_content)
            current_section = line.strip('*')
            current_content = []
        else:
            current_content.append(line)

    if current_section:
        sections_html += create_section_html(current_section, current_content)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Daily Macro & Market Brief | Week of {week_label}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5;">
        <tr>
            <td align="center" style="padding: 40px 20px;">
                <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width: 680px; background-color: #ffffff; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                    <!-- Header -->
                    <tr>
                        <td style="background-color: #040505; padding: 32px 48px 28px 48px;">
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="width: 50px; vertical-align: top;">
                                        {logo_html}
                                    </td>
                                    <td style="padding-left: 16px; vertical-align: middle;">
                                        <p style="margin: 0 0 4px 0; font-size: 11px; letter-spacing: 3px; text-transform: uppercase; color: #5597cb; font-weight: 500;">
                                            The Daily Macro & Market Brief
                                        </p>
                                        <h1 style="margin: 0; font-size: 24px; font-weight: 300; color: #ffffff; line-height: 1.2; letter-spacing: -0.5px;">
                                            Week of {week_label}
                                        </h1>
                                    </td>
                                    <td align="right" valign="top" style="padding-top: 4px;">
                                        <p style="margin: 0 0 4px 0; font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; color: #666666;">
                                            Weekly Digest
                                        </p>
                                        <p style="margin: 0; font-size: 10px; letter-spacing: 1px; color: #5597cb;">
                                            Issue #{issue_num}
                                        </p>
                                        <p style="margin: 4px 0 0 0; font-size: 10px; color: #666666;">
                                            {reading_time} min read
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- Accent Line -->
                    <tr>
                        <td style="background: linear-gradient(90deg, #5597cb 0%, #aac3e3 100%); height: 3px;"></td>
                    </tr>
                    <!-- Lead Section -->
                    <tr>
                        <td style="padding: 40px 48px 28px 48px; border-bottom: 1px solid #e8e8e8;">
                            <p style="margin: 0; font-size: 17px; line-height: 1.65; color: #1a1a1a; font-weight: 400;">
                                {lead}
                            </p>
                            <p style="margin: 20px 0 0 0; font-size: 12px; line-height: 1.5; color: #888888; font-style: italic; letter-spacing: 0.3px;">
                                What moved markets this week, by order of importance.
                            </p>
                        </td>
                    </tr>
                    <!-- Content -->
                    <tr>
                        <td style="padding: 36px 48px;">
                            {sections_html}
                        </td>
                    </tr>
                    <!-- Forward CTA -->
                    <tr>
                        <td style="padding: 0 48px 36px 48px;">
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8f9fa; border-radius: 4px;">
                                <tr>
                                    <td style="padding: 20px 24px; text-align: center;">
                                        <p style="margin: 0 0 8px 0; font-size: 13px; color: #555555;">
                                            Know someone who'd find this useful?
                                        </p>
                                        <p style="margin: 0; font-size: 14px; font-weight: 600; color: #5597cb;">
                                            Forward this email to a colleague
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- Thanks -->
                    <tr>
                        <td style="padding: 0 48px 40px 48px; text-align: center;">
                            <p style="margin: 0; font-size: 14px; color: #888888; font-style: italic;">
                                Thanks for reading. See you next week.
                            </p>
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #040505; padding: 36px 48px;">
                            <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="width: 40px; vertical-align: top;">
                                        {logo_html_small}
                                    </td>
                                    <td style="padding-left: 14px;">
                                        <p style="margin: 0 0 4px 0; font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: #5597cb;">
                                            The Daily Macro & Market Brief
                                        </p>
                                        <p style="margin: 0; font-size: 12px; color: #666666; line-height: 1.5;">
                                            Cut through the noise. Get the macro story in 5 minutes.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>'''


def send_daily_brief(date_str: str, preview: bool = False):
    """Send the daily brief for a given date."""
    brief_path = Path(f'summaries/_daily_briefs/{date_str}_daily_brief.md')
    if not brief_path.exists():
        print(f"Daily brief not found: {brief_path}")
        return False

    with open(brief_path) as f:
        content = f.read()

    issue_num = get_issue_number()
    html = create_daily_html(date_str, content, issue_num)

    if preview:
        preview_path = Path(f'substack/email_preview_daily_{date_str}.html')
        preview_path.write_text(html)
        print(f"Preview saved to: {preview_path}")
        return True

    # Parse date for subject
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    date_display = date_obj.strftime('%B %d, %Y')

    sender = EmailSender(
        smtp_server=os.getenv('SMTP_SERVER'),
        smtp_port=int(os.getenv('SMTP_PORT')),
        username=os.getenv('SMTP_USERNAME'),
        password=os.getenv('SMTP_PASSWORD'),
        from_address=os.getenv('EMAIL_FROM')
    )

    success = sender.send_summary(
        to_address=os.getenv('EMAIL_TO'),
        subject=f"Daily Macro & Market Brief — {date_display}",
        html_body=html,
        plain_text_body=content
    )

    if success:
        increment_issue_number()

    return success


def send_weekly_brief(week_str: str, preview: bool = False):
    """Send the weekly brief for a given week (YYYY-WNN format)."""
    brief_path = Path(f'summaries/_weekly_briefs/{week_str}_weekly_brief.md')
    if not brief_path.exists():
        print(f"Weekly brief not found: {brief_path}")
        return False

    with open(brief_path) as f:
        content = f.read()

    # Extract week label from first line
    first_line = content.split('\n')[0]
    week_label = first_line.replace('# Week of ', '').strip()

    issue_num = get_issue_number()
    html = create_weekly_html(week_label, content, issue_num)

    if preview:
        preview_path = Path(f'substack/email_preview_weekly_{week_str}.html')
        preview_path.write_text(html)
        print(f"Preview saved to: {preview_path}")
        return True

    sender = EmailSender(
        smtp_server=os.getenv('SMTP_SERVER'),
        smtp_port=int(os.getenv('SMTP_PORT')),
        username=os.getenv('SMTP_USERNAME'),
        password=os.getenv('SMTP_PASSWORD'),
        from_address=os.getenv('EMAIL_FROM')
    )

    success = sender.send_summary(
        to_address=os.getenv('EMAIL_TO'),
        subject=f"Weekly Macro & Market Brief — {week_label}",
        html_body=html,
        plain_text_body=content
    )

    if success:
        increment_issue_number()

    return success


def main():
    parser = argparse.ArgumentParser(description='Send daily or weekly briefs via email')
    parser.add_argument('--daily', type=str, help='Send daily brief for date (YYYY-MM-DD)')
    parser.add_argument('--weekly', type=str, help='Send weekly brief (YYYY-WNN format)')
    parser.add_argument('--preview', action='store_true', help='Save HTML preview instead of sending')
    parser.add_argument('--set-issue', type=int, help='Set the issue number')

    args = parser.parse_args()

    if args.set_issue:
        ISSUE_FILE.parent.mkdir(parents=True, exist_ok=True)
        ISSUE_FILE.write_text(str(args.set_issue))
        print(f"Issue number set to {args.set_issue}")
        return

    if args.daily:
        success = send_daily_brief(args.daily, preview=args.preview)
        if success:
            action = "Preview saved" if args.preview else "Sent"
            print(f"✓ Daily brief for {args.daily} - {action} (Issue #{get_issue_number()})")
        else:
            print(f"✗ Failed to process daily brief")
            sys.exit(1)

    if args.weekly:
        success = send_weekly_brief(args.weekly, preview=args.preview)
        if success:
            action = "Preview saved" if args.preview else "Sent"
            print(f"✓ Weekly brief for {args.weekly} - {action} (Issue #{get_issue_number()})")
        else:
            print(f"✗ Failed to process weekly brief")
            sys.exit(1)

    if not args.daily and not args.weekly and not args.set_issue:
        parser.print_help()


if __name__ == '__main__':
    main()
