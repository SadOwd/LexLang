"""Utility functions for LexLang."""

import logging
import logging.handlers
import os
import json
import pickle
import hashlib
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from functools import wraps
import numpy as np


def setup_logging(level: Union[str, int] = logging.INFO, 
                 log_file: Optional[str] = None,
                 format_string: Optional[str] = None) -> None:
    """Setup logging configuration."""
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Create formatter
    formatter = logging.Formatter(format_string)
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10485760, backupCount=5
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def load_json(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Load JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading JSON file {file_path}: {e}")
        raise


def save_json(data: Dict[str, Any], file_path: Union[str, Path]) -> None:
    """Save data to JSON file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"Error saving JSON file {file_path}: {e}")
        raise


def load_pickle(file_path: Union[str, Path]) -> Any:
    """Load pickle file."""
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        logging.error(f"Error loading pickle file {file_path}: {e}")
        raise


def save_pickle(data: Any, file_path: Union[str, Path]) -> None:
    """Save data to pickle file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
    except Exception as e:
        logging.error(f"Error saving pickle file {file_path}: {e}")
        raise


def ensure_dir(dir_path: Union[str, Path]) -> None:
    """Ensure directory exists."""
    os.makedirs(dir_path, exist_ok=True)


def get_file_hash(file_path: Union[str, Path]) -> str:
    """Get MD5 hash of file."""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        logging.error(f"Error computing hash for {file_path}: {e}")
        raise


def timing_decorator(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logging.debug(f"{func.__name__} executed in {execution_time:.4f} seconds")
        return result
    return wrapper


def batch_iterator(iterable: List[Any], batch_size: int):
    """Create batches from iterable."""
    for i in range(0, len(iterable), batch_size):
        yield iterable[i:i + batch_size]


def flatten_list(nested_list: List[List[Any]]) -> List[Any]:
    """Flatten a nested list."""
    return [item for sublist in nested_list for item in sublist]


def normalize_text(text: str) -> str:
    """Basic text normalization."""
    import unicodedata
    import re
    
    # Unicode normalization
    text = unicodedata.normalize('NFKC', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def calculate_accuracy(predictions: List[Any], labels: List[Any]) -> float:
    """Calculate accuracy score."""
    if len(predictions) != len(labels):
        raise ValueError("Predictions and labels must have same length")
    
    correct = sum(1 for p, l in zip(predictions, labels) if p == l)
    return correct / len(predictions) if len(predictions) > 0 else 0.0


def calculate_f1_score(predictions: List[str], labels: List[str], 
                      average: str = 'weighted') -> float:
    """Calculate F1 score."""
    from sklearn.metrics import f1_score
    return f1_score(labels, predictions, average=average)


def split_train_test(data: List[Any], test_size: float = 0.2, 
                    random_state: Optional[int] = None) -> tuple:
    """Split data into train and test sets."""
    if random_state:
        np.random.seed(random_state)
    
    indices = np.random.permutation(len(data))
    test_size_int = int(len(data) * test_size)
    
    test_indices = indices[:test_size_int]
    train_indices = indices[test_size_int:]
    
    train_data = [data[i] for i in train_indices]
    test_data = [data[i] for i in test_indices]
    
    return train_data, test_data


class Timer:
    """Context manager for timing code blocks."""
    
    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, *args):
        self.end_time = time.time()
        self.execution_time = self.end_time - self.start_time
        logging.info(f"{self.name} completed in {self.execution_time:.4f} seconds")


class ProgressBar:
    """Simple progress bar for console output."""
    
    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.description = description
        self.current = 0
        self.start_time = time.time()
    
    def update(self, increment: int = 1):
        """Update progress bar."""
        self.current += increment
        self._display()
    
    def _display(self):
        """Display progress bar."""
        if self.total == 0:
            return
        
        percent = (self.current / self.total) * 100
        elapsed_time = time.time() - self.start_time
        
        # Estimate remaining time
        if self.current > 0:
            eta = (elapsed_time / self.current) * (self.total - self.current)
            eta_str = f"ETA: {eta:.1f}s"
        else:
            eta_str = "ETA: --"
        
        # Create progress bar
        bar_length = 40
        filled_length = int(bar_length * self.current // self.total)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        print(f'\r{self.description}: |{bar}| {percent:.1f}% {eta_str}', 
              end='', flush=True)
        
        if self.current >= self.total:
            print()  # New line when complete


def validate_language_code(code: str) -> bool:
    """Validate language/dialect code."""
    valid_codes = ['ewe', 'anlo', 'inland', 'ho', 'kpando']
    return code.lower() in valid_codes


def memory_usage():
    """Get current memory usage in MB."""
    import psutil
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024
