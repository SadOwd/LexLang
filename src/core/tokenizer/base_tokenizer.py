"""BaseTokenizer: classe de base pour tokeniseurs."""
from abc import ABC, abstractmethod
from ..base_processor import BaseProcessor

class BaseTokenizer(BaseProcessor, ABC):
    """Interface pour tokenisation."""
    
    @abstractmethod
    def tokenize(self, text: str, dialect: str) -> list:
        """Retourne la liste des tokens."""
        pass
