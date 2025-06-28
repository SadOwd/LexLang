"""BaseProcessor: classe de base pour tous les processeurs."""
from abc import ABC, abstractmethod
from ..config import LexLangConfig

class BaseProcessor(ABC):
    """Interface commune pour les processeurs."""

    def __init__(self, config: LexLangConfig):
        self.config = config

    @abstractmethod
    def process(self, *args, **kwargs):
        """Méthode principale de traitement."""
        pass
