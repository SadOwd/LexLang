# scripts/data_processing/rongier_importer.py
class RongierImporter:
    def parse_entry(self, entry: dict) -> dict:
        """Structure une entrée du dictionnaire pour LexLang"""
        return {
            'lemma': entry['headword'],
            'pos': entry['pos'],
            'phonetic': entry['pronunciation'],
            'gloss_fr': entry['definition'],
            'examples': entry.get('examples', []),
            'morph_decomposition': self.parse_etymology(entry['etymology']),
            'tonal_pattern': self.extract_tones(entry['pronunciation']),
            'dialect_variants': {
                'badou': entry.get('badou_variant'),
                'inland': entry.get('inland_variant')
            }
        }
    
    def import_to_lexicon(self, entries: list[dict]):
        for entry in entries:
            structured = self.parse_entry(entry)
            self.save_to_database(structured)