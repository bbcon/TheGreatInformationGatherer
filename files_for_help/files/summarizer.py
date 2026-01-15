"""
AI summarizer module for generating market insights
"""

import logging
import os
from datetime import datetime


class Summarizer:
    """Generates summaries using AI (Claude or GPT)"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.summary_config = config['summary']
        
        # Initialize AI client
        self.provider = self.summary_config.get('provider', 'anthropic')
        
        if self.provider == 'anthropic':
            from anthropic import Anthropic
            self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        elif self.provider == 'openai':
            from openai import OpenAI
            self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def summarize(self, transcript, video_info):
        """
        Generate summary from transcript
        Returns formatted summary text
        """
        self.logger.info("Generating AI summary...")
        
        # Build prompt
        prompt = self._build_prompt(transcript, video_info)
        
        # Get AI response
        if self.provider == 'anthropic':
            summary = self._summarize_with_claude(prompt)
        else:
            summary = self._summarize_with_gpt(prompt)
        
        # Format the summary
        formatted = self._format_summary(summary, video_info)
        
        self.logger.info("Summary generated successfully")
        return formatted
    
    def _build_prompt(self, transcript, video_info):
        """Build the summarization prompt"""
        
        sections = self.summary_config.get('include_sections', [])
        focus_areas = self.summary_config.get('focus_areas', [])
        detail_level = self.summary_config.get('detail_level', 'concise')
        
        prompt = f"""You are a financial analyst summarizing Bloomberg's daily markets video.

VIDEO INFORMATION:
Title: {video_info.get('title', 'Unknown')}
Date: {datetime.now().strftime('%Y-%m-%d')}

TRANSCRIPT:
{transcript}

Please provide a comprehensive yet {detail_level} summary structured as follows:

"""
        
        section_descriptions = {
            'executive_summary': '1. EXECUTIVE SUMMARY: 2-3 sentences capturing the day\'s key market narrative',
            'market_movements': '2. MARKET MOVEMENTS: Key performance of major indices, currencies, and commodities',
            'top_stories': '3. TOP STORIES: 3-5 most important market-moving news items',
            'economic_data': '4. ECONOMIC DATA: Key economic releases and their implications',
            'notable_quotes': '5. NOTABLE QUOTES: Important insights from analysts or market participants',
            'outlook': '6. OUTLOOK: What to watch for in upcoming sessions'
        }
        
        for section in sections:
            if section in section_descriptions:
                prompt += f"{section_descriptions[section]}\n\n"
        
        if focus_areas:
            prompt += "FOCUS AREAS:\n"
            for area in focus_areas:
                prompt += f"- {area}\n"
            prompt += "\n"
        
        prompt += """
Format the summary in clear markdown with proper headings. Use bullet points where appropriate.
Focus on actionable insights and specific data points (percentages, prices, levels).
Maintain a professional, objective tone suitable for investment professionals.
"""
        
        return prompt
    
    def _summarize_with_claude(self, prompt):
        """Generate summary using Claude"""
        try:
            model = self.summary_config.get('model', 'claude-sonnet-4-20250514')
            max_tokens = self.summary_config.get('max_tokens', 2000)
            
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            return response.content[0].text
            
        except Exception as e:
            self.logger.error(f"Claude API error: {str(e)}")
            raise
    
    def _summarize_with_gpt(self, prompt):
        """Generate summary using GPT"""
        try:
            model = self.summary_config.get('model', 'gpt-4-turbo')
            max_tokens = self.summary_config.get('max_tokens', 2000)
            
            response = self.client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    def _format_summary(self, summary, video_info):
        """Add header and metadata to summary"""
        
        header = f"""# Bloomberg Markets Summary
**Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Video:** {video_info.get('title', 'Unknown')}  
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
        
        footer = f"""

---

*This summary was automatically generated from Bloomberg Markets video content.*
"""
        
        return header + summary + footer
