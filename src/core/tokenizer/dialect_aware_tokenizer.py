"""DialectAwareTokenizer: détection de tokens adaptée au dialecte."""
from .base_tokenizer import BaseTokenizer
import re

class DialectAwareTokenizer(BaseTokenizer):
    """Word tokenizer tenant compte des particularités dialectales."""

    def tokenize(self, text: str, dialect: str) -> list:
        # Exemple simple: segmentation par espaces et ponctuation
        tokens = re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE)
        # TODO: appliquer règles dialectales spécifiques via self.config
        return tokens
