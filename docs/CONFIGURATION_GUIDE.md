# ⚙️ Configuration Guide

**Revitron UI Enhancement Framework v2.0 (Self-Reflection Integrated)**

This comprehensive guide covers all configuration options available in the Revitron UI Enhancement Framework. The framework uses YAML-based configuration with extensive customization options to meet diverse AEC workflow requirements.

---

## 📁 Configuration Files Overview

### **Primary Configuration**
- **`config/framework_config.yaml`** - Main configuration file
- **`config/user_config.yaml`** - User-specific overrides (optional)
- **`config/local_config.yaml`** - Local environment overrides (optional)

### **Configuration Priority (Highest to Lowest)**
1. Command-line arguments (`--option value`)
2. Environment variables (`REVITRON_FRAMEWORK_OPTION`)
3. `config/local_config.yaml` (local overrides)
4. `config/user_config.yaml` (user preferences)  
5. `config/framework_config.yaml` (default configuration)

---

## 🏗️ Complete Configuration Reference

### **Framework Metadata**

```yaml
# Framework identification and versioning
framework:
  name: "Revitron UI Enhancement Framework"
  version: "2.0.0"
  codename: "Self-Reflection Integrated"
  description: "Production-ready system for systematic Revitron UI enhancement"
  
  # Framework behavior
  strict_mode: true              # Enforce all quality requirements
  debug_mode: false              # Enable debug logging and validation
  performance_monitoring: true   # Enable performance tracking
  
  # Self-reflection integration settings (v2.0)
  self_reflection:
    enabled: true                # Enable v2.0 self-reflection improvements
    address_critical_issues: true # Address the 4 critical issues identified
    target_performance: "10/10"   # Target performance standard
```

### **Research Configuration**

```yaml
research:
  # Documentation access settings (Critical Issue #1 Fix)
  primary_sources:
    - "https://revitron.readthedocs.io/en/latest/"
    - "https://github.com/revitron/revitron"
    - "https://pyrevit.readthedocs.io/"
  
  fallback_sources:
    - "local_docs/"
    - "cached_docs/"
    - "backup_sources/"
  
  # Research quality requirements (v2.0 Self-Reflection)
  completeness_threshold: 95     # Minimum 95% research completeness required
  mandatory_research: true       # Block generation without adequate research
  source_validation: true        # Validate all sources before use
  
  # Network and timing settings
  timeout_seconds: 30
  retry_attempts: 3
  retry_delay_seconds: 5
  max_concurrent_requests: 5
  
  # Caching configuration
  caching:
    enabled: true
    cache_duration_hours: 24
    cache_directory: "cache/research/"
    auto_refresh: true
    validate_cache: true
  
  # Content processing
  content_processing:
    extract_api_references: true
    identify_code_examples: true
    parse_documentation_structure: true
    analyze_functionality_coverage: true
  
  # Quality assurance
  quality_checks:
    verify_source_accessibility: true
    validate_content_completeness: true
    check_api_compatibility: true
    assess_documentation_quality: true
```

### **Generation Configuration**

```yaml
generation:
  # Button generation settings
  max_suggestions: 250           # Maximum number of buttons to generate
  batch_size: 50                 # Process buttons in batches of 50
  categories:
    - "Selection and Filtering"
    - "Model Management and Analysis"  
    - "Documentation and Reporting"
    - "Automation and Workflow"
    - "Analysis and Simulation"
  
  # Quality gates (v2.0 Enhancement)
  quality_requirements:
    minimum_description_length: 75
    require_functionality_details: true
    require_category_assignment: true
    require_api_references: true
    require_use_case_examples: true
  
  # Content generation parameters
  creativity_level: "balanced"   # Options: conservative, balanced, innovative
  technical_depth: "professional" # Options: basic, professional, expert
  target_audience: "aec_professionals"
  
  # Innovation settings
  innovation:
    encourage_novel_combinations: true
    explore_emerging_technologies: true
    consider_workflow_integration: true
    balance_innovation_feasibility: true
  
  # Template and formatting
  output_format: "markdown_table"
  include_implementation_hints: true
  generate_code_snippets: false  # Disable for initial generation
  cross_reference_related: true
```

### **Validation Configuration**

```yaml
validation:
  # Coverage requirements (Critical Issue #2 Fix)
  mandatory_coverage: 100        # 100% validation coverage required
  fail_on_incomplete_coverage: true
  log_validation_details: true
  generate_validation_reports: true
  
  # Validation criteria (7 comprehensive criteria)
  criteria:
    technical_feasibility: 
      enabled: true
      weight: 20
      strict_mode: true
    
    implementation_complexity:
      enabled: true  
      weight: 15
      max_complexity_score: 8    # Scale 1-10
    
    api_compatibility:
      enabled: true
      weight: 20
      check_revitron_api: true
      check_pyrevit_compatibility: true
    
    performance_impact:
      enabled: true
      weight: 15
      assess_memory_usage: true
      assess_processing_time: true
    
    user_value:
      enabled: true
      weight: 15
      assess_workflow_improvement: true
      assess_time_savings: true
    
    innovation_factor:
      enabled: true
      weight: 10
      reward_novel_approaches: true
      penalize_duplicates: true
    
    documentation_completeness:
      enabled: true
      weight: 5
      require_clear_description: true
      require_usage_examples: true
  
  # Validation processing
  parallel_validation: true
  max_validation_workers: 4
  validation_timeout_seconds: 60
  detailed_error_reporting: true
  
  # Quality thresholds
  thresholds:
    minimum_score: 70            # Minimum score to pass validation
    excellence_score: 90         # Score for excellence rating
    innovation_bonus: 5          # Bonus points for innovation
```

### **Duplicate Prevention Configuration**

```yaml
duplicate_prevention:
  # Anti-duplication settings (Critical Issue #3 Fix)  
  enabled: true
  zero_tolerance: true           # Zero tolerance for duplicates
  similarity_threshold: 0.9      # Similarity threshold (0.0-1.0)
  
  # API capability mapping
  api_mapping:
    revitron_functions: "data/revitron_api_mapping.json"
    pyrevit_functions: "data/pyrevit_api_mapping.json"
    custom_exclusions: "data/custom_exclusions.yaml"
  
  # Detection methods
  detection_methods:
    text_similarity: true
    semantic_similarity: true  
    functionality_overlap: true
    api_usage_patterns: true
  
  # Similarity analysis
  similarity_analysis:
    use_nlp_embeddings: true
    compare_descriptions: true
    compare_functionality: true
    compare_api_calls: true
    compare_use_cases: true
  
  # Handling duplicates
  duplicate_handling:
    auto_remove: true            # Automatically remove duplicates
    flag_for_review: true        # Flag borderline cases
    maintain_audit_trail: true   # Keep record of removals
    merge_similar_concepts: false # Don't merge, prefer unique suggestions
```

### **Implementation Specification Configuration**

```yaml
implementation:
  # Technical specification requirements (Critical Issue #4 Fix)
  specification_depth: "complete" # Options: basic, detailed, complete
  mandatory_elements: 8           # All 8 elements required per suggestion
  
  # Required specification components
  required_elements:
    api_integration: true         # Revitron/pyRevit API usage
    code_structure: true          # Implementation architecture  
    error_handling: true          # Error handling strategy
    performance_considerations: true # Performance impact analysis
    testing_strategy: true        # Testing approach
    documentation_requirements: true # Documentation needs
    deployment_notes: true        # Deployment considerations
    maintenance_requirements: true # Ongoing maintenance needs
  
  # Code generation settings
  code_generation:
    generate_templates: true
    include_error_handling: true
    add_logging_statements: true
    follow_pep8_standards: true
    include_type_hints: true
    generate_docstrings: true
  
  # Implementation complexity analysis
  complexity_analysis:
    estimate_development_time: true
    identify_dependencies: true
    assess_risk_factors: true
    recommend_testing_approach: true
```

### **Quality Control Configuration**

```yaml
quality:
  # Overall quality orchestration
  orchestration:
    multi_stage_gates: true      # Enable multi-stage quality gates
    fail_fast: true              # Stop on first quality failure
    comprehensive_reporting: true # Generate detailed quality reports
  
  # Quality metrics
  metrics:
    target_innovation_score: 85
    target_technical_score: 90
    target_implementation_score: 80
    target_documentation_score: 85
  
  # Quality assurance processes
  processes:
    peer_review_simulation: true  # Simulate peer review process
    standards_compliance_check: true # Check against AEC standards
    workflow_integration_test: true # Test workflow integration
    performance_benchmark: true   # Benchmark against targets
  
  # Continuous improvement (v2.0 Self-Reflection)
  continuous_improvement:
    track_quality_trends: true
    identify_improvement_areas: true
    implement_corrections: true
    measure_effectiveness: true
```

### **Logging Configuration**

```yaml
logging:
  # Log levels and output
  level: "INFO"                  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  console_output: true
  file_output: true
  
  # Log file settings
  files:
    main_log: "logs/framework.log"
    error_log: "logs/errors.log"
    performance_log: "logs/performance.log"
    validation_log: "logs/validation.log"
  
  # Log rotation
  rotation:
    max_size_mb: 50
    backup_count: 10
    rotate_when: "midnight"
  
  # Log formatting
  format:
    console: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
  
  # Component-specific logging
  components:
    research: "INFO"
    validation: "INFO" 
    generation: "INFO"
    implementation: "DEBUG"
    quality: "INFO"
```

### **Performance Configuration**

```yaml
performance:
  # Resource management
  memory_management:
    max_memory_mb: 4096          # Maximum memory usage
    garbage_collection: true
    memory_monitoring: true
    memory_warnings: true
  
  # Processing optimization
  processing:
    parallel_processing: true
    max_workers: 4
    batch_processing: true
    batch_size: 25
  
  # Caching strategy
  caching:
    enable_research_cache: true
    enable_validation_cache: true
    enable_generation_cache: false # Disable to ensure fresh content
    cache_cleanup_hours: 168      # Weekly cleanup
  
  # Performance monitoring
  monitoring:
    track_execution_time: true
    profile_memory_usage: true
    monitor_api_response_times: true
    generate_performance_reports: true
  
  # Performance thresholds
  thresholds:
    max_processing_time_seconds: 3600  # 1 hour maximum
    max_memory_usage_mb: 2048
    max_api_response_time_seconds: 30
    max_validation_time_seconds: 300
```

### **Output Configuration**

```yaml
output:
  # Output formats and destinations
  formats:
    primary: "markdown_table"     # Primary output format
    secondary: ["json", "csv"]    # Additional export formats
    include_metadata: true
  
  # File organization
  organization:
    output_directory: "output/"
    create_subdirectories: true
    timestamp_files: true
    include_version_info: true
  
  # Content structuring
  structure:
    group_by_category: true
    sort_by_priority: true
    include_implementation_specs: true
    include_validation_results: true
  
  # Export options
  export:
    generate_summary_report: true
    include_quality_metrics: true
    export_validation_details: true
    create_implementation_guide: true
```

### **Environment Configuration**

```yaml
environment:
  # Revit and PyRevit integration
  revit_integration:
    revit_version: "2024"
    pyrevit_path: ""              # Auto-detect if empty
    check_compatibility: true
  
  # Python environment
  python:
    minimum_version: "3.7"
    check_dependencies: true
    virtual_environment: "recommended"
  
  # System requirements
  system:
    minimum_memory_gb: 4
    recommended_memory_gb: 8
    minimum_disk_space_gb: 2
    check_system_requirements: true
  
  # Development environment
  development:
    enable_debug_tools: false
    enable_profiling: false
    enable_testing_mode: false
```

---

## 🎯 Configuration Profiles

### **Production Profile**
Optimized for production use with maximum quality and reliability.

```yaml
# config/profiles/production.yaml
framework:
  strict_mode: true
  debug_mode: false
research:
  completeness_threshold: 95
validation:
  mandatory_coverage: 100
  fail_on_incomplete_coverage: true
duplicate_prevention:
  zero_tolerance: true
quality:
  fail_fast: true
  comprehensive_reporting: true
```

### **Development Profile**  
Optimized for development with faster processing and detailed debugging.

```yaml
# config/profiles/development.yaml
framework:
  strict_mode: false
  debug_mode: true
research:
  completeness_threshold: 75
validation:
  mandatory_coverage: 75
  fail_on_incomplete_coverage: false
duplicate_prevention:
  zero_tolerance: false
logging:
  level: "DEBUG"
performance:
  parallel_processing: false    # Easier debugging
```

### **Performance Profile**
Optimized for maximum performance and speed.

```yaml
# config/profiles/performance.yaml
performance:
  parallel_processing: true
  max_workers: 8
  memory_management:
    max_memory_mb: 8192
validation:
  parallel_validation: true
  max_validation_workers: 8
caching:
  enable_research_cache: true
  enable_validation_cache: true
```

### **Quality Profile**
Maximum quality settings for comprehensive validation.

```yaml
# config/profiles/quality.yaml
research:
  completeness_threshold: 98
validation:
  mandatory_coverage: 100
  detailed_error_reporting: true
implementation:
  specification_depth: "complete"
  mandatory_elements: 8
quality:
  multi_stage_gates: true
  comprehensive_reporting: true
```

---

## 🔧 Configuration Management

### **Loading Configuration Profiles**

```bash
# Use specific profile
python main_controller.py --profile production

# Combine profiles
python main_controller.py --profile production --profile quality

# Override specific settings
python main_controller.py --profile production --max-suggestions 100
```

### **Environment Variable Override**

```bash
# Override any configuration value
export REVITRON_FRAMEWORK_MAX_SUGGESTIONS=100
export REVITRON_FRAMEWORK_VALIDATION_MANDATORY_COVERAGE=90
export REVITRON_FRAMEWORK_RESEARCH_COMPLETENESS_THRESHOLD=80

python main_controller.py
```

### **Configuration Validation**

```bash
# Validate configuration
python main_controller.py --validate-config

# Check configuration completeness
python main_controller.py --check-config-completeness

# Generate default configuration
python main_controller.py --generate-config --output config/default_config.yaml
```

### **Configuration Backup and Restore**

```bash
# Backup current configuration
python main_controller.py --backup-config --output config_backup_$(date +%Y%m%d).tar.gz

# Restore configuration
python main_controller.py --restore-config --input config_backup_20250828.tar.gz
```

---

## 🏢 Enterprise Configuration

### **Multi-User Environment**

```yaml
enterprise:
  multi_user:
    enabled: true
    user_config_directory: "config/users/"
    shared_cache: true
    centralized_logging: true
  
  access_control:
    require_authentication: false  # Not implemented in v2.0
    user_roles: ["developer", "architect", "manager"]
    permission_matrix: "config/permissions.yaml"
  
  deployment:
    centralized_config: true
    config_repository: "git@company.com:revitron-configs.git"
    auto_update_config: false
```

### **Integration Settings**

```yaml
integrations:
  # External tool integration
  external_tools:
    enable_revit_integration: true
    enable_dynamo_integration: false  # Future feature
    enable_grasshopper_integration: false  # Future feature
  
  # API integrations
  apis:
    enable_web_apis: true
    api_timeout_seconds: 30
    api_retry_attempts: 3
  
  # Database integration (future)
  database:
    enabled: false
    connection_string: ""
    pool_size: 5
```

---

## 🔍 Configuration Troubleshooting

### **Common Configuration Issues**

#### **YAML Syntax Errors**
```bash
# Validate YAML syntax
python -c "
import yaml
try:
    with open('config/framework_config.yaml', 'r') as f:
        yaml.safe_load(f)
    print('✅ Configuration syntax valid')
except yaml.YAMLError as e:
    print(f'❌ YAML error: {e}')
"
```

#### **Missing Configuration Values**
```bash
# Check for required configuration
python main_controller.py --check-required-config
```

#### **Configuration Conflicts**
```bash
# Identify configuration conflicts
python main_controller.py --check-config-conflicts --verbose
```

### **Configuration Debugging**

```bash
# Show effective configuration
python main_controller.py --show-config

# Show configuration source precedence  
python main_controller.py --show-config-sources

# Export merged configuration
python main_controller.py --export-config --output effective_config.yaml
```

---

## 📊 Configuration Schema

The framework includes a JSON schema for configuration validation:

```bash
# Validate against schema
python main_controller.py --validate-config-schema

# Generate schema documentation
python main_controller.py --generate-config-schema-docs --output config_schema.md
```

---

## 💡 Best Practices

### **Configuration Management**
1. **Version Control**: Keep configuration files in version control
2. **Environment Separation**: Use different profiles for dev/staging/production
3. **Sensitive Data**: Use environment variables for sensitive configuration
4. **Documentation**: Document custom configuration changes
5. **Validation**: Always validate configuration before deployment

### **Performance Optimization**
1. **Caching**: Enable appropriate caching for your use case
2. **Parallel Processing**: Adjust worker counts based on system capabilities
3. **Memory Management**: Set appropriate memory limits
4. **Batch Size**: Tune batch sizes for optimal performance

### **Quality Assurance**  
1. **Strict Mode**: Use strict mode in production
2. **Comprehensive Validation**: Enable all validation criteria
3. **Quality Gates**: Use multi-stage quality gates
4. **Monitoring**: Enable comprehensive monitoring and logging

---

**🎯 Framework Vision**: *A production-ready system that enables AEC professionals to systematically enhance Revitron UI with validated, implementable button suggestions backed by comprehensive technical specifications and quality assurance.*

**⚙️ Configuration Philosophy**: The v2.0 configuration system supports the self-reflection improvements by providing granular control over the 4 critical issues addressed: research completeness, validation coverage, duplicate prevention, and technical specification depth.
