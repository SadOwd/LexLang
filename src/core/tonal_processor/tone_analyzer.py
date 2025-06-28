"""ToneAnalyzer: détection et classification de tons."""
from ..base_processor import BaseProcessor

class ToneAnalyzer(BaseProcessor):
    """Analyse les tonalités des tokens."""

    def analyze(self, tokens: list, dialect: str) -> dict:
        # Ex: compter tons aigus/graves
        return {'high_tones': len([t for t in tokens if '́' in t]),
                'low_tones': len([t for t in tokens if '̀' in t])}
