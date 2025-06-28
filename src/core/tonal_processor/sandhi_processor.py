"""SandhiProcessor: gestion des changements tonals sandhi."""
from ..base_processor import BaseProcessor

class SandhiProcessor(BaseProcessor):
    """Applique les règles de sandhi tonal."""

    def process(self, tokens: list, dialect: str) -> list:
        # TODO: implémenter règles sandhi
        return tokens
