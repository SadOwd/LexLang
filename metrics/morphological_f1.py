from collections import defaultdict
from typing import List, Dict, Tuple

def morphological_f1(predicted: List[Dict], target: List[Dict]) -> Dict[str, float]:
    """
    Calcule le F1-score morphologique par catégorie
    Args:
        predicted: Liste de dicts avec des analyses morphologiques
        target: Liste de dicts avec des analyses de référence
    Returns:
        Dictionnaire des scores par catégorie morphologique
    """
    # Initialiser les compteurs
    true_pos = defaultdict(int)
    false_pos = defaultdict(int)
    false_neg = defaultdict(int)
    
    for pred, ref in zip(predicted, target):
        # Compter pour chaque catégorie morphologique
        for category in ['noun_class', 'tense', 'aspect', 'derivation']:
            pred_val = pred.get(category)
            ref_val = ref.get(category)
            
            if ref_val is not None:
                if pred_val == ref_val:
                    true_pos[category] += 1
                else:
                    false_neg[category] += 1
                    if pred_val is not None:
                        false_pos[category] += 1
            elif pred_val is not None:
                false_pos[category] += 1
    
    # Calculer les scores F1
    scores = {}
    for category in set(true_pos.keys()) | set(false_pos.keys()) | set(false_neg.keys()):
        tp = true_pos.get(category, 0)
        fp = false_pos.get(category, 0)
        fn = false_neg.get(category, 0)
        
        precision = tp / (tp + fp) if tp + fp > 0 else 0
        recall = tp / (tp + fn) if tp + fn > 0 else 0
        
        if precision + recall == 0:
            f1 = 0.0
        else:
            f1 = 2 * (precision * recall) / (precision + recall)
        
        scores[category] = {
            'f1': f1,
            'precision': precision,
            'recall': recall,
            'support': tp + fn
        }
    
    return scores