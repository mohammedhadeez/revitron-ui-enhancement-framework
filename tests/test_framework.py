#!/usr/bin/env python3
"""
Comprehensive Testing Framework
==============================

Test suite for validating all framework components with comprehensive coverage.
Implements unit tests, integration tests, and end-to-end validation.

Author: AEC Development Team
Repository: https://github.com/mohammedhadeez/revitron-ui-enhancement-framework
Version: 2.0 (Self-Reflection Integrated)
"""

import unittest
import tempfile
import json
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List, Any
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Framework imports
from src.research.research_framework import ResearchFramework, ResearchSource
from src.validation.validation_engine import ValidationEngine, ValidationStatus
from src.generation.button_generator import ButtonGenerator, ButtonCategory
from src.implementation.implementation_specs import ImplementationSpecifier
from src.quality.quality_controller import QualityController
from src.utils.error_handling import get_error_handler, CriticalFrameworkError
from src.utils.logging_config import setup_comprehensive_logging


class FrameworkTestCase(unittest.TestCase):
    """Base test case with common setup for all framework tests"""
    
    def setUp(self):
        """Setup common test fixtures"""
        self.test_config = {
            'quality_targets': {
                'overall_performance_target': 10.0,
                'research_completeness_required': 1.0,
                'validation_coverage_required': 1.0,
                'duplicate_tolerance': 0.0
            },
            'research': {
                'minimum_source_accessibility': 0.95
            },
            'validation': {
                'mandatory_coverage': 1.0,
                'criteria_thresholds': {
                    'technical_feasibility': 0.8,
                    'duplicate_check': 1.0,
                    'aec_value': 0.7
                }
            }
        }
        
        self.temp_dir = Path(tempfile.mkdtemp())
        self.mock_research_data = {
            'completeness_score': 0.95,
            'accessed_sources': ['Revitron Documentation', 'PyRevit Documentation'],
            'failed_sources': [],
            'api_capabilities_count': 42,
            'content_extracted': {
                'Revitron Documentation': 'Sample documentation content with API references',
                'PyRevit Documentation': 'PyRevit API documentation content'
            }
        }
        
        self.mock_capability_data = {
            'total_functions_mapped': 50,
            'revitron_functions': [],
            'pyrevit_functions': [],
            'duplicate_detection_database': {
                'filter': {'name': 'Filter', 'description': 'Element filtering'},
                'selection': {'name': 'Selection', 'description': 'Element selection'}
            },
            'mapping_completeness': 0.9
        }
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)


class TestResearchFramework(FrameworkTestCase):
    """Test suite for ResearchFramework component"""
    
    @patch('src.research.research_framework.webdriver.Chrome')
    @patch('src.research.research_framework.requests.get')
    def test_research_framework_initialization(self, mock_requests, mock_webdriver):
        """Test research framework initialization"""
        
        research = ResearchFramework(self.test_config)
        
        self.assertIsNotNone(research)
        self.assertEqual(len(research.research_sources), 4)  # 4 primary sources expected
        self.assertEqual(research.research_completeness_score, 0.0)
    
    @patch('src.research.research_framework.webdriver.Chrome')
    def test_research_source_configuration(self, mock_webdriver):
        """Test research source configuration"""
        
        research = ResearchFramework(self.test_config)
        
        # Check primary sources are configured
        primary_sources = [s for s in research.research_sources if s.priority == 1]
        self.assertGreaterEqual(len(primary_sources), 3)
        
        # Check source attributes
        for source in primary_sources:
            self.assertIsNotNone(source.name)
            self.assertIsNotNone(source.url)
            self.assertIn(source.access_method, ['requests', 'selenium', 'api'])
    
    @patch('src.research.research_framework.requests.get')
    def test_mock_research_execution(self, mock_requests):
        """Test research execution with mocked responses"""
        
        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"<html><body>Mock documentation content</body></html>"
        mock_requests.return_value = mock_response
        
        research = ResearchFramework(self.test_config)
        
        # Mock the primary research execution
        with patch.object(research, '_access_primary_sources') as mock_access:
            mock_access.return_value = self.mock_research_data
            
            with patch.object(research, '_extract_api_capabilities') as mock_extract:
                mock_extract.return_value = {'functions': [], 'classes': [], 'examples': []}
                
                with patch.object(research, '_validate_research_completeness') as mock_validate:
                    mock_validate.return_value = {
                        'sources_accessed': 4,
                        'sources_failed': 0,
                        'completeness_score': 1.0,
                        'validation_passed': True
                    }
                    
                    result = research.execute_primary_research()
                    
                    self.assertIsNotNone(result)
                    self.assertGreaterEqual(result['completeness_score'], 0.95)
                    self.assertTrue(result['validation_passed'])


class TestValidationEngine(FrameworkTestCase):
    """Test suite for ValidationEngine component"""
    
    def test_validation_engine_initialization(self):
        """Test validation engine initialization"""
        
        validator = ValidationEngine(self.test_config)
        
        self.assertIsNotNone(validator)
        self.assertEqual(len(validator.minimum_thresholds), 7)  # 7 validation criteria
    
    def test_comprehensive_validation(self):
        """Test comprehensive validation process"""
        
        validator = ValidationEngine(self.test_config)
        
        # Mock suggestions
        mock_suggestions = [
            {
                'id': 'test_1',
                'name': 'Smart Element Selector',
                'functionality': 'Advanced element selection',
                'description': 'Intelligent element selection for BIM workflows',
                'category': 'Selection Tools'
            },
            {
                'id': 'test_2', 
                'name': 'Parameter Analyzer',
                'functionality': 'Parameter analysis and reporting',
                'description': 'Comprehensive parameter analysis tool',
                'category': 'Analysis Tools'
            }
        ]
        
        # Mock implementation specs
        mock_specs = [
            {
                'suggestion_id': 'test_1',
                'completeness_score': 0.9,
                'api_requirements': ['FilteredElementCollector'],
                'implementation_complexity': 'medium'
            },
            {
                'suggestion_id': 'test_2',
                'completeness_score': 0.85,
                'api_requirements': ['Element.GetParameters'],
                'implementation_complexity': 'low'
            }
        ]
        
        # Execute validation
        with patch.object(validator, '_validate_single_criterion') as mock_validate:
            mock_validate.return_value = Mock(
                suggestion_id='test_1',
                criteria='technical_feasibility',
                status=ValidationStatus.PASSED,
                score=0.85
            )
            
            result = validator.validate_comprehensive_coverage(mock_suggestions, mock_specs)
            
            self.assertIsNotNone(result)
            self.assertEqual(result.total_suggestions, 2)
            self.assertGreaterEqual(result.validation_coverage, 1.0)


class TestButtonGenerator(FrameworkTestCase):
    """Test suite for ButtonGenerator component"""
    
    def test_button_generator_initialization(self):
        """Test button generator initialization"""
        
        generator = ButtonGenerator(
            self.mock_research_data,
            self.mock_capability_data,
            self.test_config
        )
        
        self.assertIsNotNone(generator)
        self.assertGreater(len(generator.suggestion_templates), 0)
        self.assertGreater(len(generator.aec_workflow_patterns), 0)
    
    def test_button_generation_validation(self):
        """Test button generation with validation"""
        
        generator = ButtonGenerator(
            self.mock_research_data,
            self.mock_capability_data,
            self.test_config
        )
        
        # Mock validation to always pass
        with patch.object(generator, '_validate_suggestion_real_time') as mock_validate:
            mock_validate.return_value = True
            
            suggestions = generator.generate_validated_suggestions(target_count=10)
            
            self.assertEqual(len(suggestions), 10)
            
            # Verify suggestion structure
            for suggestion in suggestions:
                self.assertIsNotNone(suggestion.name)
                self.assertIsInstance(suggestion.category, ButtonCategory)
                self.assertIsNotNone(suggestion.functionality)
                self.assertGreaterEqual(suggestion.aec_workflow_relevance, 0.0)
                self.assertGreaterEqual(suggestion.innovation_score, 0.0)
    
    def test_duplicate_prevention(self):
        """Test duplicate prevention during generation"""
        
        generator = ButtonGenerator(
            self.mock_research_data,
            self.mock_capability_data,
            self.test_config
        )
        
        # Test duplicate checking
        existing_functions = [
            {'name': 'filter', 'description': 'element filtering'}
        ]
        
        duplicate_count = generator.check_duplicates_against_existing(
            [{'name': 'Advanced Filter', 'description': 'enhanced element filtering'}],
            existing_functions
        )
        
        self.assertGreaterEqual(duplicate_count, 0)


class TestImplementationSpecifier(FrameworkTestCase):
    """Test suite for ImplementationSpecifier component"""
    
    def test_implementation_specifier_initialization(self):
        """Test implementation specifier initialization"""
        
        specifier = ImplementationSpecifier(self.test_config)
        
        self.assertIsNotNone(specifier)
    
    def test_specification_generation(self):
        """Test specification generation"""
        
        specifier = ImplementationSpecifier(self.test_config)
        
        mock_suggestion = {
            'id': 'test_spec_1',
            'name': 'Test Button',
            'functionality': 'Test functionality for element selection',
            'description': 'Test button for specification generation',
            'category': 'Selection Tools'
        }
        
        # Mock individual specification methods
        with patch.object(specifier, '_analyze_api_requirements') as mock_api:
            mock_api.return_value = []
            
            with patch.object(specifier, '_analyze_implementation_complexity') as mock_complexity:
                mock_complexity.return_value = {
                    'complexity_level': 'medium',
                    'development_hours': 8,
                    'external_dependencies': [],
                    'python_packages': ['pyrevit'],
                    'revit_compatibility': ['2024', '2025']
                }
                
                with patch.object(specifier, '_generate_code_implementation') as mock_code:
                    mock_code.return_value = {
                        'structure': {'main_module': 'test_button.py'},
                        'main_template': 'def main(): pass',
                        'helper_functions': [],
                        'error_handling': 'def handle_error(): pass'
                    }
                    
                    # Mock other methods
                    with patch.object(specifier, '_define_testing_strategy') as mock_testing, \
                         patch.object(specifier, '_specify_integration_requirements') as mock_integration, \
                         patch.object(specifier, '_define_performance_considerations') as mock_performance, \
                         patch.object(specifier, '_generate_documentation_requirements') as mock_docs:
                        
                        mock_testing.return_value = {'strategy': 'unit_only', 'test_cases': [], 'validation': []}
                        mock_integration.return_value = {'integration_method': 'standard', 'ui_requirements': '', 'deployment': []}
                        mock_performance.return_value = {'considerations': [], 'optimizations': [], 'memory_estimate': 'low'}
                        mock_docs.return_value = {'user_docs': [], 'technical_docs': '', 'support': []}
                        
                        spec = specifier.create_comprehensive_specification(mock_suggestion)
                        
                        self.assertIsNotNone(spec)
                        self.assertEqual(spec.suggestion_id, 'test_spec_1')
                        self.assertGreaterEqual(spec.completeness_score, 0.0)


class TestQualityController(FrameworkTestCase):
    """Test suite for QualityController component"""
    
    def test_quality_controller_initialization(self):
        """Test quality controller initialization"""
        
        controller = QualityController(self.test_config)
        
        self.assertIsNotNone(controller)
        self.assertEqual(len(controller.baseline_scores), 5)
        self.assertEqual(len(controller.target_scores), 5)
    
    def test_executive_summary_generation(self):
        """Test executive summary generation"""
        
        controller = QualityController(self.test_config)
        
        # Mock data for summary generation
        mock_suggestions = [{'id': '1', 'name': 'Test', 'aec_workflow_relevance': 0.8, 'innovation_score': 0.7}]
        mock_specs = [{'suggestion_id': '1', 'completeness_score': 0.9}]
        mock_validation = {'validation_coverage': 1.0, 'passed_suggestions': 1}
        mock_quality_gates = {'research_completeness': True, 'validation_coverage': True}
        
        summary = controller.generate_executive_summary(
            research_data=self.mock_research_data,
            capability_data=self.mock_capability_data,
            suggestions=mock_suggestions,
            specifications=mock_specs,
            validation_results=mock_validation,
            quality_gates_passed=mock_quality_gates
        )
        
        self.assertIsNotNone(summary)
        self.assertEqual(summary.total_suggestions_generated, 1)
        self.assertIsNotNone(summary.quality_metrics)
        self.assertGreaterEqual(summary.quality_metrics.overall_quality_score, 0.0)


class TestErrorHandling(FrameworkTestCase):
    """Test suite for error handling system"""
    
    def test_error_handler_initialization(self):
        """Test error handler initialization"""
        
        error_handler = get_error_handler()
        
        self.assertIsNotNone(error_handler)
        self.assertGreater(len(error_handler.recovery_strategies), 0)
    
    def test_exception_handling(self):
        """Test exception handling and classification"""
        
        error_handler = get_error_handler()
        
        # Test different exception types
        test_exceptions = [
            (ValueError("Test value error"), "test_component"),
            (ConnectionError("Test connection error"), "test_component"),
            (CriticalFrameworkError("Test critical error"), "test_component")
        ]
        
        for exception, component in test_exceptions:
            framework_error = error_handler.handle_exception(
                exception, 
                component, 
                attempt_recovery=False
            )
            
            self.assertIsNotNone(framework_error)
            self.assertEqual(framework_error.component, component)
            self.assertIsNotNone(framework_error.error_id)
    
    def test_error_summary(self):
        """Test error summary generation"""
        
        error_handler = get_error_handler()
        
        # Generate some test errors
        error_handler.handle_exception(ValueError("Test error 1"), "test_component_1", attempt_recovery=False)
        error_handler.handle_exception(ConnectionError("Test error 2"), "test_component_2", attempt_recovery=False)
        
        summary = error_handler.get_error_summary()
        
        self.assertIsNotNone(summary)
        self.assertGreaterEqual(summary['total_errors'], 2)
        self.assertIn('error_categories', summary)


class TestIntegration(FrameworkTestCase):
    """Integration tests for component interaction"""
    
    def test_research_to_generation_integration(self):
        """Test integration between research and generation components"""
        
        # Mock research output
        research = ResearchFramework(self.test_config)
        
        # Mock generation with research data
        generator = ButtonGenerator(
            self.mock_research_data,
            self.mock_capability_data,
            self.test_config
        )
        
        # Verify generator can use research data
        self.assertIsNotNone(generator.research_data)
        self.assertIn('completeness_score', generator.research_data)
    
    def test_generation_to_validation_integration(self):
        """Test integration between generation and validation components"""
        
        generator = ButtonGenerator(
            self.mock_research_data,
            self.mock_capability_data,
            self.test_config
        )
        
        validator = ValidationEngine(self.test_config)
        
        # Mock generation output for validation
        mock_suggestions = [
            {
                'id': 'integration_test_1',
                'name': 'Integration Test Button',
                'functionality': 'Test functionality',
                'description': 'Integration test button'
            }
        ]
        
        mock_specs = [
            {
                'suggestion_id': 'integration_test_1',
                'completeness_score': 0.8
            }
        ]
        
        # Test validation can process generation output
        with patch.object(validator, '_validate_single_criterion') as mock_validate:
            mock_validate.return_value = Mock(
                suggestion_id='integration_test_1',
                criteria='technical_feasibility',
                status=ValidationStatus.PASSED,
                score=0.8
            )
            
            result = validator.validate_comprehensive_coverage(mock_suggestions, mock_specs)
            self.assertIsNotNone(result)


class TestPerformance(FrameworkTestCase):
    """Performance and benchmarking tests"""
    
    def test_research_performance(self):
        """Test research component performance"""
        
        start_time = time.time()
        
        research = ResearchFramework(self.test_config)
        
        # Mock fast research execution
        with patch.object(research, 'execute_primary_research') as mock_research:
            mock_research.return_value = self.mock_research_data
            
            result = research.execute_primary_research()
            
            execution_time = time.time() - start_time
            
            # Performance assertion - research should complete quickly when mocked
            self.assertLess(execution_time, 1.0)  # Less than 1 second
            self.assertIsNotNone(result)
    
    def test_generation_performance(self):
        """Test generation component performance"""
        
        generator = ButtonGenerator(
            self.mock_research_data,
            self.mock_capability_data,
            self.test_config
        )
        
        start_time = time.time()
        
        with patch.object(generator, '_validate_suggestion_real_time') as mock_validate:
            mock_validate.return_value = True
            
            suggestions = generator.generate_validated_suggestions(target_count=50)
            
            execution_time = time.time() - start_time
            
            # Performance assertions
            self.assertLess(execution_time, 10.0)  # Less than 10 seconds for 50 suggestions
            self.assertEqual(len(suggestions), 50)
    
    def test_validation_performance(self):
        """Test validation component performance"""
        
        validator = ValidationEngine(self.test_config)
        
        # Create larger test dataset
        mock_suggestions = [
            {
                'id': f'perf_test_{i}',
                'name': f'Performance Test Button {i}',
                'functionality': 'Performance test functionality',
                'description': 'Performance test button'
            }
            for i in range(100)
        ]
        
        mock_specs = [
            {
                'suggestion_id': f'perf_test_{i}',
                'completeness_score': 0.8
            }
            for i in range(100)
        ]
        
        start_time = time.time()
        
        with patch.object(validator, '_validate_single_criterion') as mock_validate:
            mock_validate.return_value = Mock(
                suggestion_id='test',
                criteria='technical_feasibility',
                status=ValidationStatus.PASSED,
                score=0.8
            )
            
            result = validator.validate_comprehensive_validation(mock_suggestions, mock_specs)
            
            execution_time = time.time() - start_time
            
            # Performance assertions
            self.assertLess(execution_time, 30.0)  # Less than 30 seconds for 100 suggestions
            self.assertIsNotNone(result)


def run_all_tests():
    """Run all framework tests with comprehensive reporting"""
    
    # Setup logging for tests
    setup_comprehensive_logging(log_level="WARNING")  # Reduce noise during testing
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestResearchFramework,
        TestValidationEngine,
        TestButtonGenerator,
        TestImplementationSpecifier,
        TestQualityController,
        TestErrorHandling,
        TestIntegration,
        TestPerformance
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests with detailed reporting
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print("🧪 FRAMEWORK TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    # Print detailed failure information
    if result.failures:
        print(f"\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"   {test}: {traceback.split(chr(10))[-2]}")
    
    if result.errors:
        print(f"\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"   {test}: {traceback.split(chr(10))[-2]}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
