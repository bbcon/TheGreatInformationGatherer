#!/usr/bin/env python3
"""
Test script to verify setup and configuration
"""

import os
import sys
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    print("Checking dependencies...")
    
    required = [
        'yt_dlp',
        'whisper',
        'anthropic',
        'yaml',
        'dotenv',
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    return True


def check_api_keys():
    """Check if API keys are configured"""
    print("\nChecking API keys...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    keys = {
        'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    }
    
    configured = False
    for key, value in keys.items():
        if value and value != f'your_{key.lower()}_here':
            print(f"  ✓ {key}")
            configured = True
        else:
            print(f"  ✗ {key} - NOT CONFIGURED")
    
    if not configured:
        print("\nNo API keys configured!")
        print("Edit .env file with your API keys")
        return False
    
    return True


def check_ffmpeg():
    """Check if ffmpeg is installed"""
    print("\nChecking ffmpeg...")
    
    import subprocess
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("  ✓ ffmpeg installed")
            return True
    except Exception:
        pass
    
    print("  ✗ ffmpeg - NOT INSTALLED")
    print("Install with: sudo apt-get install ffmpeg")
    return False


def check_directories():
    """Check if required directories exist"""
    print("\nChecking directories...")
    
    dirs = [
        'src',
        'logs',
        'output',
        'output/summaries',
        'output/transcripts',
    ]
    
    all_exist = True
    for dir_name in dirs:
        path = Path(dir_name)
        if path.exists():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ - MISSING")
            all_exist = False
    
    return all_exist


def main():
    """Run all checks"""
    print("="*60)
    print("Bloomberg Markets Summarizer - Setup Verification")
    print("="*60)
    
    checks = [
        ("Dependencies", check_dependencies),
        ("API Keys", check_api_keys),
        ("FFmpeg", check_ffmpeg),
        ("Directories", check_directories),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\nError checking {name}: {str(e)}")
            results.append((name, False))
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    all_passed = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name:20s} {status}")
        if not result:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n✓ All checks passed! Ready to run.")
        print("\nNext steps:")
        print("  1. Configure .env with your API keys")
        print("  2. Run: python main.py")
        print("  3. Setup cron: python setup_cron.py")
        return 0
    else:
        print("\n✗ Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
