# docs/guides/ewe_processing.md
## Pipeline de traitement de l'éwé

### Étapes de traitement :
1. **Tokenisation adaptée** : Segmentation en mots avec sensibilité dialectale
2. **Adaptation dialectale** : 
   ```python
   adapter = EweDialectAdapter('badou')
   adapter.adapt("ananas")  # → "ababil"