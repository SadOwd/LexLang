import re
from unicodedata import normalize
from .dialect_handler import EweDialectAdapter

class EweTokenizer:
    def __init__(self, dialect="standard"):
        self.dialect_adapter = EweDialectAdapter(dialect)
        self.tonal_marks = '\u0300-\u036F'  # Plage Unicode des diacritiques tonals
        self.word_pattern = re.compile(
            rf"[\w{self.tonal_marks}]+(?:['’][\w{self.tonal_marks}]+)*|[\d]+|[\s.,!?;:]+"
        )
        
        # Chargement des exceptions morphologiques
        with open('data/linguistic_resources/morphology/exceptions.json') as f:
            self.morph_exceptions = json.load(f)
    
    def _normalize_tones(self, text: str) -> str:
        """Normalise les représentations tonales"""
        return normalize('NFC', text)
    
    def _handle_compounds(self, token: str) -> list:
        """Segmente les mots composés spécifiques à l'éwé"""
        if token in self.morph_exceptions['compounds']:
            return self.morph_exceptions['compounds'][token]
        
        # Règles de segmentation pour les dérivés (ex: suffixe -lá pour agent)
        for suffix in ['lá', 'ví', 'gá', 'fe']:
            if token.endswith(suffix) and len(token) > len(suffix) + 1:
                return [token[:-len(suffix)], suffix]
        
        return [token]
    
    def tokenize(self, text: str) -> list[dict]:
        """Tokenisation principale avec traitement linguistique"""
        normalized_text = self._normalize_tones(text)
        dialect_text = self.dialect_adapter.adapt(normalized_text)
        
        tokens = []
        position = 0
        for match in self.word_pattern.finditer(dialect_text):
            raw_token = match.group(0)
            start, end = match.span()
            
            # Segmentation morphologique
            segments = self._handle_compounds(raw_token)
            
            for segment in segments:
                tokens.append({
                    'text': segment,
                    'original': raw_token,
                    'position': (position, position + len(segment)),
                    'dialect': self.dialect_adapter.dialect
                })
                position += len(segment) + 1
        
        return tokens

    def sentence_tokenize(self, text: str) -> list[str]:
        """Segmentation en phrases avec règles spécifiques à l'éwé"""
        # Séparateurs de phrase incluant les marqueurs de discours
        sentence_delimiters = r'(?<!\w\.\w.)(?<![A-ZẸẸỌ][a-zàèìòù]\.)(?<=\.|\?|!|…|›)\s'
        return re.split(sentence_delimiters, text)