#!/usr/bin/env python3
“””
LexLang - Tokeniseur Multilingue
Tokenisation adaptée aux langues africaines du Togo
“””

import re
import unicodedata
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass
import logging

# Import corrigé - assumant que TogoLanguages est dans le même package

try:
from .languages.togo_languages import TogoLanguages
except ImportError:
# Fallback pour les tests ou utilisation standalone
class TogoLanguages:
def get_tokenization_rules(self, language: str) -> Dict[str, bool]:
“”“Règles de tokenisation par défaut”””
default_rules = {
‘preserve_apostrophes’: True,
‘split_on_hyphens’: False,
‘tone_marks’: True,
‘case_sensitive’: False
}

```
        language_rules = {
            'fr': {'preserve_apostrophes': True, 'split_on_hyphens': False, 'tone_marks': False},
            'ee': {'preserve_apostrophes': False, 'split_on_hyphens': True, 'tone_marks': True},
            'kbp': {'preserve_apostrophes': False, 'split_on_hyphens': True, 'tone_marks': True},
            'tem': {'preserve_apostrophes': False, 'split_on_hyphens': True, 'tone_marks': True},
            'mfq': {'preserve_apostrophes': False, 'split_on_hyphens': True, 'tone_marks': True}
        }
        
        return language_rules.get(language, default_rules)
    
    def is_tone_language(self, language: str) -> bool:
        """Vérifier si une langue est tonale"""
        tone_languages = {'ee', 'kbp', 'tem', 'mfq'}
        return language in tone_languages
```

# Correction de **name**

logger = logging.getLogger(**name**)

@dataclass
class Token:
“”“Représentation d’un token”””
text: str
start: int
end: int
is_word: bool = False
is_punctuation: bool = False
is_number: bool = False
is_whitespace: bool = False
is_sentence_end: bool = False
has_tone_marks: bool = False
original_case: str = “”
normalized: str = “”

```
def to_dict(self) -> Dict[str, Any]:
    """Convertir en dictionnaire"""
    return {
        'text': self.text,
        'start': self.start,
        'end': self.end,
        'is_word': self.is_word,
        'is_punctuation': self.is_punctuation,
        'is_number': self.is_number,
        'is_whitespace': self.is_whitespace,
        'is_sentence_end': self.is_sentence_end,
        'has_tone_marks': self.has_tone_marks,
        'original_case': self.original_case,
        'normalized': self.normalized
    }
```

class MultilingualTokenizer:
“”“Tokeniseur multilingue pour les langues du Togo”””

```
def __init__(self):
    self.languages = TogoLanguages()
    
    # Patterns de base
    self.WORD_PATTERN = re.compile(r'\b\w+\b')
    self.SENTENCE_ENDERS = re.compile(r'[.!?]+')
    self.PUNCTUATION = re.compile(r'[^\w\s]')
    self.NUMBERS = re.compile(r'\b\d+([.,]\d+)?\b')
    self.WHITESPACE = re.compile(r'\s+')
    
    # Caractères spéciaux des langues africaines
    self.AFRICAN_CHARS = {
        'ee': set('ɖɛɔŋƒʋãẽĩõũáàāéèēíìīóòōúùū'),
        'kbp': set('ɩɛɔʊɓɗáàéèíìóòúù'),
        'tem': set('ɛɔŋãẽĩõũáàéèíìóòúù'),
        'mfq': set('ɛɔŋɓɗãẽĩõũáàéèíìóòúù')
    }
    
    # Patterns de tons
    self.TONE_MARKS = re.compile(r'[áàāéèēíìīóòōúùū]')
    
    logger.info("Tokeniseur multilingue initialisé")

def tokenize(self, text: str, language: str = 'fr') -> List[Dict[str, Any]]:
    """
    Tokeniser un texte selon la langue
    
    Args:
        text: Texte à tokeniser
        language: Code de langue
        
    Returns:
        Liste de tokens avec métadonnées
    """
    if not text:
        return []
    
    # Obtenir les règles de tokenisation pour la langue
    rules = self.languages.get_tokenization_rules(language)
    
    # Pré-traitement spécifique à la langue
    processed_text = self._preprocess_text(text, language, rules)
    
    # Tokenisation principale
    tokens = self._tokenize_text(processed_text, language, rules)
    
    # Post-traitement
    tokens = self._postprocess_tokens(tokens, language)
    
    return [token.to_dict() for token in tokens]

def _preprocess_text(self, text: str, language: str, rules: Dict[str, bool]) -> str:
    """
    Pré-traiter le texte selon les règles linguistiques
    
    Args:
        text: Texte original
        language: Code de langue
        rules: Règles de tokenisation
        
    Returns:
        Texte pré-traité
    """
    processed = text
    
    # Normalisation Unicode
    processed = unicodedata.normalize('NFC', processed)
    
    # Gestion des apostrophes selon la langue
    if language == 'fr' and rules.get('preserve_apostrophes', True):
        # Préserver les contractions françaises
        processed = re.sub(r"([a-zA-ZàâäéèêëïîôöùûüÿñçÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÑÇ])'([a-zA-ZàâäéèêëïîôöùûüÿñçÀÂÄÉÈÊËÏÎÔÖÙÛÜŸÑÇ])", 
                          r'\1ʼ\2', processed)
    elif not rules.get('preserve_apostrophes', False):
        # Remplacer les apostrophes par des espaces
        processed = re.sub(r"'", ' ', processed)
    
    # Gestion des traits d'union
    if rules.get('split_on_hyphens', False):
        processed = re.sub(r'-', ' ', processed)
    
    return processed

def _tokenize_text(self, text: str, language: str, rules: Dict[str, bool]) -> List[Token]:
    """
    Tokenisation principale du texte
    
    Args:
        text: Texte à tokeniser
        language: Code de langue
        rules: Règles de tokenisation
        
    Returns:
        Liste de tokens
    """
    tokens = []
    pos = 0
    
    # Tokenisation par regex avec gestion des caractères spéciaux
    pattern = self._build_tokenization_pattern(language)
    
    for match in re.finditer(pattern, text):
        token_text = match.group()
        start = match.start()
        end = match.end()
        
        # Créer le token avec classification
        token = self._create_token(token_text, start, end, language)
        tokens.append(token)
        
        pos = end
    
    return tokens

def _build_tokenization_pattern(self, language: str) -> str:
    """
    Construire le pattern de tokenisation pour une langue
    
    Args:
        language: Code de langue
        
    Returns:
        Pattern regex
    """
    # Pattern de base pour les mots
    base_pattern = r'\b\w+'
    
    # Ajouter les caractères spéciaux de la langue
    if language in self.AFRICAN_CHARS:
        special_chars = ''.join(self.AFRICAN_CHARS[language])
        # Échapper les caractères spéciaux pour regex
        escaped_chars = re.escape(special_chars)
        base_pattern = f'\\b[\\w{escaped_chars}]+'
    
    # Pattern complet incluant ponctuation et espaces
    full_pattern = f'({base_pattern}\\b|[^\\w\\s]|\\s+)'
    
    return full_pattern

def _create_token(self, text: str, start: int, end: int, language: str) -> Token:
    """
    Créer un token avec classification
    
    Args:
        text: Texte du token
        start: Position de début
        end: Position de fin
        language: Code de langue
        
    Returns:
        Token classifié
    """
    token = Token(
        text=text,
        start=start,
        end=end,
        original_case=text
    )
    
    # Classification du token
    if self.WHITESPACE.match(text):
        token.is_whitespace = True
    elif self.NUMBERS.match(text):
        token.is_number = True
    elif self.PUNCTUATION.match(text):
        token.is_punctuation = True
        token.is_sentence_end = bool(self.SENTENCE_ENDERS.match(text))
    elif self.WORD_PATTERN.match(text):
        token.is_word = True
        token.normalized = self._normalize_word(text, language)
        token.has_tone_marks = bool(self.TONE_MARKS.search(text))
    
    return token

def _normalize_word(self, word: str, language: str) -> str:
    """
    Normaliser un mot selon la langue
    
    Args:
        word: Mot à normaliser
        language: Code de langue
        
    Returns:
        Mot normalisé
    """
    normalized = word.lower()
    
    # Normalisation spécifique aux langues tonales
    if self.languages.is_tone_language(language):
        # Préserver les marques tonales lors de la normalisation
        tone_map = {
            'á': 'a', 'à': 'a', 'ā': 'a',
            'é': 'e', 'è': 'e', 'ē': 'e',
            'í': 'i', 'ì': 'i', 'ī': 'i',
            'ó': 'o', 'ò': 'o', 'ō': 'o',
            'ú': 'u', 'ù': 'u', 'ū': 'u'
        }
        
        # Option: conserver les tons ou les supprimer
        rules = self.languages.get_tokenization_rules(language)
        if not rules.get('tone_marks', True):
            for accented, base in tone_map.items():
                normalized = normalized.replace(accented, base)
    
    return normalized

def _postprocess_tokens(self, tokens: List[Token], language: str) -> List[Token]:
    """
    Post-traitement des tokens
    
    Args:
        tokens: Liste de tokens
        language: Code de langue
        
    Returns:
        Tokens post-traités
    """
    processed_tokens = []
    
    for i, token in enumerate(tokens):
        # Ignorer les tokens vides et les espaces multiples
        if not token.text.strip():
            continue
        
        # Traitement spécial pour les contractions
        if language == 'fr' and token.is_word:
            # Gérer les contractions françaises
            if 'ʼ' in token.text:
                # Diviser les contractions en tokens séparés
                parts = token.text.split('ʼ')
                for j, part in enumerate(parts):
                    if part:
                        new_token = Token(
                            text=part,
                            start=token.start,
                            end=token.end,
                            is_word=True,
                            normalized=part.lower(),
                            original_case=part
                        )
                        processed_tokens.append(new_token)
                continue
        
        processed_tokens.append(token)
    
    return processed_tokens

def get_word_tokens(self, text: str, language: str = 'fr') -> List[str]:
    """
    Obtenir uniquement les mots d'un texte
    
    Args:
        text: Texte à tokeniser
        language: Code de langue
        
    Returns:
        Liste des mots
    """
    tokens = self.tokenize(text, language)
    return [token['text'] for token in tokens if token['is_word']]

def count_tokens(self, text: str, language: str = 'fr') -> Dict[str, int]:
    """
    Compter les différents types de tokens
    
    Args:
        text: Texte à analyser
        language: Code de langue
        
    Returns:
        Compteurs par type de token
    """
    tokens = self.tokenize(text, language)
    
    counts = {
        'total': len(tokens),
        'words': sum(1 for t in tokens if t['is_word']),
        'punctuation': sum(1 for t in tokens if t['is_punctuation']),
        'numbers': sum(1 for t in tokens if t['is_number']),
        'sentences': sum(1 for t in tokens if t['is_sentence_end']),
        'tone_marked': sum(1 for t in tokens if t['has_tone_marks'])
    }
    
    return counts

def analyze_text_complexity(self, text: str, language: str = 'fr') -> Dict[str, Any]:
    """
    Analyser la complexité d'un texte
    
    Args:
        text: Texte à analyser
        language: Code de langue
        
    Returns:
        Métriques de complexité
    """
    tokens = self.tokenize(text, language)
    word_tokens = [t for t in tokens if t['is_word']]
    
    if not word_tokens:
        return {'error': 'Aucun mot trouvé'}
    
    # Métriques basiques
    word_lengths = [len(t['text']) for t in word_tokens]
    unique_words = set(t['normalized'] for t in word_tokens)
    
    complexity = {
        'total_words': len(word_tokens),
        'unique_words': len(unique_words),
        'lexical_diversity': len(unique_words) / len(word_tokens),
        'avg_word_length': sum(word_lengths) / len(word_lengths),
        'max_word_length': max(word_lengths),
        'min_word_length': min(word_lengths)
    }
    
    # Métriques spécifiques aux langues tonales
    if self.languages.is_tone_language(language):
        tone_words = [t for t in word_tokens if t['has_tone_marks']]
        complexity.update({
            'tone_marked_words': len(tone_words),
            'tone_density': len(tone_words) / len(word_tokens)
        })
    
    return complexity

def batch_tokenize(self, texts: List[str], language: str = 'fr') -> List[List[Dict[str, Any]]]:
    """
    Tokeniser plusieurs textes en lot
    
    Args:
        texts: Liste de textes à tokeniser
        language: Code de langue
        
    Returns:
        Liste des résultats de tokenisation
    """
    return [self.tokenize(text, language) for text in texts]

def get_vocabulary(self, texts: List[str], language: str = 'fr', min_frequency: int = 1) -> Dict[str, int]:
    """
    Extraire le vocabulaire d'un corpus
    
    Args:
        texts: Liste de textes
        language: Code de langue
        min_frequency: Fréquence minimale pour inclure un mot
        
    Returns:
        Dictionnaire mot -> fréquence
    """
    vocabulary = {}
    
    for text in texts:
        word_tokens = self.get_word_tokens(text, language)
        for word in word_tokens:
            normalized = word.lower()
            vocabulary[normalized] = vocabulary.get(normalized, 0) + 1
    
    # Filtrer par fréquence minimale
    return {word: freq for word, freq in vocabulary.items() if freq >= min_frequency}

def detect_language_features(self, text: str) -> Dict[str, Any]:
    """
    Détecter les caractéristiques linguistiques d'un texte
    
    Args:
        text: Texte à analyser
        
    Returns:
        Caractéristiques détectées
    """
    features = {
        'has_french_chars': bool(re.search(r'[àâäéèêëïîôöùûüÿñç]', text)),
        'has_tone_marks': bool(self.TONE_MARKS.search(text)),
        'has_african_chars': False,
        'likely_languages': []
    }
    
    # Vérifier les caractères spécifiques aux langues africaines
    for lang, chars in self.AFRICAN_CHARS.items():
        if any(char in text for char in chars):
            features['has_african_chars'] = True
            features['likely_languages'].append(lang)
    
    if features['has_french_chars'] and not features['has_african_chars']:
        features['likely_languages'].append('fr')
    
    return features
```

# Fonction utilitaire pour créer une instance du tokeniseur

def create_tokenizer() -> MultilingualTokenizer:
“”“Créer une instance du tokeniseur multilingue”””
return MultilingualTokenizer()

# Exemple d’utilisation

if **name** == “**main**”:
# Configuration du logging
logging.basicConfig(level=logging.INFO)

```
# Créer le tokeniseur
tokenizer = create_tokenizer()

# Exemples de textes
french_text = "Bonjour ! Comment allez-vous aujourd'hui ?"
ewe_text = "Míedo ŋutɔ. Ŋkeke nye kae?"

print("=== Exemple Français ===")
tokens_fr = tokenizer.tokenize(french_text, 'fr')
for token in tokens_fr:
    print(f"'{token['text']}' -> {token}")

print(f"\nComptage: {tokenizer.count_tokens(french_text, 'fr')}")

print("\n=== Exemple Éwé ===")
tokens_ee = tokenizer.tokenize(ewe_text, 'ee')
for token in tokens_ee:
    print(f"'{token['text']}' -> {token}")

print(f"\nComptage: {tokenizer.count_tokens(ewe_text, 'ee')}")

print("\n=== Détection des caractéristiques ===")
print(f"Français: {tokenizer.detect_language_features(french_text)}")
print(f"Éwé: {tokenizer.detect_language_features(ewe_text)}")
```