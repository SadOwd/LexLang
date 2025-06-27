import tensorflow as tf
from tensorflow.keras.layers import Bidirectional, LSTM, Embedding, Dense
from tensorflow_addons.layers import CRF
from .tonal_integration import TonalFeatureExtractor
from .dialect_adaptation import DialectAdapter

class EwePOSTagger:
    def __init__(self, config):
        self.config = config
        self.tonal_extractor = TonalFeatureExtractor()
        self.dialect_adapter = DialectAdapter()
        self.model = self.build_model()
        
    def build_model(self):
        """Construit le modèle BiLSTM-CRF avec intégration tonale"""
        # Couche d'entrée
        word_input = tf.keras.Input(shape=(None,), name="word_input")
        dialect_input = tf.keras.Input(shape=(None,), name="dialect_input")
        
        # Embeddings de mots
        word_emb = Embedding(
            input_dim=self.config['vocab_size'],
            output_dim=self.config['embedding_dim'],
            mask_zero=True
        )(word_input)
        
        # Features tonales
        tonal_features = self.tonal_extractor(word_input)
        
        # Adaptation dialectale
        dialect_features = self.dialect_adapter(dialect_input)
        
        # Concaténation des caractéristiques
        combined = tf.keras.layers.concatenate(
            [word_emb, tonal_features, dialect_features]
        )
        
        # Couches BiLSTM
        bilstm = Bidirectional(
            LSTM(units=self.config['hidden_dim'],
                 return_sequences=True,
                 recurrent_dropout=0.2)
        )(combined)
        
        # Couche Dense pour les features
        dense = Dense(self.config['hidden_dim'], activation='relu')(bilstm)
        
        # Couche CRF
        crf = CRF(self.config['num_tags'], name='crf_layer')(dense)
        
        return tf.keras.Model(
            inputs=[word_input, dialect_input],
            outputs=crf
        )
    
    def preprocess(self, sentences, dialects=None):
        """Prétraite les phrases pour le tagging"""
        tokenized = [self.tokenize(sent) for sent in sentences]
        
        # Extraction des caractéristiques tonales
        tonal_features = [self.tonal_extractor.extract(sent) for sent in tokenized]
        
        # Adaptation dialectale
        if not dialects:
            dialects = ['standard'] * len(sentences)
        dialect_features = self.dialect_adapter.adapt(tokenized, dialects)
        
        return {
            'word_input': tokenized,
            'dialect_input': dialect_features,
            'tonal_features': tonal_features
        }
    
    def tag(self, sentences, dialects=None):
        """Effectue le tagging POS sur une liste de phrases"""
        preprocessed = self.preprocess(sentences, dialects)
        predictions = self.model.predict(preprocessed)
        return self.decode_predictions(predictions)
    
    def decode_predictions(self, predictions):
        """Décode les prédictions du modèle en tags POS"""
        # Implémentation de décodage Viterbi pour CRF
        pass
    
    def tokenize(self, sentence):
        """Tokenisation spécifique à l'éwé avec gestion des mots composés"""
        return self.compound_analyzer.split_compounds(sentence)

class CompoundAnalyzer:
    def __init__(self, lexicon_path="data/lexicons/ewe_compounds.json"):
        with open(lexicon_path, 'r', encoding='utf-8') as f:
            self.compound_dict = json.load(f)
    
    def split_compounds(self, sentence):
        """Décompose les mots composés en morphèmes"""
        tokens = []
        for word in sentence.split():
            if word in self.compound_dict:
                tokens.extend(self.compound_dict[word])
            else:
                tokens.append(word)
        return tokens