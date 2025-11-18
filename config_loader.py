#!/usr/bin/env python3
"""
Configuration Loader for SME Social Media Manager
Loads runtime configuration from YAML and environment variables
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from logger import get_logger

logger = get_logger(__name__)


class ConfigLoader:
    """
    Loads and manages configuration from YAML files

    Example:
        >>> config = ConfigLoader.load()
        >>> print(config['bot']['posting']['daily_post_count'])
        4
    """

    _config_cache: Optional[Dict[str, Any]] = None

    @staticmethod
    def load(config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Load configuration from YAML file

        Args:
            config_path: Path to config file (defaults to config.yaml)

        Returns:
            Dictionary with configuration values

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid
        """
        # Return cached config if available
        if ConfigLoader._config_cache is not None:
            logger.debug("Returning cached configuration")
            return ConfigLoader._config_cache

        # Determine config file path
        if config_path is None:
            config_path = Path(__file__).parent / 'config.yaml'
        else:
            config_path = Path(config_path)

        # Check if file exists
        if not config_path.exists():
            logger.warning(f"Config file not found at {config_path}, using defaults")
            return ConfigLoader._get_default_config()

        # Load YAML
        try:
            logger.info(f"Loading configuration from {config_path}")
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)

            # Validate configuration
            ConfigLoader._validate_config(config)

            # Cache the config
            ConfigLoader._config_cache = config

            logger.info("✅ Configuration loaded successfully")
            return config

        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML config: {e}")
            raise

        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise

    @staticmethod
    def _validate_config(config: Dict[str, Any]) -> None:
        """
        Validate configuration structure and values

        Args:
            config: Configuration dictionary

        Raises:
            ValueError: If configuration is invalid
        """
        required_sections = ['bot', 'viral_prediction', 'ai_providers', 'platforms']

        for section in required_sections:
            if section not in config:
                raise ValueError(f"Missing required configuration section: {section}")

        # Validate viral prediction weights sum to 1.0
        weights = config['viral_prediction']['weights']
        total_weight = sum(weights.values())
        if not (0.99 <= total_weight <= 1.01):  # Allow small floating point errors
            logger.warning(
                f"Viral prediction weights sum to {total_weight:.2f}, expected 1.0. "
                "Normalizing weights..."
            )
            # Normalize weights
            for key in weights:
                weights[key] = weights[key] / total_weight

        logger.debug("Configuration validation passed")

    @staticmethod
    def _get_default_config() -> Dict[str, Any]:
        """
        Get default configuration when YAML file is not available

        Returns:
            Dictionary with default configuration values
        """
        logger.info("Using default configuration")

        return {
            'bot': {
                'posting': {
                    'daily_post_count': 4,
                    'optimal_hours': [8, 12, 17, 20],
                    'max_retries': 3,
                    'character_limit': 280
                },
                'engagement': {
                    'mention_check_frequency': 3600,
                    'max_engagements_per_session': 3,
                    'reply_probability': 0.3,
                    'engagement_delay': 2
                },
                'rate_limits': {
                    'simulation_mode_on_limit': True,
                    'auto_detect_rate_limit': True
                }
            },
            'viral_prediction': {
                'min_acceptable_score': 70,
                'auto_optimize': True,
                'weights': {
                    'content': 0.30,
                    'engagement': 0.25,
                    'timing': 0.15,
                    'hashtags': 0.15,
                    'trends': 0.15
                }
            },
            'ai_providers': {
                'primary': 'openai',
                'fallbacks': ['anthropic', 'groq'],
                'generation': {
                    'max_tokens': 100,
                    'temperature': 0.7
                }
            },
            'platforms': {
                'twitter': {
                    'enabled': True,
                    'character_limit': 280
                },
                'linkedin': {
                    'enabled': True,
                    'character_limit': 3000,
                    'min_content_length': 300
                }
            },
            'logging': {
                'level': 'INFO',
                'console_output': True,
                'file_output': True
            }
        }

    @staticmethod
    def get(key_path: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-separated path

        Args:
            key_path: Dot-separated path (e.g., 'bot.posting.daily_post_count')
            default: Default value if key not found

        Returns:
            Configuration value or default

        Example:
            >>> ConfigLoader.get('bot.posting.daily_post_count')
            4
            >>> ConfigLoader.get('bot.missing.key', default=0)
            0
        """
        config = ConfigLoader.load()

        keys = key_path.split('.')
        value = config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                logger.debug(f"Config key not found: {key_path}, using default: {default}")
                return default

        return value

    @staticmethod
    def reload() -> Dict[str, Any]:
        """
        Reload configuration from disk (clears cache)

        Returns:
            Fresh configuration dictionary
        """
        logger.info("Reloading configuration...")
        ConfigLoader._config_cache = None
        return ConfigLoader.load()

    @staticmethod
    def get_viral_weights() -> Dict[str, float]:
        """
        Get viral prediction scoring weights

        Returns:
            Dictionary of scoring weights
        """
        return ConfigLoader.get('viral_prediction.weights', {
            'content': 0.30,
            'engagement': 0.25,
            'timing': 0.15,
            'hashtags': 0.15,
            'trends': 0.15
        })

    @staticmethod
    def get_posting_hours() -> list:
        """
        Get optimal posting hours

        Returns:
            List of optimal hours (UTC)
        """
        return ConfigLoader.get('bot.posting.optimal_hours', [8, 12, 17, 20])

    @staticmethod
    def get_min_viral_score() -> int:
        """
        Get minimum acceptable viral score

        Returns:
            Minimum score threshold
        """
        return ConfigLoader.get('viral_prediction.min_acceptable_score', 70)

    @staticmethod
    def is_feature_enabled(feature: str) -> bool:
        """
        Check if a feature is enabled

        Args:
            feature: Feature name

        Returns:
            True if enabled, False otherwise
        """
        return ConfigLoader.get(f'features.{feature}', False)


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("CONFIGURATION LOADER TEST")
    print("=" * 60)

    # Load config
    try:
        config = ConfigLoader.load()

        print("\n✅ Configuration loaded successfully\n")

        # Test get() method
        print("📝 Sample Configuration Values:")
        print(f"   Daily post count: {ConfigLoader.get('bot.posting.daily_post_count')}")
        print(f"   Optimal hours: {ConfigLoader.get_posting_hours()}")
        print(f"   Min viral score: {ConfigLoader.get_min_viral_score()}")
        print(f"   Viral weights: {ConfigLoader.get_viral_weights()}")

        # Test feature flags
        print(f"\n🎯 Feature Flags:")
        print(f"   Viral prediction: {ConfigLoader.is_feature_enabled('viral_prediction')}")
        print(f"   Multi-platform: {ConfigLoader.is_feature_enabled('multi_platform')}")
        print(f"   A/B testing: {ConfigLoader.is_feature_enabled('a_b_testing')}")

        # Test default values
        print(f"\n🔧 Default Value Test:")
        print(f"   Missing key: {ConfigLoader.get('missing.key', default='DEFAULT')}")

    except Exception as e:
        print(f"\n❌ Configuration loading failed: {e}")
