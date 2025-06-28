#!/usr/bin/env python3
"""Main entry point for LexLang application."""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from .config import load_config
from .core.pipeline import Pipeline
from .utils import setup_logging
from .exceptions import LexLangError


def main():
    """Main function to run LexLang processing."""
    parser = argparse.ArgumentParser(
        description="LexLang: Advanced NLP toolkit for Ewe language processing"
    )
    parser.add_argument(
        "input", 
        help="Input text file or string to process"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: stdout)"
    )
    parser.add_argument(
        "-c", "--config",
        default="configs/default.yaml",
        help="Configuration file path"
    )
    parser.add_argument(
        "-d", "--dialect",
        choices=["anlo", "inland", "ho", "kpando", "auto"],
        default="auto",
        help="Target dialect for processing"
    )
    parser.add_argument(
        "-t", "--tasks",
        nargs="+",
        choices=["tokenize", "normalize", "pos", "tone", "dialect"],
        default=["tokenize", "normalize", "pos"],
        help="Processing tasks to perform"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["json", "text", "conllu"],
        default="json",
        help="Output format"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(level=log_level)
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        config = load_config(args.config)
        logger.info(f"Loaded configuration from {args.config}")
        
        # Initialize pipeline
        pipeline = Pipeline(config)
        logger.info("Initialized processing pipeline")
        
        # Read input
        if Path(args.input).exists():
            with open(args.input, 'r', encoding='utf-8') as f:
                text = f.read()
            logger.info(f"Read input from file: {args.input}")
        else:
            text = args.input
            logger.info("Processing input string")
        
        # Process text
        results = pipeline.process(
            text=text,
            dialect=args.dialect,
            tasks=args.tasks,
            output_format=args.format
        )
        
        # Write output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(results)
            logger.info(f"Results written to {args.output}")
        else:
            print(results)
            
    except LexLangError as e:
        logger.error(f"LexLang error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
