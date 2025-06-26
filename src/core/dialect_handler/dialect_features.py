import json
from collections import defaultdict

class DialectFeatures:
    def __init__(self, corpus_dir="data/corpora/raw"):
        self.corpus_dir = corpus_dir
        self.features = defaultdict(lambda: defaultdict(list))
    
    def extract_from_corpus(self, dialect_label):
        """Extrait les caractéristiques d'un corpus dialectal"""
        path = Path(self.corpus_dir) / f"{dialect_label}_corpus.txt"
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Extraction des caractéristiques phonologiques
        self._extract_phonological_features(text, dialect_label)
        
        # Extraction des caractéristiques lexicales
        self._extract_lexical_features(text, dialect_label)
        
        return self.features[dialect_label]
    
    def _extract_phonological_features(self, text, dialect):
        """Identifie les motifs phonologiques récurrents"""
        # Analyse des clusters consonantiques
        consonant_clusters = re.findall(r'[kpbg][wlr]', text)
        self.features[dialect]['consonant_clusters'] = list(set(consonant_clusters))
        
        # Analyse des schémas vocaliques
        vowel_patterns = re.findall(r'[aeiou]{2,}', text)
        self.features[dialect]['vowel_patterns'] = list(set(vowel_patterns))
    
    def _extract_lexical_features(self, text, dialect):
        """Identifie les mots spécifiques au dialecte"""
        words = re.findall(r'\w+', text.lower())
        word_freq = Counter(words)
        
        # Sélection des mots significativement fréquents
        total_words = len(words)
        lexical_signatures = [
            word for word, count in word_freq.items() 
            if count/total_words > 0.001 and len(word) > 3
        ]
        
        self.features[dialect]['lexical_signatures'] = lexical_signatures
    
    def save_features(self, output_path):
        """Sauvegarde les caractéristiques extraites"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.features, f, ensure_ascii=False, indent=2)