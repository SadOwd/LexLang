"""ToneMarker: insertion de marques tonales."""
from ..base_processor import BaseProcessor

class ToneMarker(BaseProcessor):
    """Marque les tons dans le texte."""

    def mark(self, tokens: list, dialect: str) -> list:
        # TODO: appliquer règles de tonalisation
        return tokens
