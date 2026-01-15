# Your Bloomberg Shows Schedule (CET - Switzerland)

## Daily Email Timeline

```
07:45 CET  📊 The China Show
           └─ Shanghai markets recap

09:45 CET  🌍 Daybreak Europe
           └─ European market open

14:00 CET  📺 Bloomberg Surveillance
           └─ US morning show (Jon, Lisa & Annmarie)

14:30 CET  📰 Bloomberg Brief
           └─ Daily market briefing

22:45 CET  🔔 The Close
           └─ US market close wrap
```

## What You Get

Each email contains a **concise, scannable summary**:

✓ **Executive Summary** - Core thesis in 1-2 sentences
✓ **Key Macro Data** - Important numbers in bold
✓ **Markets & Positioning** - Asset class moves
✓ **Central Bank Updates** - Policy changes
✓ **Risks & Catalysts** - What to watch
✓ **Action Items** - Specific trade ideas

**Format:** Short bullets, key info in **bold**, easy to skim in 30 seconds

## Monthly Costs

- **GitHub Actions**: FREE (well within 2,000 free minutes)
- **YouTube API**: FREE (10,000 quota units daily, you use ~25)
- **Claude API**: ~$4.50-$13.50/month (5 shows × ~$0.05-$0.15 per video)

**Total: ~$5-14/month** for automated daily intelligence

## Quick Commands

```bash
# Test a single show locally
python3 process_show.py bloomberg_brief

# View all shows and schedules
python3 process_show.py list

# See schedule with cron entries
python3 show_schedule.py

# Test all shows (quick check)
./test_all_shows.sh
```

## GitHub Actions Setup

1. Push code to GitHub
2. Add secrets (API keys, email credentials)
3. Enable workflows in Actions tab
4. Test manually first
5. Enjoy automated daily summaries!

See [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) for detailed setup instructions.

## Files Created

- ✅ 5 workflow files in `.github/workflows/`
- ✅ `shows_config.yaml` - Show configuration
- ✅ `process_show.py` - Process individual shows
- ✅ `show_schedule.py` - View schedules
- ✅ `find_playlist_ids.py` - Find new shows
- ✅ Complete documentation

Ready to set up! 🚀
