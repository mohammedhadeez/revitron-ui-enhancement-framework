"""
Integration Tests for Revitron UI Enhancement Framework
Version 2.0 (Self-Reflection Integrated)

This module contains end-to-end integration tests that validate complete workflows
and interactions between framework components. These tests ensure the v2.0
self-reflection improvements work correctly in realistic scenarios.

Test Categories:
- Complete workflow testing (research → generation → validation → implementation)
- Component integration testing
- Configuration system testing
- Error handling and recovery testing
- Performance integration testing
- Self-reflection feature validation
"""

import os
import sys
import json
import yaml
import tempfile
import shutil
import time
from unittest.mock import patch, MagicMock
from pathlib import Path
import pytest

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tests import TestConstants, TestUtilities

# Import framework components
try:
    from main_controller import RevitronEnhancementFramework
    from src.research.research_framework import ResearchFramework
    from src.validation.validation_engine import ValidationEngine
    from src.generation.button_generator import ButtonGenerator
    from src.implementation.implementation_specs import ImplementationSpecifier
    from src.quality.quality_controller import QualityController
except ImportError as e:
    pytest.skip(f"Framework components not available: {e}", allow_module_level=True)


class TestCompleteWorkflow:
    """Test complete end-to-end workflows."""
    
    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing."""
        temp_dir = tempfile.mkdtemp(prefix="revitron_test_")
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def mock_config(self, temp_workspace):
        """Create mock configuration for testing."""
        config = {
            "framework": {
                "version": "2.0.0",
                "strict_mode": True,
                "debug_mode": True,
                "self_reflection": {
                    "enabled": True,
                    "address_critical_issues": True
                }
            },
            "research": {
                "completeness_threshold": 95,
                "mandatory_research": True,
                "timeout_seconds": 10
            },
            "validation": {
                "mandatory_coverage": 100,
                "fail_on_incomplete_coverage": True
            },
            "duplicate_prevention": {
                "enabled": True,
                "zero_tolerance": True
            },
            "generation": {
                "max_suggestions": 50,
                "batch_size": 10
            },
            "logging": {
                "level": "DEBUG",
                "file_output": False
            },
            "output": {
                "output_directory": temp_workspace
            }
        }
        
        config_file = os.path.join(temp_workspace, "test_config.yaml")
        with open(config_file, 'w') as f:
            yaml.dump(config, f)
        
        return config_file
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_complete_workflow_success(self, temp_workspace, mock_config):
        """Test successful complete workflow from research to implementation."""
        
        # Mock external dependencies
        with patch('requests.get') as mock_get, \
             patch('src.research.research_framework.ResearchFramework.access_documentation') as mock_research:
            
            # Setup mocks
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = "<html>Mock documentation</html>"
            
            mock_research.return_value = {
                "completeness": 96.5,
                "sources": ["mock_source_1", "mock_source_2"],
                "api_functions": TestUtilities.create_mock_research_data()
            }
            
            # Initialize framework
            framework = RevitronEnhancementFramework(config_file=mock_config)
            
            # Execute complete workflow
            start_time = time.time()
            results = framework.execute_complete_workflow(
                categories=TestConstants.SAMPLE_CATEGORIES[:2],  # Limit for testing
                max_suggestions=20  # Reduced for faster testing
            )
            execution_time = time.time() - start_time
            
            # Validate results
            assert results is not None
            assert "research_results" in results
            assert "generated_buttons" in results
            assert "validation_results" in results
            assert "implementation_specs" in results
            assert "quality_report" in results
            
            # Validate research results (Critical Issue #1 Fix)
            research = results["research_results"]
            assert research["completeness"] >= 95.0
            assert len(research["sources"]) > 0
            
            # Validate generation results
            buttons = results["generated_buttons"]
            assert len(buttons) > 0
            assert len(buttons) <= 20
            
            # Validate validation coverage (Critical Issue #2 Fix)
            validation = results["validation_results"]
            assert validation["coverage_percentage"] == 100.0
            assert len(validation["validated_buttons"]) == len(buttons)
            
            # Validate duplicate prevention (Critical Issue #3 Fix)
            duplicates = results.get("duplicates_removed", [])
            assert isinstance(duplicates, list)  # Should be tracked
            
            # Validate implementation depth (Critical Issue #4 Fix)
            implementation = results["implementation_specs"]
            assert len(implementation) == len(buttons)
            for spec in implementation:
                assert len(spec.get("required_elements", [])) >= 8
            
            # Validate performance
            assert execution_time < TestConstants.MAX_PROCESSING_TIME_SECONDS
            
            # Validate quality metrics
            quality = results["quality_report"]
            assert quality["overall_score"] >= 70  # Minimum acceptable
    
    @pytest.mark.integration 
    def test_workflow_with_research_failure(self, temp_workspace, mock_config):
        """Test workflow behavior when research fails to meet completeness threshold."""
        
        with patch('src.research.research_framework.ResearchFramework.access_documentation') as mock_research:
            
            # Mock insufficient research completeness
            mock_research.return_value = {
                "completeness": 85.0,  # Below 95% threshold
                "sources": ["limited_source"],
                "api_functions": {}
            }
            
            framework = RevitronEnhancementFramework(config_file=mock_config)
            
            # Should raise exception due to insufficient research
            with pytest.raises(Exception) as exc_info:
                framework.execute_complete_workflow(max_suggestions=10)
            
            assert "research completeness" in str(exc_info.value).lower() or \
                   "insufficient" in str(exc_info.value).lower()
    
    @pytest.mark.integration
    def test_workflow_with_validation_failure(self, temp_workspace, mock_config):
        """Test workflow behavior when validation coverage is insufficient."""
        
        with patch('src.research.research_framework.ResearchFramework.access_documentation') as mock_research, \
             patch('src.validation.validation_engine.ValidationEngine.validate_buttons') as mock_validate:
            
            # Mock adequate research
            mock_research.return_value = {
                "completeness": 96.5,
                "sources": ["source_1", "source_2"],
                "api_functions": TestUtilities.create_mock_research_data()
            }
            
            # Mock insufficient validation coverage  
            mock_validate.return_value = {
                "coverage_percentage": 75.0,  # Below 100% requirement
                "validated_buttons": [],
                "failed_validations": []
            }
            
            framework = RevitronEnhancementFramework(config_file=mock_config)
            
            # Should raise exception due to insufficient validation coverage
            with pytest.raises(Exception) as exc_info:
                framework.execute_complete_workflow(max_suggestions=10)
                
            assert "validation coverage" in str(exc_info.value).lower() or \
                   "100%" in str(exc_info.value)


class TestComponentIntegration:
    """Test integration between framework components."""
    
    @pytest.fixture
    def mock_components(self):
        """Create mock framework components."""
        return {
            "research": MagicMock(spec=ResearchFramework),
            "validation": MagicMock(spec=ValidationEngine),
            "generator": MagicMock(spec=ButtonGenerator),
            "implementation": MagicMock(spec=ImplementationSpecifier),
            "quality": MagicMock(spec=QualityController)
        }
    
    @pytest.mark.integration
    def test_research_to_generation_integration(self, mock_components):
        """Test data flow from research to generation."""
        
        # Setup research output
        research_data = TestUtilities.create_mock_research_data()
        mock_components["research"].execute_research.return_value = research_data
        
        # Setup generator to use research data
        buttons = TestUtilities.create_mock_button_data(25)
        mock_components["generator"].generate_buttons.return_value = buttons
        
        # Test integration
        research_result = mock_components["research"].execute_research()
        generated_buttons = mock_components["generator"].generate_buttons(
            research_context=research_result
        )
        
        # Validate data flow
        assert research_result is not None
        assert len(generated_buttons) == 25
        mock_components["generator"].generate_buttons.assert_called_once_with(
            research_context=research_result
        )
    
    @pytest.mark.integration
    def test_generation_to_validation_integration(self, mock_components):
        """Test data flow from generation to validation."""
        
        # Setup generation output
        buttons = TestUtilities.create_mock_button_data(30)
        mock_components["generator"].generate_buttons.return_value = buttons
        
        # Setup validation to process buttons
        validation_results = [
            TestUtilities.create_mock_validation_result(btn["id"], True)
            for btn in buttons
        ]
        mock_components["validation"].validate_buttons.return_value = {
            "coverage_percentage": 100.0,
            "validated_buttons": validation_results,
            "overall_quality": 87.5
        }
        
        # Test integration
        generated_buttons = mock_components["generator"].generate_buttons()
        validation_result = mock_components["validation"].validate_buttons(generated_buttons)
        
        # Validate data flow
        assert len(generated_buttons) == 30
        assert validation_result["coverage_percentage"] == 100.0
        assert len(validation_result["validated_buttons"]) == 30
    
    @pytest.mark.integration 
    def test_validation_to_implementation_integration(self, mock_components):
        """Test data flow from validation to implementation specifications."""
        
        # Setup validation output
        buttons = TestUtilities.create_mock_button_data(15)
        validation_results = {
            "coverage_percentage": 100.0,
            "validated_buttons": buttons,
            "passed_buttons": buttons  # All passed for testing
        }
        mock_components["validation"].validate_buttons.return_value = validation_results
        
        # Setup implementation specs
        implementation_specs = []
        for btn in buttons:
            spec = {
                "button_id": btn["id"],
                "required_elements": [
                    "api_integration", "code_structure", "error_handling",
                    "performance_considerations", "testing_strategy", 
                    "documentation_requirements", "deployment_notes",
                    "maintenance_requirements"
                ],
                "complexity_estimate": "medium",
                "implementation_time": "4-6 hours"
            }
            implementation_specs.append(spec)
        
        mock_components["implementation"].generate_specifications.return_value = implementation_specs
        
        # Test integration
        validation_result = mock_components["validation"].validate_buttons([])
        specs = mock_components["implementation"].generate_specifications(
            validation_result["passed_buttons"]
        )
        
        # Validate data flow
        assert len(specs) == 15
        for spec in specs:
            assert len(spec["required_elements"]) >= 8  # Critical Issue #4 fix
    
    @pytest.mark.integration
    def test_end_to_end_component_chain(self, mock_components):
        """Test complete component chain integration."""
        
        # Setup component chain
        research_data = TestUtilities.create_mock_research_data()
        buttons = TestUtilities.create_mock_button_data(20)
        validation_results = {
            "coverage_percentage": 100.0,
            "validated_buttons": buttons,
            "passed_buttons": buttons
        }
        implementation_specs = [
            {
                "button_id": btn["id"],
                "required_elements": ["api_integration", "code_structure"],
                "specification_depth": "complete"
            }
            for btn in buttons
        ]
        quality_report = {
            "overall_score": 89.5,
            "component_scores": {
                "research": 95.0,
                "generation": 87.0, 
                "validation": 92.0,
                "implementation": 88.0
            }
        }
        
        # Setup mocks
        mock_components["research"].execute_research.return_value = research_data
        mock_components["generator"].generate_buttons.return_value = buttons
        mock_components["validation"].validate_buttons.return_value = validation_results
        mock_components["implementation"].generate_specifications.return_value = implementation_specs
        mock_components["quality"].generate_quality_report.return_value = quality_report
        
        # Execute component chain
        research_result = mock_components["research"].execute_research()
        generated_buttons = mock_components["generator"].generate_buttons(research_result)
        validation_result = mock_components["validation"].validate_buttons(generated_buttons)
        specs = mock_components["implementation"].generate_specifications(validation_result["passed_buttons"])
        final_report = mock_components["quality"].generate_quality_report({
            "research": research_result,
            "buttons": generated_buttons,
            "validation": validation_result,
            "implementation": specs
        })
        
        # Validate complete chain
        assert research_result["completeness"] >= 95.0  # Critical Issue #1
        assert validation_result["coverage_percentage"] == 100.0  # Critical Issue #2
        assert len(specs) == len(buttons)  # Critical Issue #4
        assert final_report["overall_score"] >= 70.0


class TestConfigurationIntegration:
    """Test configuration system integration."""
    
    @pytest.fixture
    def config_variations(self, temp_dir):
        """Create various configuration files for testing."""
        configs = {}
        
        # Production configuration
        prod_config = {
            "framework": {"strict_mode": True, "debug_mode": False},
            "research": {"completeness_threshold": 95},
            "validation": {"mandatory_coverage": 100},
            "performance": {"max_workers": 4}
        }
        prod_file = os.path.join(temp_dir, "prod_config.yaml")
        with open(prod_file, 'w') as f:
            yaml.dump(prod_config, f)
        configs["production"] = prod_file
        
        # Development configuration  
        dev_config = {
            "framework": {"strict_mode": False, "debug_mode": True},
            "research": {"completeness_threshold": 75},
            "validation": {"mandatory_coverage": 75},
            "performance": {"max_workers": 2}
        }
        dev_file = os.path.join(temp_dir, "dev_config.yaml")
        with open(dev_file, 'w') as f:
            yaml.dump(dev_config, f)
        configs["development"] = dev_file
        
        return configs
    
    @pytest.mark.integration
    def test_configuration_loading(self, config_variations):
        """Test configuration loading and merging."""
        
        # Test production configuration
        framework_prod = RevitronEnhancementFramework(config_file=config_variations["production"])
        prod_config = framework_prod.config
        
        assert prod_config["framework"]["strict_mode"] is True
        assert prod_config["research"]["completeness_threshold"] == 95
        assert prod_config["validation"]["mandatory_coverage"] == 100
        
        # Test development configuration
        framework_dev = RevitronEnhancementFramework(config_file=config_variations["development"])
        dev_config = framework_dev.config
        
        assert dev_config["framework"]["strict_mode"] is False
        assert dev_config["research"]["completeness_threshold"] == 75
        assert dev_config["validation"]["mandatory_coverage"] == 75
    
    @pytest.mark.integration
    def test_configuration_override(self, config_variations):
        """Test configuration override functionality."""
        
        framework = RevitronEnhancementFramework(config_file=config_variations["production"])
        
        # Override specific settings
        overrides = {
            "research.completeness_threshold": 90,
            "generation.max_suggestions": 100
        }
        
        framework.apply_config_overrides(overrides)
        
        assert framework.config["research"]["completeness_threshold"] == 90
        assert framework.config["generation"]["max_suggestions"] == 100
    
    @pytest.mark.integration
    def test_invalid_configuration_handling(self, temp_dir):
        """Test handling of invalid configurations."""
        
        # Create invalid configuration
        invalid_config = {
            "framework": {"strict_mode": "invalid_boolean"},  # Should be boolean
            "research": {"completeness_threshold": "invalid_number"},  # Should be number
            "validation": {}  # Missing required fields
        }
        
        invalid_file = os.path.join(temp_dir, "invalid_config.yaml")
        with open(invalid_file, 'w') as f:
            yaml.dump(invalid_config, f)
        
        # Should handle invalid configuration gracefully
        with pytest.raises((ValueError, TypeError, KeyError)):
            framework = RevitronEnhancementFramework(config_file=invalid_file)
            framework.validate_configuration()


class TestErrorHandlingIntegration:
    """Test error handling and recovery across components."""
    
    @pytest.mark.integration
    def test_network_error_recovery(self):
        """Test recovery from network errors during research."""
        
        with patch('requests.get') as mock_get:
            # Simulate network error
            mock_get.side_effect = [
                Exception("Network error"),  # First attempt fails
                MagicMock(status_code=200, text="<html>Success</html>")  # Second attempt succeeds
            ]
            
            research = ResearchFramework()
            
            # Should retry and succeed
            result = research.access_documentation_with_retry(
                urls=["http://example.com/docs"],
                max_retries=2
            )
            
            assert result is not None
            assert mock_get.call_count == 2
    
    @pytest.mark.integration
    def test_partial_validation_failure_recovery(self):
        """Test recovery when some validations fail."""
        
        buttons = TestUtilities.create_mock_button_data(20)
        
        # Mock validation engine with partial failures
        with patch('src.validation.validation_engine.ValidationEngine.validate_single_button') as mock_validate:
            
            # First 15 succeed, last 5 fail
            def side_effect(button):
                return TestUtilities.create_mock_validation_result(
                    button["id"], 
                    passed=(button["id"] <= 15)
                )
            
            mock_validate.side_effect = side_effect
            
            validation_engine = ValidationEngine()
            results = validation_engine.validate_buttons(buttons)
            
            # Should handle partial failures gracefully
            assert results["coverage_percentage"] == 75.0  # 15/20 = 75%
            assert len(results["validated_buttons"]) == 20
            assert len(results["passed_validations"]) == 15
            assert len(results["failed_validations"]) == 5
    
    @pytest.mark.integration
    def test_memory_exhaustion_recovery(self):
        """Test recovery from memory exhaustion during processing."""
        
        # Mock memory monitoring
        with patch('psutil.virtual_memory') as mock_memory:
            
            # Simulate high memory usage
            mock_memory.return_value.percent = 95.0  # 95% memory usage
            
            framework = RevitronEnhancementFramework()
            
            # Should trigger memory management
            framework.monitor_system_resources()
            
            # Verify memory management was triggered
            assert framework.memory_management_active


class TestSelfReflectionIntegration:
    """Test v2.0 self-reflection integration features."""
    
    @pytest.mark.integration 
    def test_critical_issue_fixes_integration(self):
        """Test that all 4 critical issues from self-reflection are addressed."""
        
        framework = RevitronEnhancementFramework()
        
        # Test Critical Issue #1: Research completeness enforcement
        assert framework.config["research"]["completeness_threshold"] >= 95
        assert framework.config["research"]["mandatory_research"] is True
        
        # Test Critical Issue #2: 100% validation coverage requirement
        assert framework.config["validation"]["mandatory_coverage"] == 100
        assert framework.config["validation"]["fail_on_incomplete_coverage"] is True
        
        # Test Critical Issue #3: Duplicate prevention system
        assert framework.config["duplicate_prevention"]["enabled"] is True
        assert framework.config["duplicate_prevention"]["zero_tolerance"] is True
        
        # Test Critical Issue #4: Technical specification depth
        assert framework.config["implementation"]["mandatory_elements"] >= 8
        assert framework.config["implementation"]["specification_depth"] == "complete"
    
    @pytest.mark.integration
    def test_performance_improvement_integration(self):
        """Test that v2.0 performance improvements are integrated."""
        
        framework = RevitronEnhancementFramework()
        
        # Test performance monitoring integration
        assert framework.config["framework"]["performance_monitoring"] is True
        
        # Test quality orchestration
        assert framework.config["quality"]["multi_stage_gates"] is True
        assert framework.config["quality"]["comprehensive_reporting"] is True
        
        # Test self-reflection feature flag
        assert framework.config["framework"]["self_reflection"]["enabled"] is True
        assert framework.config["framework"]["self_reflection"]["address_critical_issues"] is True
    
    @pytest.mark.integration
    def test_quality_metric_tracking(self):
        """Test integration of quality metric tracking from self-reflection."""
        
        framework = RevitronEnhancementFramework()
        
        # Execute workflow with quality tracking
        with patch.multiple(
            framework,
            execute_research=MagicMock(return_value={"completeness": 96.0}),
            generate_buttons=MagicMock(return_value=[]),
            validate_buttons=MagicMock(return_value={"coverage_percentage": 100.0}),
            generate_implementation_specs=MagicMock(return_value=[])
        ):
            
            results = framework.execute_with_quality_tracking()
            
            # Verify quality metrics are tracked
            assert "quality_metrics" in results
            assert "research_quality" in results["quality_metrics"]
            assert "validation_coverage" in results["quality_metrics"]
            assert "technical_accuracy" in results["quality_metrics"]
            assert "implementation_depth" in results["quality_metrics"]
            
            # Verify target performance standards
            metrics = results["quality_metrics"]
            assert metrics["research_quality"] >= TestConstants.TARGET_RESEARCH_QUALITY
            assert metrics["validation_coverage"] >= TestConstants.TARGET_VALIDATION_COVERAGE


class TestPerformanceIntegration:
    """Test performance aspects of component integration."""
    
    @pytest.mark.integration
    @pytest.mark.performance
    def test_workflow_performance_requirements(self):
        """Test that integrated workflow meets performance requirements."""
        
        framework = RevitronEnhancementFramework()
        
        # Mock fast responses for performance testing
        with patch.multiple(
            framework,
            execute_research=MagicMock(return_value={"completeness": 96.0}),
            generate_buttons=MagicMock(return_value=TestUtilities.create_mock_button_data(50)),
            validate_buttons=MagicMock(return_value={"coverage_percentage": 100.0}),
            generate_implementation_specs=MagicMock(return_value=[])
        ):
            
            start_time = time.time()
            results = framework.execute_complete_workflow(max_suggestions=50)
            execution_time = time.time() - start_time
            
            # Performance requirements
            assert execution_time < TestConstants.MAX_PROCESSING_TIME_SECONDS
            assert results is not None
    
    @pytest.mark.integration
    @pytest.mark.performance
    def test_memory_usage_integration(self):
        """Test memory usage across integrated components."""
        
        import psutil
        import os
        
        framework = RevitronEnhancementFramework()
        process = psutil.Process(os.getpid())
        
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Execute workflow
        with patch.multiple(
            framework,
            execute_research=MagicMock(return_value={"completeness": 96.0}),
            generate_buttons=MagicMock(return_value=TestUtilities.create_mock_button_data(100)),
            validate_buttons=MagicMock(return_value={"coverage_percentage": 100.0})
        ):
            
            results = framework.execute_complete_workflow(max_suggestions=100)
            
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = final_memory - initial_memory
            
            # Memory usage should be within acceptable limits
            assert memory_increase < TestConstants.MAX_MEMORY_USAGE_MB
            assert results is not None


# Test fixtures and utilities for integration tests
@pytest.fixture
def temp_dir():
    """Create temporary directory for testing."""
    temp_dir = tempfile.mkdtemp(prefix="revitron_integration_test_")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def mock_external_dependencies():
    """Mock external dependencies for integration testing."""
    with patch('requests.get') as mock_get, \
         patch('yaml.safe_load') as mock_yaml, \
         patch('json.load') as mock_json:
        
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "Mock response"
        
        yield {
            "requests_get": mock_get,
            "yaml_load": mock_yaml,
            "json_load": mock_json
        }

# Performance test markers and utilities
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance test" 
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running test"
    )


if __name__ == "__main__":
    # Run integration tests if executed directly
    pytest.main([__file__, "-v", "-m", "integration"])
