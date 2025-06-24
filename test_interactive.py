#!/usr/bin/env python3
"""
Test interactif du moteur NLP LexLang
Interface en ligne de commande pour tester manuellement
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.nlp_engine import NLPProcessor
import json
from datetime import datetime

class InteractiveNLPTester:
    """Testeur interactif pour le moteur NLP"""
    
    def __init__(self):
        print("🚀 Initialisation du testeur interactif LexLang...")
        try:
            self.processor = NLPProcessor()
            print("✅ Processeur NLP initialisé avec succès!\n")
        except Exception as e:
            print(f"❌ Erreur d'initialisation: {e}")
            sys.exit(1)
    
    def show_menu(self):
        """Affiche le menu principal"""
        print("=" * 60)
        print("🧪 TESTEUR INTERACTIF LEXLANG - MOTEUR NLP")
        print("=" * 60)
        print("1️⃣  Analyser un texte")
        print("2️⃣  Rechercher un token")
        print("3️⃣  Voir les statistiques")
        print("4️⃣  Tester la tokenisation")
        print("5️⃣  Voir les n-grammes")
        print("6️⃣  Tests prédéfinis")
        print("7️⃣  Sauvegarder la base")
        print("8️⃣  Charger une base")
        print("9️⃣  Export JSON")
        print("0️⃣  Quitter")
        print("-" * 60)
    
    def analyze_text(self):
        """Interface pour analyser un texte"""
        print("\n📝 ANALYSE DE TEXTE")
        print("-" * 30)
        
        text = input("Entrez votre texte à analyser:\n> ")
        
        if not text.strip():
            print("❌ Texte vide!")
            return
        
        print(f"\n🔍 Analyse en cours de: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        
        try:
            result = self.processor.process_text(text)
            
            print("✅ Analyse terminée!")
            print(f"📊 Résultats:")
            print(f"   • Tokens trouvés: {result['tokens_count']}")
            print(f"   • Tokens uniques: {result['unique_tokens']}")
            print(f"   • N-grammes générés: {result['ngrams_generated']}")
            
            # Détails des tokens
            if result['tokens']:
                print(f"\n🏷️  Détail des tokens:")
                for i, token_data in enumerate(result['tokens'][:10], 1):
                    print(f"   {i:2}. {token_data['text']:15} [{token_data['pos']:4}] "
                          f"freq:{token_data['frequency']} features:{len(token_data['features'])}")
                
                if len(result['tokens']) > 10:
                    print(f"   ... et {len(result['tokens']) - 10} autres tokens")
        
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse: {e}")
    
    def search_token(self):
        """Interface pour rechercher un token"""
        print("\n🔍 RECHERCHE DE TOKEN")
        print("-" * 30)
        
        word = input("Entrez le mot à rechercher: ").strip()
        
        if not word:
            print("❌ Mot vide!")
            return
        
        token = self.processor.lexical_db.get_token(word)
        
        if token:
            print("✅ Token trouvé!")
            print(f"   • Texte: {token.text}")
            print(f"   • Lemme: {token.lemma}")
            print(f"   • POS: {token.pos}")
            print(f"   • Fréquence: {token.frequency}")
            print(f"   • Caractéristiques: {token.features}")
            if token.contexts:
                print(f"   • Contextes ({len(token.contexts)}):")
                for i, context in enumerate(token.contexts[:3], 1):
                    print(f"     {i}. {context[:60]}{'...' if len(context) > 60 else ''}")
        else:
            print("❌ Token non trouvé dans la base")
            
            # Suggestions
            similar = []
            for token_key in self.processor.lexical_db.tokens.keys():
                if word.lower() in token_key or token_key in word.lower():
                    similar.append(token_key)
            
            if similar:
                print(f"💡 Suggestions similaires: {', '.join(similar[:5])}")
    
    def show_statistics(self):
        """Affiche les statistiques de la base"""
        print("\n📈 STATISTIQUES DE LA BASE LEXICALE")
        print("-" * 40)
        
        try:
            stats = self.processor.get_statistics()
            
            print(f"📊 Statistiques générales:")
            print(f"   • Total des tokens: {stats['total_tokens']}")
            print(f"   • Lemmes uniques: {stats['unique_lemmas']}")
            
            print(f"\n🏷️  Distribution POS:")
            for pos, count in sorted(stats['pos_distribution'].items()):
                print(f"   • {pos:6}: {count:4} tokens")
            
            print(f"\n🔥 Mots les plus fréquents:")
            for i, (word, freq) in enumerate(stats['most_frequent'], 1):
                print(f"   {i:2}. {word:15} (fréquence: {freq})")
            
            # Statistiques n-grammes
            print(f"\n📝 N-grammes:")
            for n in [2, 3, 4]:
                count = len(self.processor.lexical_db.n_grams[n])
                print(f"   • {n}-grammes: {count}")
        
        except Exception as e:
            print(f"❌ Erreur lors du calcul des statistiques: {e}")
    
    def test_tokenization(self):
        """Interface pour tester la tokenisation"""
        print("\n🔤 TEST DE TOKENISATION")
        print("-" * 30)
        
        text = input("Entrez le texte à tokeniser:\n> ")
        
        if not text.strip():
            print("❌ Texte vide!")
            return
        
        try:
            # Test de normalisation
            normalized = self.processor.normalize_text(text)
            print(f"📝 Texte normalisé: '{normalized}'")
            
            # Test de tokenisation
            tokens = self.processor.tokenize(text)
            print(f"🔤 Tokens ({len(tokens)}):")
            for i, token in enumerate(tokens, 1):
                pos = self.processor.simple_pos_tag(token)
                print(f"   {i:2}. '{token}' [{pos}]")
        
        except Exception as e:
            print(f"❌ Erreur lors de la tokenisation: {e}")
    
    def show_ngrams(self):
        """Affiche les n-grammes les plus fréquents"""
        print("\n📊 N-GRAMMES LES PLUS FRÉQUENTS")
        print("-" * 35)
        
        try:
            n = int(input("Entrez n (2, 3, ou 4): "))
            if n not in [2, 3, 4]:
                print("❌ n doit être 2, 3 ou 4!")
                return
        except ValueError:
            print("❌ Veuillez entrer un nombre valide!")
            return
        
        ngrams = self.processor.lexical_db.n_grams[n]
        
        if not ngrams:
            print(f"❌ Aucun {n}-gramme trouvé. Analysez d'abord du texte!")
            return
        
        # Tri par fréquence
        sorted_ngrams = sorted(ngrams.items(), key=lambda x: x[1], reverse=True)
        
        print(f"🔥 Top {n}-grammes (max 15):")
        for i, (ngram, freq) in enumerate(sorted_ngrams[:15], 1):
            print(f"   {i:2}. '{ngram}' (fréquence: {freq})")
    
    def predefined_tests(self):
        """Lance des tests prédéfinis"""
        print("\n🧪 TESTS PRÉDÉFINIS")
        print("-" * 25)
        
        test_texts = [
            ("Français simple", "Bonjour, comment allez-vous aujourd'hui ?"),
            ("Français + Wolof", "Salam aleikum ! Nanga def ak sa famille ?"),
            ("Texte technique", "L'intelligence artificielle transforme le traitement des langues naturelles."),
            ("Ponctuation", "Wow ! C'est incroyable... Vraiment ? Oui, absolument !"),
            ("Mélange langues", "Hello, bonjour, salam ! Comment ça va today ?")
        ]
        
        for i, (name, text) in enumerate(test_texts, 1):
            print(f"\n--- Test {i}: {name} ---")
            print(f"Texte: {text}")
            
            try:
                result = self.processor.process_text(text)
                print(f"✅ {result['tokens_count']} tokens, {result['unique_tokens']} uniques")
            except Exception as e:
                print(f"❌ Erreur: {e}")
        
        print(f"\n📊 Statistiques après tests:")
        self.show_statistics()
    
    def save_database(self):
        """Sauvegarde la base de données"""
        print("\n💾 SAUVEGARDE DE LA BASE")
        print("-" * 30)
        
        filename = input("Nom du fichier (avec .pkl): ").strip()
        if not filename:
            filename = f"lexlang_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
        
        try:
            self.processor.save_database(filename)
            print(f"✅ Base sauvegardée dans: {filename}")
        except Exception as e:
            print(f"❌ Erreur de sauvegarde: {e}")
    
    def load_database(self):
        """Charge une base de données"""
        print("\n📂 CHARGEMENT DE BASE")
        print("-" * 25)
        
        filename = input("Nom du fichier à charger: ").strip()
        if not filename:
            print("❌ Nom de fichier requis!")
            return
        
        try:
            self.processor.load_database(filename)
            print(f"✅ Base chargée depuis: {filename}")
            print(f"📊 {len(self.processor.lexical_db.tokens)} tokens chargés")
        except Exception as e:
            print(f"❌ Erreur de chargement: {e}")
    
    def export_json(self):
        """Exporte la base en JSON"""
        print("\n📤 EXPORT JSON")
        print("-" * 20)
        
        filename = input("Nom du fichier JSON: ").strip()
        if not filename:
            filename = f"lexlang_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        try:
            # Export simple en JSON
            export_data = {
                "export_info": {
                    "date": datetime.now().isoformat(),
                    "total_tokens": len(self.processor.lexical_db.tokens)
                },
                "tokens": []
            }
            
            for token in self.processor.lexical_db.tokens.values():
                export_data["tokens"].append({
                    "text": token.text,
                    "lemma": token.lemma,
                    "pos": token.pos,
                    "frequency": token.frequency,
                    "features": token.features
                })
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Export JSON réussi: {filename}")
            print(f"📊 {len(export_data['tokens'])} tokens exportés")
        
        except Exception as e:
            print(f"❌ Erreur d'export: {e}")
    
    def run(self):
        """Lance l'interface interactive"""
        while True:
            self.show_menu()
            
            try:
                choice = input("Votre choix: ").strip()
                
                if choice == '1':
                    self.analyze_text()
                elif choice == '2':
                    self.search_token()
                elif choice == '3':
                    self.show_statistics()
                elif choice == '4':
                    self.test_tokenization()
                elif choice == '5':
                    self.show_ngrams()
                elif choice == '6':
                    self.predefined_tests()
                elif choice == '7':
                    self.save_database()
                elif choice == '8':
                    self.load_database()
                elif choice == '9':
                    self.export_json()
                elif choice == '0':
                    print("\n👋 Au revoir!")
                    break
                else:
                    print("❌ Choix invalide!")
                
                input("\n⏸️  Appuyez sur Entrée pour continuer...")
            
            except KeyboardInterrupt:
                print("\n\n👋 Au revoir!")
                break
            except Exception as e:
                print(f"❌ Erreur inattendue: {e}")
                input("\n⏸️  Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    tester = InteractiveNLPTester()
    tester.run()
