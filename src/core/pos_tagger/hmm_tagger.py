"""HMMTagger: étiquetage POS par modèle HMM."""
from ..base_processor import BaseProcessor

class HMMTagger(BaseProcessor):
    """Implémentation basique d'un HMM POS tagger."""

    def tag(self, tokens: list, dialect: str) -> list:
        # TODO: charger modèle HMM via self.config
        return [(tok, 'NOUN') for tok in tokens]
