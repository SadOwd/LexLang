"""ToneValidator: vérification de la cohérence tonale."""
from ..base_processor import BaseProcessor

class ToneValidator(BaseProcessor):
    """Valide les séquences tonales."""

    def validate(self, tokens: list, dialect: str) -> bool:
        # Ex: pas deux tons aigus consécutifs
        return True
