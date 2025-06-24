"""
LexLang - API REST pour la base lexicale publique
Interface web pour accéder aux fonctionnalités NLP
Priorité: ÉLEVÉE - Interface publique principale
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
from datetime import datetime
import logging
from typing import Dict, List, Optional
import os

from nlp_engine import NLPProcessor, Token

app = Flask(__name__)
CORS(app)

# Configuration du rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('lexlang_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Instance globale du processeur NLP
nlp_processor = NLPProcessor()

# Chargement de la base existante si elle existe
DATABASE_PATH = 'lexlang_database.pkl'
if os.path.exists(DATABASE_PATH):
    try:
        nlp_processor.load_database(DATABASE_PATH)
        logger.info("Base de données lexicale chargée avec succès")
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la base: {e}")

@app.route('/')
def home():
    """Page d'accueil avec documentation API"""
    return jsonify({
        "name": "LexLang API",
        "version": "1.0.0",
        "description": "API publique pour base lexicale multilingue (Français + Langues Africaines)",
        "endpoints": {
            "/analyze": "POST - Analyse un texte et extrait les informations lexicales",
            "/search": "GET - Recherche dans la base lexicale",
            "/stats": "GET - Statistiques de la base lexicale",
            "/ngrams": "GET - Récupère les n-grammes les plus fréquents",
            "/token/<word>": "GET - Informations détaillées sur un token",
            "/contribute": "POST - Contribue du nouveau contenu à la base"
        },
        "languages_supported": ["French", "Wolof", "Bambara", "Lingala", "Swahili"],
        "total_tokens": len(nlp_processor.lexical_db.tokens)
    })

@app.route('/analyze', methods=['POST'])
@limiter.limit("10 per minute")
def analyze_text():
    """Analyse un texte et retourne les informations lexicales"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Le champ 'text' est requis"}), 400
        
        text = data['text']
        if len(text) > 5000:  # Limite de longueur
            return jsonify({"error": "Texte trop long (max 5000 caractères)"}), 400
        
        # Traitement du texte
        result = nlp_processor.process_text(text)
        
        # Sauvegarde automatique après traitement
        nlp_processor.save_database(DATABASE_PATH)
        
        # Log de l'activité
        logger.info(f"Texte analysé: {len(text)} caractères, {result['tokens_count']} tokens")
        
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "analysis": result,
            "metadata": {
                "text_length": len(text),
                "processing_time": "< 1s"
            }
        })
    
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {e}")
        return jsonify({"error": "Erreur interne du serveur"}), 500

@app.route('/search', methods=['GET'])
@limiter.limit("30 per minute")
def search_tokens():
    """Recherche dans la base lexicale"""
    try:
        # Paramètres de recherche
        query = request.args.get('q', '').strip()
        search_type = request.args.get('type', 'text')  # text, lemma, pos
        limit = min(int(request.args.get('limit', 50)), 100)
        
        if not query:
            return jsonify({"error": "Paramètre 'q' requis"}), 400
        
        results = []
        
        if search_type == 'text':
            # Recherche par texte (correspondance partielle)
            for token_key, token in nlp_processor.lexical_db.tokens.items():
                if query.lower() in token_key:
                    results.append({
                        "text": token.text,
                        "lemma": token.lemma,
                        "pos": token.pos,
                        "frequency": token.frequency,
                        "features": token.features
                    })
                    if len(results) >= limit:
                        break
        
        elif search_type == 'lemma':
            # Recherche par lemme
            tokens = nlp_processor.lexical_db.search_by_lemma(query.lower())
            for token in tokens[:limit]:
                results.append({
                    "text": token.text,
                    "lemma": token.lemma,
                    "pos": token.pos,
                    "frequency": token.frequency,
                    "features": token.features
                })
        
        elif search_type == 'pos':
            # Recherche par catégorie grammaticale
            tokens = nlp_processor.lexical_db.search_by_pos(query.upper())
            for token in tokens[:limit]:
                results.append({
                    "text": token.text,
                    "lemma": token.lemma,
                    "pos": token.pos,
                    "frequency": token.frequency,
                    "features": token.features
                })
        
        return jsonify({
            "status": "success",
            "query": query,
            "search_type": search_type,
            "results_count": len(results),
            "results": results
        })
    
    except Exception as e:
        logger.error(f"Erreur lors de la recherche: {e}")
        return jsonify({"error": "Erreur interne du serveur"}), 500

@app.route('/stats', methods=['GET'])
def get_statistics():
    """Retourne les statistiques de la base lexicale"""
    try:
        stats = nlp_processor.get_statistics()
        
        # Ajout d'informations supplémentaires
        extended_stats = {
            **stats,
            "database_info": {
                "last_updated": datetime.now().isoformat(),
                "version": "1.0.0",
                "languages": ["fr", "wo", "bm", "ln", "sw"]
            },
            "api_info": {
                "total_requests_today": "N/A",  # À implémenter avec Redis/DB
                "active_users": "N/A"
            }
        }
        
        return jsonify({
            "status": "success",
            "statistics": extended_stats
        })
    
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des stats: {e}")
        return jsonify({"error": "Erreur interne du serveur"}), 500

@app.route('/ngrams', methods=['GET'])
def get_ngrams():
    """Retourne les n-grammes les plus fréquents"""
    try:
        n = int(request.args.get('n', 2))
        limit = min(int(request.args.get('limit', 20)), 100)
        
        if n not in [2, 3, 4]:
            return jsonify({"error": "n doit être 2, 3 ou 4"}), 400
        
        ngrams = nlp_processor.lexical_db.n_grams[n]
        
        # Tri par fréquence
        sorted_ngrams = sorted(
            ngrams.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        return jsonify({
            "status": "success",
            "n": n,
            "total_ngrams": len(ngrams),
            "top_ngrams": [
                {"ngram": ngram, "frequency": freq}
                for ngram, freq in sorted_ngrams
            ]
        })
    
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des n-grammes: {e}")
        return jsonify({"error": "Erreur interne du serveur"}), 500

@app.route('/token/<word>', methods=['GET'])
def get_token_info(word):
    """Informations détaillées sur un token spécifique"""
    try:
        token = nlp_processor.lexical_db.get_token(word)
        
        if not token:
            return jsonify({"error": "Token non trouvé"}), 404
        
        # Recherche de tokens similaires
        similar_tokens = []
        for token_key, other_token in nlp_processor.lexical_db.tokens.items():
            if (other_token.lemma == token.lemma and 
                other_token.text != token.text):
                similar_tokens.append({
                    "text": other_token.text,
                    "frequency": other_token.frequency
                })
        
        return jsonify({
            "status": "success",
            "token": {
                "text": token.text,
                "lemma": token.lemma,
                "pos": token.pos,
                "frequency": token.frequency,
                "features": token.features,
                "contexts": token.contexts[:5]  # Limite les contextes
            },
            "similar_tokens": similar_tokens[:10],
            "metadata": {
                "first_seen": "N/A",  # À implémenter
                "last_updated": datetime.now().isoformat()
            }
        })
    
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du token: {e}")
        return jsonify({"error": "Erreur interne du serveur"}), 500

@app.route('/contribute', methods=['POST'])
@limiter.limit("5 per minute")
def contribute_content():
    """Permet aux utilisateurs de contribuer du contenu"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Le champ 'text' est requis"}), 400
        
        text = data['text']
        language = data.get('language', 'unknown')
        source = data.get('source', 'user_contribution')
        
        if len(text) > 1000:  # Limite pour les contributions
            return jsonify({"error": "Contribution trop longue (max 1000 caractères)"}), 400
        
        # Traitement du texte contribué
        result = nlp_processor.process_text(text)
        
        # Sauvegarde
        nlp_processor.save_database(DATABASE_PATH)
        
        # Log de la contribution
        logger.info(f"Nouvelle contribution: {len(text)} caractères, langue: {language}")
        
        return jsonify({
            "status": "success",
            "message": "Merci pour votre contribution !",
            "tokens_added": result['tokens_count'],
            "unique_tokens": result['unique_tokens']
        })
    
    except Exception as e:
        logger.error(f"Erreur lors de la contribution: {e}")
        return jsonify({"error": "Erreur interne du serveur"}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"error": "Limite de taux dépassée", "retry_after": str(e.retry_after)}), 429

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint non trouvé"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Erreur interne du serveur"}), 500

if __name__ == '__main__':
    # Chargement de données d'exemple au démarrage
    sample_texts = [
        "Bonjour tout le monde, comment allez-vous aujourd'hui ?",
        "Salam aleikum, nanga def ? Ça va bien ak sa famille ?",
        "Mbote mingi, lokola nini ? Famille ya yo ezali malamu ?",
        "Les langues africaines sont très riches et diversifiées.",
        "L'intelligence artificielle peut aider à préserver nos langues."
    ]
    
    for text in sample_texts:
        nlp_processor.process_text(text)
    
    nlp_processor.save_database(DATABASE_PATH)
    logger.info("Base de données initialisée avec des exemples")
    
    # Démarrage du serveur
    app.run(host='0.0.0.0', port=5000, debug=False)
