"""
Base classes for the LangGraph Learning Demo system.

This module defines the core abstractions used throughout the learning system,
including learning modules, exercises, and validation mechanisms.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union


class DifficultyLevel(Enum):
    """Difficulty levels for learning modules and exercises."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class ExerciseType(Enum):
    """Types of exercises available in the learning system."""
    CODING = "coding"
    QUIZ = "quiz"
    PROJECT = "project"
    REFLECTION = "reflection"


@dataclass
class ValidationResult:
    """Result of validating a student's work."""
    is_valid: bool
    score: float  # 0.0 to 1.0
    passed_criteria: List[str]
    failed_criteria: List[str]
    detailed_feedback: str
    suggestions: List[str]
    execution_logs: Optional[str] = None
    
    def generate_student_feedback(self) -> str:
        """Generate human-readable feedback for the student."""
        feedback_parts = [
            f"Score: {self.score:.1%}",
            f"Status: {'✅ Passed' if self.is_valid else '❌ Failed'}",
            "",
            "Detailed Feedback:",
            self.detailed_feedback,
        ]
        
        if self.passed_criteria:
            feedback_parts.extend([
                "",
                "✅ Passed Criteria:",
                *[f"  • {criterion}" for criterion in self.passed_criteria]
            ])
        
        if self.failed_criteria:
            feedback_parts.extend([
                "",
                "❌ Failed Criteria:",
                *[f"  • {criterion}" for criterion in self.failed_criteria]
            ])
        
        if self.suggestions:
            feedback_parts.extend([
                "",
                "💡 Suggestions for Improvement:",
                *[f"  • {suggestion}" for suggestion in self.suggestions]
            ])
        
        return "\n".join(feedback_parts)


@dataclass
class Exercise:
    """Represents a learning exercise."""
    exercise_id: str
    title: str
    description: str
    exercise_type: ExerciseType
    difficulty: DifficultyLevel
    estimated_time: int  # minutes
    instructions: str
    starter_code: Optional[str] = None
    solution_code: Optional[str] = None
    validation_criteria: List[str] = None
    hints: List[str] = None
    
    def __post_init__(self):
        if self.validation_criteria is None:
            self.validation_criteria = []
        if self.hints is None:
            self.hints = []


@dataclass
class StudentSubmission:
    """Represents a student's submission for an exercise."""
    submission_id: str
    student_id: str
    exercise_id: str
    code: str
    documentation: str
    submission_time: datetime
    validation_results: Optional[ValidationResult] = None


class LearningModule(ABC):
    """
    Abstract base class for all learning modules.
    
    Each learning module represents a self-contained educational unit
    with specific learning objectives, content, and validation criteria.
    """
    
    def __init__(
        self,
        module_id: str,
        title: str,
        description: str,
        prerequisites: List[str] = None,
        difficulty: DifficultyLevel = DifficultyLevel.BEGINNER,
        estimated_duration: int = 60  # minutes
    ):
        self.module_id = module_id
        self.title = title
        self.description = description
        self.prerequisites = prerequisites or []
        self.difficulty = difficulty
        self.estimated_duration = estimated_duration
        self.learning_objectives: List[str] = []
        self.exercises: List[Exercise] = []
        self.resources: List[Dict[str, str]] = []
    
    @abstractmethod
    def get_learning_objectives(self) -> List[str]:
        """Return the learning objectives for this module."""
        pass
    
    @abstractmethod
    def get_content_sections(self) -> List[Dict[str, Any]]:
        """Return the content sections for this module."""
        pass
    
    @abstractmethod
    def get_exercises(self) -> List[Exercise]:
        """Return the exercises for this module."""
        pass
    
    @abstractmethod
    def validate_submission(self, submission: StudentSubmission) -> ValidationResult:
        """Validate a student's submission for this module."""
        pass
    
    def validate_prerequisites(self, completed_modules: List[str]) -> bool:
        """Check if all prerequisite modules have been completed."""
        return all(prereq in completed_modules for prereq in self.prerequisites)
    
    def add_resource(self, title: str, url: str, resource_type: str = "documentation"):
        """Add a learning resource to this module."""
        self.resources.append({
            "title": title,
            "url": url,
            "type": resource_type
        })
    
    def get_progress_summary(self, completed_exercises: List[str]) -> Dict[str, Any]:
        """Get a summary of progress through this module."""
        total_exercises = len(self.exercises)
        completed_count = len([ex for ex in self.exercises if ex.exercise_id in completed_exercises])
        
        return {
            "module_id": self.module_id,
            "title": self.title,
            "total_exercises": total_exercises,
            "completed_exercises": completed_count,
            "progress_percentage": (completed_count / total_exercises * 100) if total_exercises > 0 else 0,
            "is_complete": completed_count == total_exercises,
            "difficulty": self.difficulty.value,
            "estimated_duration": self.estimated_duration
        }


class ProjectValidator(ABC):
    """Abstract base class for project validators."""
    
    @abstractmethod
    def validate_code_structure(self, code: str, requirements: List[str]) -> ValidationResult:
        """Validate the structure of submitted code."""
        pass
    
    @abstractmethod
    def validate_functionality(self, code: str, test_cases: List[Dict[str, Any]]) -> ValidationResult:
        """Validate the functionality of submitted code."""
        pass
    
    @abstractmethod
    def validate_best_practices(self, code: str) -> ValidationResult:
        """Validate adherence to best practices."""
        pass


class ProgressTracker:
    """Tracks student progress through the learning system."""
    
    def __init__(self):
        self.student_progress: Dict[str, Dict[str, Any]] = {}
    
    def record_module_completion(self, student_id: str, module_id: str, score: float):
        """Record completion of a learning module."""
        if student_id not in self.student_progress:
            self.student_progress[student_id] = {
                "completed_modules": [],
                "module_scores": {},
                "start_date": datetime.now(),
                "last_activity": datetime.now()
            }
        
        progress = self.student_progress[student_id]
        if module_id not in progress["completed_modules"]:
            progress["completed_modules"].append(module_id)
        progress["module_scores"][module_id] = score
        progress["last_activity"] = datetime.now()
    
    def get_student_progress(self, student_id: str) -> Dict[str, Any]:
        """Get comprehensive progress report for a student."""
        if student_id not in self.student_progress:
            return {
                "student_id": student_id,
                "completed_modules": [],
                "module_scores": {},
                "overall_progress": 0.0,
                "start_date": None,
                "last_activity": None
            }
        
        progress = self.student_progress[student_id]
        total_modules = 9  # Based on our learning system design
        completed_count = len(progress["completed_modules"])
        
        return {
            "student_id": student_id,
            "completed_modules": progress["completed_modules"],
            "module_scores": progress["module_scores"],
            "overall_progress": (completed_count / total_modules * 100),
            "start_date": progress["start_date"],
            "last_activity": progress["last_activity"]
        }
    
    def recommend_next_steps(self, student_id: str, available_modules: List[str]) -> List[str]:
        """Recommend next learning steps for a student."""
        progress = self.get_student_progress(student_id)
        completed = set(progress["completed_modules"])
        
        # Simple recommendation: suggest modules not yet completed
        recommendations = [module for module in available_modules if module not in completed]
        
        # Sort by module order (assuming module IDs are ordered)
        recommendations.sort()
        
        return recommendations[:3]  # Return top 3 recommendations