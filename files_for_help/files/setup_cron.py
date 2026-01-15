#!/usr/bin/env python3
"""
Setup cron job for daily Bloomberg summarizer
"""

import os
import sys
from pathlib import Path
from crontab import CronTab
import yaml


def setup_cron():
    """Setup cron job for daily execution"""
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    schedule_config = config.get('schedule', {})
    run_time = schedule_config.get('time', '07:00')
    
    # Parse time
    hour, minute = run_time.split(':')
    
    # Get current user
    user = os.getenv('USER', 'root')
    
    # Get absolute paths
    project_dir = Path(__file__).parent.absolute()
    python_path = sys.executable
    main_script = project_dir / 'main.py'
    log_file = project_dir / 'logs' / 'cron.log'
    
    # Create cron job
    cron = CronTab(user=user)
    
    # Remove existing jobs with the same comment
    cron.remove_all(comment='bloomberg-markets-summarizer')
    
    # Create new job
    job = cron.new(
        command=f'cd {project_dir} && {python_path} {main_script} >> {log_file} 2>&1',
        comment='bloomberg-markets-summarizer'
    )
    
    # Set schedule
    job.hour.on(int(hour))
    job.minute.on(int(minute))
    
    # Write crontab
    cron.write()
    
    print("="*60)
    print("Cron job setup successful!")
    print("="*60)
    print(f"Schedule: Daily at {run_time}")
    print(f"Command: {job.command}")
    print(f"User: {user}")
    print("\nTo view your crontab:")
    print("  crontab -l")
    print("\nTo manually edit your crontab:")
    print("  crontab -e")
    print("\nTo check logs:")
    print(f"  tail -f {log_file}")
    print("="*60)


if __name__ == "__main__":
    try:
        setup_cron()
    except Exception as e:
        print(f"Error setting up cron: {str(e)}", file=sys.stderr)
        print("\nManual setup instructions:")
        print("1. Edit your crontab: crontab -e")
        print("2. Add the following line:")
        print(f"   0 7 * * * cd {Path(__file__).parent.absolute()} && python3 main.py >> logs/cron.log 2>&1")
        sys.exit(1)
