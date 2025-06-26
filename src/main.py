// TODO: Fill in content for main.py
from pathlib import Path
from .core import EweProcessor
from .configs import load_config

def main():
    """Point d'entrée principal pour le traitement linguistique"""
    config = load_config('configs/main_config.yaml')
    processor = EweProcessor(config)
    
    # Exemple de pipeline
    text = "Míawo dzo kplé ablabil le agble me"
    processed = processor.full_pipeline(text)
    
    print("Résultat du traitement:")
    print(processed.to_json(indent=2))

if __name__ == "__main__":
    main()