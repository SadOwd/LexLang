"""Configuration management for LexLang."""

import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class ModelConfig:
    """Model configuration."""
    pos_model_path: str = "models/pos/pos_model_v1.2.pkl"
    embedding_model_path: str = "models/embeddings/ewe_word2vec_v2.1.bin"
    dialect_model_path: str = "models/classifiers/dialect_classifier_v3.0.pkl"
    tone_model_path: str = "models/classifiers/tone_classifier_v2.5.pkl"
    transformer_model_path: str = "models/pretrained/transformer_base_v1.0.pt"


@dataclass
class DataConfig:
    """Data configuration."""
    corpus_path: str = "data/corpora/"
    lexicon_path: str = "data/lexicons/"
    linguistic_resources_path: str = "data/linguistic_resources/"
    cache_dir: str = ".cache/"


@dataclass
class ProcessingConfig:
    """Processing configuration."""
    max_sequence_length: int = 512
    batch_size: int = 32
    num_workers: int = 4
    enable_caching: bool = True
    enable_gpu: bool = True
    default_dialect: str = "auto"


@dataclass
class APIConfig:
    """API configuration."""
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    secret_key: str = "lexlang-secret-key"
    cors_origins: list = field(default_factory=lambda: ["*"])
    rate_limit: int = 100


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = None
    max_bytes: int = 10485760  # 10MB
    backup_count: int = 5


@dataclass
class LexLangConfig:
    """Main configuration class."""
    models: ModelConfig = field(default_factory=ModelConfig)
    data: DataConfig = field(default_factory=DataConfig)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    api: APIConfig = field(default_factory=APIConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)


def load_config(config_path: str = "configs/default.yaml") -> LexLangConfig:
    """Load configuration from YAML file."""
    try:
        config_file = Path(config_path)
        
        if not config_file.exists():
            logger.warning(f"Config file {config_path} not found, using defaults")
            return LexLangConfig()
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        
        # Override with environment variables
        config_data = _override_with_env(config_data)
        
        # Create configuration object
        config = LexLangConfig()
        
        if 'models' in config_data:
            config.models = ModelConfig(**config_data['models'])
        if 'data' in config_data:
            config.data = DataConfig(**config_data['data'])
        if 'processing' in config_data:
            config.processing = ProcessingConfig(**config_data['processing'])
        if 'api' in config_data:
            config.api = APIConfig(**config_data['api'])
        if 'logging' in config_data:
            config.logging = LoggingConfig(**config_data['logging'])
        
        logger.info(f"Configuration loaded from {config_path}")
        return config
        
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise


def _override_with_env(config_data: Dict[str, Any]) -> Dict[str, Any]:
    """Override configuration with environment variables."""
    env_mappings = {
        'DATABASE_URL': ['database', 'url'],
        'API_HOST': ['api', 'host'],
        'API_PORT': ['api', 'port'],
        'SECRET_KEY': ['api', 'secret_key'],
        'DEBUG': ['api', 'debug'],
        'LOG_LEVEL': ['logging', 'level'],
        'MODEL_PATH': ['models', 'base_path'],
        'DATA_PATH': ['data', 'base_path'],
        'MAX_WORKERS': ['processing', 'num_workers'],
        'BATCH_SIZE': ['processing', 'batch_size']
    }
    
    for env_var, config_path in env_mappings.items():
        value = os.getenv(env_var)
        if value is not None:
            # Navigate to nested config
            current = config_data
            for key in config_path[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            # Convert value to appropriate type
            if env_var in ['API_PORT', 'MAX_WORKERS', 'BATCH_SIZE']:
                value = int(value)
            elif env_var in ['DEBUG']:
                value = value.lower() in ('true', '1', 'yes', 'on')
            
            current[config_path[-1]] = value
    
    return config_data


def save_config(config: LexLangConfig, config_path: str):
    """Save configuration to YAML file."""
    try:
        config_dict = {
            'models': config.models.__dict__,
            'data': config.data.__dict__,
            'processing': config.processing.__dict__,
            'api': config.api.__dict__,
            'logging': config.logging.__dict__
        }
        
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_dict, f, default_flow_style=False, 
                     allow_unicode=True, indent=2)
        
        logger.info(f"Configuration saved to {config_path}")
        
    except Exception as e:
        logger.error(f"Error saving configuration: {e}")
        raise
