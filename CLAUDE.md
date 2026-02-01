# Project: The Daily Macro & Market Brief

## What This Is
Automated system to extract Bloomberg TV transcripts, generate macro summaries via Claude, and send styled email newsletters.

## Key Files
- process_show.py - Process a single Bloomberg show
- generate_daily_brief.py - Combine show summaries into daily brief
- generate_weekly_brief.py - Synthesize weekly themes
- send_briefs.py - Send HTML emails

## Style Preferences
- Briefs should be ~750 words (daily), ~1000 words (weekly), ~1500 words (monthly)
- Use bullet points liberally
- Bold key data points in bullets (e.g., **Meta gained 8%**)
- No emojis
- Intro: "What moved markets today, by order of importance."
- Outro: "Thanks for reading. See you tomorrow."

## Writing Tone
- Write like a Goldman Sachs research analyst, not a journalist
- Be measured and analytical - avoid sensationalism
- Use strong words (historic, unprecedented, crisis) ONLY when truly justified - not for routine market moves
- Default to neutral language: fell/rose, declined/gained, increased/decreased
- Let data speak for itself - "gold fell 8%" is impactful without adding "worst since 1983"
- Readers are sophisticated professionals who find unnecessary hyperbole off-putting

## Macro Consistency
- Ensure narratives are macroeconomically consistent and logical
- Example: Trump pressuring Fed = wanting LOWER rates (dovish). Nominating a hawk like Warsh contradicts this narrative, or suggests Warsh may be more dovish than expected
- Don't combine contradictory narratives into a single "theme" - acknowledge the tension
- Think through cause and effect: if X happens, what does it imply for Y?

## Acknowledge Uncertainty
- Reality is messy - avoid false narrative closure
- Don't declare crises "resolved" when outcomes remain uncertain (e.g., a nomination doesn't resolve political tensions, it shifts them)
- Use hedging language: "appears to," "may signal," "remains to be seen"
- Avoid wrapping everything into neat stories - sometimes things are genuinely unclear
- Distinguish between facts (what happened) and interpretation (what it might mean)
- Macro is never black and white - be comfortable with ambiguity

## Time References in Weekly/Monthly Briefs
- When citing specific numbers in weekly briefs, include the day (e.g., "gold fell 8% on Friday", "S&P touched 7,000 on Tuesday")
- When citing specific numbers in monthly briefs, include timing (e.g., "gold peaked mid-month", "dollar weakness accelerated in the final week")
- Numbers without time context are less useful - readers need to know WHEN things happened

## Common Mistakes to Avoid
- Don't use **text** markdown in HTML - convert to <strong>
- Email logos must use HTML tables, not SVG/base64 (email client compatibility)
- Make sure days of the week correspond with the date
- It's "Daily Macro & Market Brief" (not just "Daily Macro Brief")
- When generating daily briefs from multiple shows, always use the latest data on a given theme. If an early show says the dollar strengthened but a later show says it weakened, report the final state (weakened), not the obsolete earlier state.
- Store summaries by video publication date, not processing date (e.g., The Close from Jan 29 goes in 2026-01-29/ folder even if processed on Jan 30)

## Lombard Odier Brand Colors
- Dark: #040505
- Blue accent: #5597cb
- Light blue: #aac3e3