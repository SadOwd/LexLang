"""TonalNormalizer: normalisation spécifique aux tons."""
from ..base_processor import BaseProcessor

class TonalNormalizer(BaseProcessor):
    """Nettoie et unifie les annotations tonales."""

    def normalize(self, tokens: list, dialect: str) -> list:
        # Exemple: retirer diacritiques redondants
        normalized = []
        for tok in tokens:
            # TODO: utiliser self.config.models.tone_rules
            normalized.append(tok)
        return normalized
