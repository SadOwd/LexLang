// TODO: Fill in content for tonal_evaluation.py
import numpy as np
from typing import List, Tuple

def tonal_accuracy(predicted: List[str], target: List[str]) -> float:
    """
    Calcule la précision tonale entre séquences prédites et réelles
    Args:
        predicted: Séquences tonales prédites (ex: ['H', 'M', 'L'])
        target: Séquences tonales réelles
    Returns:
        Précision tonale (0.0-1.0)
    """
    if len(predicted) != len(target):
        raise ValueError("Les séquences doivent avoir la même longueur")
    
    matches = sum(1 for p, t in zip(predicted, target) if p == t)
    return matches / len(predicted)

def tonal_confusion_matrix(predicted: List[str], target: List[str]) -> dict:
    """Génère une matrice de confusion tonale"""
    categories = ['H', 'M', 'L']
    matrix = {real: {pred: 0 for pred in categories} for real in categories}
    
    for p, t in zip(predicted, target):
        if t in categories and p in categories:
            matrix[t][p] += 1
    
    return matrix

def tonal_f1_score(predicted: List[str], target: List[str], tone: str) -> float:
    """
    Calcule le F1-score pour une catégorie tonale spécifique
    Args:
        tone: Catégorie tonale à évaluer ('H', 'M', 'L')
    """
    true_pos = sum(1 for p, t in zip(predicted, target) if p == tone and t == tone)
    false_pos = sum(1 for p, t in zip(predicted, target) if p == tone and t != tone)
    false_neg = sum(1 for p, t in zip(predicted, target) if p != tone and t == tone)
    
    precision = true_pos / (true_pos + false_pos) if (true_pos + false_pos) > 0 else 0
    recall = true_pos / (true_pos + false_neg) if (true_pos + false_neg) > 0 else 0
    
    if precision + recall == 0:
        return 0.0
    
    return 2 * (precision * recall) / (precision + recall)