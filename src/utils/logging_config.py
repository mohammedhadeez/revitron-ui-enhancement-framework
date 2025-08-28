#!/usr/bin/env python3
"""
Comprehensive Logging Configuration
==================================

Centralized logging system for the entire Revitron UI Enhancement Framework.
Provides structured logging with multiple handlers and formatting options.

Author: AEC Development Team
Repository: https://github.com/mohammedhadeez/revitron-ui-enhancement-framework
Version: 2.0 (Self-Reflection Integrated)
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
import structlog
from rich.console import Console
from rich.logging import RichHandler


def setup_comprehensive_logging(
    log_level: str = "INFO",
    log_file: Optional[Path] = None,
    enable_rich_formatting: bool = True
) -> logging.Logger:
    """
    Setup comprehensive logging system for framework components.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for logging output
        enable_rich_formatting: Enable rich console formatting
        
    Returns:
        Configured logger instance
    """
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Set default log file if not provided
    if log_file is None:
        log_file = logs_dir / "framework_execution.log"
    
    # Configure logging level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Clear existing handlers
    logging.root.handlers = []
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Console handler with Rich formatting
    if enable_rich_formatting:
        console = Console()
        console_handler = RichHandler(
            console=console,
            rich_tracebacks=True,
            markup=True,
            show_path=False,
            show_time=True
        )
        console_handler.setFormatter(simple_formatter)
    else:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(simple_formatter)
    
    console_handler.setLevel(logging.INFO)
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(detailed_formatter)
    file_handler.setLevel(logging.DEBUG)
    
    # Error file handler
    error_log_file = logs_dir / "framework_errors.log"
    error_handler = logging.handlers.RotatingFileHandler(
        filename=error_log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    error_handler.setFormatter(detailed_formatter)
    error_handler.setLevel(logging.ERROR)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)
    
    # Configure structured logging
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="ISO"),
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Return configured logger
    logger = logging.getLogger("revitron_framework")
    logger.info("🔧 Comprehensive logging system initialized")
    logger.info(f"📁 Log files: {log_file}, {error_log_file}")
    
    return logger


def get_component_logger(component_name: str) -> logging.Logger:
    """
    Get logger for specific framework component.
    
    Args:
        component_name: Name of the framework component
        
    Returns:
        Component-specific logger
    """
    return logging.getLogger(f"revitron_framework.{component_name}")


class FrameworkLoggerMixin:
    """
    Mixin class providing logging functionality to framework components.
    """
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.logger = get_component_logger(cls.__name__.lower())
    
    def log_execution_start(self, operation_name: str):
        """Log the start of an operation"""
        self.logger.info(f"🚀 Starting {operation_name}")
    
    def log_execution_end(self, operation_name: str, execution_time: float = None):
        """Log the end of an operation"""
        time_msg = f" ({execution_time:.2f}s)" if execution_time else ""
        self.logger.info(f"✅ Completed {operation_name}{time_msg}")
    
    def log_progress(self, current: int, total: int, description: str = ""):
        """Log progress of an operation"""
        percentage = (current / total * 100) if total > 0 else 0
        desc_msg = f" - {description}" if description else ""
        self.logger.info(f"📈 Progress: {current}/{total} ({percentage:.1f}%){desc_msg}")
    
    def log_error(self, error: Exception, context: str = ""):
        """Log an error with context"""
        context_msg = f" in {context}" if context else ""
        self.logger.error(f"❌ Error{context_msg}: {str(error)}")
    
    def log_warning(self, message: str, context: str = ""):
        """Log a warning with context"""
        context_msg = f" [{context}]" if context else ""
        self.logger.warning(f"⚠️ Warning{context_msg}: {message}")
    
    def log_success(self, message: str):
        """Log a success message"""
        self.logger.info(f"🎉 {message}")


# Performance logging utilities
class PerformanceLogger:
    """
    Utility class for performance monitoring and logging.
    """
    
    def __init__(self, logger_name: str = "performance"):
        self.logger = get_component_logger(logger_name)
        self.start_times = {}
    
    def start_timer(self, operation_id: str):
        """Start timing an operation"""
        import time
        self.start_times[operation_id] = time.time()
        self.logger.debug(f"⏱️ Started timer for: {operation_id}")
    
    def end_timer(self, operation_id: str) -> float:
        """End timing an operation and return duration"""
        import time
        if operation_id not in self.start_times:
            self.logger.warning(f"⚠️ No start time found for: {operation_id}")
            return 0.0
        
        duration = time.time() - self.start_times[operation_id]
        del self.start_times[operation_id]
        
        self.logger.info(f"⏱️ {operation_id}: {duration:.2f}s")
        return duration
    
    def log_memory_usage(self, context: str = ""):
        """Log current memory usage"""
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            context_msg = f" [{context}]" if context else ""
            self.logger.info(f"💾 Memory usage{context_msg}: {memory_mb:.1f} MB")
        except ImportError:
            self.logger.debug("psutil not available for memory monitoring")


# Quality assurance logging
class QualityLogger:
    """
    Specialized logger for quality assurance and validation events.
    """
    
    def __init__(self):
        self.logger = get_component_logger("quality")
    
    def log_quality_gate_start(self, gate_name: str):
        """Log the start of a quality gate check"""
        self.logger.info(f"🚪 Quality Gate: {gate_name} - Starting validation")
    
    def log_quality_gate_pass(self, gate_name: str, score: float = None):
        """Log successful quality gate passage"""
        score_msg = f" (Score: {score:.2f})" if score else ""
        self.logger.info(f"✅ Quality Gate: {gate_name} - PASSED{score_msg}")
    
    def log_quality_gate_fail(self, gate_name: str, reason: str, score: float = None):
        """Log quality gate failure"""
        score_msg = f" (Score: {score:.2f})" if score else ""
        self.logger.error(f"❌ Quality Gate: {gate_name} - FAILED{score_msg} - {reason}")
    
    def log_validation_result(self, item_name: str, passed: bool, details: str = ""):
        """Log validation result for individual items"""
        status = "✅ PASSED" if passed else "❌ FAILED"
        details_msg = f" - {details}" if details else ""
        self.logger.info(f"🔍 Validation: {item_name} - {status}{details_msg}")
    
    def log_metrics_summary(self, metrics: dict):
        """Log summary of quality metrics"""
        self.logger.info("📊 Quality Metrics Summary:")
        for metric_name, value in metrics.items():
            if isinstance(value, (int, float)):
                self.logger.info(f"   {metric_name}: {value:.2f}")
            else:
                self.logger.info(f"   {metric_name}: {value}")


# Export key components
__all__ = [
    'setup_comprehensive_logging',
    'get_component_logger', 
    'FrameworkLoggerMixin',
    'PerformanceLogger',
    'QualityLogger'
]
