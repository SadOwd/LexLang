import json
from pathlib import Path

class LinguisticResourceLoader:
    RESOURCE_PATHS = {
        'phonemes': 'phonetics/phonemes.json',
        'tones': 'tonal/tones.json',
        'allophonic_rules': 'phonetics/allophonic_rules.json',
        'stems': 'morphology/stems.json',
        'prefixes': 'morphology/prefixes.json',
        'suffixes': 'morphology/suffixes.json',
        'dialects': {
            'anlo': 'dialects/anlo.json',
            'inland': 'dialects/inland.json'
        }
    }
    
    def __init__(self, base_path='data/linguistic_resources/'):
        self.base_path = Path(base_path)
        self.cache = {}
    
    def load_resource(self, resource_name: str, dialect=None):
        if resource_name in self.cache:
            return self.cache[resource_name]
        
        if resource_name == 'dialects' and dialect:
            path_key = dialect
        else:
            path_key = resource_name
        
        rel_path = self.RESOURCE_PATHS.get(path_key)
        if not rel_path:
            raise ValueError(f"Resource {resource_name} not defined")
        
        full_path = self.base_path / rel_path
        if not full_path.exists():
            raise FileNotFoundError(f"Resource file not found: {full_path}")
        
        with open(full_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.cache[resource_name] = data
            return data
    
    def get_phoneme(self, symbol: str) -> dict:
        phonemes = self.load_resource('phonemes')
        return next((p for p in phonemes if p['symbol'] == symbol), None)
    
    def get_morph_rules(self, category: str) -> list:
        return self.load_resource(category)
    
    def get_dialect_variants(self, dialect: str) -> dict:
        return self.load_resource('dialects', dialect)