import re
from collections import Counter
from pathlib import Path
import json

class DialectDetector:
    def __init__(self, features_path="data/linguistic_resources/dialects/dialect_features.json"):
        self.features = self._load_features(features_path)
        self.dialect_weights = {
            'anlo': 1.0,
            'inland': 1.0,
            'gbekplo': 0.8
        }
    
    def _load_features(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def detect(self, text):
        """Détermine le dialecte dominant dans un texte"""
        scores = {dialect: 0 for dialect in self.features}
        
        # Analyse lexicale
        words = re.findall(r'\w+', text.lower())
        word_count = Counter(words)
        
        for dialect, features in self.features.items():
            # Correspondance lexicale
            for word in features['lexical_signatures']:
                if word in word_count:
                    scores[dialect] += word_count[word] * self.dialect_weights[dialect]
            
            # Correspondance phonologique
            for pattern in features['phonological_patterns']:
                matches = len(re.findall(pattern, text))
                scores[dialect] += matches * self.dialect_weights[dialect] * 0.5
        
        # Retourne le dialecte avec le score le plus élevé
        return max(scores, key=scores.get)
    
    def analyze_mixed_text(self, text):
        """Identifie les sections dialectales dans un texte mixte"""
        sentences = re.split(r'[.!?]', text)
        results = []
        
        for sentence in sentences:
            if not sentence.strip():
                continue
            dialect = self.detect(sentence)
            results.append({
                'text': sentence,
                'dialect': dialect,
                'confidence': self._calculate_confidence(sentence, dialect)
            })
        
        return results
    
    def _calculate_confidence(self, text, dialect):
        """Calcule un score de confiance pour la détection"""
        total_features = 0
        matched_features = 0
        
        # Compte des caractéristiques correspondantes
        for word in re.findall(r'\w+', text.lower()):
            total_features += 1
            if word in self.features[dialect]['lexical_signatures']:
                matched_features += 1
        
        return matched_features / total_features if total_features > 0 else 0