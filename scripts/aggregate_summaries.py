#!/usr/bin/env python3
"""
Aggregate Summaries - Create a meta-summary from recent show summaries.

This script collects summaries from the past N days across all shows and generates
a consolidated summary of key events, trends, and takeaways.
"""

import os
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any
import anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def load_config():
    """Load configuration from config.yaml."""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)


def load_shows_config():
    """Load shows configuration."""
    with open('shows_config.yaml', 'r') as f:
        return yaml.safe_load(f)


def find_recent_summaries(days: int = 10, start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
    """
    Find all summary files from the past N days or within a date range.

    Args:
        days: Number of days to look back (used if start_date/end_date not provided)
        start_date: Start date in YYYY-MM-DD format (inclusive)
        end_date: End date in YYYY-MM-DD format (inclusive)

    Returns:
        List of summary data with metadata
    """
    summaries = []

    # Determine date range
    if start_date and end_date:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    else:
        end_dt = datetime.now()
        start_dt = end_dt - timedelta(days=days)

    summaries_dir = Path('summaries')

    if not summaries_dir.exists():
        print("No summaries directory found.")
        return []

    # Iterate through all show directories
    for show_dir in summaries_dir.iterdir():
        if not show_dir.is_dir():
            continue

        show_name = show_dir.name

        # Iterate through date directories
        for date_dir in show_dir.iterdir():
            if not date_dir.is_dir():
                continue

            try:
                # Parse date from directory name (YYYY-MM-DD format)
                dir_date = datetime.strptime(date_dir.name, '%Y-%m-%d')

                # Skip if outside date range
                if dir_date < start_dt or dir_date > end_dt:
                    continue

                # Find JSON summary files in this directory
                for json_file in date_dir.glob('summary_*.json'):
                    try:
                        with open(json_file, 'r') as f:
                            data = json.load(f)

                        summaries.append({
                            'show_name': show_name,
                            'date': dir_date,
                            'date_str': date_dir.name,
                            'file_path': str(json_file),
                            'title': data.get('title', 'Unknown'),
                            'summary': data.get('summary', ''),
                            'metadata': data.get('metadata', {})
                        })
                    except Exception as e:
                        print(f"Warning: Could not load {json_file}: {e}")

            except ValueError:
                # Skip directories that don't match date format
                continue

    # Sort by date, most recent first
    summaries.sort(key=lambda x: x['date'], reverse=True)
    return summaries


def generate_aggregate_summary(summaries: List[Dict[str, Any]], config: dict) -> str:
    """
    Generate a meta-summary from multiple show summaries using Claude.

    Args:
        summaries: List of summary data
        config: Configuration dictionary

    Returns:
        Aggregated summary text
    """
    if not summaries:
        return "No summaries found for the specified time period."

    # Build context from all summaries
    context_parts = []
    for s in summaries:
        context_parts.append(
            f"## {s['show_name'].replace('_', ' ').title()} - {s['date_str']}\n"
            f"{s['summary']}\n"
        )

    context = "\n\n".join(context_parts)

    # Build the aggregation prompt
    prompt = f"""You are analyzing summaries from Bloomberg financial news shows over the past {len(set(s['date_str'] for s in summaries))} days.

Here are the individual show summaries:

{context}

Please create a comprehensive meta-summary that synthesizes these insights into a cohesive narrative. This should be MORE DETAILED than the individual summaries - add context, connections, and implications.

Structure your summary with these sections:

## 1. Executive Overview
- **2-3 paragraphs** providing the big picture of what happened over this period
- Connect the dots between different days and shows
- What's the overarching narrative? (e.g., "risk-off driven by...", "rotation from X to Y")

## 2. Major Themes & Market Narratives
- Identify **3-5 major themes** that emerged across multiple shows/days
- For each theme, provide context and explain WHY it matters
- Note any evolution or shifts in narrative over the period
- Highlight divergences between market pricing and fundamentals

## 3. Key Market Developments
Break down by asset class with specific details:
- **Equities**: Major moves, sector rotation, earnings highlights
- **Fixed Income**: Yield movements, curve dynamics, credit spreads
- **FX**: Notable currency moves and drivers
- **Commodities**: Oil, metals, agri - significant moves and reasons
- Include actual numbers, percentage moves, and specific levels where mentioned

## 4. Central Bank & Policy Watch
- Fed, ECB, BoE, BoJ, PBoC - any commentary, data, or positioning changes
- Market expectations vs reality
- Forward guidance and policy trajectory implications
- Any notable divergences between central banks

## 5. Geopolitical & Macro Catalysts
- Significant political/geopolitical events affecting markets
- Macro data releases and surprises
- Policy announcements or regulatory changes
- Trade/tariff developments

## 6. Sector & Regional Focus
- Which sectors outperformed/underperformed and why
- Regional market dynamics (US, Europe, Asia, EM)
- Any sector-specific catalysts or developments
- Notable company/industry developments

## 7. Actionable Insights & Forward Look
- What are the key takeaways for positioning?
- What are markets pricing in vs what might actually happen?
- Key risks to watch
- Upcoming catalysts and data to monitor
- Trade ideas or positioning suggestions mentioned by commentators

CRITICAL REQUIREMENTS:
- **Add meat and substance** - this should be LONGER and MORE DETAILED than the individual summaries
- Use **bold** for critical numbers, dates, levels, and key takeaways
- Provide CONTEXT - don't just list facts, explain WHY they matter
- Connect themes across different shows and days
- Include specific data points, percentages, and levels when available
- Highlight what's consensus vs what's contrarian
- Make it informative enough that someone could discuss these topics intelligently

Target length: This should take 5-7 minutes to read thoroughly. Don't be afraid to add detail and context."""

    # Call Claude API
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = anthropic.Anthropic(api_key=api_key)

    print(f"\nGenerating aggregate summary from {len(summaries)} show summaries...")

    response = client.messages.create(
        model=config.get('model', 'claude-opus-4-5-20251101'),
        max_tokens=8192,  # Increased for more detailed output
        temperature=config.get('temperature', 0.3),
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    summary_text = response.content[0].text

    # Print token usage
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens

    # Rough cost estimation (opus 4.5 pricing: $15/MTok input, $75/MTok output)
    cost = (input_tokens / 1_000_000 * 15) + (output_tokens / 1_000_000 * 75)

    print(f"✓ Aggregate summary generated!")
    print(f"  Input tokens: {input_tokens:,}")
    print(f"  Output tokens: {output_tokens:,}")
    print(f"  Estimated cost: ${cost:.4f}")

    return summary_text


def markdown_to_html(markdown_text: str) -> str:
    """
    Convert markdown to simple HTML for email.

    Args:
        markdown_text: Markdown formatted text

    Returns:
        HTML formatted text
    """
    import re

    html = markdown_text

    # Headers
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

    # Bullet points - convert to proper list
    lines = html.split('\n')
    in_list = False
    new_lines = []

    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                new_lines.append('<ul>')
                in_list = True
            new_lines.append(f'<li>{line.strip()[2:]}</li>')
        else:
            if in_list:
                new_lines.append('</ul>')
                in_list = False
            new_lines.append(line)

    if in_list:
        new_lines.append('</ul>')

    html = '\n'.join(new_lines)

    # Paragraphs (add <br> for double newlines)
    html = re.sub(r'\n\n+', '<br><br>', html)

    return html


def save_aggregate_summary(summary_text: str, summaries: List[Dict[str, Any]], period_desc: str) -> str:
    """
    Save the aggregate summary to a file.

    Args:
        summary_text: The generated summary
        summaries: List of source summaries
        period_desc: Description of the period covered

    Returns:
        Path to saved file
    """
    output_dir = Path('summaries') / '_aggregates'
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"aggregate_{timestamp}.md"
    filepath = output_dir / filename

    # Build markdown with metadata
    markdown = f"""# Bloomberg Shows Aggregate Summary
**Period**: {period_desc} ({len(set(s['date_str'] for s in summaries))} unique dates)
**Shows covered**: {', '.join(sorted(set(s['show_name'].replace('_', ' ').title() for s in summaries)))}
**Total summaries**: {len(summaries)}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

{summary_text}

---

## Source Summaries
"""

    for s in summaries:
        markdown += f"\n- [{s['show_name'].replace('_', ' ').title()}] {s['date_str']}: {s['title']}"

    with open(filepath, 'w') as f:
        f.write(markdown)

    print(f"\n✓ Aggregate summary saved to: {filepath}")
    return str(filepath)


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Generate aggregate summary from recent show summaries'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=10,
        help='Number of days to look back (default: 10)'
    )
    parser.add_argument(
        '--no-email',
        action='store_true',
        help='Skip sending email (just save to file)'
    )
    parser.add_argument(
        '--start-date',
        type=str,
        help='Start date in YYYY-MM-DD format (inclusive)'
    )
    parser.add_argument(
        '--end-date',
        type=str,
        help='End date in YYYY-MM-DD format (inclusive)'
    )

    args = parser.parse_args()

    # Determine period description
    if args.start_date and args.end_date:
        period_desc = f"{args.start_date} to {args.end_date}"
    else:
        period_desc = f"Past {args.days} Days"

    print("=" * 70)
    print(f"Aggregate Summaries - {period_desc}")
    print("=" * 70)

    # Load configurations
    config = load_config()

    # Find recent summaries
    print(f"\n[1/3] Finding summaries for {period_desc}...")
    summaries = find_recent_summaries(
        days=args.days,
        start_date=args.start_date,
        end_date=args.end_date
    )

    if not summaries:
        print(f"\nNo summaries found in the past {args.days} days.")
        return

    unique_dates = len(set(s['date_str'] for s in summaries))
    unique_shows = len(set(s['show_name'] for s in summaries))

    print(f"✓ Found {len(summaries)} summaries across {unique_dates} days from {unique_shows} shows")

    # Generate aggregate summary
    print(f"\n[2/3] Generating aggregate summary...")
    summary_text = generate_aggregate_summary(summaries, config.get('summarizer', {}))

    # Save to file
    print(f"\n[3/3] Saving aggregate summary...")
    filepath = save_aggregate_summary(summary_text, summaries, period_desc)

    # Optionally send email
    if not args.no_email:
        try:
            from src.email_sender import EmailSender

            sender = EmailSender(
                smtp_server=os.getenv('SMTP_SERVER'),
                smtp_port=int(os.getenv('SMTP_PORT', 587)),
                username=os.getenv('SMTP_USERNAME'),
                password=os.getenv('SMTP_PASSWORD'),
                from_address=os.getenv('EMAIL_FROM')
            )

            subject = f"Bloomberg Aggregate Summary - {period_desc}"

            # Convert markdown to HTML
            summary_html = markdown_to_html(summary_text)

            html_body = f"""<html><body style="font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px;">
<h1 style="color: #333; border-bottom: 2px solid #0066cc; padding-bottom: 10px;">Bloomberg Shows Aggregate Summary</h1>
<p style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
<strong>Period:</strong> {period_desc} ({unique_dates} unique dates)<br>
<strong>Shows covered:</strong> {', '.join(sorted(set(s['show_name'].replace('_', ' ').title() for s in summaries)))}<br>
<strong>Total summaries:</strong> {len(summaries)}
</p>
<div style="margin-top: 20px;">
{summary_html}
</div>
<hr style="margin-top: 30px; border: none; border-top: 1px solid #ccc;">
<p style="color: #666; font-size: 0.9em; text-align: center;">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</body></html>"""

            success = sender.send_summary(
                to_address=os.getenv('EMAIL_TO'),
                subject=subject,
                html_body=html_body,
                plain_text_body=summary_text
            )

            if success:
                print(f"✓ Email sent successfully to {os.getenv('EMAIL_TO')}")
            else:
                print("✗ Failed to send email")

        except Exception as e:
            print(f"Warning: Could not send email: {e}")

    print("\n" + "=" * 70)
    print("✓ Complete!")
    print("=" * 70)


if __name__ == '__main__':
    main()
