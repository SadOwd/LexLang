class LexiconManager:
    def __init__(self, main_lexicon="data/lexicons/ewe-french.json"):
        self.lexicon = self.load_lexicon(main_lexicon)
        self.change_log = []
    
    def load_lexicon(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_lexicon(self, path=None):
        path = path or f"data/lexicons/ewe-french_{datetime.now().strftime('%Y%m%d')}.json"
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.lexicon, f, ensure_ascii=False, indent=2)
    
    def add_entry(self, entry):
        """Ajoute une nouvelle entrée au lexique"""
        # Vérification des doublons
        if any(e['ewe'] == entry['ewe'] and e['tones'] == entry['tones'] for e in self.lexicon):
            raise ValueError("Entrée déjà existante")
        
        self.lexicon.append(entry)
        self.log_change("ADD", entry)
    
    def update_entry(self, word, tones, new_data):
        """Met à jour une entrée existante"""
        for entry in self.lexicon:
            if entry['ewe'] == word and entry['tones'] == tones:
                entry.update(new_data)
                self.log_change("UPDATE", {"word": word, "tones": tones, "changes": new_data})
                return
        raise KeyError("Entrée non trouvée")
    
    def log_change(self, action, data):
        """Enregistre les modifications dans le journal"""
        self.change_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "data": data,
            "user": os.getenv("USER")
        })
    
    def find_entries(self, **criteria):
        """Recherche des entrées selon plusieurs critères"""
        results = []
        for entry in self.lexicon:
            match = True
            for key, value in criteria.items():
                if key not in entry or entry[key] != value:
                    match = False
                    break
            if match:
                results.append(entry)
        return results
    
    def generate_report(self):
        """Génère un rapport de maintenance"""
        report = {
            "total_entries": len(self.lexicon),
            "by_pos": Counter(entry['pos'] for entry in self.lexicon),
            "dialect_coverage": self.calculate_dialect_coverage(),
            "recent_changes": self.change_log[-10:]
        }
        return report
    
    def calculate_dialect_coverage(self):
        """Calcule la couverture dialectale"""
        dialects = set()
        for entry in self.lexicon:
            if 'dialects' in entry:
                dialects.update(entry['dialects'].keys())
        return {
            "covered_dialects": list(dialects),
            "coverage_percentage": len(dialects) / 3 * 100  # 3 dialectes principaux
        }

# Exemple d'utilisation
if __name__ == "__main__":
    manager = LexiconManager()
    
    # Ajout d'une nouvelle entrée
    new_entry = {
        "ewe": "gbem",
        "phonetic": "/gbèm/",
        "tones": "LH",
        "pos": "NOUN",
        "french": ["animal"],
        "dialects": {
            "anlo": "gbem",
            "inland": "gem"
        }
    }
    manager.add_entry(new_entry)
    
    # Mise à jour d'une entrée
    manager.update_entry("dzo", "H", {"french": ["aller", "se déplacer"]})
    
    # Sauvegarde
    manager.save_lexicon()
    
    # Génération de rapport
    print(manager.generate_report())