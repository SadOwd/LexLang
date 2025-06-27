from src.core.dialect_handler import DialectDetector, DialectConverter

class DialectAdapter:
    def __init__(self):
        self.detector = DialectDetector()
        self.converter = DialectConverter()
        self.dialect_embeddings = {
            'anlo': [1, 0, 0],
            'inland': [0, 1, 0],
            'gbekplo': [0, 0, 1],
            'standard': [0.5, 0.5, 0]
        }
    
    def adapt(self, tokenized_sentences, dialects=None):
        """Adapte les phrases aux caractéristiques dialectales"""
        if not dialects:
            dialects = [self.detector.detect(' '.join(tokens)) for tokens in tokenized_sentences]
        
        adapted_sentences = []
        for tokens, dialect in zip(tokenized_sentences, dialects):
            # Conversion lexicale
            converted_tokens = [self.converter.convert_token(token, 'standard', dialect) for token in tokens]
            adapted_sentences.append(converted_tokens)
        
        return adapted_sentences
    
    def get_dialect_features(self, dialects):
        """Retourne les embeddings de dialecte"""
        return [self.dialect_embeddings.get(d, [0, 0, 0]) for d in dialects]
    
    def convert_token(self, token, source_dialect, target_dialect):
        """Convertit un token entre dialectes"""
        if source_dialect == target_dialect:
            return token
        
        # Règles spécifiques pour le POS tagging
        if target_dialect == 'anlo':
            # Simplification des clusters consonantiques
            token = re.sub(r'kp', 'p', token)
            token = re.sub(r'gb', 'b', token)
        elif target_dialect == 'inland':
            # Formes conservatrices
            token = re.sub(r'c', 'ts', token)
            token = re.sub(r'j', 'dz', token)
        
        return token