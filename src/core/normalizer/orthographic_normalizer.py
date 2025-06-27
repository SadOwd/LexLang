from ..dialect_handler import DialectDetector, DialectConverter

class DialectNormalizer:
    def __init__(self, target_dialect="anlo"):
        self.detector = DialectDetector()
        self.converter = DialectConverter()
        self.target_dialect = target_dialect
    
    def normalize(self, text):
        """Normalise un texte vers le dialecte cible"""
        detected_dialect = self.detector.detect(text)
        
        if detected_dialect == self.target_dialect:
            return text
        
        return self.converter.convert(text, detected_dialect, self.target_dialect)
    
    def preserve_dialect_features(self, text):
        """Préserve les caractéristiques dialectales tout en normalisant l'essentiel"""
        # Analyse des éléments dialectaux
        dialect_features = self.detector.analyze_mixed_text(text)
        
        # Normalisation de base
        normalized_text = text
        for feature in dialect_features:
            dialect = feature['dialect']
            if dialect != self.target_dialect:
                segment = feature['text']
                normalized_segment = self.converter.convert(
                    segment, 
                    dialect, 
                    self.target_dialect
                )
                normalized_text = normalized_text.replace(segment, normalized_segment)
        
        return normalized_text