// TODO: Fill in content for cli.py
@click.command()
@click.option("--dialect", help="Dialecte éwé (standard, anlo, inland, badou)")
@click.option("--analyze", is_flag=True, help="Lancer l'analyse morphologique")
@click.argument("input", type=click.Path(exists=True))
def process(input, dialect, analyze):
    """Traite un texte en éwé avec LexLang"""
    pipeline = EweProcessingPipeline(dialect)
    
    if os.path.isfile(input):
        with open(input, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = input
    
    results = pipeline.process(text)
    
    if analyze:
        for result in results:
            click.echo(f"{result['original']} → {result['dialect_form']}")
            click.echo(f"  Analyse: {result['analysis']}")
    else:
        click.echo(json.dumps(results, indent=2, ensure_ascii=False))