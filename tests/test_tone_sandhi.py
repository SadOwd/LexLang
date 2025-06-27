import pytest
from src.core.tonal_processor import TonalSandhiRules

class TestTonalSandhi:
    @pytest.fixture
    def processor(self):
        return TonalSandhiRules()
    
    @pytest.mark.parametrize("input_seq,expected", [
        (["H", "L"], ["M", "L"]),      # H + L > M + L (Anlo)
        (["L", "H"], ["L", "H"]),      # L + H inchangé
        (["H", "H"], ["H", "H"]),      # H + H inchangé
        (["L", "L"], ["L", "L"]),      # L + L inchangé
        (["H", "L", "H"], ["M", "L", "H"]), # Chaîne complexe
        (["M", "L"], ["M", "L"])       # M + L inchangé
    ])
    def test_sandhi_application(self, processor, input_seq, expected):
        """Teste les règles de sandhi tonal"""
        assert processor.apply_sandhi(input_seq) == expected
    
    def test_dialect_variation(self, processor):
        """Teste les variations dialectales des règles sandhi"""
        # Règles pour le dialecte Inland
        processor.set_dialect("inland")
        assert processor.apply_sandhi(["H", "L"]) == ["L", "L"]
        
        # Règles pour le dialecte Gbekplo
        processor.set_dialect("gbekplo")
        assert processor.apply_sandhi(["H", "L"]) == ["H", "M"]
    
    def test_real_word_examples(self, processor):
        """Teste avec des exemples lexicaux réels"""
        test_cases = [
            ("tó", "là", "tò là"),    # H + L > M + L
            ("dó", "gà", "dó gà"),     # H + L > M + L (non visible orthographiquement)
            ("vă", "!", "và !")        # Impératif
        ]
        
        for word1, word2, expected in test_cases:
            result = processor.apply_to_phrase(f"{word1} {word2}")
            assert result == expected