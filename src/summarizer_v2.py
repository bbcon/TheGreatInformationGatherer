"""
AI-powered video transcript summarization module for macro trading analysis.
"""
from typing import Dict, Optional
from anthropic import Anthropic
from config_handler import ConfigHandler


class MacroTradingSummarizer:
    """Generates macro trading-focused summaries from video transcripts."""

    SYSTEM_PROMPT = """You are an expert macro trading analyst specializing in synthesizing market commentary into actionable intelligence. Your role is to analyze video transcripts from market analysts and extract key information relevant to global macro trading decisions.

TONE:
- Write like a Goldman Sachs research note, not a news article
- Be measured and analytical - avoid sensationalism
- Use strong words (historic, unprecedented, crisis, crashed, plunged) ONLY when truly justified - not for routine market moves
- Default to neutral language: fell/rose, declined/gained, increased/decreased
- Let data speak for itself - "gold fell 8%" is impactful without adding "worst since 1983"
- Readers are sophisticated professionals who find unnecessary hyperbole off-putting

MACRO CONSISTENCY:
- Ensure all narratives are logically consistent
- Think through cause and effect: policy X should logically lead to market reaction Y
- If data seems contradictory, note the tension rather than glossing over it

ACKNOWLEDGE UNCERTAINTY:
- Don't over-interpret single data points or events
- Use hedging language where appropriate: "appears to," "may signal," "suggests"
- Distinguish between what happened (facts) and what it means (interpretation)
- Avoid false narrative closure - many situations remain genuinely uncertain"""

    SUMMARY_PROMPT = """Analyze this video transcript and provide a comprehensive summary focused on macro trading insights.

Structure your summary with the following sections:

## 🎯 Executive Summary
(2-3 sentences capturing the core thesis and market view)

## 📊 Key Macro Indicators Discussed
- List specific economic indicators mentioned (GDP, inflation, employment, PMI, etc.)
- Include any data points, forecasts, or trends discussed
- Note any surprises or divergences from consensus

## 💹 Market Outlook & Positioning
- Asset class views (equities, bonds, FX, commodities)
- Geographic/sector preferences or concerns
- Risk-on vs risk-off sentiment
- Any specific trade ideas or positioning recommendations

## 🏦 Central Bank & Policy Developments
- Federal Reserve, ECB, BOJ, or other central bank commentary
- Interest rate expectations and monetary policy outlook
- Fiscal policy discussions

## ⚠️ Key Risks & Catalysts
- Upside and downside risks mentioned
- Upcoming events or catalysts to watch
- Tail risk scenarios

## 📈 Technical Levels & Price Action (if discussed)
- Key support/resistance levels mentioned
- Chart patterns or technical setups discussed

## 🔑 Actionable Takeaways
- 3-5 bullet points of the most actionable insights for traders

Keep the summary concise but comprehensive. Focus on facts, data, and specific views rather than general commentary.
If certain sections have no relevant content, you may omit them.

VIDEO TRANSCRIPT:
{transcript}

Provide your analysis now:"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929", config: Optional[ConfigHandler] = None):
        """
        Initialize the summarizer.

        Args:
            api_key: Anthropic API key
            model: Claude model to use (default: claude-sonnet-4-5-20250929)
            config: Optional ConfigHandler for customization
        """
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.config = config or ConfigHandler()

    def _build_prompt(self, transcript: str) -> str:
        """Build custom prompt based on configuration."""
        sections = self.config.get_prompt_sections()
        length = self.config.get_summary_length()
        custom_instructions = self.config.get_custom_instructions()

        # Build section list based on config with improved instructions
        section_list = []
        if sections.get('executive_summary', True):
            section_list.append("## 🎯 Executive Summary\n**1-2 sentences max.** Core thesis only. What changed? What matters most?")
        if sections.get('macro_indicators', True):
            section_list.append("## 📊 Key Macro Data\n**Short bullets only.** Lead with actual numbers in bold. Format: **Indicator: Value** - brief context")
        if sections.get('market_outlook', True):
            section_list.append("## 💹 Markets & Positioning\n**Concise bullets by asset class.** Format: **Asset: Direction** - key driver. Skip generic commentary.")
        if sections.get('central_bank_policy', True):
            section_list.append("## 🏦 Central Banks\n**Key developments only.** Lead with **bold policy changes**. Skip if nothing material.")
        if sections.get('risks_catalysts', True):
            section_list.append("## ⚠️ Risks & Catalysts\n**2-3 most important items only.** Format: **Risk/Event** - impact. Prioritize by materiality.")
        if sections.get('technical_levels', False):
            section_list.append("## 📈 Technical Levels\n**Key levels only.** Format: **Asset: Level** - setup. Skip if not discussed.")
        if sections.get('actionable_takeaways', True):
            section_list.append("## 🔑 Action Items\n**3-5 specific trades/positions.** Format: **Action** - rationale (1 line max). Must be immediately tradeable.")

        sections_text = "\n\n".join(section_list)

        # Length instructions - emphasize conciseness
        length_instruction = {
            'concise': "Extremely brief. Every bullet should be 1 line. Use short phrases.",
            'standard': "Concise but complete. Each bullet 1-2 lines maximum. No paragraphs.",
            'detailed': "Moderate detail allowed but stay concise. Prefer bullets over paragraphs."
        }.get(length, "Concise but complete. Each bullet 1-2 lines maximum.")

        prompt = f"""Analyze this video transcript and provide a CONCISE, SCANNABLE summary.

CRITICAL: Make this easy to skim in 30 seconds. Prioritize brevity and clarity.

Structure your summary with these sections:

{sections_text}

FORMATTING RULES:
- Use **bold** for all key numbers, data points, asset names, and action verbs
- Lead each bullet with the most important information
- Keep bullets to 1-2 lines maximum
- Use short phrases - eliminate filler words
- Skip anything non-material or generic
- If a section has no material content, omit it entirely

{custom_instructions}

VIDEO TRANSCRIPT:
{transcript}

Provide your concise analysis now:"""

        return prompt

    def generate_summary(self, transcript: str, video_metadata: Optional[Dict] = None) -> Dict:
        """
        Generate a macro trading-focused summary of the video transcript.

        Args:
            transcript: Full video transcript text
            video_metadata: Optional metadata about the video

        Returns:
            Dictionary containing the summary and metadata
        """
        try:
            # Create the prompt with the transcript
            prompt = self._build_prompt(transcript)

            # Call Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0.3,  # Lower temperature for more consistent, factual output
                system=self.SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract the summary text
            summary_text = message.content[0].text

            # Build result
            result = {
                'summary': summary_text,
                'model': self.model,
                'tokens_used': {
                    'input': message.usage.input_tokens,
                    'output': message.usage.output_tokens
                }
            }

            if video_metadata:
                result['video_metadata'] = video_metadata

            return result

        except Exception as e:
            print(f"Error generating summary: {e}")
            raise

    def generate_summary_with_context(
        self,
        transcript: str,
        video_metadata: Optional[Dict] = None,
        previous_summaries: Optional[list] = None
    ) -> Dict:
        """
        Generate a summary with additional context from previous videos.

        Args:
            transcript: Full video transcript text
            video_metadata: Optional metadata about the video
            previous_summaries: Optional list of previous video summaries for context

        Returns:
            Dictionary containing the summary and metadata
        """
        # For now, this is a placeholder for future enhancement
        # You could include previous_summaries in the prompt to track
        # evolving views and changes in outlook
        return self.generate_summary(transcript, video_metadata)

    def format_as_markdown(self, summary_data: Dict) -> str:
        """
        Format summary data as standalone markdown.

        Args:
            summary_data: Dictionary containing summary and metadata

        Returns:
            Markdown formatted summary
        """
        return summary_data['summary']

    def format_email_body(self, summary_data: Dict) -> str:
        """
        Format the summary data into an email body.

        Args:
            summary_data: Dictionary containing summary and metadata

        Returns:
            Formatted email body as HTML
        """
        metadata = summary_data.get('video_metadata', {})
        summary = summary_data['summary']

        # Convert markdown to simple HTML-like formatting for email
        # Most email clients support basic HTML
        email_body = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #2980b9; margin-top: 20px; }}
        .metadata {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .summary {{ background-color: #fff; padding: 20px; }}
        ul {{ padding-left: 20px; }}
        a {{ color: #3498db; text-decoration: none; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #bdc3c7; font-size: 0.9em; color: #7f8c8d; }}
    </style>
</head>
<body>
    <h1>📊 Daily Macro Trading Video Summary</h1>

    <div class="metadata">
        <strong>Video Title:</strong> {metadata.get('title', 'N/A')}<br>
        <strong>Channel:</strong> {metadata.get('channel_title', 'N/A')}<br>
        <strong>Published:</strong> {metadata.get('published_at', 'N/A')}<br>
        <strong>URL:</strong> <a href="{metadata.get('url', '#')}">{metadata.get('url', 'N/A')}</a>
    </div>

    <div class="summary">
        {self._markdown_to_html(summary)}
    </div>

    <div class="footer">
        <p>This summary was automatically generated by The Great Information Gatherer.</p>
        <p><strong>Model used:</strong> {summary_data.get('model', 'N/A')} |
           <strong>Tokens:</strong> {summary_data.get('tokens_used', {}).get('input', 0)} input,
           {summary_data.get('tokens_used', {}).get('output', 0)} output</p>
    </div>
</body>
</html>
"""
        return email_body

    def _markdown_to_html(self, markdown_text: str) -> str:
        """
        Convert markdown to HTML for email formatting.

        Args:
            markdown_text: Markdown formatted text

        Returns:
            HTML formatted text
        """
        import re

        lines = markdown_text.split('\n')
        result = []
        in_list = False

        for line in lines:
            stripped = line.strip()

            # Skip empty lines
            if not stripped:
                if in_list:
                    result.append('</ul>')
                    in_list = False
                continue

            # Headers (##)
            if stripped.startswith('## '):
                if in_list:
                    result.append('</ul>')
                    in_list = False
                header_text = stripped[3:].strip()
                result.append(f'<h2>{header_text}</h2>')

            # Bullet points (-)
            elif stripped.startswith('- '):
                if not in_list:
                    result.append('<ul>')
                    in_list = True
                # Process the list item text for inline formatting
                item_text = self._process_inline_markdown(stripped[2:])
                result.append(f'<li>{item_text}</li>')

            # Regular paragraphs
            else:
                if in_list:
                    result.append('</ul>')
                    in_list = False
                # Process inline formatting
                processed_text = self._process_inline_markdown(stripped)
                result.append(f'<p>{processed_text}</p>')

        # Close any open list
        if in_list:
            result.append('</ul>')

        return '\n'.join(result)

    def _process_inline_markdown(self, text: str) -> str:
        """
        Process inline markdown formatting (bold, italic, etc).

        Args:
            text: Text with markdown formatting

        Returns:
            HTML formatted text
        """
        import re

        # Bold (**text** or __text__)
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)

        # Italic (*text* or _text_)
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)

        # Code (`text`)
        text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)

        return text
