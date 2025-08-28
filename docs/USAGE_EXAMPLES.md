# Revitron UI Enhancement Framework - Usage Examples

## 🚀 Quick Start Examples

### Basic Framework Execution

```python
#!/usr/bin/env python3
"""
Example: Basic Framework Execution
Generate 250 validated Revitron UI button suggestions with complete specifications
"""

from pathlib import Path
import yaml
from main_controller import RevitronEnhancementFramework

def main():
    """Execute framework with default configuration"""
    
    # Initialize framework
    config_path = Path("config/framework_config.yaml")
    framework = RevitronEnhancementFramework(config_path)
    
    # Execute comprehensive enhancement pipeline
    results = framework.execute_comprehensive_enhancement_pipeline(target_button_count=250)
    
    # Display results summary
    print("=" * 60)
    print("🎯 FRAMEWORK EXECUTION SUMMARY")
    print("=" * 60)
    print(f"✅ Overall Quality Score: {results['overall_score']:.1f}/10")
    print(f"📊 Validation Coverage: {results['validation_coverage']:.1%}")
    print(f"💡 Suggestions Generated: {results['total_suggestions']}")
    print(f"🔧 Specifications Created: {results['specifications_count']}")
    print(f"⏱️ Execution Time: {results['execution_time']:.1f} seconds")
    
    # Quality improvements
    print("\n📈 QUALITY IMPROVEMENTS:")
    print(f"   Research Quality: 6/10 → {results['quality_metrics']['research_quality']:.1f}/10")
    print(f"   Content Innovation: 7/10 → {results['quality_metrics']['innovation']:.1f}/10") 
    print(f"   Technical Accuracy: 5/10 → {results['quality_metrics']['accuracy']:.1f}/10")
    print(f"   Validation Coverage: 4/10 → {results['quality_metrics']['validation']:.1f}/10")
    
    print(f"\n📄 Detailed reports saved to: reports/")
    
if __name__ == "__main__":
    main()
```

### Research-Only Mode

```python
#!/usr/bin/env python3
"""
Example: Research-Only Execution
Execute comprehensive research phase to understand Revitron API capabilities
"""

from main_controller import RevitronEnhancementFramework

def research_only_example():
    """Execute only research phase for API analysis"""
    
    framework = RevitronEnhancementFramework()
    
    # Execute research phase only
    try:
        research_results = framework._execute_research_phase()
        
        print("🔬 RESEARCH PHASE RESULTS:")
        print(f"   Completeness Score: {research_results['completeness_score']:.1%}")
        print(f"   Sources Accessed: {len(research_results['accessed_sources'])}")
        print(f"   API Capabilities Found: {research_results['api_capabilities_count']}")
        
        if research_results['failed_sources']:
            print(f"   ⚠️ Failed Sources: {research_results['failed_sources']}")
            
    except Exception as e:
        print(f"❌ Research failed: {e}")
        print("💡 Try checking network connectivity and source accessibility")

if __name__ == "__main__":
    research_only_example()
```

### Custom Configuration Example

```python
#!/usr/bin/env python3
"""
Example: Custom Configuration
Customize framework behavior with specific quality targets and validation criteria
"""

import yaml
from pathlib import Path
from main_controller import RevitronEnhancementFramework

def create_custom_config():
    """Create custom configuration with specific requirements"""
    
    custom_config = {
        'quality_targets': {
            'overall_performance_target': 9.5,  # Lower target for faster execution
            'validation_coverage_required': 0.95,  # 95% instead of 100%
            'duplicate_tolerance': 0.05,  # Allow 5% similarity
        },
        'generation': {
            'default_button_count': 100,  # Generate fewer buttons
            'categories': [
                {
                    'name': 'Selection and Filtering Tools',
                    'target_count': 40,  # Focus on selection tools
                    'focus_areas': [
                        'Smart selection algorithms',
                        'Advanced filtering capabilities'
                    ]
                },
                {
                    'name': 'Model Management',
                    'target_count': 30,
                    'focus_areas': [
                        'Model health monitoring',
                        'Performance optimization'
                    ]
                },
                {
                    'name': 'Documentation Tools',
                    'target_count': 30,
                    'focus_areas': [
                        'Automated documentation',
                        'Report generation'
                    ]
                }
            ]
        },
        'validation': {
            'criteria_thresholds': {
                'technical_feasibility': 0.7,  # Lower threshold
                'aec_value': 0.6,
                'innovation_score': 0.4,
            }
        }
    }
    
    # Save custom configuration
    config_path = Path("config/custom_config.yaml")
    config_path.parent.mkdir(exist_ok=True)
    
    with open(config_path, 'w') as f:
        yaml.dump(custom_config, f, default_flow_style=False, indent=2)
    
    return config_path

def execute_with_custom_config():
    """Execute framework with custom configuration"""
    
    # Create and use custom configuration
    config_path = create_custom_config()
    
    framework = RevitronEnhancementFramework(config_path)
    results = framework.execute_comprehensive_enhancement_pipeline(target_button_count=100)
    
    print(f"🎯 Custom execution completed with {results['overall_score']:.1f}/10 quality score")

if __name__ == "__main__":
    execute_with_custom_config()
```

## 🔧 Advanced Usage Examples

### Individual Component Usage

```python
#!/usr/bin/env python3
"""
Example: Individual Component Usage
Use specific framework components independently for targeted functionality
"""

from src.research.research_framework import ResearchFramework
from src.validation.validation_engine import ValidationEngine
from src.generation.button_generator import ButtonGenerator
from pathlib import Path
import yaml

def research_component_example():
    """Use research framework component independently"""
    
    # Load configuration
    with open("config/framework_config.yaml", 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize research framework
    research = ResearchFramework(config)
    
    # Execute research
    research_results = research.execute_primary_research()
    
    print("🔬 Independent Research Component Results:")
    print(f"   API capabilities found: {len(research_results.get('api_capabilities', []))}")
    print(f"   Research completeness: {research_results['completeness_score']:.1%}")
    
    return research_results

def validation_component_example(suggestions):
    """Use validation engine component independently"""
    
    with open("config/framework_config.yaml", 'r') as f:
        config = yaml.safe_load(f)
    
    validator = ValidationEngine(config)
    
    # Create mock implementation specs
    mock_specs = [
        {
            'suggestion_id': s.get('id', 'unknown'),
            'completeness_score': 0.85,
            'api_requirements': ['FilteredElementCollector', 'Transaction'],
            'implementation_complexity': 'medium'
        }
        for s in suggestions
    ]
    
    # Execute validation
    validation_results = validator.validate_comprehensive_coverage(suggestions, mock_specs)
    
    print("✅ Independent Validation Component Results:")
    print(f"   Validation coverage: {validation_results.validation_coverage:.1%}")
    print(f"   Passed suggestions: {validation_results.passed_suggestions}")
    print(f"   Overall quality: {validation_results.overall_quality_score:.2f}")
    
    return validation_results

def generation_component_example(research_data, capability_data):
    """Use button generator component independently"""
    
    with open("config/framework_config.yaml", 'r') as f:
        config = yaml.safe_load(f)
    
    generator = ButtonGenerator(research_data, capability_data, config)
    
    # Generate validated suggestions
    suggestions = generator.generate_validated_suggestions(target_count=50)
    
    print("💡 Independent Generation Component Results:")
    print(f"   Suggestions generated: {len(suggestions)}")
    print(f"   Average AEC relevance: {sum(s.aec_workflow_relevance for s in suggestions) / len(suggestions):.2f}")
    print(f"   Average innovation: {sum(s.innovation_score for s in suggestions) / len(suggestions):.2f}")
    
    # Convert to dict format for compatibility
    suggestion_dicts = [
        {
            'id': s.id,
            'name': s.name,
            'category': s.category.value,
            'functionality': s.functionality,
            'description': s.description,
            'aec_workflow_relevance': s.aec_workflow_relevance,
            'innovation_score': s.innovation_score
        }
        for s in suggestions
    ]
    
    return suggestion_dicts

def main():
    """Demonstrate individual component usage"""
    
    print("🔧 ADVANCED USAGE: Individual Components")
    print("=" * 50)
    
    # 1. Research component
    research_data = research_component_example()
    
    # 2. Mock capability data for demonstration
    capability_data = {
        'total_functions_mapped': 42,
        'duplicate_detection_database': {
            'filter': {'name': 'Filter', 'description': 'Element filtering'},
            'select': {'name': 'Selection', 'description': 'Element selection'},
        }
    }
    
    # 3. Generation component
    suggestions = generation_component_example(research_data, capability_data)
    
    # 4. Validation component
    validation_results = validation_component_example(suggestions)
    
    print("\n🎯 COMPONENT INTEGRATION SUCCESSFUL")

if __name__ == "__main__":
    main()
```

### Error Handling and Recovery

```python
#!/usr/bin/env python3
"""
Example: Error Handling and Recovery
Demonstrate comprehensive error handling and recovery strategies
"""

from src.utils.error_handling import (
    get_error_handler, 
    CriticalFrameworkError, 
    ValidationError,
    handle_framework_error
)
from main_controller import RevitronEnhancementFramework
from pathlib import Path

def error_handling_example():
    """Demonstrate error handling capabilities"""
    
    error_handler = get_error_handler()
    
    try:
        # Simulate various error scenarios
        
        # 1. Network error simulation
        try:
            raise ConnectionError("Unable to access documentation sources")
        except Exception as e:
            framework_error = handle_framework_error(
                e, 
                component="research_framework",
                context={'url': 'https://revitron.readthedocs.io'},
                attempt_recovery=True
            )
            print(f"🔄 Network error handled: {framework_error.error_id}")
            print(f"   Recovery attempted: {framework_error.recovery_attempted}")
            print(f"   User message: {framework_error.user_message}")
        
        # 2. Validation error simulation
        try:
            raise ValidationError("Validation coverage below threshold", validation_type="coverage")
        except Exception as e:
            framework_error = handle_framework_error(
                e,
                component="validation_engine",
                context={'coverage_achieved': 0.85, 'threshold': 1.0}
            )
            print(f"\n✅ Validation error handled: {framework_error.error_id}")
            print(f"   Suggested resolution: {framework_error.suggested_resolution}")
        
        # 3. Critical error simulation
        try:
            raise CriticalFrameworkError("Research completeness below minimum threshold")
        except Exception as e:
            framework_error = handle_framework_error(
                e,
                component="main_controller",
                context={'completeness': 0.7, 'minimum': 0.95}
            )
            print(f"\n🚨 Critical error handled: {framework_error.error_id}")
            print(f"   Blocks execution: {framework_error.blocks_execution}")
        
        # Display error summary
        error_summary = error_handler.get_error_summary()
        print(f"\n📊 ERROR HANDLING SUMMARY:")
        print(f"   Total errors: {error_summary['total_errors']}")
        print(f"   Critical errors: {error_summary['critical_errors']}")
        print(f"   Recovery success rate: {error_summary['recovery_success_rate']:.1%}")
        
        # Export error report
        report_path = Path("reports/error_report.json")
        report_path.parent.mkdir(exist_ok=True)
        error_handler.export_error_report(report_path)
        print(f"   Error report exported: {report_path}")
        
    except Exception as e:
        print(f"❌ Unexpected error in demonstration: {e}")

def graceful_degradation_example():
    """Demonstrate graceful degradation with error handling"""
    
    print("\n🛡️ GRACEFUL DEGRADATION EXAMPLE:")
    
    try:
        framework = RevitronEnhancementFramework()
        
        # Attempt execution with error handling
        results = framework.execute_comprehensive_enhancement_pipeline(target_button_count=50)
        
        print("✅ Framework executed successfully")
        print(f"   Quality score: {results['overall_score']:.1f}/10")
        
    except CriticalFrameworkError as e:
        print(f"🚨 Critical error - using fallback mode:")
        print(f"   Error: {e}")
        print("   Switching to reduced functionality mode...")
        
        # Implement fallback with reduced requirements
        fallback_results = execute_fallback_mode()
        print(f"   Fallback results: {fallback_results}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("💡 Check logs for detailed error information")

def execute_fallback_mode():
    """Execute framework in fallback mode with reduced requirements"""
    
    # Simplified execution with lower quality thresholds
    return {
        'mode': 'fallback',
        'suggestions_generated': 25,
        'quality_score': 7.5,
        'message': 'Executed with reduced functionality due to errors'
    }

def main():
    """Demonstrate comprehensive error handling"""
    
    print("🛡️ ERROR HANDLING AND RECOVERY EXAMPLES")
    print("=" * 50)
    
    error_handling_example()
    graceful_degradation_example()

if __name__ == "__main__":
    main()
```

### Performance Monitoring

```python
#!/usr/bin/env python3
"""
Example: Performance Monitoring
Monitor and analyze framework performance with detailed metrics
"""

from src.utils.logging_config import PerformanceLogger, setup_comprehensive_logging
from main_controller import RevitronEnhancementFramework
import time
import psutil
from pathlib import Path

def performance_monitoring_example():
    """Demonstrate comprehensive performance monitoring"""
    
    # Setup logging with performance monitoring
    setup_comprehensive_logging(log_level="DEBUG", enable_rich_formatting=True)
    
    # Initialize performance logger
    perf_logger = PerformanceLogger("main_execution")
    
    print("⚡ PERFORMANCE MONITORING EXAMPLE")
    print("=" * 50)
    
    # Monitor overall execution
    perf_logger.start_timer("framework_execution")
    perf_logger.log_memory_usage("startup")
    
    try:
        # Initialize framework
        perf_logger.start_timer("framework_initialization")
        framework = RevitronEnhancementFramework()
        init_time = perf_logger.end_timer("framework_initialization")
        perf_logger.log_memory_usage("post_initialization")
        
        # Monitor research phase
        perf_logger.start_timer("research_phase")
        # framework._execute_research_phase() would be called here
        research_time = perf_logger.end_timer("research_phase")
        perf_logger.log_memory_usage("post_research")
        
        # Monitor generation phase
        perf_logger.start_timer("generation_phase")
        # Simulation of generation phase
        time.sleep(2)  # Simulate processing time
        generation_time = perf_logger.end_timer("generation_phase")
        perf_logger.log_memory_usage("post_generation")
        
        # Monitor validation phase
        perf_logger.start_timer("validation_phase")
        time.sleep(1)  # Simulate processing time
        validation_time = perf_logger.end_timer("validation_phase")
        perf_logger.log_memory_usage("post_validation")
        
        # Complete execution monitoring
        total_time = perf_logger.end_timer("framework_execution")
        perf_logger.log_memory_usage("completion")
        
        # Performance summary
        print(f"\n📊 PERFORMANCE SUMMARY:")
        print(f"   Total Execution Time: {total_time:.2f}s")
        print(f"   Initialization: {init_time:.2f}s ({init_time/total_time*100:.1f}%)")
        print(f"   Research Phase: {research_time:.2f}s ({research_time/total_time*100:.1f}%)")
        print(f"   Generation Phase: {generation_time:.2f}s ({generation_time/total_time*100:.1f}%)")
        print(f"   Validation Phase: {validation_time:.2f}s ({validation_time/total_time*100:.1f}%)")
        
        # System resource usage
        process = psutil.Process()
        cpu_percent = process.cpu_percent()
        memory_mb = process.memory_info().rss / 1024 / 1024
        
        print(f"\n💻 RESOURCE USAGE:")
        print(f"   CPU Usage: {cpu_percent:.1f}%")
        print(f"   Memory Usage: {memory_mb:.1f} MB")
        print(f"   Disk Usage: {get_disk_usage()}")
        
        # Performance recommendations
        generate_performance_recommendations(total_time, memory_mb)
        
    except Exception as e:
        perf_logger.end_timer("framework_execution")
        print(f"❌ Performance monitoring interrupted: {e}")

def get_disk_usage():
    """Get disk usage for framework files"""
    
    try:
        framework_paths = [
            Path("logs"),
            Path("reports"),
            Path("cache")
        ]
        
        total_size = 0
        for path in framework_paths:
            if path.exists():
                if path.is_file():
                    total_size += path.stat().st_size
                else:
                    total_size += sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
        
        return f"{total_size / 1024 / 1024:.1f} MB"
    
    except Exception:
        return "Unable to calculate"

def generate_performance_recommendations(execution_time: float, memory_mb: float):
    """Generate performance optimization recommendations"""
    
    print(f"\n💡 PERFORMANCE RECOMMENDATIONS:")
    
    if execution_time > 300:  # 5 minutes
        print("   ⚠️ Execution time is high - consider:")
        print("     • Reducing target button count")
        print("     • Using cached research data")
        print("     • Parallel processing for validation")
    
    if memory_mb > 1000:  # 1GB
        print("   ⚠️ Memory usage is high - consider:")
        print("     • Processing buttons in smaller batches")
        print("     • Clearing intermediate results")
        print("     • Using memory-efficient data structures")
    
    if execution_time < 60 and memory_mb < 500:
        print("   ✅ Performance is optimal")
        print("     • Consider increasing button count")
        print("     • Enable additional validation criteria")
        print("     • Add more comprehensive analysis")

def benchmark_comparison():
    """Compare performance across different configurations"""
    
    configurations = [
        {'name': 'Minimal', 'buttons': 50, 'validation': 0.8},
        {'name': 'Standard', 'buttons': 100, 'validation': 0.9},
        {'name': 'Comprehensive', 'buttons': 250, 'validation': 1.0},
    ]
    
    print(f"\n🏁 BENCHMARK COMPARISON:")
    print("Configuration | Buttons | Validation | Est. Time | Est. Memory")
    print("-" * 65)
    
    for config in configurations:
        # Estimate performance based on configuration
        est_time = config['buttons'] * 0.5 + config['validation'] * 30
        est_memory = config['buttons'] * 2 + 200
        
        print(f"{config['name']:<12} | {config['buttons']:<7} | {config['validation']:<10.1f} | "
              f"{est_time:<8.1f}s | {est_memory:<6.1f}MB")

def main():
    """Execute performance monitoring examples"""
    
    performance_monitoring_example()
    benchmark_comparison()

if __name__ == "__main__":
    main()
```

## 📋 Template Examples

### Custom Button Template

```python
#!/usr/bin/env python3
"""
Template: Custom Revitron UI Button
Generated by Revitron UI Enhancement Framework

Button Name: {{BUTTON_NAME}}
Category: {{CATEGORY}}
Description: {{DESCRIPTION}}
"""

from pyrevit import revit, forms, script
import revitron
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

__title__ = "{{BUTTON_NAME}}"
__doc__ = """{{DESCRIPTION}}

Usage:
1. {{USAGE_STEP_1}}
2. {{USAGE_STEP_2}}
3. {{USAGE_STEP_3}}

Requirements:
- {{REQUIREMENT_1}}
- {{REQUIREMENT_2}}
"""

def main():
    """Main execution function"""
    
    try:
        # Get current document and UI document
        doc = revit.doc
        uidoc = revit.uidoc
        
        # Validate prerequisites
        if not doc:
            forms.alert("No active document found.")
            return
        
        # Execute main functionality
        result = execute_{{FUNCTION_NAME}}(doc, uidoc)
        
        # Display results
        if result:
            forms.alert(f"✅ Operation completed successfully: {result}")
        else:
            forms.alert("⚠️ Operation completed with no results.")
            
    except Exception as e:
        forms.alert(f"❌ Error: {str(e)}")
        script.exit()

def execute_{{FUNCTION_NAME}}(doc, uidoc):
    """Execute the main functionality"""
    
    with Transaction(doc, "{{BUTTON_NAME}} Operation") as t:
        t.Start()
        try:
            # {{IMPLEMENTATION_LOGIC}}
            
            result = perform_operation(doc, uidoc)
            t.Commit()
            return result
            
        except Exception as e:
            t.RollBack()
            raise e

def perform_operation(doc, uidoc):
    """Core operation implementation"""
    
    # {{CORE_LOGIC}}
    return "Operation completed"

if __name__ == "__main__":
    main()
```

## 🧪 Testing Examples

See the complete testing framework in `/tests/` directory for comprehensive test examples including:

- Unit tests for individual components
- Integration tests for component interaction
- End-to-end framework testing
- Performance benchmarking
- Quality assurance validation

## 📚 Additional Resources

- **API Reference**: `/docs/API_REFERENCE.md`
- **Configuration Guide**: `/docs/CONFIGURATION_GUIDE.md`
- **Contributing Guidelines**: `/docs/CONTRIBUTING.md`
- **Troubleshooting**: `/docs/TROUBLESHOOTING.md`

---

**Repository**: https://github.com/mohammedhadeez/revitron-ui-enhancement-framework  
**Version**: 2.0 (Self-Reflection Integrated)  
**Last Updated**: August 2025
