# 🔧 Troubleshooting Guide

**Revitron UI Enhancement Framework v2.0 (Self-Reflection Integrated)**

This comprehensive troubleshooting guide helps you diagnose and resolve issues with the Revitron UI Enhancement Framework. All solutions are based on real-world usage patterns and the self-reflection improvements implemented in v2.0.

---

## 🚨 Emergency Quick Fixes

### **Framework Won't Start**
```bash
# Quick diagnostic
python main_controller.py --version
python -c "import sys; print(f'Python: {sys.version}')"

# Reset to defaults
python main_controller.py --reset-config
```

### **Validation Fails Immediately**
```bash
# Check research completeness
python main_controller.py --check-research
python main_controller.py --research-only --force-refresh
```

### **Memory/Performance Issues**
```bash
# Reduce processing load
python main_controller.py --batch-size 10 --max-suggestions 50
```

---

## 🔍 Common Issues & Solutions

### **1. Installation and Setup Issues**

#### **1.1 ModuleNotFoundError: 'revitron' not found**
**Symptoms:**
```
ImportError: No module named 'revitron'
ModuleNotFoundError: No module named 'revitron.Filter'
```

**Root Cause:** Revitron dependency not properly installed or not in Python path.

**Solutions:**
```bash
# Method 1: Install via pip
pip install revitron

# Method 2: Manual installation
git clone https://github.com/revitron/revitron.git
cd revitron
pip install -e .

# Method 3: Verify installation
python -c "import revitron; print(revitron.__version__)"
```

**Prevention:** Always verify Revitron installation before running the framework.

#### **1.2 PyRevit Integration Errors**
**Symptoms:**
```
RuntimeError: pyRevit not detected in environment
AttributeError: module 'pyrevit' has no attribute 'framework'
```

**Root Cause:** PyRevit environment not properly configured.

**Solutions:**
```bash
# Check PyRevit installation
pyrevit --version

# Reload PyRevit environment
pyrevit reload

# Verify environment variables
echo $PYREVIT_CLI_PATH
```

**Configuration Fix:**
```yaml
# config/framework_config.yaml
environment:
  pyrevit_path: "C:\\pyRevit\\bin"
  revit_version: "2024"
  check_environment: true
```

#### **1.3 Permission Errors**
**Symptoms:**
```
PermissionError: [Errno 13] Permission denied: 'config/framework_config.yaml'
OSError: [Errno 13] Permission denied: 'logs/'
```

**Solutions:**
```bash
# Fix file permissions (Linux/Mac)
chmod -R 755 ./
sudo chown -R $USER:$USER ./

# Fix file permissions (Windows)
icacls . /grant %USERNAME%:F /T
```

### **2. Research and Data Access Issues**

#### **2.1 Documentation Access Failures**
**Symptoms:**
```
ERROR: Failed to access primary documentation
WARNING: Research completeness below 95% threshold
ResearchException: Cannot proceed without adequate documentation
```

**Root Cause:** Network issues, blocked URLs, or authentication problems.

**Diagnostic Steps:**
```python
# Test connectivity
python -c "
import requests
try:
    response = requests.get('https://revitron.readthedocs.io', timeout=10)
    print(f'Status: {response.status_code}')
except Exception as e:
    print(f'Error: {e}')
"
```

**Solutions:**
```yaml
# config/framework_config.yaml - Add fallback sources
research:
  primary_sources:
    - "https://revitron.readthedocs.io"
    - "https://github.com/revitron/revitron/blob/master/README.md"
  fallback_sources:
    - "local_docs/"
    - "cached_docs/"
  timeout: 30
  retry_attempts: 3
```

**Advanced Fix:**
```bash
# Download documentation locally
mkdir local_docs
curl -o local_docs/revitron_api.html https://revitron.readthedocs.io/en/latest/
python main_controller.py --use-local-docs local_docs/
```

#### **2.2 API Rate Limiting**
**Symptoms:**
```
HTTPError: 429 Too Many Requests
WARNING: API rate limit exceeded, waiting...
```

**Solutions:**
```python
# Implement exponential backoff
research:
  rate_limiting:
    enabled: true
    initial_delay: 1.0
    max_delay: 60.0
    backoff_factor: 2.0
```

### **3. Validation and Quality Issues**

#### **3.1 Validation Engine Failures**
**Symptoms:**
```
ValidationError: 0% validation coverage achieved
ERROR: Mandatory validation requirements not met
CRITICAL: Validation engine crashed during processing
```

**Diagnostic Commands:**
```bash
# Test validation engine independently
python src/validation/validation_engine.py --test-mode

# Check validation criteria
python main_controller.py --list-validation-criteria

# Validate sample data
python main_controller.py --validate-sample
```

**Configuration Fix:**
```yaml
# Reduce validation requirements temporarily
validation:
  mandatory_coverage: 90  # Reduced from 100%
  criteria:
    technical_feasibility: true
    implementation_complexity: true
    api_compatibility: false  # Disable if causing issues
    performance_impact: true
```

#### **3.2 Duplicate Detection False Positives**
**Symptoms:**
```
WARNING: Legitimate suggestion marked as duplicate
ERROR: API capability mapper overly aggressive
INFO: 95% of suggestions flagged as existing functionality
```

**Solutions:**
```bash
# Reset API capability mapping
python src/research/api_capability_mapper.py --rebuild-cache

# Adjust sensitivity
python main_controller.py --duplicate-threshold 0.7  # Default: 0.9
```

**Configuration Adjustment:**
```yaml
duplicate_prevention:
  similarity_threshold: 0.85  # Increased tolerance
  ignore_minor_variations: true
  custom_exclusions:
    - "Smart"
    - "Enhanced" 
    - "Advanced"
```

### **4. Generation and Output Issues**

#### **4.1 Button Generation Hangs**
**Symptoms:**
- Process appears frozen during generation
- High CPU usage with no progress
- Memory usage continuously increasing

**Immediate Actions:**
```bash
# Terminate hanging process
pkill -f "main_controller.py"

# Restart with reduced load
python main_controller.py --max-suggestions 25 --timeout 300
```

**Root Cause Analysis:**
```python
# Enable debug logging
python main_controller.py --log-level DEBUG --log-file debug.log

# Monitor resource usage
python main_controller.py --enable-profiling
```

#### **4.2 Low-Quality Suggestions**
**Symptoms:**
```
WARNING: Generated suggestions below quality threshold
ERROR: Technical specifications incomplete
INFO: Implementation details missing for 40% of suggestions
```

**Quality Enhancement:**
```yaml
# Increase quality requirements
generation:
  quality_gates:
    minimum_description_length: 100
    require_implementation_details: true
    require_api_references: true
    require_use_cases: true
```

### **5. Performance and Memory Issues**

#### **5.1 Memory Exhaustion**
**Symptoms:**
```
MemoryError: Unable to allocate memory
CRITICAL: Process killed by system (OOM)
WARNING: Memory usage exceeded 4GB threshold
```

**Immediate Solutions:**
```bash
# Reduce batch processing
python main_controller.py --batch-size 5 --memory-limit 2048

# Enable garbage collection
python main_controller.py --aggressive-gc
```

**Long-term Optimization:**
```yaml
performance:
  memory_management:
    max_memory_mb: 2048
    batch_size: 10
    enable_gc: true
    gc_threshold: 1024
```

#### **5.2 Slow Processing**
**Symptoms:**
- Framework takes hours to complete
- Individual operations timeout
- Progress appears stalled

**Performance Tuning:**
```python
# Profile performance bottlenecks
python -m cProfile main_controller.py > performance_profile.txt

# Enable parallel processing
python main_controller.py --parallel --workers 4
```

**Optimization Configuration:**
```yaml
performance:
  parallel_processing:
    enabled: true
    max_workers: 4
  caching:
    enable_research_cache: true
    enable_validation_cache: true
    cache_duration_hours: 24
```

### **6. Configuration and Environment Issues**

#### **6.1 YAML Configuration Errors**
**Symptoms:**
```
yaml.scanner.ScannerError: mapping values are not allowed here
ConfigurationError: Invalid configuration structure
```

**Validation:**
```bash
# Validate YAML syntax
python -c "
import yaml
with open('config/framework_config.yaml', 'r') as f:
    try:
        config = yaml.safe_load(f)
        print('✅ YAML syntax valid')
    except yaml.YAMLError as e:
        print(f'❌ YAML error: {e}')
"
```

**Auto-Fix:**
```bash
# Generate clean configuration
python main_controller.py --generate-config --output config/framework_config_new.yaml
```

#### **6.2 Environment Variable Issues**
**Symptoms:**
```
EnvironmentError: Required environment variables not set
WARNING: Framework running in degraded mode
```

**Environment Setup:**
```bash
# Check required variables
python main_controller.py --check-env

# Set required variables
export REVITRON_FRAMEWORK_HOME=$(pwd)
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
```

**Permanent Configuration:**
```bash
# Add to shell profile
echo 'export REVITRON_FRAMEWORK_HOME=$(pwd)' >> ~/.bashrc
echo 'export PYTHONPATH=$PYTHONPATH:$(pwd)/src' >> ~/.bashrc
source ~/.bashrc
```

---

## 🔍 Advanced Diagnostics

### **System Health Check**
```bash
python main_controller.py --health-check --verbose
```

**Expected Output:**
```
✅ Python version: 3.9+ 
✅ Dependencies installed: revitron, pyyaml, requests
✅ Configuration valid: framework_config.yaml
✅ Research access: All sources reachable
✅ Validation engine: Functional
✅ Memory available: 4GB+
✅ Disk space: 1GB+ available
```

### **Comprehensive Diagnostic Report**
```bash
python main_controller.py --diagnostic-report --output diagnostic_report.json
```

**Report Contents:**
- System configuration
- Dependency versions
- Network connectivity
- File permissions
- Performance metrics
- Error history

### **Debug Mode Operation**
```bash
# Enable maximum debugging
python main_controller.py --debug --verbose --log-level DEBUG --profile --trace
```

---

## 🛠️ Framework-Specific Troubleshooting

### **Self-Reflection Integration Issues (v2.0)**

#### **Research Completeness Failures**
The v2.0 framework requires 95%+ research completeness before proceeding.

**Symptoms:**
```
CRITICAL: Research completeness: 73% (95% required)
ERROR: Cannot proceed without adequate documentation access
```

**Solutions:**
```bash
# Force research completion
python main_controller.py --force-research-completion --accept-lower-quality

# Use cached research
python main_controller.py --use-research-cache --cache-age-hours 168
```

#### **100% Validation Coverage Issues**
The framework now requires 100% validation coverage, which can cause performance issues.

**Temporary Workaround:**
```yaml
# Emergency configuration
validation:
  mandatory_coverage: 75  # Temporary reduction
  fail_on_coverage: false
  log_validation_gaps: true
```

**Permanent Solution:**
```bash
# Optimize validation engine
python src/validation/validation_engine.py --optimize-performance
```

### **Integration Testing Failures**

#### **End-to-End Workflow Issues**
```bash
# Test complete workflow
python -m pytest tests/test_framework.py::test_complete_workflow -v

# If failing, run component tests individually
python -m pytest tests/test_framework.py::test_research_framework -v
python -m pytest tests/test_framework.py::test_validation_engine -v
python -m pytest tests/test_framework.py::test_button_generator -v
```

---

## 📊 Monitoring and Alerting

### **Log Analysis**
```bash
# View recent errors
tail -f logs/framework.log | grep ERROR

# Analyze performance patterns
grep "PERFORMANCE" logs/framework.log | tail -20

# Check validation patterns
grep "VALIDATION" logs/framework.log | grep -c "PASSED"
```

### **Performance Monitoring**
```python
# Monitor memory usage
import psutil
import os

process = psutil.Process(os.getpid())
print(f"Memory: {process.memory_info().rss / 1024 / 1024:.1f} MB")
print(f"CPU: {process.cpu_percent()}%")
```

### **Automated Health Monitoring**
```bash
# Create monitoring script
cat > monitor_framework.sh << 'EOF'
#!/bin/bash
while true; do
    python main_controller.py --health-check --quiet
    if [ $? -ne 0 ]; then
        echo "$(date): Framework health check failed" >> health_monitor.log
        # Send alert (customize as needed)
        # mail -s "Framework Alert" admin@company.com < health_monitor.log
    fi
    sleep 300  # Check every 5 minutes
done
EOF

chmod +x monitor_framework.sh
```

---

## 🆘 Getting Help

### **Self-Diagnosis First**
1. **Check Logs**: Review `logs/framework.log` for recent errors
2. **Run Health Check**: `python main_controller.py --health-check`
3. **Verify Environment**: Ensure all dependencies are installed
4. **Test Individual Components**: Run component tests to isolate issues

### **Community Resources**
- **GitHub Issues**: [Report bugs and request features](https://github.com/mohammedhadeez/revitron-ui-enhancement-framework/issues)
- **Documentation**: [Complete documentation suite](docs/)
- **Examples**: [Working examples](docs/USAGE_EXAMPLES.md)

### **Reporting Issues**
When reporting issues, please include:

```bash
# Generate diagnostic information
python main_controller.py --diagnostic-report --output issue_diagnostic.json
```

**Include in your issue:**
1. **Framework Version**: `python main_controller.py --version`
2. **System Information**: OS, Python version, dependencies
3. **Error Messages**: Complete error messages and stack traces
4. **Configuration**: Sanitized configuration files (remove sensitive data)
5. **Steps to Reproduce**: Detailed steps to reproduce the issue
6. **Expected vs Actual Behavior**: What you expected vs what happened

### **Emergency Support Procedures**
For critical issues affecting production workflows:

1. **Immediate Fallback**: Use v1.0.0 configuration if available
2. **Disable Problematic Features**: Temporarily disable failing components
3. **Manual Processing**: Use individual components if full framework fails
4. **Document Workarounds**: Record successful workarounds for team use

---

## 🔄 Recovery Procedures

### **Complete Framework Reset**
```bash
# Backup current state
cp -r config/ config_backup_$(date +%Y%m%d)
cp -r logs/ logs_backup_$(date +%Y%m%d)

# Reset to defaults
python main_controller.py --reset-all --confirm

# Restore custom configuration
cp config_backup_*/custom_settings.yaml config/
```

### **Partial Recovery**
```bash
# Reset only configuration
python main_controller.py --reset-config

# Reset only caches
python main_controller.py --clear-cache --all

# Reset only validation
python main_controller.py --reset-validation-engine
```

### **Data Recovery**
```bash
# Recover from backup
python main_controller.py --restore-from-backup backup_20250828/

# Rebuild from scratch
python main_controller.py --rebuild-database --source config/
```

---

**💡 Remember:** The v2.0 framework addresses all critical issues identified in the comprehensive self-reflection analysis. If you encounter issues that seem related to the v1.0 problems (research access, validation coverage, duplicates, technical depth), verify you're using the correct v2.0 configuration and all self-reflection improvements are enabled.

**🎯 Framework Vision**: *A production-ready system that enables AEC professionals to systematically enhance Revitron UI with validated, implementable button suggestions backed by comprehensive technical specifications and quality assurance.*
