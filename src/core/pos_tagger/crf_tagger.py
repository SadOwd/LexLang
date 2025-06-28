"""CRFTagger: étiquetage POS par CRF."""
from ..base_processor import BaseProcessor

class CRFTagger(BaseProcessor):
    """Utilise un modèle CRF pour POS tagging."""

    def tag(self, tokens: list, dialect: str) -> list:
        # TODO: charger crf model et extraire features
        return [(tok, 'VERB') for tok in tokens]
