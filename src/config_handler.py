"""
Configuration handler for The Great Information Gatherer.
"""
import os
import yaml
from typing import Dict, Any
from pathlib import Path


class ConfigHandler:
    """Handles loading and parsing configuration."""

    DEFAULT_CONFIG = {
        'summary': {
            'length': 'standard',
            'sections': {
                'executive_summary': True,
                'macro_indicators': True,
                'market_outlook': True,
                'central_bank_policy': True,
                'risks_catalysts': True,
                'technical_levels': False,
                'actionable_takeaways': True,
            },
            'style': {
                'tone': 'analytical',
                'angle': 'macro_trading',
                'include_data_points': True,
                'emphasize_actionable': True,
            }
        },
        'output': {
            'save_json': True,
            'save_markdown': True,
            'folder_structure': 'by_date',
            'date_format': 'YYYY-MM-DD',
        },
        'email': {
            'include_sections': [
                'executive_summary',
                'macro_indicators',
                'market_outlook',
                'actionable_takeaways'
            ],
            'format': 'html',
            'include_file_link': True,
        },
        'custom_instructions': ''
    }

    def __init__(self, config_path: str = 'config.yaml'):
        """
        Initialize config handler.

        Args:
            config_path: Path to config YAML file
        """
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file or use defaults."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    user_config = yaml.safe_load(f) or {}

                # Merge with defaults (user config takes precedence)
                config = self._deep_merge(self.DEFAULT_CONFIG.copy(), user_config)
                print(f"Loaded configuration from {self.config_path}")
                return config
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
                print("Using default configuration")
                return self.DEFAULT_CONFIG.copy()
        else:
            print(f"Config file not found at {self.config_path}, using defaults")
            return self.DEFAULT_CONFIG.copy()

    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
        """Deep merge two dictionaries."""
        result = base.copy()
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def get(self, *keys, default=None):
        """
        Get nested config value.

        Args:
            *keys: Keys to traverse (e.g., 'summary', 'length')
            default: Default value if key not found

        Returns:
            Config value or default
        """
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def get_prompt_sections(self) -> Dict[str, bool]:
        """Get which sections should be included in the prompt."""
        return self.get('summary', 'sections', default={})

    def get_summary_length(self) -> str:
        """Get desired summary length."""
        return self.get('summary', 'length', default='standard')

    def get_custom_instructions(self) -> str:
        """Get custom prompt instructions."""
        return self.get('custom_instructions', default='')

    def should_save_markdown(self) -> bool:
        """Check if markdown output should be saved."""
        return self.get('output', 'save_markdown', default=True)

    def should_save_json(self) -> bool:
        """Check if JSON output should be saved."""
        return self.get('output', 'save_json', default=True)

    def get_folder_structure(self) -> str:
        """Get folder structure preference."""
        return self.get('output', 'folder_structure', default='by_date')

    def get_email_sections(self) -> list:
        """Get sections to include in email."""
        return self.get('email', 'include_sections', default=[])
