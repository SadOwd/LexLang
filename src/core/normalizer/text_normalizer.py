"""TextNormalizer: normalisation de haut niveau."""
from ..base_processor import BaseProcessor
from .orthographic_normalizer import OrthographicNormalizer
from .unicode_normalizer import UnicodeNormalizer

class TextNormalizer(BaseProcessor):
    """Pipeline de normalisation du texte."""

    def __init__(self, config):
        super().__init__(config)
        self.orthonorm = OrthographicNormalizer(config)
        self.uninorm = UnicodeNormalizer(config)

    def normalize(self, tokens: list, dialect: str) -> list:
        # Applique normalisation orthographique puis Unicode
        tokens = self.orthonorm.normalize(tokens, dialect)
        tokens = self.uninorm.normalize(tokens, dialect)
        return tokens
