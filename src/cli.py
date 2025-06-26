// TODO: Fill in content for cli.py
import click
from pathlib import Path
from .core import EweProcessor
from .configs import load_config

@click.group()
@click.version_option("0.1.0")
def cli():
    """LexLang - Outil linguistique pour la langue éwé"""
    pass

@cli.command()
@click.argument("input_text", type=str)
@click.option("--dialect", default="anlo", 
              help="Dialecte: anlo/inland (défaut: anlo)")
@click.option("--output", type=click.Path(), 
              help="Fichier de sortie (optionnel)")
@click.option("--task", default="all", 
              help="Tokenize/pos/tonal (défaut: all)")
def process(input_text, dialect, output, task):
    """Traite un texte en éwé"""
    config = load_config(f"configs/dialect_{dialect}.yaml")
    processor = EweProcessor(config)
    
    # Gestion des fichiers ou texte direct
    if Path(input_text).exists():
        with open(input_text, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = input_text
    
    # Sélection des tâches
    if task == "tokenize":
        result = processor.tokenize(text)
    elif task == "pos":
        result = processor.pos_tag(text)
    elif task == "tonal":
        result = processor.tonal_analysis(text)
    else:
        result = processor.full_pipeline(text)
    
    # Sortie des résultats
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(result.to_json())
        click.echo(f"Résultats sauvegardés dans {output}")
    else:
        click.echo("Résultats du traitement:")
        click.echo(result.pretty_print())

@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_dir", type=click.Path())
def convert(input_file, output_dir):
    """Convertit les données entre formats"""
    from .scripts.conversion import convert_format
    convert_format(input_file, output_dir)
    click.echo(f"Conversion terminée: {input_file} -> {output_dir}")

@cli.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option("--data-dir", default="data/corpora", 
              help="Répertoire des données d'entraînement")
def train(config_file, data_dir):
    """Entraîne un modèle linguistique"""
    from .scripts.training import train_model
    results = train_model(config_file, data_dir)
    click.echo(f"Entraînement terminé. Score: {results['accuracy']:.2f}")

if __name__ == "__main__":
    cli()