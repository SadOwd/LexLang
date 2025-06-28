"""WordTokenizer: découpe de phrases en mots."""
from .base_tokenizer import BaseTokenizer
import re

class WordTokenizer(BaseTokenizer):
    """Tokenisation simple des mots d'une phrase."""

    def tokenize(self, sentence: str, dialect: str) -> list:
        # Sépare sur les espaces et enlève la ponctuation isolée
        tokens = re.findall(r"\w+|[^\w\s]", sentence, flags=re.UNICODE)
        return tokens
