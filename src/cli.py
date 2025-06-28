"""Command line interface for LexLang."""

import click
import json
import logging
from pathlib import Path
from typing import List, Optional

from .config import load_config
from .core.pipeline import Pipeline
from .utils import setup_logging
from .exceptions import LexLangError


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--config', '-c', default='configs/default.yaml', 
              help='Configuration file path')
@click.pass_context
def cli(ctx, verbose: bool, config: str):
    """LexLang: Advanced NLP toolkit for Ewe language processing."""
    ctx.ensure_object(dict)
    
    # Setup logging
    log_level = logging.DEBUG if verbose else logging.INFO
    setup_logging(level=log_level)
    
    # Load configuration
    try:
        ctx.obj['config'] = load_config(config)
        ctx.obj['pipeline'] = Pipeline(ctx.obj['config'])
    except Exception as e:
        click.echo(f"Error loading configuration: {e}", err=True)
        ctx.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--dialect', '-d', 
              type=click.Choice(['anlo', 'inland', 'ho', 'kpando', 'auto']),
              default='auto', help='Target dialect')
@click.option('--format', '-f',
              type=click.Choice(['json', 'text', 'conllu']),
              default='json', help='Output format')
@click.pass_context
def process(ctx, input_file: str, output: Optional[str], 
           dialect: str, format: str):
    """Process a text file."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        pipeline = ctx.obj['pipeline']
        results = pipeline.process(
            text=text,
            dialect=dialect,
            tasks=['tokenize', 'normalize', 'pos', 'tone'],
            output_format=format
        )
        
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(results)
            click.echo(f"Results written to {output}")
        else:
            click.echo(results)
            
    except Exception as e:
        click.echo(f"Error processing file: {e}", err=True)


@cli.command()
@click.argument('text')
@click.option('--dialect', '-d',
              type=click.Choice(['anlo', 'inland', 'ho', 'kpando', 'auto']),
              default='auto', help='Target dialect')
@click.pass_context
def analyze(ctx, text: str, dialect: str):
    """Analyze a text string."""
    try:
        pipeline = ctx.obj['pipeline']
        results = pipeline.process(
            text=text,
            dialect=dialect,
            tasks=['tokenize', 'normalize', 'pos', 'tone', 'dialect'],
            output_format='json'
        )
        
        # Pretty print JSON
        parsed = json.loads(results)
        click.echo(json.dumps(parsed, indent=2, ensure_ascii=False))
        
    except Exception as e:
        click.echo(f"Error analyzing text: {e}", err=True)


@cli.command()
@click.argument('model_type', 
               type=click.Choice(['pos', 'dialect', 'tone', 'embeddings']))
@click.argument('training_data', type=click.Path(exists=True))
@click.option('--output-dir', '-o', type=click.Path(), 
              help='Output directory for trained model')
@click.pass_context
def train(ctx, model_type: str, training_data: str, output_dir: Optional[str]):
    """Train a specific model."""
    try:
        from .scripts.training import train_model
        
        config = ctx.obj['config']
        output_path = train_model(
            model_type=model_type,
            training_data=training_data,
            config=config,
            output_dir=output_dir
        )
        
        click.echo(f"Model trained successfully: {output_path}")
        
    except Exception as e:
        click.echo(f"Error training model: {e}", err=True)


@cli.command()
@click.argument('model_path', type=click.Path(exists=True))
@click.argument('test_data', type=click.Path(exists=True))
@click.pass_context
def evaluate(ctx, model_path: str, test_data: str):
    """Evaluate a trained model."""
    try:
        from .scripts.evaluation import evaluate_model
        
        results = evaluate_model(model_path, test_data)
        
        click.echo("Evaluation Results:")
        for metric, value in results.items():
            click.echo(f"  {metric}: {value:.4f}")
            
    except Exception as e:
        click.echo(f"Error evaluating model: {e}", err=True)


def main():
    """Entry point for CLI."""
    cli()


if __name__ == '__main__':
    main()
