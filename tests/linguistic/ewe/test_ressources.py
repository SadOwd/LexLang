import unittest
from src.core.linguistic_loader import LinguisticResourceLoader

class TestLinguisticResources(unittest.TestCase):
    def setUp(self):
        self.loader = LinguisticResourceLoader()
    
    def test_phoneme_loading(self):
        phonemes = self.loader.load_resource('phonemes')
        self.assertGreater(len(phonemes), 20)
        self.assertEqual(phonemes[0]['symbol'], 'a')
    
    def test_tone_rules(self):
        tones = self.loader.load_resource('tones')
        self.assertIn('rising_high_to_low', [r['name'] for r in tones['tone_rules']])
    
    def test_dialect_variants(self):
        anlo_variants = self.loader.get_dialect_variants('anlo')
        self.assertEqual(anlo_variants['lexical_variants']['école'], 'suku')
    
    def test_morphology_stems(self):
        stems = self.loader.load_resource('stems')
        self.assertIn('dze', stems['verbs'])
        self.assertEqual(stems['verbs']['dze']['gloss'], 'manger')

if __name__ == '__main__':
    unittest.main()