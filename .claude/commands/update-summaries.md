Catch up all missing daily, weekly, and monthly summaries for the project at /Users/brendanberthold/Dropbox/My Computer/GitHub/TheGreatInformationGatherer.

Follow these steps exactly:

## Step 1: Find missing daily briefs

Run this to see what show summary folders exist across all five shows:
```
ls summaries/bloomberg_brief/ summaries/bloomberg_surveillance/ summaries/daybreak_europe/ summaries/the_china_show/ summaries/the_close/
```

Then list existing daily briefs:
```
ls summaries/_daily_briefs/
```

A daily brief can be generated for date YYYY-MM-DD if at least one show has a summary folder for that date. Cross-reference the two lists and identify all dates that have show summaries but no corresponding `YYYY-MM-DD_daily_brief.md`. Exclude today's date and future dates. Only include weekdays (Mon-Fri).

For each missing daily brief date (oldest first), run:
```
python3 generate_daily_brief.py --date YYYY-MM-DD
```

## Step 2: Find missing weekly briefs

List existing weekly briefs:
```
ls summaries/_weekly_briefs/
```

For each daily brief that exists, compute its ISO week (YYYY-WNN format). Collect the set of all ISO weeks represented. For each ISO week that has at least one daily brief but no corresponding weekly brief file, and where the week has fully ended (i.e. the Sunday of that week is before today), generate the weekly brief (oldest first):
```
python3 generate_weekly_brief.py --week YYYY-WNN
```

## Step 3: Find missing monthly briefs

List existing monthly briefs:
```
ls summaries/_monthly_briefs/
```

For each weekly brief that exists, determine which month it belongs to (use the Monday of that ISO week to assign it to a month). Collect the set of all months represented. For each month that has at least one weekly brief but no `YYYY-MM_monthly_brief.md`, and where the month has fully ended (i.e. it is not the current month), generate the monthly brief (oldest first):
```
python3 generate_monthly_brief.py --month YYYY-MM
```

## Step 4: Report

After all generation is done, print a summary of what was generated (or "already up to date" if nothing was missing).

Important notes:
- Run all commands from the project root directory: /Users/brendanberthold/Dropbox/My Computer/GitHub/TheGreatInformationGatherer
- Use the virtual environment if needed: source .venv/bin/activate
- If a generation command fails, report the error and continue with the next item
- Do not regenerate briefs that already exist (no --force flag)
