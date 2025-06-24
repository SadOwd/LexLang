"""
LexLang - Gestionnaire de données
Module pour l'import/export et la gestion des données lexicales
Priorité: ÉLEVÉE - Gestion des données cruciale
"""

import json
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
import sqlite3
from typing import Dict, List, Optional, Union, Iterator
import logging
from datetime import datetime
import pandas as pd
import zipfile
import requests
from io import StringIO

from nlp_engine import NLPProcessor, Token, LexicalDatabase

logger = logging.getLogger(__name__)


class DataManager:
    """Gestionnaire pour l'import/export de données lexicales"""
    
    def __init__(self, nlp_processor: NLPProcessor):
        self.nlp_processor = nlp_processor
        self.supported_formats = ['json', 'csv', 'xml', 'txt', 'conllu', 'sqlite']
        
    def export_to_json(self, filepath: str, include_contexts: bool = False) -> bool:
        """Exporte la base lexicale en JSON"""
        try:
            export_data = {
                "metadata": {
                    "export_date": datetime.now().isoformat(),
                    "version": "1.0.0",
                    "total_tokens": len(self.nlp_processor.lexical_db.tokens),
                    "format": "LexLang JSON v1"
                },
                "tokens": [],
                "ngrams": self.nlp_processor.lexical_db.n_grams,
                "statistics": self.nlp_processor.get_statistics()
            }
            
            # Export des tokens
            for token in self.nlp_processor.lexical_db.tokens.values():
                token_data = {
                    "text": token.text,
                    "lemma": token.lemma,
                    "pos": token.pos,
                    "frequency": token.frequency,
                    "features": token.features
                }
                
                if include_contexts:
                    token_data["contexts"] = token.contexts
                
                export_data["tokens"].append(token_data)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Export JSON réussi: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'export JSON: {e}")
            return False
    
    def import_from_json(self, filepath: str) -> bool:
        """Importe une base lexicale depuis JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Vérification du format
            if "tokens" not in data:
                logger.error("Format JSON invalide: champ 'tokens' manquant")
                return False
            
            imported_count = 0
            for token_data in data["tokens"]:
                try