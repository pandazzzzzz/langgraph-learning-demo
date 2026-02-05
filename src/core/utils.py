"""
Utility functions for the LangGraph Learning Demo system.

This module provides common utilities for logging, configuration,
environment setup, and other shared functionality.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv


def setup_logging(
    level: str = "INFO",
    format_string: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging configuration for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom format string for log messages
        log_file: Optional file path to write logs to
    
    Returns:
        Configured logger instance
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_string,
        handlers=[]
    )
    
    logger = logging.getLogger("langgraph_learning")
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(format_string))
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(format_string))
        logger.addHandler(file_handler)
    
    return logger


def load_config() -> Dict[str, Any]:
    """
    Load configuration from environment variables.
    
    Returns:
        Dictionary containing configuration values
    """
    # Load environment variables from .env file
    load_dotenv()
    
    config = {
        # API Keys
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
        "langchain_api_key": os.getenv("LANGCHAIN_API_KEY"),
        
        # LangSmith Configuration
        "langchain_tracing_v2": os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true",
        "langchain_project": os.getenv("LANGCHAIN_PROJECT", "langgraph-learning-demo"),
        
        # Vector Database Configuration
        "pinecone_api_key": os.getenv("PINECONE_API_KEY"),
        "pinecone_environment": os.getenv("PINECONE_ENVIRONMENT"),
        "weaviate_url": os.getenv("WEAVIATE_URL"),
        "weaviate_api_key": os.getenv("WEAVIATE_API_KEY"),
        
        # Local LLM Configuration
        "ollama_base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        
        # Application Configuration
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "database_url": os.getenv("DATABASE_URL", "sqlite:///./langgraph_learning.db"),
        
        # Cache Configuration
        "cache_type": os.getenv("CACHE_TYPE", "memory"),
        "redis_url": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    }
    
    return config


def validate_environment() -> Dict[str, bool]:
    """
    Validate that required environment variables and dependencies are available.
    
    Returns:
        Dictionary with validation results for each component
    """
    config = load_config()
    validation_results = {}
    
    # Check API keys
    validation_results["openai_api_key"] = bool(config["openai_api_key"])
    validation_results["anthropic_api_key"] = bool(config["anthropic_api_key"])
    
    # Check optional services
    validation_results["langsmith_configured"] = bool(config["langchain_api_key"])
    validation_results["pinecone_configured"] = bool(
        config["pinecone_api_key"] and config["pinecone_environment"]
    )
    validation_results["weaviate_configured"] = bool(
        config["weaviate_url"] and config["weaviate_api_key"]
    )
    
    # Check Python packages
    try:
        import langgraph
        validation_results["langgraph_installed"] = True
    except ImportError:
        validation_results["langgraph_installed"] = False
    
    try:
        import langchain
        validation_results["langchain_installed"] = True
    except ImportError:
        validation_results["langchain_installed"] = False
    
    try:
        import chromadb
        validation_results["chromadb_installed"] = True
    except ImportError:
        validation_results["chromadb_installed"] = False
    
    return validation_results


def get_project_root() -> Path:
    """
    Get the root directory of the project.
    
    Returns:
        Path object pointing to the project root
    """
    current_file = Path(__file__)
    # Navigate up from src/core/utils.py to project root
    return current_file.parent.parent.parent


def ensure_directory(path: Path) -> Path:
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        path: Path to the directory
    
    Returns:
        Path object pointing to the directory
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_example_data(filename: str) -> str:
    """
    Load example data from the examples directory.
    
    Args:
        filename: Name of the file to load
    
    Returns:
        Content of the file as a string
    """
    project_root = get_project_root()
    examples_dir = project_root / "examples"
    file_path = examples_dir / filename
    
    if not file_path.exists():
        raise FileNotFoundError(f"Example file not found: {file_path}")
    
    return file_path.read_text(encoding="utf-8")


def save_student_work(student_id: str, module_id: str, exercise_id: str, content: str) -> Path:
    """
    Save student work to the appropriate directory.
    
    Args:
        student_id: Unique identifier for the student
        module_id: Module identifier
        exercise_id: Exercise identifier
        content: Content to save
    
    Returns:
        Path to the saved file
    """
    project_root = get_project_root()
    work_dir = project_root / "student_work" / student_id / module_id
    ensure_directory(work_dir)
    
    file_path = work_dir / f"{exercise_id}.py"
    file_path.write_text(content, encoding="utf-8")
    
    return file_path


def format_duration(minutes: int) -> str:
    """
    Format duration in minutes to a human-readable string.
    
    Args:
        minutes: Duration in minutes
    
    Returns:
        Formatted duration string
    """
    if minutes < 60:
        return f"{minutes} minutes"
    
    hours = minutes // 60
    remaining_minutes = minutes % 60
    
    if remaining_minutes == 0:
        return f"{hours} hour{'s' if hours != 1 else ''}"
    
    return f"{hours} hour{'s' if hours != 1 else ''} {remaining_minutes} minutes"


def print_validation_summary(validation_results: Dict[str, bool]) -> None:
    """
    Print a summary of environment validation results.
    
    Args:
        validation_results: Dictionary with validation results
    """
    print("🔍 Environment Validation Results:")
    print("=" * 40)
    
    for component, is_valid in validation_results.items():
        status = "✅" if is_valid else "❌"
        component_name = component.replace("_", " ").title()
        print(f"{status} {component_name}")
    
    # Summary
    total_checks = len(validation_results)
    passed_checks = sum(validation_results.values())
    
    print("=" * 40)
    print(f"Summary: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks < total_checks:
        print("\n⚠️  Some components are not configured. Check your .env file and installed packages.")
    else:
        print("\n🎉 All components are properly configured!")


class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to log messages."""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)