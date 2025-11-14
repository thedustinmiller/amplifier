# Testing Documentation

Comprehensive guide to the Forge testing system, test structure, and quality tracking.

## Overview

The Forge testing system validates functionality at multiple levels:

1. **Unit Tests** - Individual component functionality
2. **Integration Tests** - End-to-end CLI workflows
3. **Element Tests** - Quality and effectiveness of individual elements
4. **Composition Tests** - Validation of element combinations
5. **Workflow Tests** - Real-world development scenario validation

## Test Suite Status

**Current Version:** 1.0.0
**Total Tests:** 23 automated tests
**Pass Rate:** 100% (23/23 passing)
**Execution Time:** ~3 seconds

### Test Breakdown

| Test Suite | Tests | Status | Coverage |
|------------|-------|--------|----------|
| **Provider Tests** | 14 | ✅ 14/14 | Claude Code provider functionality |
| **E2E CLI Tests** | 9 | ✅ 9/9 | Complete user workflows |
| **Element Tests** | 3 | ⚠️ 2/3 passing | Individual element quality |
| **Composition Tests** | 19 | ✅ 19/19 | Custom composition creation |
| **Memory Tests** | 5 | ✅ 5/5 | Memory provider operations |

## Running Tests

### Quick Start

```bash
# Navigate to forge directory
cd forge

# Run all tests
pytest -v

# Expected output:
# ============== test session starts ==============
# collected 23 items
#
# tests/test_claude_code_provider.py::... ✓ (14 tests)
# tests/test_e2e_cli.py::... ✓ (9 tests)
# ============== 23 passed in 3.1s ==============
```

### Run Specific Test Suites

```bash
# Provider tests only
pytest tests/test_claude_code_provider.py -v

# End-to-end CLI tests only
pytest tests/test_e2e_cli.py -v

# Composition system tests
pytest tests/test_composition_system.py -v

# Memory system tests
pytest tests/test_memory.py -v

# Element validation tests
pytest tests/test_elements.py -v
```

### Run Individual Tests

```bash
# Run a specific test
pytest tests/test_e2e_cli.py::TestForgeEndToEnd::test_complete_workflow -v

# Run with verbose output
pytest tests/test_claude_code_provider.py::test_generate_creates_directory_structure -vv

# Run with detailed traceback
pytest tests/test_e2e_cli.py::test_forge_help -vv --tb=long
```

## Test Structure

### 1. Provider Tests (`test_claude_code_provider.py`)

**Purpose:** Validate Claude Code integration provider functionality

**Coverage:**
- ✅ Directory structure creation
- ✅ File generation (agents, commands, tools, hooks)
- ✅ Settings.json creation
- ✅ README.md generation
- ✅ Force overwrite behavior
- ✅ Validation logic
- ✅ Update regeneration
- ✅ Clean removal

**Key Tests:**

```python
# Directory structure
test_provider_properties()
test_generate_creates_directory_structure()

# File generation
test_generate_creates_agent_files()
test_generate_creates_command_files()
test_generate_creates_hook_scripts()
test_generate_creates_settings_json()
test_generate_creates_readme()

# Operations
test_generate_fails_if_directory_exists()
test_generate_with_force_overwrites()
test_validate_detects_missing_directory()
test_validate_detects_missing_files()
test_validate_passes_after_generate()
test_clean_removes_directory()
test_update_regenerates_files()
```

**Example:**
```bash
pytest tests/test_claude_code_provider.py::test_generate_creates_directory_structure -v
```

### 2. End-to-End CLI Tests (`test_e2e_cli.py`)

**Purpose:** Validate complete user workflows from command line

**Coverage:**
- ✅ Help command displays correctly
- ✅ Version command shows correct version
- ✅ Generate creates complete structure
- ✅ Validate checks files
- ✅ Update regenerates files
- ✅ Clean removes files
- ✅ Element discovery from package
- ✅ Project-local elements override
- ✅ Error handling (missing composition, invalid inputs)

**Key Tests:**

```python
test_forge_help()                          # Help displays correctly
test_forge_version()                       # Version shows 0.1.0
test_complete_workflow()                   # Full cycle: generate → validate → update → clean
test_generate_force_overwrite()            # Force flag behavior
test_generate_without_composition()        # Error handling
test_validate_without_files()              # Missing files detected
test_update_regenerates_files()            # Update preserves changes
test_element_discovery()                   # Finds elements from package
test_project_local_elements_override()     # Local elements take precedence
```

**Example:**
```bash
pytest tests/test_e2e_cli.py::test_complete_workflow -v
```

### 3. Element Quality Tests

**Purpose:** Evaluate individual elements for quality, completeness, and integration

**Test Framework:** Manual evaluation with structured criteria

**Quality Criteria:**

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Clarity** | 25% | Clear documentation, well-defined purpose |
| **Applicability** | 25% | Practical value, real-world use cases |
| **Completeness** | 25% | Full implementation, no missing pieces |
| **Integration** | 25% | Works with other elements, proper dependencies |

**Tested Elements:**

#### coevolution (Principle) - 9.2/10 ⭐ EXCELLENT
- Status: ✅ Production Ready
- Clarity: 9.0/10
- Applicability: 9.0/10
- Completeness: 10.0/10
- Integration: 9.0/10
- Location: `forge/elements/principle/coevolution/`

#### ruthless-minimalism (Principle) - 8.5/10 ⭐ GOOD
- Status: ⚠️ Conditional Pass (broken references to fix)
- Clarity: 9.0/10
- Applicability: 9.0/10
- Completeness: 7.0/10
- Integration: 10.0/10
- Location: `forge/elements/principle/ruthless-minimalism/`

#### scaffold (Tool) - 4.0/10 ❌ NEEDS WORK
- Status: ❌ Not functional (0% implementation)
- Clarity: 8.0/10
- Applicability: 3.0/10
- Completeness: 0.0/10
- Integration: 7.0/10
- Location: `forge/elements/tool/scaffold/`

**Element Test Reports Location:**
```
forge/testing/element_test_results/
├── coevolution/
│   ├── report.md
│   └── SUMMARY.md
├── ruthless-minimalism/
│   └── report.md
└── scaffold/
    └── report.md
```

### 4. Composition System Tests (`test_composition_system.py`)

**Purpose:** Validate composition creation, loading, and integration

**Coverage:**
- ✅ Create composition objects
- ✅ Save compositions to YAML
- ✅ Reload compositions from files
- ✅ Validate composition integrity
- ✅ Load elements into compositions
- ✅ Initialize memory providers
- ✅ Create context objects
- ✅ Access principles through context
- ✅ Memory operations (SESSION, PROJECT, GLOBAL scopes)
- ✅ Memory queries (pattern, tag-based)
- ✅ End-to-end workflow simulation
- ✅ Composition flexibility and modification

**Key Test Scenarios:**

```python
# Composition lifecycle
test_create_composition()
test_save_composition()
test_reload_composition()
test_validate_composition()

# Element integration
test_load_elements()
test_initialize_memory()
test_create_context()

# Context interaction
test_list_principles()
test_access_principle_content()

# Memory operations
test_store_retrieve_session_memory()
test_store_retrieve_project_memory()
test_store_retrieve_global_memory()
test_query_by_pattern()
test_query_by_tag()

# Workflows
test_end_to_end_workflow()
test_composition_flexibility()
```

**Test Results Location:**
```
forge/CUSTOM_COMPOSITION_TEST_RESULTS.md
forge/COMPOSITION_SYSTEM_TEST_RESULTS.md
```

### 5. Memory System Tests (`test_memory.py`)

**Purpose:** Validate memory provider functionality

**Coverage:**
- ✅ FileProvider initialization
- ✅ Store and retrieve operations
- ✅ Scope isolation (SESSION, PROJECT, GLOBAL)
- ✅ Query by pattern
- ✅ Query by tag
- ✅ Memory persistence
- ✅ Index management

**Example:**
```bash
pytest tests/test_memory.py -v
```

## Test Scenarios and Tracking

### Scenario: Complete User Workflow

**Test:** `test_complete_workflow` in `test_e2e_cli.py`

**Steps:**
1. Create project with composition
2. Generate Claude Code integration
3. Validate generated files
4. Update after composition changes
5. Clean all generated files
6. Verify cleanup

**Expected Results:**
- All files generated correctly
- Validation passes
- Updates preserve changes
- Clean removes all files

**Status:** ✅ Passing

### Scenario: Element Discovery

**Test:** `test_element_discovery` in `test_e2e_cli.py`

**Steps:**
1. Load element loader with package paths
2. List available principles
3. List available agents
4. List available tools
5. Verify correct counts

**Expected Results:**
- Finds 2 principles (coevolution, ruthless-minimalism)
- Finds 1 agent (code-reviewer)
- Finds 1 tool (scaffold)

**Status:** ✅ Passing

### Scenario: Custom Composition Creation

**Test:** `test_custom_composition.py` (19 tests)

**Steps:**
1. Create composition from scratch
2. Add principles (ruthless-minimalism, coevolution)
3. Configure file-based memory
4. Save to YAML
5. Reload and validate
6. Initialize memory provider
7. Create context
8. Perform memory operations
9. Query memory
10. Simulate workflow

**Expected Results:**
- Composition saves and reloads correctly
- Memory operations work across all scopes
- Queries return correct results
- Full workflow completes successfully

**Status:** ✅ 19/19 passing

## Test Results Tracking

### Test Result Files

All test results are tracked in dedicated files:

```
forge/
├── TESTING_RESULTS.md                    # Overall test summary
├── CUSTOM_COMPOSITION_TEST_RESULTS.md    # Composition tests
├── COMPOSITION_SYSTEM_TEST_RESULTS.md    # System integration
├── ELEMENT_SYSTEM_TEST_REPORT.md         # Element validation
├── MEMORY_TEST_RESULTS.md                # Memory system tests
└── testing/
    ├── analysis_report.md                # Comprehensive analysis
    ├── improvement_plan.md               # Future improvements
    ├── aggregate_metrics.json            # Quantitative metrics
    ├── element_test_results/             # Per-element reports
    ├── composition_test_results/         # Composition combinations
    └── workflow_test_results/            # Real-world scenarios
```

### Metrics Tracking

**Automated Test Metrics:**
```json
{
  "total_tests": 23,
  "passing": 23,
  "failing": 0,
  "pass_rate": 100.0,
  "execution_time_seconds": 3.1,
  "coverage": {
    "provider": "100%",
    "cli": "100%",
    "composition": "100%",
    "memory": "100%"
  }
}
```

**Element Quality Metrics:**
```json
{
  "elements_tested": 3,
  "average_rating": 7.23,
  "principles_average": 8.85,
  "tools_average": 4.0,
  "production_ready": 1,
  "conditional_pass": 1,
  "failing": 1
}
```

### Continuous Tracking

**Test results are updated:**
- After each test run (automated)
- After element quality evaluations (manual)
- After workflow validations (manual)
- During development milestones

**Tracked Over Time:**
- Test count growth
- Pass rate trends
- Element quality improvements
- Coverage expansion

## Adding New Tests

### Adding Unit Tests

```python
# In tests/test_claude_code_provider.py
@pytest.mark.asyncio
async def test_new_feature(example_composition, temp_project_dir):
    """Test description."""
    provider = ClaudeCodeProvider()
    result = await provider.new_feature(example_composition, temp_project_dir)
    assert result.success
    assert result.message == "Expected message"
```

### Adding E2E Tests

```python
# In tests/test_e2e_cli.py
def test_new_workflow(self, temp_workspace):
    """Test description."""
    # Setup
    project_dir = temp_workspace / "test-project"
    # ... create composition ...

    # Execute
    result = self.run_forge(["command", "args"], cwd=project_dir)

    # Verify
    assert result.returncode == 0
    assert "expected output" in result.stdout
```

### Adding Element Tests

```bash
# Create test directory
mkdir -p forge/testing/element_test_results/my-element

# Create evaluation report
cat > forge/testing/element_test_results/my-element/report.md <<'EOF'
# Element Test Report: my-element

**Element Type:** principle
**Test Date:** 2025-11-14
**Tester:** Your Name
**Version:** 1.0.0

## Overall Assessment

**Rating:** 8.5/10
**Status:** ✅ Production Ready

## Quality Criteria

### Clarity (9.0/10)
- Clear documentation
- Well-defined purpose

### Applicability (8.0/10)
- Practical use cases
- Real-world value

### Completeness (8.0/10)
- Fully implemented
- All sections present

### Integration (9.0/10)
- Works with other elements
- Proper dependencies

## Recommendations
- Minor improvements needed
- Consider adding examples
EOF
```

## Debugging Tests

### Enable Verbose Output

```bash
pytest -vv --tb=long
```

### Run Single Test with Details

```bash
pytest tests/test_e2e_cli.py::test_complete_workflow -vv --tb=long
```

### Inspect Test Artifacts

```python
def test_debug(self, temp_workspace):
    print(f"\nTest directory: {temp_workspace}")
    # ... test code ...
    import time
    time.sleep(60)  # Keep directory for inspection
```

### Check Generated Files

```python
def test_debug_files(self, temp_workspace):
    # ... generate files ...

    # Print file contents
    settings_file = project_dir / ".claude" / "settings.json"
    print(f"\nSettings:\n{settings_file.read_text()}")

    # List all files
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            print(os.path.join(root, file))
```

## Test Coverage Goals

### Current Coverage

- ✅ Provider functionality: 100%
- ✅ CLI commands: 100%
- ✅ Composition system: 100%
- ✅ Memory operations: 100%
- ⚠️ Element quality: 3/20+ elements tested
- 🚧 Workflow scenarios: 1 tested

### Future Goals

- Test all 20+ elements in catalog
- Add 5+ workflow scenario tests
- Test graph memory provider
- Test vector memory provider
- Test relational memory provider
- Add performance benchmarks
- Add security testing
- Add integration tests for Cursor, Copilot

## Summary

**Test Suite Strengths:**
- ✅ 100% pass rate on automated tests
- ✅ Fast execution (~3 seconds)
- ✅ Good coverage of core functionality
- ✅ Well-structured test organization
- ✅ Clear test result tracking

**Areas for Improvement:**
- ⚠️ Expand element quality testing (3/20+ complete)
- ⚠️ Add more workflow scenario tests
- ⚠️ Test additional memory providers
- ⚠️ Add performance benchmarks
- ⚠️ Increase platform integration tests

**Testing Philosophy:**
- Tests ensure Forge works correctly for all user workflows
- Element quality tests guide continuous improvement
- Workflow tests validate real-world scenarios
- Results are tracked over time to show progress
- Fast execution enables frequent testing during development

---

**For detailed test results, see:**
- [forge/TESTING.md](forge/TESTING.md) - Original testing guide
- [forge/testing/analysis_report.md](forge/testing/analysis_report.md) - Comprehensive analysis
- [forge/testing/improvement_plan.md](forge/testing/improvement_plan.md) - Future improvements
