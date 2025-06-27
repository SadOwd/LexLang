import numpy as np
from typing import List, Dict

def tonal_edit_distance(seq1: List[str], seq2: List[str]) -> int:
    """
    Calcule la distance d'édition tonale (basée sur Levenshtein)
    avec coûts adaptés aux relations tonales
    """
    len1, len2 = len(seq1), len(seq2)
    matrix = np.zeros((len1 + 1, len2 + 1))
    
    # Initialisation
    for i in range(len1 + 1):
        matrix[i][0] = i
    for j in range(len2 + 1):
        matrix[0][j] = j
    
    # Calcul de la distance
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if seq1[i-1] == seq2[j-1] else tonal_cost(seq1[i-1], seq2[j-1])
            matrix[i][j] = min(
                matrix[i-1][j] + 1,        # Suppression
                matrix[i][j-1] + 1,        # Insertion
                matrix[i-1][j-1] + cost    # Substitution
            )
    
    return matrix[len1][len2]

def tonal_cost(tone1: str, tone2: str) -> float:
    """Coût de substitution basé sur la distance tonale"""
    tonal_hierarchy = {'L': 0, 'M': 1, 'H': 2}
    
    try:
        diff = abs(tonal_hierarchy[tone1] - tonal_hierarchy[tone2])
        return diff / 2.0  # Coût réduit pour substitutions proches
    except KeyError:
        return 1.0  # Coût maximal pour catégories inconnues

def tonal_system_distance(system1: Dict, system2: Dict) -> float:
    """
    Calcule la distance entre deux systèmes tonaux
    Basé sur les règles sandhi et les patrons dominants
    """
    # Similarité des règles sandhi
    sandhi_sim = len(set(system1['sandhi_rules']) & set(system2['sandhi_rules'])) / max(
        len(system1['sandhi_rules']), len(system2['sandhi_rules']), 1
    )
    
    # Similarité des patrons dominants
    pattern_sim = 1.0 if system1['dominant_pattern'] == system2['dominant_pattern'] else 0.5
    
    # Distance globale
    return 1 - (0.7 * sandhi_sim + 0.3 * pattern_sim)