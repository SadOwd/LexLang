import re
import unicodedata
from typing import Dict, List, Tuple

class OrthographicNormalizer:
    def __init__(self):
        # Mise à jour des mappings avec des regex plus précis
        self.variant_map: List[Tuple[str, str]] = [
            (r'e[èéêë]', 'e'),        # Voyelles antérieures
            (r'o[òóôö]', 'o'),        # Voyelles postérieures
            (r'[ŋñ]', 'ŋ'),           # Consonnes nasales
            (r'g[b]', 'gb'),          # Consonne labio-vélaire
            (r'k[p]', 'kp'),          # Consonne labio-vélaire
            (r'ts', 'c'),             # Affriquées
            (r'dz', 'j'),
            (r'ny', 'ɲ')
        ]
        
        # Erreurs courantes spécifiques à l'éwé
        self.common_errors = [
            (r'\bnu([ae])', r'n\1'),  # "nua" → "na"
            (r'\bgb([ae])', r'g\1'),  # "gbe" → "ge"
            (r'([aeiou])h', r'\1'),   # Suppression du 'h' parasite
            (r'([kpdgb])w', r'\1'),   # Simplification des clusters
            (r'([aeiou])\1', r'\1')   # Dédoublement vocalique
        ]
        
        # Mapping historique pour la normalisation
        self.historical_map: Dict[str, str] = {
            'ts': 'c',
            'dz': 'j',
            'ny': 'ɲ',
            'ɛ': 'e',
            'ɔ': 'o',
            'ɣ': 'g',
            'ʋ': 'v'
        }

    def normalize(self, text: str, dialect: str = 'standard') -> str:
        """
        Normalise l'orthographe d'un texte en éwé
        Args:
            text: Texte à normaliser
            dialect: Variante dialectale ('standard', 'anlo', 'inland')
        Returns:
            Texte normalisé
        """
        # Normalisation Unicode
        text = unicodedata.normalize('NFC', text)
        
        # Application des règles dialectales
        text = self.apply_dialect_rules(text, dialect)
        
        # Remplacement des variantes orthographiques
        for pattern, replacement in self.variant_map:
            text = re.sub(pattern, replacement, text)
        
        # Correction des erreurs courantes
        for pattern, replacement in self.common_errors:
            text = re.sub(pattern, replacement, text)
        
        # Normalisation des tons
        text = self.normalize_tones(text)
        
        return text

    def apply_dialect_rules(self, text: str, dialect: str) -> str:
        """Applique les transformations spécifiques au dialecte"""
        dialect_rules = {
            'anlo': [
                (r'kp', 'p'),      # Simplification en anlo
                (r'gb', 'b'),
                (r'ɖ', 'd')
            ],
            'inland': [
                (r'c', 'ts'),      # Formes conservatrices
                (r'j', 'dz'),
                (r'ɲ', 'ny')
            ]
        }
        
        if dialect in dialect_rules:
            for pattern, replacement in dialect_rules[dialect]:
                text = re.sub(pattern, replacement, text)
        
        return text

    def normalize_tones(self, text: str) -> str:
        """Uniformise la représentation des tons"""
        tone_mapping = [
            (r'[áàāâ]', 'a'),  # a tonique
            (r'[éèēê]', 'e'),  # e tonique
            (r'[íìīî]', 'i'),  # i tonique
            (r'[óòōô]', 'o'),  # o tonique
            (r'[úùūû]', 'u'),  # u tonique
            (r'[ÁÀ]', 'A'),    # A tonique
            (r'[ÉÈ]', 'E'),    # E tonique
            (r'[ÍÌ]', 'I'),    # I tonique
            (r'[ÓÒ]', 'O'),    # O tonique
            (r'[ÚÙ]', 'U')     # U tonique
        ]
        
        for pattern, replacement in tone_mapping:
            text = re.sub(pattern, replacement, text)
        
        return text

    def handle_historical_spelling(self, text: str) -> str:
        """Adapte l'orthographe historique aux normes modernes"""
        # Normalisation préalable
        text = unicodedata.normalize('NFD', text)
        
        # Application du mapping historique
        for old, new in self.historical_map.items():
            text = text.replace(old, new)
        
        # Suppression des diacritiques obsolètes
        text = re.sub(r'[`´^~¨]', '', text)
        
        return unicodedata.normalize('NFC', text)
    
    def syllabify(self, text: str) -> List[str]:
        """Découpe les mots en syllabes (CV structure)"""
        # Structure syllabique typique de l'éwé : (C)(C)V(V)(N)
        syllables = re.findall(
            r'[kpgbtdɖʧʤfvszhmnŋrlwy]?'
            r'[kp]?[wl]?'
            r'[aeiouɛɔ]+'
            r'[ŋ]?',
            text,
            re.IGNORECASE
        )
        return [syl for syl in syllables if syl]

# Exemple d'utilisation
if __name__ == "__main__":
    normalizer = OrthographicNormalizer()
    
    sample_text = "Míawo dzo kplé àblábìl le agble me"
    print("Original:", sample_text)
    
    normalized = normalizer.normalize(sample_text, dialect='inland')
    print("Normalisé:", normalized)
    
    historical = "Tswɔ nyuie dzi"
    print("Historique:", historical)
    print("Modernisé:", normalizer.handle_historical_spelling(historical))