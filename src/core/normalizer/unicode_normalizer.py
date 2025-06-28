"""UnicodeNormalizer: nettoyage Unicode."""
from ..base_processor import BaseProcessor
import unicodedata

class UnicodeNormalizer(BaseProcessor):
    """Normalisation Unicode NFKC."""

    def normalize(self, tokens: list, dialect: str) -> list:
        return [unicodedata.normalize('NFKC', tok) for tok in tokens]
