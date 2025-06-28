"""Custom exceptions for LexLang."""


class LexLangError(Exception):
    """Base exception for LexLang."""
    pass


class ConfigurationError(LexLangError):
    """Configuration related errors."""
    pass


class ModelLoadError(LexLangError):
    """Model loading errors."""
    pass


class ProcessingError(LexLangError):
    """Text processing errors."""
    pass


class TokenizationError(ProcessingError):
    """Tokenization specific errors."""
    pass


class NormalizationError(ProcessingError):
    """Normalization specific errors."""
    pass


class POSTaggingError(ProcessingError):
    """POS tagging specific errors."""
    pass


class TonalProcessingError(ProcessingError):
    """Tonal processing specific errors."""
    pass


class DialectDetectionError(ProcessingError):
    """Dialect detection specific errors."""
    pass


class MorphologyError(ProcessingError):
    """Morphological analysis errors."""
    pass


class EmbeddingError(LexLangError):
    """Word embedding related errors."""
    pass


class DataError(LexLangError):
    """Data loading/processing errors."""
    pass


class ValidationError(LexLangError):
    """Data validation errors."""
    pass


class APIError(LexLangError):
    """API related errors."""
    pass


class AuthenticationError(APIError):
    """Authentication errors."""
    pass


class RateLimitError(APIError):
    """Rate limiting errors."""
    pass


class TrainingError(LexLangError):
    """Model training errors."""
    pass


class EvaluationError(LexLangError):
    """Model evaluation errors."""
    pass
