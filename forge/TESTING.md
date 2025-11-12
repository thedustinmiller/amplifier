# Testing Guide for Forge

This document describes how to test Forge at various levels.

## Test Suite Overview

Forge has comprehensive test coverage:

- **Unit Tests** (`test_claude_code_provider.py`): 14 tests for provider functionality
- **Integration Tests** (`test_e2e_cli.py`): 9 tests for complete user workflows
- **Total**: 23 tests with 100% pass rate

## Running Tests

### All Tests

```bash
cd forge
pytest -v
```

### Provider Tests Only

```bash
pytest tests/test_claude_code_provider.py -v
```

Output:
```
tests/test_claude_code_provider.py::test_provider_properties PASSED
tests/test_claude_code_provider.py::test_generate_creates_directory_structure PASSED
tests/test_claude_code_provider.py::test_generate_creates_agent_files PASSED
tests/test_claude_code_provider.py::test_generate_creates_command_files PASSED
tests/test_claude_code_provider.py::test_generate_creates_hook_scripts PASSED
tests/test_claude_code_provider.py::test_generate_creates_settings_json PASSED
tests/test_claude_code_provider.py::test_generate_creates_readme PASSED
tests/test_claude_code_provider.py::test_generate_fails_if_directory_exists PASSED
tests/test_claude_code_provider.py::test_generate_with_force_overwrites PASSED
tests/test_claude_code_provider.py::test_validate_detects_missing_directory PASSED
tests/test_claude_code_provider.py::test_validate_detects_missing_files PASSED
tests/test_claude_code_provider.py::test_validate_passes_after_generate PASSED
tests/test_claude_code_provider.py::test_clean_removes_directory PASSED
tests/test_claude_code_provider.py::test_update_regenerates_files PASSED

14 passed
```

### End-to-End Tests Only

```bash
pytest tests/test_e2e_cli.py -v
```

Output:
```
tests/test_e2e_cli.py::TestForgeEndToEnd::test_forge_help PASSED
tests/test_e2e_cli.py::TestForgeEndToEnd::test_forge_version PASSED
tests/test_e2e_cli.py::TestForgeEndToEnd::test_complete_workflow PASSED
tests/test_e2e_cli.py::TestForgeEndToEnd::test_generate_force_overwrite PASSED
tests/test_e2e_cli.py::TestForgeEndToEnd::test_generate_without_composition PASSED
tests/test_e2e_cli.py::TestForgeEndToEnd::test_validate_without_files PASSED
tests/test_e2e_cli.py::TestForgeEndToEnd::test_update_regenerates_files PASSED
tests/test_e2e_cli.py::TestForgeEndToEnd::test_element_discovery PASSED
tests/test_e2e_cli.py::TestForgeEndToEnd::test_project_local_elements_override PASSED

9 passed
```

### Specific Test

```bash
pytest tests/test_e2e_cli.py::TestForgeEndToEnd::test_complete_workflow -v
```

## Manual Testing

### Test Element Discovery

Verify elements can be found from package:

```python
from forge.utils import get_element_search_paths
from forge.core.element import ElementLoader, ElementType

# Get search paths
paths = get_element_search_paths()
print(f"Search paths: {paths}")

# Load elements
loader = ElementLoader(search_paths=paths)
principles = loader.list_elements(ElementType.PRINCIPLE)
agents = loader.list_elements(ElementType.AGENT)
tools = loader.list_elements(ElementType.TOOL)

print(f"Found {len(principles)} principles:")
for p in principles:
    print(f"  - {p.name}: {p.metadata.description}")

print(f"\nFound {len(agents)} agents:")
for a in agents:
    print(f"  - {a.name}: {a.metadata.description}")

print(f"\nFound {len(tools)} tools:")
for t in tools:
    print(f"  - {t.name}: {t.metadata.description}")
```

Expected output:
```
Search paths: [PosixPath('/path/to/forge/elements')]
Found 2 principles:
  - coevolution: Specifications and code evolve together through dialogue
  - ruthless-minimalism: Ship simplest thing that works, adapt based on needs

Found 1 agents:
  - code-reviewer: Reviews code for quality, security, and best practices

Found 1 tools:
  - scaffold: Scaffolds new project structures and boilerplate code
```

### Test Complete Workflow

Create a test project and verify all commands work:

```bash
# Setup
mkdir test-project && cd test-project
mkdir -p .forge

# Create composition
cat > .forge/composition.yaml <<'EOF'
composition:
  name: test-project
  type: preset
  version: 1.0.0

elements:
  principles:
    - ruthless-minimalism
  agents:
    - code-reviewer
  tools:
    - scaffold
  hooks:
    SessionStart: session-logger

settings:
  memory:
    provider: file
EOF

# Test generate
forge generate claude-code
# Expected: Creates .claude/ with 5 files

# Verify files
ls -la .claude/
# Expected: agents/, commands/, tools/, settings.json, README.md

# Test validate
forge validate claude-code
# Expected: ✓ Validation passed!

# Test update
forge update claude-code
# Expected: ✓ Update complete!

# Test clean
echo "yes" | forge clean claude-code
# Expected: ✓ Clean complete! Removed 5+ files

# Verify clean
ls .claude/
# Expected: ls: .claude/: No such file or directory
```

### Test Error Handling

```bash
# Test without composition
cd /tmp/empty-dir
forge generate claude-code
# Expected: ✗ Composition not found

# Test duplicate generate without force
cd test-project
forge generate claude-code
forge generate claude-code
# Expected: ✗ .claude/ already exists

# Test with force
forge generate claude-code --force
# Expected: ✓ Generation complete!
```

### Test Help and Version

```bash
# Help
forge
# Expected: Shows usage, commands, examples

# Version
forge version
# Expected: Forge version 0.1.0
```

## Test Coverage

### Provider Tests

**Directory Structure:**
- ✅ Creates `.claude/` directory
- ✅ Creates `agents/`, `commands/`, `tools/` subdirectories
- ✅ Creates `settings.json` and `README.md`

**File Generation:**
- ✅ Agent files with correct frontmatter and content
- ✅ Command files with correct frontmatter and instructions
- ✅ Hook scripts with correct shebang and implementation
- ✅ Settings.json with hooks configuration

**Operations:**
- ✅ Force flag overwrites existing files
- ✅ Fails without force when directory exists
- ✅ Validate detects missing/invalid files
- ✅ Update regenerates changed files
- ✅ Clean removes all generated files

### End-to-End Tests

**CLI Commands:**
- ✅ Help displays correctly
- ✅ Version shows correct version
- ✅ Generate creates complete structure
- ✅ Validate checks files
- ✅ Update regenerates files
- ✅ Clean removes files

**Element Discovery:**
- ✅ Finds elements from installed package
- ✅ Project-local elements override package elements
- ✅ Works in development mode (repository)

**Error Handling:**
- ✅ Missing composition error
- ✅ Missing platform files warning
- ✅ Dependency validation

**Complete Workflows:**
- ✅ Full cycle: generate → validate → update → clean
- ✅ Force overwrite behavior
- ✅ Update preserves composition changes

## Continuous Integration

Add to CI pipeline:

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest pytest-asyncio
      - name: Run tests
        run: pytest -v
      - name: Test CLI
        run: |
          forge version
          forge --help
```

## Test Development

### Adding New Tests

1. **Provider Tests**: Add to `test_claude_code_provider.py`
   ```python
   @pytest.mark.asyncio
   async def test_new_feature(example_composition, temp_project_dir):
       provider = ClaudeCodeProvider()
       result = await provider.new_feature(example_composition, temp_project_dir)
       assert result.success
   ```

2. **E2E Tests**: Add to `test_e2e_cli.py`
   ```python
   def test_new_workflow(self, temp_workspace):
       result = self.run_forge(["command", "args"], cwd=temp_workspace)
       assert result.returncode == 0
       assert "expected output" in result.stdout
   ```

### Test Fixtures

**Provider Tests:**
- `temp_project_dir` - Temporary project directory
- `element_loader` - Configured element loader
- `example_composition` - Loaded example composition

**E2E Tests:**
- `temp_workspace` - Temporary workspace directory
- `self.run_forge()` - Helper to run forge commands

## Debugging Failed Tests

### Enable Verbose Output

```bash
pytest -vv --tb=long
```

### Run Single Test

```bash
pytest tests/test_e2e_cli.py::TestForgeEndToEnd::test_complete_workflow -vv
```

### Keep Test Artifacts

Modify test to print temp directory and not clean up:

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
    print(f"\nSettings content:\n{settings_file.read_text()}")

    # List all files
    import os
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            print(os.path.join(root, file))
```

## Test Maintenance

### Update Tests After Changes

When adding new features:
1. Add provider unit tests
2. Add E2E integration tests
3. Update test documentation
4. Verify all tests pass

### Test Data

Element examples in `elements/`:
- `agent/code-reviewer/` - Agent with dependencies
- `tool/scaffold/` - Tool with instructions
- `hook/session-logger/` - Hook with script
- `principle/ruthless-minimalism/` - Principle with content
- `principle/coevolution/` - Principle with content

Test compositions in `examples/`:
- `example-composition.yaml` - Complete working example

## Performance

Current test suite performance:
- Provider tests: ~0.5 seconds
- E2E tests: ~2.6 seconds
- Total: ~3.1 seconds

All tests run quickly enough for frequent execution during development.

## Summary

✅ 23 tests total (14 provider + 9 E2E)
✅ 100% pass rate
✅ Full workflow coverage
✅ Error handling tested
✅ Element discovery verified
✅ Fast execution (~3 seconds)

Tests ensure Forge works correctly for all user workflows and edge cases.
