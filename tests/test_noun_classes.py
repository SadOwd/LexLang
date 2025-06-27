import pytest
from src.core.morphology import EweNounAnalyzer

class TestEweNounClasses:
    @pytest.fixture
    def analyzer(self):
        return EweNounAnalyzer()
    
    @pytest.mark.parametrize("noun,expected_class", [
        ("atí", "a-"),
        ("fia", "Ø"),
        ("nyɔnu", "Ø"),
        ("dzo", "Ø"),
        ("agble", "a-")
    ])
    def test_noun_class_detection(self, analyzer, noun, expected_class):
        """Teste l'identification des classes nominales"""
        assert analyzer.detect_noun_class(noun) == expected_class
    
    def test_plural_formation(self, analyzer):
        """Teste la formation du pluriel"""
        test_cases = [
            ("atí", "atíwo"),      # Classe a- + -wo
            ("ade", "adewo"),       # Classe a- + -wo
            ("fia", "fiawo"),       # Classe Ø + -wo
            ("nyɔnu", "nyɔnuwo"),   # Classe Ø + -wo
            ("dzo", "dzowo")        # Classe Ø + -wo
        ]
        
        for singular, expected_plural in test_cases:
            assert analyzer.form_plural(singular) == expected_plural
    
    def test_class_sensitive_agreement(self, analyzer):
        """Teste l'accord de classe nominale"""
        test_cases = [
            ("atí", "gá", "atí gá"),       # a- + adjectif
            ("fia", "gá", "fia gá"),        # Ø + adjectif
            ("nyɔnu", "nyuie", "nyɔnu nyuie") # Ø + adjectif
        ]
        
        for noun, adjective, expected in test_cases:
            assert analyzer.apply_adjective_agreement(noun, adjective) == expected