# src/core/dialect_handler/dynamic_mapper.py
class EweDialectAdapter:
    def __init__(self, dialect="standard"):
        self.config = self.load_config(f"configs/dialect_{dialect}.yaml")
        self.phonetic_map = self.config.get('phonetic_rules', {})
        self.lexical_map = self.config.get('lexical_variants', {})
    
    def adapt(self, token: str) -> str:
        """Adapte un token selon les règles dialectales"""
        # 1. Adaptation lexicale
        if token in self.lexical_map:
            return self.lexical_map[token]
        
        # 2. Adaptation phonétique
        for source, target in self.phonetic_map.items():
            token = token.replace(source, target)
        
        return token

# src/core/dialect_handler/dialect_router.py
class DialectRouter:
    DIALECT_REGIONS = {
        'anlo': ['keta', 'ave'],
        'inland': ['ho', 'kpalime'],
        'badou': ['badou', 'natchigou']
    }
    
    def detect(self, text: str) -> str:
        """Détecte le dialecte basé sur des marqueurs régionaux"""
        for dialect, markers in self.DIALECT_REGIONS.items():
            if any(marker in text.lower() for marker in markers):
                return dialect
        return 'standard'