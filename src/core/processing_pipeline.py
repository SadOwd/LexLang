# src/core/processing_pipeline.py
class EweProcessingPipeline:
    def __init__(self, dialect=None):
        self.dialect_router = DialectRouter()
        self.dialect = dialect or 'standard'
        self.tokenizer = DialectAwareTokenizer()
        self.tonal_processor = EweTonalProcessor(self.dialect)
        self.morph_analyzer = EweMorphologicalAnalyzer()
        self.dialect_adapter = EweDialectAdapter(self.dialect)
    
    def process(self, text: str) -> list[dict]:
        # Détection automatique du dialecte si non spécifié
        if not self.dialect:
            self.dialect = self.dialect_router.detect(text)
            self.dialect_adapter = EweDialectAdapter(self.dialect)
            self.tonal_processor = EweTonalProcessor(self.dialect)
        
        # Traitement en pipeline
        tokens = self.tokenizer.tokenize(text)
        results = []
        
        for token in tokens:
            # Adaptation dialectale
            adapted_token = self.dialect_adapter.adapt(token)
            
            # Traitement tonal
            tonal_token = self.tonal_processor.apply(adapted_token)
            
            # Analyse morphologique
            analysis = self.morph_analyzer.analyze(tonal_token)
            
            results.append({
                'original': token,
                'dialect_form': adapted_token,
                'tonal_form': tonal_token,
                'analysis': analysis,
                'dialect': self.dialect
            })
        
        return results