# 🌍 LexLang - Base Lexicale Publique Multilingue

> **Base lexicale open-source pour le français et les langues africaines avec API REST et outils NLP**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![API Status](https://img.shields.io/badge/API-Active-green.svg)]()

## 🎯 Objectif

LexLang est une plateforme open-source qui vise à créer et maintenir une base lexicale publique multilingue, avec un focus particulier sur les langues africaines souvent sous-représentées dans les outils NLP existants.

## ✨ Fonctionnalités

### 🔥 Moteur NLP Core
- **Tokenisation multilingue** adaptée aux langues africaines
- **Analyse morpho-syntaxique** avec étiquetage POS
- **Extraction de caractéristiques** linguistiques
- **Génération de n-grammes** (2, 3, 4-grammes)
- **Normalisation de texte** Unicode complète

### 🌐 API REST Publique
- **Analyse de texte** en temps réel
- **Recherche lexicale** avancée
- **Statistiques** de la base de données
- **Contributions communautaires** 
- **Rate limiting** et sécurité

### 📊 Gestion de Données
- **Import/Export** multiples formats (JSON, CSV, XML, CoNLL-U)
- **Base de données** SQLite intégrée
- **Sauvegarde automatique** 
- **Versioning** des données

## 🗣️ Langues Supportées

| Langue | Code | Statut | Tokens |
|--------|------|--------|--------|
| Français | `fr` | ✅ Complet | 50K+ |
| Wolof | `wo` | 🔄 En cours | 15K+ |
| Bambara | `bm` | 🔄 En cours | 12K+ |
| Lingala | `ln` | 🚧 Basique | 5K+ |
| Swahili | `sw` | 🚧 Basique | 8K+ |

## 🚀 Installation Rapide

### Prérequis
- Python 3.8+
- pip

### Installation
```bash
# Cloner le repository
git clone https://github.com/SadOwd/LexLang.git
cd LexLang

# Installer les dépendances
pip install -r requirements.txt

# Initialiser la base de données
python scripts/setup_database.py

# Lancer l'API
python src/api/lexical_api.py
```

L'API sera accessible sur `http://localhost:5000`

## 📖 Utilisation

### API REST

#### Analyser un texte
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Salam aleikum, nanga def?"}'
```

#### Rechercher dans la base
```bash
curl "http://localhost:5000/search?q=bonjour&type=text&limit=10"
```

#### Obtenir les statistiques
```bash
curl "http://localhost:5000/stats"
```

### Utilisation Python

```python
from src.core.nlp_engine import NLPProcessor

# Initialiser le processeur
processor = NLPProcessor()

# Analyser un texte
result = processor.process_text("Bonjour, comment allez-vous ?")
print(result)

# Rechercher un token
token = processor.lexical_db.get_token("bonjour")
print(f"Fréquence: {token.frequency}")
```

## 🏗️ Architecture

```
LexLang/
├── src/core/           # 🔥 Moteur NLP principal
├── src/api/            # 🌐 API REST publique
├── src/utils/          # 🛠️ Utilitaires et gestionnaires
├── data/               # 📊 Données lexicales
├── tests/              # ✅ Tests unitaires
└── docs/               # 📚 Documentation
```

## 🤝 Contribution

Nous encourageons vivement les contributions, surtout pour :

- **Ajout de nouvelles langues** africaines
- **Amélioration des algorithmes** NLP
- **Correction des données** lexicales
- **Traduction de la documentation**

### Comment contribuer

1. **Fork** le projet
2. Créer une **branche** (`git checkout -b feature/nouvelle-langue`)
3. **Committer** vos changements (`git commit -am 'Ajout du Kikongo'`)
4. **Push** sur la branche (`git push origin feature/nouvelle-langue`)
5. Créer une **Pull Request**

### Contribuer des données

```bash
# Via l'API
curl -X POST http://localhost:5000/contribute \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Texte en langue africaine",
    "language": "wo",
    "source": "corpus_traditionnel"
  }'
```

## 📊 Statistiques du Projet

- **Total tokens**: 90,000+
- **Langues actives**: 5
- **Contributeurs**: Rejoignez-nous !
- **API calls/jour**: 1,000+

## 🛣️ Roadmap

### Version 1.1 (Q3 2025)
- [ ] Support de 3 nouvelles langues africaines
- [ ] Interface web pour les contributions
- [ ] Modèles pré-entraînés disponibles

### Version 1.2 (Q4 2025)
- [ ] Analyse syntaxique avancée
- [ ] Détection automatique de langue
- [ ] Support des dialectes régionaux

### Version 2.0 (2026)
- [ ] Intégration Transformer models
- [ ] API GraphQL
- [ ] Application mobile

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- Communauté des linguistes africains
- Contributeurs open-source
- Universités partenaires en Afrique

## 📞 Contact

- **Email**: lexlang.project@gmail.com
- **Issues**: [GitHub Issues](https://github.com/SadOwd/LexLang/issues)
- **Discussions**: [GitHub Discussions](https://github.com/SadOwd/LexLang/discussions)

---

**🌍 Ensemble, préservons et valorisons la richesse linguistique africaine !**