from .tokenizer.ewe_tokenizer import EweTokenizer
from .linguistic_loader import LinguisticResourceLoader

class EweLinguisticProcessor:
    def __init__(self, dialect="standard"):
        self.dialect = dialect
        self.tokenizer = EweTokenizer(dialect)
        self.loader = LinguisticResourceLoader()
        self.resources = self._load_resources()
    
    def _load_resources(self) -> dict:
        return {
            'phonology': {
                'phonemes': self.loader.load_resource('phonemes'),
                'tones': self.loader.load_resource('tones')
            },
            'morphology': {
                'stems': self.loader.load_resource('stems'),
                'affixes': {
                    'prefixes': self.loader.load_resource('prefixes'),
                    'suffixes': self.loader.load_resource('suffixes')
                }
            },
            'dialect': self.loader.get_dialect_variants(self.dialect)
        }
    
    def analyze_text(self, text: str) -> dict:
        tokens = self.tokenizer.tokenize(text)
        analysis = []
        
        for token in tokens:
            token_analysis = {'token': token['text'], 'analysis': []}
            
            # Analyse morphologique
            for affix_type in ['prefixes', 'suffixes']:
                for affix in self.resources['morphology']['affixes'][affix_type]:
                    if token['text'].endswith(affix['suffix']):
                        stem = token['text'][:-len(affix['suffix'])]
                        token_analysis['analysis'].append({
                            'type': 'derivation',
                            'stem': stem,
                            'affix': affix['suffix'],
                            'gloss': affix['gloss']
                        })
            
            analysis.append(token_analysis)
        
        return {
            'dialect': self.dialect,
            'tokens': tokens,
            'linguistic_analysis': analysis,
            'phonology': self.resources['phonology']
        }
    
    def generate_word(self, stem: str, affix_type: str) -> str:
        """Génère un mot dérivé selon les règles morphologiques"""
        affixes = self.resources['morphology']['affixes'][affix_type]
        valid_affixes = [a for a in affixes if stem.endswith(tuple(a['compatibility']))]
        
        if not valid_affixes:
            return stem
        
        affix = random.choice(valid_affixes)
        return stem + affix['suffix']