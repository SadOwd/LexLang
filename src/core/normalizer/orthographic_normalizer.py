"""OrthographicNormalizer: règles orthographiques."""
from ..base_processor import BaseProcessor

class OrthographicNormalizer(BaseProcessor):
    """Uniformise l'orthographe selon les standards."""

    def normalize(self, tokens: list, dialect: str) -> list:
        # Exemple trivial: tout en minuscules
        return [tok.lower() for tok in tokens]
