"""DialectDetector: détection automatique du dialecte."""
from ..base_processor import BaseProcessor

class DialectDetector(BaseProcessor):
    """Détermine le dialecte le plus probable."""

    def detect(self, text: str) -> str:
        # TODO: charger classifieur et prédire
        return 'anlo'

    def analyze(self, text: str, detailed: bool = False) -> dict:
        info = {'predicted': self.detect(text)}
        if detailed:
            info['scores'] = {'anlo': 0.7, 'inland': 0.3}
        return info
