"""Main processing pipeline for LexLang."""

import logging
import json
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

from ..config import LexLangConfig
from ..exceptions import ProcessingError, ConfigurationError
from ..utils import timing_decorator, Timer
from .tokenizer import EweTokenizer, DialectAwareTokenizer
from .normalizer import TextNormalizer, TonalNormalizer
from .pos_tagger import POSTagger
from .tonal_processor import TonalProcessor
from .dialect_handler import DialectDetector
from .morphology import MorphologicalAnalyzer
from .embeddings import WordEmbeddings

logger = logging.getLogger(__name__)


class Pipeline:
    """Main processing pipeline for Ewe language text."""
    
    def __init__(self, config: LexLangConfig):
        """Initialize pipeline with configuration."""
        self.config = config
        self._processors = {}
        self._initialize_processors()
        logger.info("Pipeline initialized successfully")
    
    def _initialize_processors(self):
        """Initialize all processors."""
        try:
            # Tokenizer
            self._processors['tokenizer'] = EweTokenizer(
                dialect_aware=True,
                config=self.config
            )
            
            # Normalizer
            self._processors['normalizer'] = TextNormalizer(
                config=self.config
            )
            
            # POS Tagger
            self._processors['pos_tagger'] = POSTagger(
                model_path=self.config.models.pos_model_path,
                config=self.config
            )
            
            # Tonal Processor
            self._processors['tonal_processor'] = TonalProcessor(
                config=self.config
            )
            
            # Dialect Detector
            self._processors['dialect_detector'] = DialectDetector(
                model_path=self.config.models.dialect_model_path,
                config=self.config
            )
            
            # Morphological Analyzer
            self._processors['morphology'] = MorphologicalAnalyzer(
                config=self.config
            )
            
            # Word Embeddings
            self._processors['embeddings'] = WordEmbeddings(
                model_path=self.config.models.embedding_model_path,
                config=self.config
            )
            
        except Exception as e:
            logger.error(f"Error initializing processors: {e}")
            raise ConfigurationError(f"Failed to initialize pipeline: {e}")
    
    @timing_decorator
    def process(self, 
                text: str,
                dialect: str = "auto",
                tasks: List[str] = None,
                output_format: str = "json") -> Union[str, Dict[str, Any]]:
        """
        Process text through the pipeline.
        
        Args:
            text: Input text to process
            dialect: Target dialect ('auto', 'anlo', 'inland', 'ho', 'kpando')
            tasks: List of tasks to perform
            output_format: Output format ('json', 'text', 'conllu')
        
        Returns:
            Processed results in specified format
        """
        if not text or not text.strip():
            raise ProcessingError("Input text is empty")
        
        if tasks is None:
            tasks = ["tokenize", "normalize", "pos"]
        
        results = {
            "input_text": text,
            "dialect": dialect,
            "tasks": tasks,
            "timestamp": datetime.utcnow().isoformat(),
            "processing_steps": {}
        }
        
        try:
            with Timer("Full pipeline processing"):
                # Step 1: Dialect detection (if auto)
                if dialect == "auto":
                    detected_dialect = self._processors['dialect_detector'].detect(text)
                    results["dialect_detected"] = detected_dialect
                    dialect = detected_dialect
                
                results["final_dialect"] = dialect
                
                # Step 2: Tokenization
                if "tokenize" in tasks:
                    tokens = self._processors['tokenizer'].tokenize(
                        text, dialect=dialect
                    )
                    results["tokens"] = tokens
                    results["processing_steps"]["tokenization"] = "completed"
                    logger.debug(f"Tokenized into {len(tokens)} tokens")
                
                # Step 3: Normalization
                if "normalize" in tasks:
                    if "tokens" not in results:
                        tokens = self._processors['tokenizer'].tokenize(
                            text, dialect=dialect
                        )
                    
                    normalized_tokens = self._processors['normalizer'].normalize(
                        tokens, dialect=dialect
                    )
                    results["normalized_tokens"] = normalized_tokens
                    results["processing_steps"]["normalization"] = "completed"
                
                # Step 4: POS Tagging
                if "pos" in tasks:
                    input_tokens = results.get("normalized_tokens", 
                                             results.get("tokens", []))
                    if not input_tokens:
                        input_tokens = self._processors['tokenizer'].tokenize(
                            text, dialect=dialect
                        )
                    
                    pos_tags = self._processors['pos_tagger'].tag(
                        input_tokens, dialect=dialect
                    )
                    results["pos_tags"] = pos_tags
                    results["processing_steps"]["pos_tagging"] = "completed"
                
                # Step 5: Tonal Processing
                if "tone" in tasks:
                    input_tokens = results.get("normalized_tokens",
                                             results.get("tokens", []))
                    if not input_tokens:
                        input_tokens = self._processors['tokenizer'].tokenize(
                            text, dialect=dialect
                        )
                    
                    tonal_analysis = self._processors['tonal_processor'].analyze(
                        input_tokens, dialect=dialect
                    )
                    results["tonal_analysis"] = tonal_analysis
                    results["processing_steps"]["tonal_processing"] = "completed"
                
                # Step 6: Morphological Analysis
                if "morphology" in tasks:
                    input_tokens = results.get("normalized_tokens",
                                             results.get("tokens", []))
                    if not input_tokens:
                        input_tokens = self._processors['tokenizer'].tokenize(
                            text, dialect=dialect
                        )
                    
                    morphology = self._processors['morphology'].analyze(
                        input_tokens, dialect=dialect
                    )
                    results["morphological_analysis"] = morphology
                    results["processing_steps"]["morphology"] = "completed"
                
                # Step 7: Dialect Analysis (detailed)
                if "dialect" in tasks:
                    dialect_info = self._processors['dialect_detector'].analyze(
                        text, detailed=True
                    )
                    results["dialect_analysis"] = dialect_info
                    results["processing_steps"]["dialect_analysis"] = "completed"
                
                # Step 8: Word Embeddings
                if "embeddings" in tasks:
                    input_tokens = results.get("normalized_tokens",
                                             results.get("tokens", []))
                    if not input_tokens:
                        input_tokens = self._processors['tokenizer'].tokenize(
                            text, dialect=dialect
                        )
                    
                    embeddings = self._processors['embeddings'].get_embeddings(
                        input_tokens
                    )
                    results["embeddings"] = embeddings
                    results["processing_steps"]["embeddings"] = "completed"
            
            # Format output
            return self._format_output(results, output_format)
            
        except Exception as e:
            logger.error(f"Pipeline processing error: {e}")
            raise ProcessingError(f"Processing failed: {e}")
    
    def _format_output(self, results: Dict[str, Any], 
                      output_format: str) -> Union[str, Dict[str, Any]]:
        """Format results according to specified output format."""
        try:
            if output_format == "json":
                return json.dumps(results, ensure_ascii=False, indent=2)
            
            elif output_format == "text":
                return self._format_text_output(results)
            
            elif output_format == "conllu":
                return self._format_conllu_output(results)
            
            else:
                raise ProcessingError(f"Unsupported output format: {output_format}")
                
        except Exception as e:
            logger.error(f"Output formatting error: {e}")
            raise ProcessingError(f"Failed to format output: {e}")
    
    def _format_text_output(self, results: Dict[str, Any]) -> str:
        """Format results as readable text."""
        output_lines = []
        output_lines.append(f"Input: {results['input_text']}")
        output_lines.append(f"Dialect: {results.get('final_dialect', 'unknown')}")
        output_lines.append("")
        
        if "tokens" in results:
            output_lines.append("Tokens:")
            output_lines.append(" ".join(results["tokens"]))
            output_lines.append("")
        
        if "pos_tags" in results:
            output_lines.append("POS Tags:")
            for token, pos in results["pos_tags"]:
                output_lines.append(f"  {token}\t{pos}")
            output_lines.append("")
        
        if "tonal_analysis" in results:
            output_lines.append("Tonal Analysis:")
            for key, value in results["tonal_analysis"].items():
                output_lines.append(f"  {key}: {value}")
            output_lines.append("")
        
        return "\n".join(output_lines)
    
    def _format_conllu_output(self, results: Dict[str, Any]) -> str:
        """Format results in CoNLL-U format."""
        output_lines = []
        output_lines.append(f"# text = {results['input_text']}")
        output_lines.append(f"# dialect = {results.get('final_dialect', 'unknown')}")
        
        tokens = results.get("tokens", [])
        pos_tags = dict(results.get("pos_tags", []))
        
        for i, token in enumerate(tokens, 1):
            pos = pos_tags.get(token, "_")
            line = f"{i}\t{token}\t_\t{pos}\t_\t_\t_\t_\t_\t_"
            output_lines.append(line)
        
        output_lines.append("")
        return "\n".join(output_lines)
    
    def batch_process(self, 
                     texts: List[str],
                     dialect: str = "auto",
                     tasks: List[str] = None,
                     output_format: str = "json") -> List[Union[str, Dict[str, Any]]]:
        """Process multiple texts in batch."""
        results = []
        
        for i, text in enumerate(texts):
            try:
                result = self.process(
                    text=text,
                    dialect=dialect,
                    tasks=tasks,
                    output_format=output_format
                )
                results.append(result)
                logger.debug(f"Processed batch item {i+1}/{len(texts)}")
                
            except Exception as e:
                logger.error(f"Error processing batch item {i+1}: {e}")
                # Add error result
                error_result = {
                    "error": str(e),
                    "input_text": text,
                    "batch_index": i
                }
                if output_format == "json":
                    results.append(json.dumps(error_result))
                else:
                    results.append(f"Error: {e}")
        
        return results
    
    def get_available_tasks(self) -> List[str]:
        """Get list of available processing tasks."""
        return [
            "tokenize",
            "normalize", 
            "pos",
            "tone",
            "morphology",
            "dialect",
            "embeddings"
        ]
    
    def get_supported_dialects(self) -> List[str]:
        """Get list of supported dialects."""
        return ["auto", "anlo", "inland", "ho", "kpando"]
    
    def get_processor(self, processor_name: str):
        """Get specific processor instance."""
        if processor_name not in self._processors:
            raise ProcessingError(f"Unknown processor: {processor_name}")
        return self._processors[processor_name]
