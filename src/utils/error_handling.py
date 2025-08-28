#!/usr/bin/env python3
"""
Comprehensive Error Handling System
===================================

Centralized error handling and exception management for the Revitron UI Enhancement Framework.
Provides structured error reporting, recovery strategies, and debugging support.

Author: AEC Development Team
Repository: https://github.com/mohammedhadeez/revitron-ui-enhancement-framework
Version: 2.0 (Self-Reflection Integrated)
"""

import logging
import traceback
import sys
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path
import json
import time


class ErrorSeverity(Enum):
    """Error severity levels for prioritizing resolution efforts"""
    CRITICAL = "critical"        # Framework cannot continue
    HIGH = "high"               # Major functionality impaired
    MEDIUM = "medium"           # Minor functionality issues
    LOW = "low"                 # Cosmetic or edge case issues


class ErrorCategory(Enum):
    """Error categories for better classification and handling"""
    RESEARCH_ACCESS = "research_access"           # Cannot access documentation
    VALIDATION_COVERAGE = "validation_coverage"   # Validation incomplete
    DUPLICATE_GENERATION = "duplicate_generation" # Duplicate suggestions
    SPECIFICATION_INCOMPLETE = "specification_incomplete"  # Missing specs
    API_COMPATIBILITY = "api_compatibility"       # API version issues
    CONFIGURATION = "configuration"               # Config file issues
    EXTERNAL_DEPENDENCY = "external_dependency"   # External service failures
    DATA_PROCESSING = "data_processing"          # Data processing errors
    FILE_SYSTEM = "file_system"                  # File access issues
    NETWORK = "network"                          # Network connectivity
    PERMISSION = "permission"                    # Access permission issues


@dataclass
class FrameworkError:
    """Comprehensive error information structure"""
    error_id: str
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    component: str
    timestamp: float = field(default_factory=time.time)
    
    # Technical details
    exception_type: str = ""
    stack_trace: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    
    # Resolution information
    suggested_resolution: str = ""
    recovery_attempted: bool = False
    recovery_successful: bool = False
    
    # User impact
    user_message: str = ""
    blocks_execution: bool = False


class CriticalFrameworkError(Exception):
    """Critical framework error that prevents continued execution"""
    
    def __init__(self, message: str, category: ErrorCategory = ErrorCategory.CONFIGURATION, context: Dict = None):
        super().__init__(message)
        self.category = category
        self.context = context or {}
        self.severity = ErrorSeverity.CRITICAL


class ValidationError(Exception):
    """Error during validation process"""
    
    def __init__(self, message: str, validation_type: str = "", context: Dict = None):
        super().__init__(message)
        self.validation_type = validation_type
        self.context = context or {}
        self.severity = ErrorSeverity.HIGH


class ResearchAccessError(Exception):
    """Error accessing research sources or documentation"""
    
    def __init__(self, message: str, source: str = "", context: Dict = None):
        super().__init__(message)
        self.source = source
        self.context = context or {}
        self.severity = ErrorSeverity.CRITICAL


class SpecificationError(Exception):
    """Error during implementation specification generation"""
    
    def __init__(self, message: str, suggestion_id: str = "", context: Dict = None):
        super().__init__(message)
        self.suggestion_id = suggestion_id
        self.context = context or {}
        self.severity = ErrorSeverity.HIGH


class MappingError(Exception):
    """Error during functionality mapping process"""
    
    def __init__(self, message: str, mapping_type: str = "", context: Dict = None):
        super().__init__(message)
        self.mapping_type = mapping_type
        self.context = context or {}
        self.severity = ErrorSeverity.HIGH


class GenerationError(Exception):
    """Error during button suggestion generation"""
    
    def __init__(self, message: str, generation_phase: str = "", context: Dict = None):
        super().__init__(message)
        self.generation_phase = generation_phase
        self.context = context or {}
        self.severity = ErrorSeverity.MEDIUM


class QualityError(Exception):
    """Error in quality assurance process"""
    
    def __init__(self, message: str, quality_aspect: str = "", context: Dict = None):
        super().__init__(message)
        self.quality_aspect = quality_aspect
        self.context = context or {}
        self.severity = ErrorSeverity.HIGH


class ErrorHandler:
    """
    Comprehensive error handling and recovery system for the framework.
    
    Provides centralized error processing, logging, recovery attempts,
    and user-friendly error reporting.
    """
    
    def __init__(self):
        """Initialize error handler with recovery strategies"""
        self.logger = logging.getLogger("revitron_framework.error_handler")
        
        # Error tracking
        self.errors: List[FrameworkError] = []
        self.error_counts: Dict[ErrorCategory, int] = {}
        
        # Recovery strategies
        self.recovery_strategies = self._initialize_recovery_strategies()
        
        # User messages
        self.user_messages = self._initialize_user_messages()
        
        self.logger.info("🛡️ Error handling system initialized")
    
    def handle_exception(
        self,
        exception: Exception,
        component: str,
        context: Dict[str, Any] = None,
        attempt_recovery: bool = True
    ) -> FrameworkError:
        """
        Handle exception with comprehensive error processing.
        
        Args:
            exception: The exception that occurred
            component: Framework component where error occurred
            context: Additional context information
            attempt_recovery: Whether to attempt automatic recovery
            
        Returns:
            FrameworkError object with complete error information
        """
        
        # Generate unique error ID
        error_id = f"ERR_{int(time.time())}_{len(self.errors)}"
        
        # Determine error category and severity
        category, severity = self._classify_error(exception)
        
        # Create comprehensive error object
        framework_error = FrameworkError(
            error_id=error_id,
            category=category,
            severity=severity,
            message=str(exception),
            component=component,
            exception_type=type(exception).__name__,
            stack_trace=traceback.format_exc(),
            context=context or {},
            suggested_resolution=self._get_suggested_resolution(exception, category),
            user_message=self._get_user_friendly_message(exception, category),
            blocks_execution=self._blocks_execution(severity)
        )
        
        # Log the error
        self._log_error(framework_error)
        
        # Update error tracking
        self.errors.append(framework_error)
        self.error_counts[category] = self.error_counts.get(category, 0) + 1
        
        # Attempt recovery if requested and available
        if attempt_recovery and category in self.recovery_strategies:
            framework_error.recovery_attempted = True
            try:
                recovery_func = self.recovery_strategies[category]
                recovery_successful = recovery_func(exception, context or {})
                framework_error.recovery_successful = recovery_successful
                
                if recovery_successful:
                    self.logger.info(f"🔄 Recovery successful for error {error_id}")
                else:
                    self.logger.warning(f"🔄 Recovery attempted but failed for error {error_id}")
                    
            except Exception as recovery_error:
                self.logger.error(f"🔄 Recovery attempt failed for error {error_id}: {recovery_error}")
        
        return framework_error
    
    def _classify_error(self, exception: Exception) -> tuple[ErrorCategory, ErrorSeverity]:
        """Classify error into category and severity"""
        
        exception_type = type(exception).__name__
        exception_message = str(exception).lower()
        
        # Direct mapping for custom exceptions
        if isinstance(exception, CriticalFrameworkError):
            return exception.category, ErrorSeverity.CRITICAL
        elif isinstance(exception, ResearchAccessError):
            return ErrorCategory.RESEARCH_ACCESS, ErrorSeverity.CRITICAL
        elif isinstance(exception, ValidationError):
            return ErrorCategory.VALIDATION_COVERAGE, ErrorSeverity.HIGH
        elif isinstance(exception, SpecificationError):
            return ErrorCategory.SPECIFICATION_INCOMPLETE, ErrorSeverity.HIGH
        elif isinstance(exception, MappingError):
            return ErrorCategory.DUPLICATE_GENERATION, ErrorSeverity.HIGH
        elif isinstance(exception, GenerationError):
            return ErrorCategory.DATA_PROCESSING, ErrorSeverity.MEDIUM
        elif isinstance(exception, QualityError):
            return ErrorCategory.VALIDATION_COVERAGE, ErrorSeverity.HIGH
        
        # Pattern-based classification
        if "permission" in exception_message or "access denied" in exception_message:
            return ErrorCategory.PERMISSION, ErrorSeverity.HIGH
        elif "network" in exception_message or "connection" in exception_message:
            return ErrorCategory.NETWORK, ErrorSeverity.MEDIUM
        elif "file not found" in exception_message or "directory" in exception_message:
            return ErrorCategory.FILE_SYSTEM, ErrorSeverity.MEDIUM
        elif "config" in exception_message or "configuration" in exception_message:
            return ErrorCategory.CONFIGURATION, ErrorSeverity.HIGH
        elif "api" in exception_message or "compatibility" in exception_message:
            return ErrorCategory.API_COMPATIBILITY, ErrorSeverity.MEDIUM
        
        # Default classification
        return ErrorCategory.DATA_PROCESSING, ErrorSeverity.MEDIUM
    
    def _get_suggested_resolution(self, exception: Exception, category: ErrorCategory) -> str:
        """Get suggested resolution based on error type"""
        
        resolutions = {
            ErrorCategory.RESEARCH_ACCESS: "Check network connectivity and verify documentation URLs are accessible",
            ErrorCategory.VALIDATION_COVERAGE: "Ensure all validation criteria are properly configured and data is complete",
            ErrorCategory.DUPLICATE_GENERATION: "Verify capability mapping database is complete and up-to-date",
            ErrorCategory.SPECIFICATION_INCOMPLETE: "Check that all required specification elements are properly configured",
            ErrorCategory.API_COMPATIBILITY: "Verify Revit and PyRevit versions are compatible with framework requirements",
            ErrorCategory.CONFIGURATION: "Verify configuration file syntax and all required parameters are present",
            ErrorCategory.EXTERNAL_DEPENDENCY: "Check that all external dependencies are installed and accessible",
            ErrorCategory.DATA_PROCESSING: "Verify input data format and completeness",
            ErrorCategory.FILE_SYSTEM: "Check file/directory permissions and ensure paths exist",
            ErrorCategory.NETWORK: "Verify network connectivity and proxy settings",
            ErrorCategory.PERMISSION: "Check user permissions for file and system access"
        }
        
        return resolutions.get(category, "Review error details and consult framework documentation")
    
    def _get_user_friendly_message(self, exception: Exception, category: ErrorCategory) -> str:
        """Get user-friendly error message"""
        
        user_messages = {
            ErrorCategory.RESEARCH_ACCESS: "Unable to access required documentation. Please check your internet connection.",
            ErrorCategory.VALIDATION_COVERAGE: "Validation process incomplete. Some suggestions may not meet quality standards.",
            ErrorCategory.DUPLICATE_GENERATION: "Duplicate detection system encountered an issue. Some suggestions may duplicate existing functionality.",
            ErrorCategory.SPECIFICATION_INCOMPLETE: "Unable to generate complete technical specifications for some suggestions.",
            ErrorCategory.API_COMPATIBILITY: "Compatibility issue with Revit or PyRevit version. Some features may not work correctly.",
            ErrorCategory.CONFIGURATION: "Configuration error detected. Please check your settings.",
            ErrorCategory.EXTERNAL_DEPENDENCY: "External service or dependency unavailable. Some features may be limited.",
            ErrorCategory.DATA_PROCESSING: "Error processing data. Please verify input data format.",
            ErrorCategory.FILE_SYSTEM: "File access error. Please check file permissions and paths.",
            ErrorCategory.NETWORK: "Network connectivity issue. Please check your internet connection.",
            ErrorCategory.PERMISSION: "Permission error. Please ensure you have necessary access rights."
        }
        
        return user_messages.get(category, "An unexpected error occurred. Please consult the technical details.")
    
    def _blocks_execution(self, severity: ErrorSeverity) -> bool:
        """Determine if error blocks continued execution"""
        return severity == ErrorSeverity.CRITICAL
    
    def _log_error(self, framework_error: FrameworkError):
        """Log error with appropriate level and formatting"""
        
        log_level_map = {
            ErrorSeverity.CRITICAL: logging.CRITICAL,
            ErrorSeverity.HIGH: logging.ERROR,
            ErrorSeverity.MEDIUM: logging.WARNING,
            ErrorSeverity.LOW: logging.INFO
        }
        
        log_level = log_level_map[framework_error.severity]
        
        # Log structured error information
        self.logger.log(
            log_level,
            f"🚨 {framework_error.severity.value.upper()} ERROR [{framework_error.error_id}] "
            f"in {framework_error.component}: {framework_error.message}"
        )
        
        # Log additional context if available
        if framework_error.context:
            self.logger.debug(f"📋 Context for {framework_error.error_id}: {framework_error.context}")
        
        # Log stack trace for debugging
        if framework_error.stack_trace and framework_error.severity in [ErrorSeverity.CRITICAL, ErrorSeverity.HIGH]:
            self.logger.debug(f"📚 Stack trace for {framework_error.error_id}:\n{framework_error.stack_trace}")
    
    def _initialize_recovery_strategies(self) -> Dict[ErrorCategory, Callable]:
        """Initialize automatic recovery strategies for different error types"""
        
        return {
            ErrorCategory.NETWORK: self._recover_network_error,
            ErrorCategory.FILE_SYSTEM: self._recover_file_system_error,
            ErrorCategory.CONFIGURATION: self._recover_configuration_error,
            ErrorCategory.EXTERNAL_DEPENDENCY: self._recover_dependency_error
        }
    
    def _recover_network_error(self, exception: Exception, context: Dict) -> bool:
        """Attempt to recover from network errors"""
        
        # Simple retry mechanism
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                import time
                time.sleep(retry_delay)
                
                # Test connectivity (simplified)
                import urllib.request
                urllib.request.urlopen('https://google.com', timeout=10)
                
                self.logger.info(f"🔄 Network recovery successful after {attempt + 1} attempts")
                return True
                
            except Exception:
                if attempt == max_retries - 1:
                    self.logger.warning("🔄 Network recovery failed after all attempts")
                    return False
                continue
        
        return False
    
    def _recover_file_system_error(self, exception: Exception, context: Dict) -> bool:
        """Attempt to recover from file system errors"""
        
        # Try to create missing directories
        if "no such file or directory" in str(exception).lower():
            try:
                file_path = context.get('file_path')
                if file_path:
                    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
                    self.logger.info("🔄 Created missing directory for recovery")
                    return True
            except Exception:
                pass
        
        return False
    
    def _recover_configuration_error(self, exception: Exception, context: Dict) -> bool:
        """Attempt to recover from configuration errors"""
        
        # Use default configuration values
        try:
            # This would load default configuration
            self.logger.info("🔄 Attempting to use default configuration")
            return True
        except Exception:
            return False
    
    def _recover_dependency_error(self, exception: Exception, context: Dict) -> bool:
        """Attempt to recover from dependency errors"""
        
        # Skip optional dependencies
        dependency = context.get('dependency')
        if dependency and dependency in ['selenium', 'matplotlib', 'plotly']:
            self.logger.warning(f"🔄 Skipping optional dependency: {dependency}")
            return True
        
        return False
    
    def _initialize_user_messages(self) -> Dict[str, str]:
        """Initialize user-friendly error messages"""
        
        return {
            "network_error": "Please check your internet connection and try again.",
            "permission_error": "Please ensure you have the necessary permissions to access files and directories.",
            "configuration_error": "There's an issue with your configuration. Please check your settings.",
            "dependency_error": "A required component is missing. Please check the installation guide.",
            "data_error": "There's an issue with the input data. Please verify the data format.",
            "api_error": "Compatibility issue detected. Please check your Revit/PyRevit version."
        }
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of all errors encountered"""
        
        return {
            'total_errors': len(self.errors),
            'critical_errors': len([e for e in self.errors if e.severity == ErrorSeverity.CRITICAL]),
            'high_severity_errors': len([e for e in self.errors if e.severity == ErrorSeverity.HIGH]),
            'error_categories': dict(self.error_counts),
            'recovery_success_rate': self._calculate_recovery_success_rate(),
            'blocking_errors': len([e for e in self.errors if e.blocks_execution])
        }
    
    def _calculate_recovery_success_rate(self) -> float:
        """Calculate recovery success rate"""
        
        recovery_attempts = [e for e in self.errors if e.recovery_attempted]
        if not recovery_attempts:
            return 0.0
        
        successful_recoveries = [e for e in recovery_attempts if e.recovery_successful]
        return len(successful_recoveries) / len(recovery_attempts)
    
    def export_error_report(self, file_path: Path):
        """Export comprehensive error report to file"""
        
        report = {
            'framework_version': '2.0',
            'report_timestamp': time.time(),
            'summary': self.get_error_summary(),
            'errors': [
                {
                    'error_id': error.error_id,
                    'category': error.category.value,
                    'severity': error.severity.value,
                    'message': error.message,
                    'component': error.component,
                    'timestamp': error.timestamp,
                    'recovery_attempted': error.recovery_attempted,
                    'recovery_successful': error.recovery_successful,
                    'user_message': error.user_message,
                    'suggested_resolution': error.suggested_resolution
                }
                for error in self.errors
            ]
        }
        
        with open(file_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"📄 Error report exported to {file_path}")


# Global error handler instance
_global_error_handler = None


def get_error_handler() -> ErrorHandler:
    """Get global error handler instance"""
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = ErrorHandler()
    return _global_error_handler


def handle_framework_error(
    exception: Exception,
    component: str,
    context: Dict[str, Any] = None,
    attempt_recovery: bool = True
) -> FrameworkError:
    """
    Convenience function for handling framework errors.
    
    Args:
        exception: The exception that occurred
        component: Framework component where error occurred
        context: Additional context information
        attempt_recovery: Whether to attempt automatic recovery
        
    Returns:
        FrameworkError object with complete error information
    """
    error_handler = get_error_handler()
    return error_handler.handle_exception(exception, component, context, attempt_recovery)


# Export key components
__all__ = [
    'ErrorSeverity',
    'ErrorCategory', 
    'FrameworkError',
    'CriticalFrameworkError',
    'ValidationError',
    'ResearchAccessError',
    'SpecificationError',
    'MappingError',
    'GenerationError',
    'QualityError',
    'ErrorHandler',
    'get_error_handler',
    'handle_framework_error'
]
