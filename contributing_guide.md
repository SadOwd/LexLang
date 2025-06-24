# Guide de contribution - LexLang

Merci de votre intérêt pour contribuer à LexLang ! Ce guide vous aidera à comprendre comment participer efficacement au projet.

## 🤝 Comment contribuer

### 1. Préparer votre environnement

```bash
# Forker le repository sur GitHub
# Puis cloner votre fork
git clone https://github.com/votre-username/LexLang.git
cd LexLang

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Créer une branche

```bash
git checkout -b feature/nouvelle-fonctionnalite
# ou
git checkout -b fix/correction-bug
# ou
git checkout -b docs/amelioration-documentation
```

### 3. Faire vos modifications

Suivez les conventions décrites dans ce document pour vos modifications.

### 4. Tester vos modifications

```bash
# Lancer les tests
python -m pytest tests/

# Vérifier le style de code
flake8 lexlang/
black --check lexlang/

# Valider les données JSON
python scripts/validation/validate_dictionaries.py
```

### 5. Soumettre votre contribution

```bash
git add .
git commit -m "type: description courte de la modification"
git push origin nom-de-votre-branche
```

Puis créez une Pull Request sur GitHub.

## 📝 Types de contributions

### 🔤 Ajout d’entrées lexicales

**Format requis pour les entrées de dictionnaire :**

```json
{
  "id": "word_XXX",
  "ewe": "mot_ewe",
  "french": "traduction_française",
  "english": "english_translation",
  "pos": "NOUN|VERB|ADJ|...",
  "tone": "H-L|L-H|...",
  "phonetic": "/transcription_phonétique/",
  "examples": [
    {
      "ewe": "Phrase d'exemple en éwé",
      "french": "Traduction française",
      "english": "English translation"
    }
  ],
  "dialect_variants": {
    "anlo": "variante_anlo",
    "ewedome": "variante_ewedome"
  },
  "morphology": {
    "root": "racine",
    "class": "classe_morphologique"
  }
}
```

### 🐛 Signalement et correction de bugs

1. Vérifiez d’abord si le bug n’est pas déjà signalé
1. Créez une issue avec :
- Description claire du problème
- Étapes pour reproduire
- Comportement attendu vs observé
- Environnement (OS, version Python, etc.)

### 📚 Amélioration de la documentation

- Corriger les erreurs de frappe
- Améliorer la clarté des explications
- Ajouter des exemples
- Traduire la documentation

### 🔧 Développement d’outils

- Tokenizer
- Normalisateur
- POS tagger
- Outils de validation

## 📋 Standards et conventions

### Orthographe éwé

- Utiliser l’orthographe éwé standardisée
- Notation des tons : H (haut), L (bas), M (moyen)
- Caractères spéciaux : ɖ, ɛ, ɔ, ŋ, ʋ

### Catégories grammaticales (POS)

|Code|Description |Exemple              |
|----|------------|---------------------|
|NOUN|Nom         |ame (personne)       |
|VERB|Verbe       |dzo (partir)         |
|ADJ |Adjectif    |nyui (bon)           |
|ADV |Adverbe     |kabakaba (rapidement)|
|PRON|Pronom      |nye (je)             |
|DET |Déterminant |la (le/la)           |
|ADP |Adposition  |le (dans)            |
|CONJ|Conjonction |kple (et)            |
|PART|Particule   |a (particule)        |
|INTJ|Interjection|aa (ah)              |

### Style de code Python

```python
# Utiliser Black pour le formatage
black lexlang/

# Suivre PEP 8
# Noms de variables en snake_case
# Noms de classes en PascalCase
# Constantes en UPPER_CASE

# Exemple de classe
class EweDictionary:
    """Dictionnaire éwé avec fonctionnalités de recherche."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self._entries = {}
    
    def search(self, word: str, lang: str = "ewe") -> List[Dict]:
        """Rechercher un mot dans le dictionnaire."""
        pass
```

### Commits et messages

Format des messages de commit :

```
type(scope): description

type: feat, fix, docs, style, refactor, test, chore
scope: dictionaries, tools, docs, tests, etc.

Exemples :
feat(dictionaries): ajouter 100 nouveaux verbes éwé
fix(tokenizer): corriger la gestion des caractères spéciaux
docs(readme): améliorer les instructions d'installation
```

## ✅ Critères de qualité

### Pour les données lexicales

- **Exactitude linguistique** : Vérification par des locuteurs natifs
- **Cohérence** : Respect des conventions établies
- **Complétude** : Tous les champs requis remplis
- **Unicité** : Pas de doublons

### Pour le code

- **Tests** : Couverture minimale de 80%
- **Documentation** : Docstrings pour toutes les fonctions publiques
- **Style** : Conformité à PEP 8 et Black
- **Performance** : Optimisation raisonnable

### Pour la documentation

- **Clarté** : Explications compréhensibles
- **Exemples** : Code fonctionnel et testé
- **Mise à jour** : Synchronisation avec le code

## 🎯 Priorités actuelles

### Phase 1 (En cours)

- [ ] Dictionnaire de base (5000 entrées)
- [ ] Validation des formats JSON
- [ ] Tests unitaires
- [ ] Documentation API

### Contributions les plus utiles

1. **Entrées lexicales** : Mots courants, verbes, noms
1. **Validation** : Révision par des locuteurs natifs
1. **Tests** : Cas d’usage réels
1. **Documentation** : Guides d’utilisation

## 🚨 Ce qu’il faut éviter

- Entrées sans source fiable
- Code sans tests
- Modifications de format sans discussion
- Commits avec messages peu clairs
- Pull requests trop volumineuses

## 📞 Obtenir de l’aide

- **Issues GitHub** : Pour les questions techniques
- **Discussions** : Pour les questions générales
- **Wiki** : Pour la documentation collaborative

## 🏆 Reconnaissance

Tous les contributeurs seront reconnus dans :

- Le fichier CONTRIBUTORS.md
- Les notes de version
- La documentation

## 📄 Licence des contributions

En contribuant à LexLang, vous acceptez que vos contributions soient distribuées sous licence MIT.

-----

Merci de contribuer à la préservation et au développement technologique de la langue éwé ! 🌍