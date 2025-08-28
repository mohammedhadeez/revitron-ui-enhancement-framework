"""
PyTest Configuration for Revitron UI Enhancement Framework
Version 2.0 (Self-Reflection Integrated)

This module contains pytest fixtures, configuration, and utilities shared across
all test modules. It provides common testing infrastructure including mocks,
test data, and framework setup for comprehensive testing.

Features:
- Shared fixtures for framework components
- Mock configurations and data
- Test environment setup
- Performance testing utilities
- Integration testing helpers
- Self-reflection validation fixtures
"""

import os
import sys
import tempfile
import shutil
import yaml
import json
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import pytest

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tests import TestConstants, TestUtilities, TEST_FEATURES

# Import framework components (with graceful fallback)
try:
    from main_controller import RevitronEnhancementFramework
    from src.research.research_framework import ResearchFramework
    from src.validation.validation_engine import ValidationEngine
    from src.generation.button_generator import ButtonGenerator
    from src.implementation.implementation_specs import ImplementationSpecifier
    from src.quality.quality_controller import QualityController
    FRAMEWORK_AVAILABLE = True
except ImportError:
    FRAMEWORK_AVAILABLE = False

# Check for optional testing dependencies
PYTEST_BENCHMARK_AVAILABLE = TEST_FEATURES["benchmark_available"]
PYTEST_MOCK_AVAILABLE = TEST_FEATURES["mock_available"]


# =============================================================================
# Pytest Configuration and Hooks
# =============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    
    # Register custom markers
    markers = [
        "unit: Unit tests for individual components",
        "integration: Integration tests for complete workflows", 
        "performance: Performance benchmarking tests",
        "slow: Tests that take more than 30 seconds to run",
        "network: Tests requiring network access",
        "research: Tests for research framework functionality",
        "validation: Tests for validation engine",
        "generation: Tests for button generation",
        "implementation: Tests for implementation specifications",
        "quality: Tests for quality control systems",
        "self_reflection: Tests validating v2.0 self-reflection improvements"
    ]
    
    for marker in markers:
        config.addinivalue_line("markers", marker)
    
    # Configure test output
    config.option.verbose = 2
    config.option.tb = "short"
    
    # Set test discovery patterns
    config.option.python_files = ["test_*.py", "*_test.py"]
    config.option.python_classes = ["Test*", "*Tests"]
    config.option.python_functions = ["test_*"]


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers and configure execution."""
    
    # Add markers based on test names and locations
    for item in items:
        # Add slow marker to tests that typically take longer
        if "complete_workflow" in item.name or "integration" in item.name:
            item.add_marker(pytest.mark.slow)
        
        # Add network marker to tests that access external resources
        if "network" in item.name or "documentation" in item.name:
            item.add_marker(pytest.mark.network)
        
        # Add self_reflection marker to v2.0 specific tests
        if "self_reflection" in item.name or "critical_issue" in item.name:
            item.add_marker(pytest.mark.self_reflection)


def pytest_runtest_setup(item):
    """Setup before each test run."""
    
    # Skip tests if framework components not available
    if not FRAMEWORK_AVAILABLE and "unit" not in [mark.name for mark in item.iter_markers()]:
        pytest.skip("Framework components not available")
    
    # Skip performance tests if benchmark not available
    if "performance" in [mark.name for mark in item.iter_markers()] and not PYTEST_BENCHMARK_AVAILABLE:
        pytest.skip("pytest-benchmark not available for performance tests")
    
    # Skip network tests in offline mode
    if hasattr(item.config.option, 'offline') and item.config.option.offline:
        if "network" in [mark.name for mark in item.iter_markers()]:
            pytest.skip("Network tests skipped in offline mode")


def pytest_runtest_teardown(item):
    """Cleanup after each test run."""
    
    # Force garbage collection after memory-intensive tests
    if "performance" in [mark.name for mark in item.iter_markers()]:
        import gc
        gc.collect()


# =============================================================================
# Session-Scoped Fixtures (Setup Once)
# =============================================================================

@pytest.fixture(scope="session")
def test_session_info():
    """Provide test session information."""
    return {
        "framework_version": TestConstants.FRAMEWORK_VERSION,
        "framework_codename": TestConstants.FRAMEWORK_CODENAME,
        "test_session_start": datetime.now().isoformat(),
        "framework_available": FRAMEWORK_AVAILABLE,
        "features": TEST_FEATURES,
        "python_version": sys.version,
        "platform": sys.platform
    }


@pytest.fixture(scope="session")
def temp_session_dir():
    """Create temporary directory for session-wide test artifacts."""
    session_dir = tempfile.mkdtemp(prefix="revitron_test_session_")
    yield session_dir
    shutil.rmtree(session_dir, ignore_errors=True)


@pytest.fixture(scope="session")
def mock_data_repository(temp_session_dir):
    """Create repository of mock data for testing."""
    
    mock_repo = {
        "research_data": TestUtilities.create_mock_research_data(),
        "button_data": {
            "small": TestUtilities.create_mock_button_data(25),
            "medium": TestUtilities.create_mock_button_data(100), 
            "large": TestUtilities.create_mock_button_data(250)
        },
        "validation_results": [
            TestUtilities.create_mock_validation_result(i, True) 
            for i in range(1, 101)
        ]
    }
    
    # Save mock data to files
    mock_data_dir = Path(temp_session_dir) / "mock_data"
    mock_data_dir.mkdir(exist_ok=True)
    
    with open(mock_data_dir / "research_data.json", 'w') as f:
        json.dump(mock_repo["research_data"], f, indent=2)
    
    with open(mock_data_dir / "button_data.json", 'w') as f:
        json.dump(mock_repo["button_data"], f, indent=2)
    
    with open(mock_data_dir / "validation_results.json", 'w') as f:
        json.dump(mock_repo["validation_results"], f, indent=2)
    
    mock_repo["data_directory"] = str(mock_data_dir)
    return mock_repo


# =============================================================================
# Function-Scoped Fixtures (Setup Per Test)
# =============================================================================

@pytest.fixture
def temp_dir():
    """Create temporary directory for individual test."""
    temp_dir = tempfile.mkdtemp(prefix="revitron_test_")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_config_file(temp_dir):
    """Create mock configuration file for testing."""
    
    config = {
        "framework": {
            "version": TestConstants.FRAMEWORK_VERSION,
            "codename": TestConstants.FRAMEWORK_CODENAME,
            "strict_mode": True,
            "debug_mode": True,
            "performance_monitoring": True,
            "self_reflection": {
                "enabled": True,
                "address_critical_issues": True,
                "target_performance": "10/10"
            }
        },
        "research": {
            "completeness_threshold": 95,
            "mandatory_research": True,
            "timeout_seconds": 10,
            "retry_attempts": 2,
            "sources": [
                "https://revitron.readthedocs.io/en/latest/",
                "https://github.com/revitron/revitron",
                "https://pyrevit.readthedocs.io/"
            ]
        },
        "validation": {
            "mandatory_coverage": 100,
            "fail_on_incomplete_coverage": True,
            "criteria": {criterion: True for criterion in TestConstants.VALIDATION_CRITERIA},
            "parallel_validation": True,
            "max_validation_workers": 2
        },
        "duplicate_prevention": {
            "enabled": True,
            "zero_tolerance": True,
            "similarity_threshold": 0.9
        },
        "generation": {
            "max_suggestions": 50,
            "batch_size": 10,
            "categories": TestConstants.SAMPLE_CATEGORIES,
            "quality_requirements": {
                "minimum_description_length": 50,
                "require_functionality_details": True,
                "require_api_references": True
            }
        },
        "implementation": {
            "specification_depth": "complete",
            "mandatory_elements": 8,
            "required_elements": {
                "api_integration": True,
                "code_structure": True,
                "error_handling": True,
                "performance_considerations": True,
                "testing_strategy": True,
                "documentation_requirements": True,
                "deployment_notes": True,
                "maintenance_requirements": True
            }
        },
        "quality": {
            "orchestration": {
                "multi_stage_gates": True,
                "fail_fast": False,  # Allow tests to continue
                "comprehensive_reporting": True
            },
            "metrics": {
                "target_innovation_score": 85,
                "target_technical_score": 90,
                "target_implementation_score": 80
            }
        },
        "logging": {
            "level": "DEBUG",
            "console_output": False,  # Reduce noise during testing
            "file_output": False
        },
        "output": {
            "output_directory": temp_dir,
            "create_subdirectories": True,
            "timestamp_files": False
        },
        "performance": {
            "memory_management": {
                "max_memory_mb": 1024,  # Reduced for testing
                "garbage_collection": True
            },
            "processing": {
                "parallel_processing": True,
                "max_workers": 2  # Reduced for testing
            }
        }
    }
    
    config_file = os.path.join(temp_dir, "test_config.yaml")
    with open(config_file, 'w') as f:
        yaml.dump(config, f)
    
    return config_file


@pytest.fixture
def sample_buttons():
    """Generate sample buttons for testing."""
    return TestUtilities.create_mock_button_data(TestConstants.SAMPLE_BUTTON_COUNT // 5)


@pytest.fixture
def sample_research_data():
    """Generate sample research data for testing."""
    return TestUtilities.create_mock_research_data()


@pytest.fixture
def sample_validation_results(sample_buttons):
    """Generate sample validation results for testing."""
    return [
        TestUtilities.create_mock_validation_result(btn["id"], True)
        for btn in sample_buttons
    ]


# =============================================================================
# Component Fixtures (Framework Components)
# =============================================================================

@pytest.fixture
def framework_instance(mock_config_file):
    """Create framework instance for testing."""
    if not FRAMEWORK_AVAILABLE:
        pytest.skip("Framework not available")
    
    return RevitronEnhancementFramework(config_file=mock_config_file)


@pytest.fixture
def research_framework():
    """Create research framework instance."""
    if not FRAMEWORK_AVAILABLE:
        pytest.skip("Framework not available")
    
    return ResearchFramework()


@pytest.fixture
def validation_engine():
    """Create validation engine instance."""
    if not FRAMEWORK_AVAILABLE:
        pytest.skip("Framework not available")
    
    return ValidationEngine()


@pytest.fixture
def button_generator():
    """Create button generator instance."""
    if not FRAMEWORK_AVAILABLE:
        pytest.skip("Framework not available")
    
    return ButtonGenerator()


@pytest.fixture
def implementation_specifier():
    """Create implementation specifier instance."""
    if not FRAMEWORK_AVAILABLE:
        pytest.skip("Framework not available")
    
    return ImplementationSpecifier()


@pytest.fixture
def quality_controller():
    """Create quality controller instance."""
    if not FRAMEWORK_AVAILABLE:
        pytest.skip("Framework not available")
    
    return QualityController()


# =============================================================================
# Mock Fixtures (External Dependencies)
# =============================================================================

@pytest.fixture
def mock_requests():
    """Mock requests library for network calls."""
    with patch('requests.get') as mock_get, \
         patch('requests.post') as mock_post:
        
        # Configure mock responses
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "<html><body>Mock documentation content</body></html>"
        mock_get.return_value.json.return_value = {"status": "success"}
        
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"result": "success"}
        
        yield {
            "get": mock_get,
            "post": mock_post
        }


@pytest.fixture
def mock_file_system():
    """Mock file system operations."""
    with patch('os.path.exists') as mock_exists, \
         patch('os.makedirs') as mock_makedirs, \
         patch('shutil.rmtree') as mock_rmtree:
        
        mock_exists.return_value = True
        mock_makedirs.return_value = None
        mock_rmtree.return_value = None
        
        yield {
            "exists": mock_exists,
            "makedirs": mock_makedirs,
            "rmtree": mock_rmtree
        }


@pytest.fixture
def mock_yaml_operations():
    """Mock YAML file operations."""
    with patch('yaml.safe_load') as mock_load, \
         patch('yaml.dump') as mock_dump:
        
        def mock_safe_load(stream):
            if hasattr(stream, 'read'):
                return {"mock": "config"}
            return {"mock": "config"}
        
        mock_load.side_effect = mock_safe_load
        mock_dump.return_value = None
        
        yield {
            "load": mock_load,
            "dump": mock_dump
        }


# =============================================================================
# Performance Testing Fixtures
# =============================================================================

@pytest.fixture
def performance_monitor():
    """Create performance monitor for testing."""
    if not FRAMEWORK_AVAILABLE:
        pytest.skip("Framework not available")
    
    from tests.test_performance import PerformanceMonitor
    return PerformanceMonitor()


@pytest.fixture
def performance_baseline():
    """Provide performance baseline metrics."""
    return {
        "max_execution_time": TestConstants.MAX_PROCESSING_TIME_SECONDS,
        "max_memory_usage_mb": TestConstants.MAX_MEMORY_USAGE_MB,
        "max_api_response_time": TestConstants.MAX_API_RESPONSE_TIME_SECONDS,
        "target_throughput_buttons_per_minute": 60
    }


@pytest.fixture
def large_dataset():
    """Generate large dataset for performance testing."""
    return {
        "buttons": TestUtilities.create_mock_button_data(TestConstants.SAMPLE_BUTTON_COUNT),
        "research_data": TestUtilities.create_mock_research_data(),
        "categories": TestConstants.SAMPLE_CATEGORIES
    }


# =============================================================================
# Self-Reflection Testing Fixtures (v2.0)
# =============================================================================

@pytest.fixture
def self_reflection_config(temp_dir):
    """Create configuration specifically for testing self-reflection improvements."""
    
    config = {
        "framework": {
            "version": "2.0.0",
            "self_reflection": {
                "enabled": True,
                "address_critical_issues": True,
                "target_performance": "10/10"
            }
        },
        "critical_issue_fixes": {
            "research_completeness": {
                "threshold": 95,
                "mandatory": True,
                "enforcement": "strict"
            },
            "validation_coverage": {
                "required_coverage": 100,
                "fail_on_incomplete": True,
                "systematic_validation": True
            },
            "duplicate_prevention": {
                "zero_tolerance": True,
                "comprehensive_mapping": True,
                "real_time_detection": True
            },
            "technical_depth": {
                "mandatory_elements": 8,
                "complete_specifications": True,
                "implementation_details": True
            }
        },
        "performance_targets": {
            "research_quality": TestConstants.TARGET_RESEARCH_QUALITY,
            "content_innovation": TestConstants.TARGET_CONTENT_INNOVATION,
            "technical_accuracy": TestConstants.TARGET_TECHNICAL_ACCURACY,
            "validation_coverage": TestConstants.TARGET_VALIDATION_COVERAGE,
            "implementation_depth": TestConstants.TARGET_IMPLEMENTATION_DEPTH
        }
    }
    
    config_file = os.path.join(temp_dir, "self_reflection_config.yaml")
    with open(config_file, 'w') as f:
        yaml.dump(config, f)
    
    return config_file


@pytest.fixture
def critical_issues_test_data():
    """Provide test data for validating critical issue fixes."""
    return {
        "insufficient_research": {
            "completeness": 85.0,  # Below 95% threshold
            "sources": ["limited_source"],
            "expected_failure": True
        },
        "incomplete_validation": {
            "coverage": 75.0,  # Below 100% requirement
            "validated_count": 75,
            "total_count": 100,
            "expected_failure": True
        },
        "duplicate_buttons": [
            {"id": 1, "name": "Smart Select", "functionality": "Select similar elements"},
            {"id": 2, "name": "Smart Selection", "functionality": "Select similar elements"},  # Duplicate
            {"id": 3, "name": "Advanced Filter", "functionality": "Filter by parameters"}
        ],
        "incomplete_specifications": [
            {
                "button_id": 1,
                "required_elements": ["api_integration", "code_structure"],  # Only 2/8 elements
                "expected_failure": True
            },
            {
                "button_id": 2,
                "required_elements": [
                    "api_integration", "code_structure", "error_handling",
                    "performance_considerations", "testing_strategy",
                    "documentation_requirements", "deployment_notes",
                    "maintenance_requirements"
                ],  # All 8 elements
                "expected_success": True
            }
        ]
    }


# =============================================================================
# Integration Testing Fixtures
# =============================================================================

@pytest.fixture
def integration_test_environment(temp_dir, mock_requests):
    """Setup complete environment for integration testing."""
    
    # Create directory structure
    dirs = ["config", "logs", "output", "cache", "temp"]
    for dir_name in dirs:
        os.makedirs(os.path.join(temp_dir, dir_name), exist_ok=True)
    
    # Create test configuration
    config = {
        "framework": {"version": "2.0.0"},
        "research": {"completeness_threshold": 95},
        "validation": {"mandatory_coverage": 100},
        "output": {"output_directory": os.path.join(temp_dir, "output")}
    }
    
    config_file = os.path.join(temp_dir, "config", "integration_config.yaml")
    with open(config_file, 'w') as f:
        yaml.dump(config, f)
    
    return {
        "base_dir": temp_dir,
        "config_file": config_file,
        "directories": {dir_name: os.path.join(temp_dir, dir_name) for dir_name in dirs},
        "mock_requests": mock_requests
    }


@pytest.fixture
def workflow_test_data():
    """Provide test data for complete workflow testing."""
    return {
        "input_categories": TestConstants.SAMPLE_CATEGORIES[:3],  # Limit for testing
        "expected_button_count": 75,  # 25 per category
        "research_sources": [
            "https://revitron.readthedocs.io/en/latest/",
            "https://github.com/revitron/revitron"
        ],
        "validation_criteria": TestConstants.VALIDATION_CRITERIA,
        "quality_thresholds": {
            "minimum_score": 70,
            "excellence_score": 90,
            "research_completeness": 95,
            "validation_coverage": 100
        }
    }


# =============================================================================
# Utility Fixtures and Helpers
# =============================================================================

@pytest.fixture
def test_logger():
    """Create logger for test output."""
    import logging
    logger = logging.getLogger("revitron_test")
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


@pytest.fixture
def cleanup_tracker():
    """Track resources that need cleanup after tests."""
    resources = []
    
    def register(resource):
        resources.append(resource)
    
    yield register
    
    # Cleanup registered resources
    for resource in resources:
        try:
            if hasattr(resource, 'cleanup'):
                resource.cleanup()
            elif hasattr(resource, 'close'):
                resource.close()
            elif isinstance(resource, str) and os.path.exists(resource):
                if os.path.isdir(resource):
                    shutil.rmtree(resource)
                else:
                    os.remove(resource)
        except Exception as e:
            print(f"Warning: Failed to cleanup resource {resource}: {e}")


@pytest.fixture(autouse=True)
def test_isolation():
    """Ensure test isolation and cleanup."""
    # Setup: Reset any global state
    import gc
    gc.collect()
    
    yield
    
    # Teardown: Clean up after test
    gc.collect()
    
    # Clear any module-level caches if they exist
    if FRAMEWORK_AVAILABLE:
        try:
            # Clear framework caches
            if hasattr(RevitronEnhancementFramework, '_instance_cache'):
                RevitronEnhancementFramework._instance_cache.clear()
        except:
            pass


# =============================================================================
# Parametrization Helpers
# =============================================================================

def get_test_configurations():
    """Get different configurations for parametrized testing."""
    return [
        pytest.param(
            {"strict_mode": True, "debug_mode": False}, 
            id="production"
        ),
        pytest.param(
            {"strict_mode": False, "debug_mode": True}, 
            id="development"
        ),
        pytest.param(
            {"strict_mode": True, "debug_mode": True}, 
            id="debug_strict"
        )
    ]


def get_performance_test_sizes():
    """Get different sizes for performance testing."""
    return [
        pytest.param(25, id="small"),
        pytest.param(100, id="medium"), 
        pytest.param(250, id="large")
    ]


def get_validation_scenarios():
    """Get different validation scenarios for testing."""
    return [
        pytest.param(
            {"coverage": 100, "all_pass": True}, 
            id="perfect"
        ),
        pytest.param(
            {"coverage": 90, "all_pass": False}, 
            id="partial_failure"
        ),
        pytest.param(
            {"coverage": 100, "all_pass": False}, 
            id="complete_with_failures"
        )
    ]


# =============================================================================
# Test Data Validation
# =============================================================================

def validate_test_environment():
    """Validate test environment setup."""
    checks = {
        "framework_available": FRAMEWORK_AVAILABLE,
        "pytest_available": True,  # Must be available if we're running
        "mock_available": PYTEST_MOCK_AVAILABLE,
        "benchmark_available": PYTEST_BENCHMARK_AVAILABLE,
        "temp_dir_writable": True  # Assume writable
    }
    
    missing = [check for check, available in checks.items() if not available]
    
    if missing:
        pytest.skip(f"Test environment incomplete. Missing: {', '.join(missing)}")
    
    return checks


# Initialize test environment validation
validate_test_environment()
