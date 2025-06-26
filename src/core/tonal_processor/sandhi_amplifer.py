# src/core/tonal_processor/sandhi_applier.py
class EweTonalProcessor:
    def __init__(self, dialect="standard"):
        self.rules = self.load_rules(f"configs/tonal_rules_{dialect}.yaml")
        self.exceptions = self.load_exceptions("data/linguistic_resources/tonal/exceptions.json")
    
    def apply(self, token: str) -> str:
        """Applique les règles de sandhi contextuelles"""
        if token in self.exceptions:
            return self.exceptions[token]
        
        # Application des règles spécifiques au dialecte
        for pattern, replacement in self.rules.items():
            if re.match(pattern, token):
                return re.sub(pattern, replacement, token)
        return token

# src/core/morphology/compound_analyzer.py
class EweMorphologicalAnalyzer:
    DERIVATIONAL_SUFFIXES = {
        '-fe': ('location', 'n'),
        '-lá': ('agent', 'n'),
        '-ví': ('diminutive', 'n'),
        '-gá': ('augmentative', 'n')
    }
    
    def analyze(self, token: str) -> dict:
        """Analyse morphémique des mots composés"""
        for suffix, (gloss, pos) in self.DERIVATIONAL_SUFFIXES.items():
            if token.endswith(suffix):
                return {
                    'stem': token[:-len(suffix)],
                    'suffix': suffix,
                    'gloss': gloss,
                    'pos': pos,
                    'type': 'derivational'
                }
        
        # Détection des composés sémantiques (ex: yamevú = air + dans + véhicule)
        if len(token) > 5:
            for i in range(3, len(token)-2):
                part1, part2 = token[:i], token[i:]
                if self.is_valid_morpheme(part1) and self.is_valid_morpheme(part2):
                    return {
                        'components': [part1, part2],
                        'gloss': f"{self.get_gloss(part1)} + {self.get_gloss(part2)}",
                        'type': 'compound'
                    }
        return {'type': 'root'}