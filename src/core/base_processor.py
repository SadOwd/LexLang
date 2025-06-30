"""
Exceptions personnalisées pour LexLang
"""


class LexLangException(Exception):
    """Exception de base pour LexLang"""
    pass


class ConfigurationError(LexLangException):
    """Erreur de configuration"""
    pass


class ModelError(LexLangException):
    """Erreur liée aux modèles"""
    pass


class ModelNotFoundError(ModelError):
    """Modèle non trouvé"""
    pass


class ModelLoadError(ModelError):
    """Erreur lors du chargement d'un modèle"""
    pass


class DataError(LexLangException):
    """Erreur liée aux données"""
    pass


class CorpusError(DataError):
    """Erreur liée au corpus"""
    pass


class LexiconError(DataError):
    """Erreur liée au lexique"""
    pass


class ProcessingError(LexLangException):
    """Erreur de traitement"""
    pass


class TokenizationError(ProcessingError):
    """Erreur de tokenisation"""
    pass


class NormalizationError(ProcessingError):
    """Erreur de normalisation"""
    pass


class POSTaggingError(ProcessingError):
    """Erreur de POS tagging"""
    pass


class TonalProcessingError(ProcessingError):
    """Erreur de traitement tonal"""
    pass


class DialectProcessingError(ProcessingError):
    """Erreur de traitement dialectal"""
    pass


class MorphologicalError(ProcessingError):
    """Erreur d'analyse morphologique"""
    pass


class EmbeddingError(ProcessingError):
    """Erreur liée aux embeddings"""
    pass


class APIError(LexLangException):
    """Erreur de l'API"""
    pass


class AuthenticationError(APIError):
    """Erreur d'authentification"""
    pass


class ValidationError(APIError):
    """Erreur de validation"""
    pass


class RateLimitError(APIError):
    """Erreur de limite de taux"""
    pass


class DatabaseError(LexLangException):
    """Erreur de base de données"""
    pass


class LinguisticError(LexLangException):
    """Erreur linguistique"""
    pass


class UnsupportedDialectError(LinguisticError):
    """Dialecte non supporté"""
    pass


class InvalidToneError(LinguisticError):
    """Ton invalide"""
    pass


class InvalidMorphologyError(LinguisticError):
    """Morphologie invalide"""
    pass


class UnsupportedLanguageError(LinguisticError):
    """Langue non supportée"""
    pass


class MetricsError(LexLangException):
    """Erreur de métriques"""
    pass


class EvaluationError(MetricsError):
    """Erreur d'évaluation"""
    pass


class BenchmarkError(MetricsError):
    """Erreur de benchmark"""
    pass


class DeploymentError(LexLangException):
    """Erreur de déploiement"""
    pass


class ContainerError(DeploymentError):
    """Erreur de conteneur"""
    pass


class NetworkError(LexLangException):
    """Erreur réseau"""
    pass


class TimeoutError(LexLangException):
    """Erreur de timeout"""
    pass


class ResourceError(LexLangException):
    """Erreur de ressource"""
    pass


class MemoryError(ResourceError):
    """Erreur de mémoire"""
    pass


class DiskSpaceError(ResourceError):
    """Erreur d'espace disque"""
    pass


def handle_exception(func):
    """Décorateur pour gérer les exceptions"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except LexLangException:
            # Re-raise les exceptions LexLang
            raise
        except FileNotFoundError as e:
            raise DataError(f"Fichier non trouvé: {e}")
        except PermissionError as e:
            raise DataError(f"Permission refusée: {e}")
        except ValueError as e:
            raise ValidationError(f"Valeur invalide: {e}")
        except KeyError as e:
            raise ConfigurationError(f"Clé manquante: {e}")
        except Exception as e:
            raise LexLangException(f"Erreur inattendue: {e}")
    
    return wrapper


class ErrorHandler:
    """Gestionnaire d'erreurs centralisé"""
    
    @staticmethod
    def log_error(error: Exception, context: str = None):
        """Log une erreur avec contexte"""
        import logging
        logger = logging.getLogger(__name__)
        
        error_msg = f"Erreur: {error}"
        if context:
            error_msg = f"{context} - {error_msg}"
            
        logger.error(error_msg, exc_info=True)
    
    @staticmethod
    def format_error_response(error: Exception) -> dict:
        """Formate une erreur pour la réponse API"""
        error_type = type(error).__name__
        error_message = str(error)
        
        return {
            "error": {
                "type": error_type,
                "message": error_message,
                "timestamp": __import__('datetime').datetime.now().isoformat()
            }
        }
    
    @staticmethod
    def is_retriable_error(error: Exception) -> bool:
        """Détermine si une erreur peut être retentée"""
        retriable_errors = (
            NetworkError,
            TimeoutError,
            DatabaseError,
            ResourceError
        )
        return isinstance(error, retriable_errors)