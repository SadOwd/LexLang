# tests/linguistic/ewe/tonal/test_sandhi.py
def test_complex_sandhi_rules():
    processor = EweTonalProcessor()
    
    # Test règle: ton montant + ton haut → ton bas
    assert processor.apply("vă") == "và"  # Impératif
    
    # Test règle: ton descendant + ton bas → ton haut
    assert processor.apply("nê ò") == "né ò"
    
    # Test exception lexicale
    assert processor.apply("akpé") == "akpé"  # Non modifié

# tests/linguistic/ewe/dialects/test_badou_adapter.py
def test_badou_adaptation():
    adapter = EweDialectAdapter('badou')
    assert adapter.adapt("ananas") == "ababil"
    assert adapter.adapt("école") == "sukû"