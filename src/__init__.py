"""
LangGraph Learning Demo

A comprehensive learning project for mastering LangGraph framework,
from basic concepts to advanced multi-agent systems.
"""

__version__ = "0.1.0"
__author__ = "LangGraph Learning Demo"
__email__ = "demo@example.com"

from .core.base import LearningModule, Exercise, ValidationResult
from .core.utils import setup_logging, load_config

__all__ = [
    "LearningModule",
    "Exercise", 
    "ValidationResult",
    "setup_logging",
    "load_config",
]