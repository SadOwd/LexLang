from src.core.tokenizer.word_tokenizer import WordTokenizer

def test_basic_tokenization():
    tokenizer = WordTokenizer(config=None)
    tokens = tokenizer.tokenize("Ame si le afi ma.", "anlo")
    assert tokens == ["Ame", "si", "le", "afi", "ma", "."]
