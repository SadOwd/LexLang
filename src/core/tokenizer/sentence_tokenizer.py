"""SentenceTokenizer: segmentation en phrases."""
from .base_tokenizer import BaseTokenizer
import re

class SentenceTokenizer(BaseTokenizer):
    """Découpe le texte en phrases."""

    def tokenize(self, text: str, dialect: str) -> list:
        # Sépare sur points, points d'interrogation/exclamation
        sentences = re.split(r'(?<=[\.\?\!])\s+', text.strip())
        return [s for s in sentences if s]
