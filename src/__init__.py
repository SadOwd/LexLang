"""LexLang: Advanced NLP toolkit for Ewe language processing."""

__version__ = "1.0.0"
__author__ = "LexLang Team"
__email__ = "contact@lexlang.org"

from .core import Pipeline
from .core.tokenizer import EweTokenizer
from .core.normalizer import TextNormalizer
from .core.pos_tagger import POSTagger
from .core.tonal_processor import TonalProcessor
from .core.dialect_handler import DialectDetector

__all__ = [
    "Pipeline",
    "EweTokenizer", 
    "TextNormalizer",
    "POSTagger",
    "TonalProcessor",
    "DialectDetector"
]
