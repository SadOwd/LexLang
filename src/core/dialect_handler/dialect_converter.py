import json
from pathlib import Path

class DialectConverter:
    def __init__(self, rules_dir="data/linguistic_resources/dialects"):
        self.rules = self._load_rules(rules_dir)
    
    def _load_rules(self, dir_path):
        rules = {}
        for path in Path(dir_path).glob('*.json'):
            dialect = path.stem
            with open(path, 'r', encoding='utf-8') as f:
                rules[dialect] = json.load(f)
        return rules
    
    def convert(self, text, source_dialect, target_dialect):
        """Convertit un texte d'un dialecte à un autre"""
        if source_dialect == target_dialect:
            return text
        
        # Conversion phonologique
        for rule in self.rules[target_dialect]['phonological_rules']:
            text = re.sub(rule['pattern'], rule['replacement'], text)
        
        # Conversion lexicale
        for source_word, target_word in self.rules[target_dialect]['lexical_mappings'].items():
            text = re.sub(r'\b' + source_word + r'\b', target_word, text)
        
        # Conversion tonale
        if 'tonal_rules' in self.rules[target_dialect]:
            for rule in self.rules[target_dialect]['tonal_rules']:
                text = re.sub(rule['pattern'], rule['replacement'], text)
        
        return text
    
    def create_mixed_dialect(self, text, primary_dialect, secondary_dialect, ratio=0.3):
        """Crée un texte en dialecte mixte"""
        words = text.split()
        mixed_text = []
        
        for word in words:
            if len(word) > 3 and random.random() < ratio:
                converted = self.convert(word, primary_dialect, secondary_dialect)
                mixed_text.append(converted)
            else:
                mixed_text.append(word)
        
        return ' '.join(mixed_text)