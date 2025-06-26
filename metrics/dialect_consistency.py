# metrics/dialect_consistency.py
def calculate_dialect_consistency(lexicon: list) -> float:
    """Calcule le taux de couverture des variantes dialectales"""
    variants_count = 0
    total_entries = len(lexicon)
    
    for entry in lexicon:
        if entry.get('dialect_variants'):
            variants_count += len(entry['dialect_variants'])
    
    return variants_count / total_entries

# metrics/tonal_accuracy.py
def evaluate_tonal_system(test_cases: list) -> dict:
    """Évalue la précision du système tonal"""
    results = {'correct': 0, 'total': len(test_cases)}
    
    for input, expected in test_cases:
        processor = EweTonalProcessor()
        output = processor.apply(input)
        if output == expected:
            results['correct'] += 1
    
    results['accuracy'] = results['correct'] / results['total']
    return results