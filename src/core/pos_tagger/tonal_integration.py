import re
import numpy as np

class TonalFeatureExtractor:
    def __init__(self, tonal_alphabet="data/linguistic_resources/tonal/tonal_alphabet.json"):
        with open(tonal_alphabet, 'r', encoding='utf-8') as f:
            self.tonal_map = json.load(f)
    
    def extract(self, tokens):
        """Extrait les caractéristiques tonales pour chaque token"""
        features = []
        for token in tokens:
            # Analyse tonale
            tonal_pattern = self.get_tonal_pattern(token)
            tone_density = self.calculate_tone_density(token)
            dominant_tone = self.get_dominant_tone(token)
            
            features.append([
                len(tonal_pattern),
                tone_density,
                self.tonal_map[dominant_tone] if dominant_tone in self.tonal_map else 0
            ])
        return np.array(features)
    
    def get_tonal_pattern(self, word):
        """Extrait le patron tonal d'un mot"""
        return re.findall(r'[áéíóúÁÉÍÓÚ]', word)
    
    def calculate_tone_density(self, word):
        """Calcule la densité tonale (rapport syllabes tonales/total syllabes)"""
        tonal_syllables = len(self.get_tonal_pattern(word))
        total_syllables = len(re.findall(r'[aeiouáéíóú]', word, re.IGNORECASE))
        return tonal_syllables / total_syllables if total_syllables > 0 else 0
    
    def get_dominant_tone(self, word):
        """Détermine le ton dominant dans un mot"""
        tones = self.get_tonal_pattern(word)
        if not tones:
            return 'M'  # Ton moyen par défaut
        
        counter = Counter(tones)
        return counter.most_common(1)[0][0]