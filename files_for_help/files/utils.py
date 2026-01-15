"""
Utility functions for the Bloomberg summarizer
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logging(config):
    """Setup logging configuration"""
    
    log_config = config.get('logging', {})
    log_level = getattr(logging, log_config.get('level', 'INFO'))
    log_file = log_config.get('file', 'logs/bloomberg_summarizer.log')
    max_bytes = log_config.get('max_size_mb', 10) * 1024 * 1024
    backup_count = log_config.get('backup_count', 5)
    
    # Create logs directory
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Setup file handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    
    # Setup console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger


def ensure_directories(config):
    """Ensure all required directories exist"""
    
    output_dir = Path(config['output']['directory'])
    
    directories = [
        output_dir,
        output_dir / 'summaries',
        output_dir / 'transcripts',
        Path('temp'),
        Path('logs'),
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def format_duration(seconds):
    """Format duration in seconds to readable string"""
    if not seconds:
        return "Unknown"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"
