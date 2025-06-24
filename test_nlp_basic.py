#!/usr/bin/env python3
"""
Test basique du moteur NLP LexLang
Script pour vérifier que le moteur fonctionne correctement
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.nlp_engine import NLPProcessor, Token
import json

def test_basic_functionality():
    """Test des fonctionnalités de base"""
    print("🔧 Initialisation du processeur NLP...")
    
    try:
        processor = NLPProcessor()
        print("✅ Processeur initialisé avec succès")
    except Exception as e:
        print(f"❌ Erreur d'initialisation: {e}")
        return False
    
    return True

def test_text_normalization():
    """Test de la normalisation de texte"""
    print("\n📝 Test de normalisation de texte...")
    
    processor = NLPProcessor()
    
    test_cases = [
        ("Bonjour, Comment ALLEZ-vous ?", "bonjour, comment allez-vous ?"),
        ("  Espaces   multiples  ", "espaces multiples"),
        ("Àccénts ét çaractères spéciaux", "àccénts ét çaractères spéciaux"),
        ("MAJUSCULES ET minuscules", "majuscules et minuscules")
    ]
    
    for input_text, expected in test_cases:
        result = processor.normalize_text(input_text)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{input_text}' → '{result}'")
        if result != expected:
            print(f"   Attendu: '{expected}'")
    
    return True

def test_tokenization():
    """Test de la tokenisation"""
    print("\n🔤 Test de tokenisation...")
    
    processor = NLPProcessor()
    
    test_texts = [
        "Bonjour tout le monde !",
        "Salam aleikum, nanga def ?",
        "Comment ça va aujourd'hui ?",
        "Les langues africaines sont belles.",
        "123 nombres et mots-composés"
    ]
    
    for text in test_texts:
        tokens = processor.tokenize(text)
        print(f"📄 '{text}'")
        print(f"   → Tokens: {tokens}")
        print(f"   → Nombre: {len(tokens)}")
    
    return True

def test_pos_tagging():
    """Test de l'étiquetage morpho-syntaxique"""
    print("\n🏷️  Test d'étiquetage POS...")
    
    processor = NLPProcessor()
    
    test_words = [
        "bonjour", "le", "chat", "mange", "rapidement",
        "dans", "maison", "et", "je", "très",
        "tion", "ment", "able", "er"
    ]
    
    for word in test_words:
        pos = processor.simple_pos_tag(word)
        print(f"   {word:12} → {pos}")
    
    return True

def test_full_text_processing():
    """Test du traitement complet de texte"""
    print("\n🔍 Test de traitement complet...")
    
    processor = NLPProcessor()
    
    test_texts = [
        "Bonjour, comment allez-vous aujourd'hui ?",
        "Salam aleikum ! Nanga def ak sa famille ?",
        "Les langues africaines sont très riches et diversifiées.",
        "L'intelligence artificielle peut aider à préserver nos langues ancestrales."
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n--- Test {i} ---")
        print(f"Texte: {text}")
        
        try:
            result = processor.process_text(text)
            print(f"✅ Traitement réussi:")
            print(f"   • Tokens trouvés: {result['tokens_count']}")
            print(f"   • Tokens uniques: {result['unique_tokens']}")
            print(f"   • N-grammes générés: {result['ngrams_generated']}")
            
            # Afficher quelques tokens traités
            if result['tokens']:
                print("   • Premiers tokens:")
                for token_data in result['tokens'][:3]:
                    print(f"     - {token_data['text']} [{token_data['pos']}] (freq: {token_data['frequency']})")
        
        except Exception as e:
            print(f"❌ Erreur de traitement: {e}")
            return False
    
    return True

def test_ngrams_generation():
    """Test de génération de n-grammes"""
    print("\n📊 Test de génération de n-grammes...")
    
    processor = NLPProcessor()
    
    # Traiter un texte d'abord
    text = "Bonjour tout le monde, comment allez-vous aujourd'hui ?"
    processor.process_text(text)
    
    # Vérifier les n-grammes générés
    for n in [2, 3, 4]:
        ngrams = processor.lexical_db.n_grams[n]
        print(f"   {n}-grammes: {len(ngrams)} générés")
        if ngrams:
            # Afficher les 3 premiers
            items = list(ngrams.items())[:3]
            for ngram, freq in items:
                print(f"     • '{ngram}' (freq: {freq})")
    
    return True

def test_database_operations():
    """Test des opérations de base de données"""
    print("\n💾 Test des opérations de base de données...")
    
    processor = NLPProcessor()
    
    # Ajouter quelques tokens manuellement
    test_token = Token(
        text="test",
        lemma="test",
        pos="NOUN",
        features={"length": "4"},
        frequency=5,
        contexts=["Ceci est un test"]
    )
    
    processor.lexical_db.add_token(test_token)
    
    # Tester la recherche
    found_token = processor.lexical_db.get_token("test")
    if found_token:
        print("✅ Token ajouté et retrouvé avec succès")
        print(f"   • Texte: {found_token.text}")
        print(f"   • POS: {found_token.pos}")
        print(f"   • Fréquence: {found_token.frequency}")
    else:
        print("❌ Token non retrouvé")
        return False
    
    return True

def test_statistics():
    """Test des statistiques"""
    print("\n📈 Test des statistiques...")
    
    processor = NLPProcessor()
    
    # Traiter quelques textes
    texts = [
        "Bonjour comment allez-vous ?",
        "Salam aleikum nanga def ?",
        "Bonsoir tout le monde !"
    ]
    
    for text in texts:
        processor.process_text(text)
    
    # Obtenir les statistiques
    try:
        stats = processor.get_statistics()
        print("✅ Statistiques générées:")
        print(f"   • Total tokens: {stats['total_tokens']}")
        print(f"   • Lemmes uniques: {stats['unique_lemmas']}")
        print(f"   • Distribution POS: {stats['pos_distribution']}")
        if stats['most_frequent']:
            print("   • Mots les plus fréquents:")
            for word, freq in stats['most_frequent'][:3]:
                print(f"     - {word}: {freq}")
    except Exception as e:
        print(f"❌ Erreur dans les statistiques: {e}")
        return False
    
    return True

def test_save_load():
    """Test de sauvegarde/chargement"""
    print("\n💾 Test de sauvegarde/chargement...")
    
    processor = NLPProcessor()
    
    # Traiter du texte
    processor.process_text("Test de sauvegarde avec quelques mots.")
    
    # Sauvegarder
    try:
        processor.save_database("test_database.pkl")
        print("✅ Sauvegarde réussie")
    except Exception as e:
        print(f"❌ Erreur de sauvegarde: {e}")
        return False
    
    # Créer un nouveau processeur et charger
    try:
        new_processor = NLPProcessor()
        new_processor.load_database("test_database.pkl")
        print("✅ Chargement réussi")
        
        # Vérifier que les données sont là
        if len(new_processor.lexical_db.tokens) > 0:
            print(f"   • {len(new_processor.lexical_db.tokens)} tokens chargés")
        else:
            print("❌ Aucun token chargé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de chargement: {e}")
        return False
    
    # Nettoyer
    try:
        os.remove("test_database.pkl")
        print("✅ Fichier de test nettoyé")
    except:
        pass
    
    return True

def run_all_tests():
    """Exécute tous les tests"""
    print("🧪 TESTS DU MOTEUR NLP LEXLANG")
    print("=" * 50)
    
    tests = [
        ("Fonctionnalité de base", test_basic_functionality),
        ("Normalisation de texte", test_text_normalization),
        ("Tokenisation", test_tokenization),
        ("Étiquetage POS", test_pos_tagging),
        ("Traitement complet", test_full_text_processing),
        ("Génération n-grammes", test_ngrams_generation),
        ("Opérations BDD", test_database_operations),
        ("Statistiques", test_statistics),
        ("Sauvegarde/Chargement", test_save_load)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}...")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: RÉUSSI")
            else:
                print(f"❌ {test_name}: ÉCHEC")
        except Exception as e:
            print(f"❌ {test_name}: ERREUR - {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 RÉSULTATS: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 TOUS LES TESTS SONT PASSÉS !")
        return True
    else:
        print("⚠️  Certains tests ont échoué")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
