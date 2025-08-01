import os
import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

class SettingsManager:
    def __init__(self):
        self.settings_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'settings.json')
        self.settings = self._load_settings()
        self._auto_set_default_roots()
        self._check_environment_variables()

    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading settings: {e}")
        return self._get_default_settings()

    def _auto_set_default_roots(self):
        """Auto set default root paths if only one folder is present and default is empty."""
        folder_paths = self.settings.get('folder_paths', {})
        updated = False
        # loras
        loras = folder_paths.get('loras', [])
        if isinstance(loras, list) and len(loras) == 1 and not self.settings.get('default_lora_root'):
            self.settings['default_lora_root'] = loras[0]
            updated = True
        # checkpoints
        checkpoints = folder_paths.get('checkpoints', [])
        if isinstance(checkpoints, list) and len(checkpoints) == 1 and not self.settings.get('default_checkpoint_root'):
            self.settings['default_checkpoint_root'] = checkpoints[0]
            updated = True
        # embeddings
        embeddings = folder_paths.get('embeddings', [])
        if isinstance(embeddings, list) and len(embeddings) == 1 and not self.settings.get('default_embedding_root'):
            self.settings['default_embedding_root'] = embeddings[0]
            updated = True
        if updated:
            self._save_settings()

    def _check_environment_variables(self) -> None:
        """Check for environment variables and update settings if needed"""
        env_api_key = os.environ.get('CIVITAI_API_KEY')
        if env_api_key:  # Check if the environment variable exists and is not empty
            logger.info("Found CIVITAI_API_KEY environment variable")
            # Always use the environment variable if it exists
            self.settings['civitai_api_key'] = env_api_key
            self._save_settings()

    def refresh_environment_variables(self) -> None:
        """Refresh settings from environment variables"""
        self._check_environment_variables()

    def _get_default_settings(self) -> Dict[str, Any]:
        """Return default settings"""
        return {
            "civitai_api_key": "",
            "show_only_sfw": False
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Get setting value"""
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set setting value and save"""
        self.settings[key] = value
        self._save_settings()

    def _save_settings(self) -> None:
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving settings: {e}")

settings = SettingsManager()
