from src.core.pos_tagger.neural_tagger import NeuralTagger

def test_pos_tagger():
    tagger = NeuralTagger(model_path="models/pos/pos_model_v1.2.pkl", config=None)
    tags = tagger.tag(["Ame", "si"], "anlo")
    assert all(len(pair) == 2 for pair in tags)
