"""
Core module for LangGraph Learning Demo

Contains base classes, utilities, and common functionality
used across all learning modules.
"""

from .base import LearningModule, Exercise, ValidationResult
from .utils import setup_logging, load_config

__all__ = [
    "LearningModule",
    "Exercise",
    "ValidationResult", 
    "setup_logging",
    "load_config",
]