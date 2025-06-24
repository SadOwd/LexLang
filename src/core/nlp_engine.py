"""
LexLang - Core NLP Engine
Module principal pour le traitement du langage naturel
Priorité: CRITIQUE - Base de tous les autres modules
"""

import re
import json
import pickle
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
import unicodedata


@dataclass
class Token:
    """Représentation d'un token linguistique"""
    text: str
    lemma: str
    pos: str  # Part of speech
    features: Dict[str, str]
    frequency: int = 1
    contexts: List[str] = None
    
    def __post_init__(self):
        if self.contexts is None:
            self.contexts = []


class LexicalDatabase:
    """Base de données lexicale optimisée pour les langues africaines et le français"""
    
    def __init__(self):
        self.tokens: Dict[str, Token] = {}
        self.lemma_index: Dict[str, Set[str]] = defaultdict(set)
        self.pos_index: Dict[str, Set[str]] = defaultdict(set)
        self.frequency_index: Dict[int, Set[str]] = defaultdict(set)
        self.n_grams: Dict[int, Dict[str, int]] = {2: {}, 3: {}, 4: {}}
        
    def add_token(self, token: Token) -> None:
        """Ajoute un token à la base lexicale"""
        key = token.text.lower()
        
        if key in self.tokens:
            self.tokens[key].frequency += token.frequency
            self.tokens[key].contexts.extend(token.contexts)
        else:
            self.tokens[key] = token
            
        # Mise à jour des index
        self.lemma_index[token.lemma].add(key)
        self.pos_index[token.pos].add(key)
        self.frequency_index[token.frequency].add(key)
    
    def get_token(self, text: str) -> Optional[Token]:
        """Récupère un token par son texte"""
        return self.tokens.get(text.lower())
    
    def search_by_lemma(self, lemma: str) -> List[Token]:
        """Recherche par lemme"""
        return [self.tokens[key] for key in self.lemma_index.get(lemma, [])]
    
    def search_by_pos(self, pos: str) -> List[Token]:
        """Recherche par catégorie grammaticale"""
        return [self.tokens[key] for key in self.pos_index.get(pos, [])]


class NLPProcessor:
    """Processeur NLP principal pour LexLang"""
    
    def __init__(self):
        self.lexical_db = LexicalDatabase()
        self.stop_words = self._load_stop_words()
        self.tokenizer_patterns = self._compile_patterns()
        
    def _load_stop_words(self) -> Set[str]:
        """Charge les mots vides pour français et langues africaines communes"""
        french_stops = {
            'le', 'de', 'et', 'à', 'un', 'il', 'être', 'et', 'en', 'avoir', 
            'que', 'pour', 'dans', 'ce', 'son', 'une', 'sur', 'avec', 'ne',
            'se', 'pas', 'tout', 'plus', 'par', 'grand', 'en', 'mais', 'si'
        }
        
        # Mots vides courants en langues africaines (exemple Wolof/Bambara)
        african_stops = {
            'ak', 'te', 'la', 'ka', 'ni', 'ye', 'ko', 'min', 'be', 'na'
        }
        
        return french_stops.union(african_stops)
    
    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """Compile les patterns regex pour la tokenisation"""
        return {
            'word': re.compile(r'\b\w+\b', re.UNICODE),
            'sentence': re.compile(r'[.!?]+', re.UNICODE),
            'punctuation': re.compile(r'[^\w\s]', re.UNICODE),
            'whitespace': re.compile(r'\s+', re.UNICODE),
            # Patterns spéciaux pour caractères africains
            'african_chars': re.compile(r'[àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]', re.UNICODE)
        }
    
    def normalize_text(self, text: str) -> str:
        """Normalise le texte pour un traitement uniforme"""
        # Normalisation Unicode
        text = unicodedata.normalize('NFKD', text)
        
        # Conversion en minuscules
        text = text.lower()
        
        # Suppression des caractères de contrôle
        text = ''.join(char for char in text if unicodedata.category(char)[0] != 'C')
        
        # Normalisation des espaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenise le texte en mots"""
        normalized = self.normalize_text(text)
        tokens = self.tokenizer_patterns['word'].findall(normalized)
        return [token for token in tokens if len(token) > 1]
    
    def extract_features(self, token: str, context: List[str]) -> Dict[str, str]:
        """Extrait les caractéristiques linguistiques d'un token"""
        features = {}
        
        # Longueur
        features['length'] = str(len(token))
        
        # Présence de caractères spéciaux
        if self.tokenizer_patterns['african_chars'].search(token):
            features['has_diacritics'] = 'true'
        
        # Position dans la phrase (approximative)
        if context:
            pos_ratio = context.index(token) / len(context) if token in context else 0.5
            if pos_ratio < 0.3:
                features['position'] = 'start'
            elif pos_ratio > 0.7:
                features['position'] = 'end'
            else:
                features['position'] = 'middle'
        
        # Fréquence relative des caractères
        char_freq = Counter(token)
        most_common = char_freq.most_common(1)
        if most_common:
            features['dominant_char'] = most_common[0][0]
        
        return features
    
    def simple_pos_tag(self, token: str) -> str:
        """Étiquetage morpho-syntaxique simple basé sur des règles"""
        token_lower = token.lower()
        
        # Articles français
        if token_lower in ['le', 'la', 'les', 'un', 'une', 'des', 'du', 'de']:
            return 'DET'
        
        # Pronoms
        if token_lower in ['je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles']:
            return 'PRON'
        
        # Prépositions
        if token_lower in ['à', 'de', 'dans', 'sur', 'avec', 'pour', 'par', 'en']:
            return 'ADP'
        
        # Conjonctions
        if token_lower in ['et', 'ou', 'mais', 'car', 'donc', 'que', 'si']:
            return 'CONJ'
        
        # Règles morphologiques simples
        if token.endswith(('tion', 'sion', 'ance', 'ence')):
            return 'NOUN'
        if token.endswith(('er', 'ir', 'oire', 'quer')):
            return 'VERB'
        if token.endswith(('ment',)):
            return 'ADV'
        if token.endswith(('eux', 'euse', 'ique', 'able')):
            return 'ADJ'
        
        # Par défaut
        return 'NOUN'
    
    def generate_ngrams(self, tokens: List[str], n: int = 2) -> List[str]:
        """Génère des n-grammes à partir d'une liste de tokens"""
        if len(tokens) < n:
            return []
        
        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngram = ' '.join(tokens[i:i+n])
            ngrams.append(ngram)
        
        return ngrams
    
    def process_text(self, text: str) -> Dict[str, any]:
        """Traite un texte complet et met à jour la base lexicale"""
        # Tokenisation
        tokens = self.tokenize(text)
        
        # Traitement de chaque token
        processed_tokens = []
        for token_text in tokens:
            if token_text.lower() not in self.stop_words:
                # Extraction des caractéristiques
                features = self.extract_features(token_text, tokens)
                
                # Étiquetage morpho-syntaxique
                pos = self.simple_pos_tag(token_text)
                
                # Lemmatisation simple (ici juste conversion en minuscules)
                lemma = token_text.lower()
                
                # Création du token
                token = Token(
                    text=token_text,
                    lemma=lemma,
                    pos=pos,
                    features=features,
                    contexts=[text[:100]]  # Contexte limité
                )
                
                # Ajout à la base lexicale
                self.lexical_db.add_token(token)
                processed_tokens.append(token)
        
        # Génération des n-grammes
        for n in [2, 3, 4]:
            ngrams = self.generate_ngrams([t.text for t in processed_tokens], n)
            for ngram in ngrams:
                if ngram in self.lexical_db.n_grams[n]:
                    self.lexical_db.n_grams[n][ngram] += 1
                else:
                    self.lexical_db.n_grams[n][ngram] = 1
        
        return {
            'tokens_count': len(processed_tokens),
            'unique_tokens': len(set(t.text for t in processed_tokens)),
            'ngrams_generated': sum(len(self.lexical_db.n_grams[n]) for n in [2, 3, 4]),
            'tokens': [asdict(t) for t in processed_tokens]
        }
    
    def get_statistics(self) -> Dict[str, any]:
        """Retourne les statistiques de la base lexicale"""
        total_tokens = len(self.lexical_db.tokens)
        pos_distribution = Counter()
        
        for token in self.lexical_db.tokens.values():
            pos_distribution[token.pos] += 1
        
        return {
            'total_tokens': total_tokens,
            'unique_lemmas': len(self.lexical_db.lemma_index),
            'pos_distribution': dict(pos_distribution),
            'most_frequent': sorted(
                [(t.text, t.frequency) for t in self.lexical_db.tokens.values()],
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }
    
    def save_database(self, filepath: str) -> None:
        """Sauvegarde la base lexicale"""
        with open(filepath, 'wb') as f:
            pickle.dump(self.lexical_db, f)
    
    def load_database(self, filepath: str) -> None:
        """Charge une base lexicale"""
        with open(filepath, 'rb') as f:
            self.lexical_db = pickle.load(f)


# Exemple d'utilisation
if __name__ == "__main__":
    processor = NLPProcessor()
    
    # Test avec du texte français
    text_fr = "Bonjour, comment allez-vous ? J'espère que tout va bien."
    result_fr = processor.process_text(text_fr)
    print("Résultats français:", result_fr)
    
    # Test avec du texte mixte (français + mots africains simulés)
    text_mix = "Salam aleikum, ça va bien ak toi ? Nanga def ak sa famille ?"
    result_mix = processor.process_text(text_mix)
    print("Résultats mixte:", result_mix)
    
    # Statistiques
    stats = processor.get_statistics()
    print("Statistiques:", stats)
