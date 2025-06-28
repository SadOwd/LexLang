"""NeuralTagger: étiquetage POS par réseau de neurones."""
from ..base_processor import BaseProcessor
import torch

class NeuralTagger(BaseProcessor):
    """Réseau neuronal pour POS tagging."""

    def __init__(self, model_path: str, config):
        super().__init__(config)
        # Chargement du modèle PyTorch
        self.model = torch.load(model_path, map_location='cpu')
        self.model.eval()

    def tag(self, tokens: list, dialect: str) -> list:
        # TODO: préparer batch, encoder, passer dans self.model
        tags = ['ADJ' for _ in tokens]
        return list(zip(tokens, tags))
