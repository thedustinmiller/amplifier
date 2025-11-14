# Forge Command Reference

Comprehensive guide to all Forge CLI commands with detailed usage, options, and examples.

## Table of Contents

- [Global Options](#global-options)
- [forge (Help)](#forge-help)
- [forge version](#forge-version)
- [forge init](#forge-init)
- [forge generate](#forge-generate)
- [forge validate](#forge-validate)
- [forge update](#forge-update)
- [forge clean](#forge-clean)
- [forge test](#forge-test)

---

## Global Options

These options apply to all Forge commands:

```bash
--help, -h        Show help message and exit
--version         Show version information
```

## forge (Help)

**Purpose:** Display help information and available commands.

### Usage

```bash
forge
forge --help
forge -h
```

### Output

```
🔨 Forge - Composable AI Development System

Usage:
  forge                    Show this help message
  forge version            Show version information
  forge init               Initialize a new Forge project
  forge generate <target>  Generate platform-specific files
  forge validate <target>  Validate platform integration
  forge update <target>    Update platform integration
  forge clean <target>     Clean platform integration
  forge test               Run test suite

Examples:
  forge init                      # Interactive project wizard
  forge generate claude-code      # Generate Claude Code integration
  forge validate claude-code      # Validate generated files
  forge update claude-code        # Update after composition changes
  forge clean claude-code         # Remove generated files

For detailed help on a command:
  forge <command> --help

Documentation: https://github.com/yourorg/forge
```

### Examples

```bash
# Show help
forge

# Show help for specific command
forge generate --help
```

---

## forge version

**Purpose:** Display Forge version information.

### Usage

```bash
forge version
```

### Output

```
Forge version 0.1.0
```

### Examples

```bash
# Check version
forge version
```

---

## forge init

**Purpose:** Initialize a new Forge project with interactive wizard.

### Usage

```bash
forge init [OPTIONS]
```

### Options

Currently no options (wizard is interactive).

### Wizard Flow

1. **Project Information**
   - Project name
   - Directory creation

2. **Element Selection**
   - Choose guiding principles
   - Select tools (optional)
   - Select agents (optional)
   - Select templates (optional)

3. **Memory Configuration**
   - Provider selection (file, graph, vector, relational)
   - Storage path configuration

4. **Composition Creation**
   - Composition name
   - Description
   - Save to `.forge/composition.yaml`

5. **Memory Initialization**
   - Create directory structure
   - Initialize provider

6. **Documentation Creation**
   - Generate README.md (optional)

### Example Session

```bash
forge init
```

**Interactive prompts:**

```
🔨 Forge Project Wizard
============================================================

Welcome to Forge!
...

▶ Project Information

Project name [my-project]: hello-forge
✓ Created project directory: /home/user/projects/hello-forge

▶ Loading Available Elements

✓ Found 2 principles

▶ Choose Guiding Principles

Select principles to guide your project:
  1. ruthless-minimalism
  2. coevolution

Your selection: 1 2
✓ Selected 2 principles

▶ Memory Configuration

Memory provider [file]:
Memory storage path [.forge/memory]:
✓ Configured file memory

▶ Creating Composition

Composition name [hello-forge]:
Description: My first Forge project
✓ Saved composition

🎉 Project Initialized!

Next steps:
  1. cd hello-forge
  2. Review .forge/composition.yaml
  3. forge generate claude-code
```

### Result Structure

```
hello-forge/
├── .forge/
│   ├── composition.yaml
│   └── memory/
│       ├── session/
│       ├── project/
│       └── global/
└── README.md (optional)
```

---

## forge generate

**Purpose:** Generate platform-specific integration files from Forge composition.

### Usage

```bash
forge generate [PROVIDER] [OPTIONS]
```

### Arguments

- `PROVIDER` - Target platform (default: `claude-code`)
  - Currently supported: `claude-code`
  - Planned: `cursor`, `copilot`

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--project-dir DIR` | `-d DIR` | Project directory (default: current directory) |
| `--force` | `-f` | Overwrite existing files without prompting |
| `--help` | `-h` | Show help message |

### Behavior

1. **Load Composition**
   - Read `.forge/composition.yaml`
   - Load all referenced elements
   - Validate dependencies

2. **Generate Files**
   - Create platform-specific directory structure
   - Generate configuration files
   - Create agent definitions
   - Create command files
   - Create tool files
   - Create hook scripts

3. **Report Results**
   - List created files
   - Show warnings (if any)
   - Display next steps

### Exit Codes

- `0` - Success
- `1` - Error (missing composition, invalid provider, generation failed)

### Examples

```bash
# Generate Claude Code integration (current directory)
forge generate claude-code

# Generate with explicit project directory
forge generate claude-code --project-dir /path/to/project

# Generate and overwrite existing files
forge generate claude-code --force

# Short form with force
forge generate claude-code -f
```

### Output Example

```
📁 Project: /home/user/hello-forge
🔨 Provider: claude-code

▶ Loaded composition: hello-forge
  • 2 principles
  • 0 agents
  • 0 tools
  • 0 hooks

▶ Generating claude-code files...

✓ Generation complete!

📝 Created 5 files:
  • .claude/settings.json
  • .claude/README.md
  • .claude/agents/
  • .claude/commands/
  • .claude/tools/

🎉 Done! Your AI platform files are ready.
```

### Generated Structure (Claude Code)

```
.claude/
├── settings.json          # Claude Code configuration
├── README.md              # Integration documentation
├── agents/                # Agent definitions
│   └── *.md              # One file per agent
├── commands/              # Slash commands
│   └── *.md              # One file per command
└── tools/                 # Tool definitions
    └── *.md              # One file per tool
```

### Error Handling

```bash
# Missing composition
$ forge generate claude-code
✗ Composition not found: .forge/composition.yaml
✗ Run 'forge init' to create a new project first.

# Directory already exists (without --force)
$ forge generate claude-code
✗ .claude/ already exists
✗ Use --force to overwrite

# Unknown provider
$ forge generate unknown-platform
✗ Unknown provider: unknown-platform
Available providers: claude-code
```

---

## forge validate

**Purpose:** Validate platform integration files against Forge composition.

### Usage

```bash
forge validate [PROVIDER] [OPTIONS]
```

### Arguments

- `PROVIDER` - Target platform (default: `claude-code`)

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--project-dir DIR` | `-d DIR` | Project directory (default: current directory) |
| `--help` | `-h` | Show help message |

### Validation Checks

1. **Directory Structure**
   - Platform directory exists
   - Required subdirectories present

2. **Required Files**
   - Configuration files exist
   - README present

3. **Element Files**
   - All agents have corresponding files
   - All tools have corresponding files
   - All commands have corresponding files
   - All hooks have corresponding scripts

4. **Content Validation**
   - Files have correct format
   - Required frontmatter present
   - Content matches composition

### Exit Codes

- `0` - Validation passed
- `1` - Validation failed

### Examples

```bash
# Validate Claude Code integration
forge validate claude-code

# Validate specific project
forge validate claude-code --project-dir /path/to/project
```

### Output Example (Success)

```
📁 Project: /home/user/hello-forge
🔨 Provider: claude-code

▶ Validating claude-code files...

✓ Found .claude/ directory
✓ Found settings.json
✓ Found README.md
✓ Validated agents/ (0 files)
✓ Validated commands/ (0 files)
✓ Validated tools/ (0 files)

✓ Validation passed!
```

### Output Example (Errors)

```
📁 Project: /home/user/hello-forge
🔨 Provider: claude-code

▶ Validating claude-code files...

✗ Validation failed!

Errors:
  ✗ Missing directory: .claude/
  ✗ Missing file: settings.json

Suggestions:
  💡 Run 'forge generate claude-code' to create files
```

---

## forge update

**Purpose:** Update platform integration files after composition changes.

### Usage

```bash
forge update [PROVIDER] [OPTIONS]
```

### Arguments

- `PROVIDER` - Target platform (default: `claude-code`)

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--project-dir DIR` | `-d DIR` | Project directory (default: current directory) |
| `--help` | `-h` | Show help message |

### Behavior

1. **Load Current Composition**
   - Read `.forge/composition.yaml`
   - Load all elements
   - Identify changes from last generation

2. **Update Files**
   - Regenerate configuration files
   - Add new element files
   - Remove files for deleted elements
   - Update existing files with new content

3. **Preserve Changes**
   - Keep user customizations where possible
   - Warn about conflicts

### Exit Codes

- `0` - Success
- `1` - Error

### Examples

```bash
# Update after adding elements to composition
forge update claude-code

# Update specific project
forge update claude-code --project-dir /path/to/project
```

### Output Example

```
📁 Project: /home/user/hello-forge
🔨 Provider: claude-code

▶ Loaded composition: hello-forge
  • 2 principles
  • 1 agent (1 new)
  • 1 tool (1 new)
  • 0 hooks

▶ Updating claude-code files...

✓ Update complete!

📝 Created 2 files:
  • .claude/agents/code-reviewer.md
  • .claude/tools/scaffold.md

🔄 Updated 2 files:
  • .claude/settings.json
  • .claude/README.md

🎉 Done! Your AI platform files have been updated.
```

### When to Use

- After adding elements to `composition.yaml`
- After removing elements from `composition.yaml`
- After updating element versions
- After changing composition settings

---

## forge clean

**Purpose:** Remove generated platform integration files.

### Usage

```bash
forge clean [PROVIDER] [OPTIONS]
```

### Arguments

- `PROVIDER` - Target platform (default: `claude-code`)

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--project-dir DIR` | `-d DIR` | Project directory (default: current directory) |
| `--force` | `-f` | Skip confirmation prompt |
| `--help` | `-h` | Show help message |

### Behavior

1. **Confirmation** (unless `--force`)
   - Prompt user to confirm deletion
   - Require typing "yes" to proceed

2. **Remove Files**
   - Delete platform directory
   - Remove all generated files
   - Clean up empty directories

3. **Report Results**
   - List removed files
   - Show any errors

### Exit Codes

- `0` - Success or aborted
- `1` - Error

### Examples

```bash
# Clean with confirmation
forge clean claude-code

# Clean without confirmation
forge clean claude-code --force

# Clean specific project
forge clean claude-code --project-dir /path/to/project -f
```

### Output Example (With Confirmation)

```
📁 Project: /home/user/hello-forge
🔨 Provider: claude-code

⚠️  WARNING: This will remove all claude-code files from:
   /home/user/hello-forge

Are you sure? Type 'yes' to confirm: yes

▶ Cleaning claude-code files...

✓ Clean complete!

🗑️  Removed 5 files:
  • .claude/settings.json
  • .claude/README.md
  • .claude/agents/
  • .claude/commands/
  • .claude/tools/

🎉 Done! AI platform files have been removed.
```

### Output Example (Aborted)

```
📁 Project: /home/user/hello-forge
🔨 Provider: claude-code

⚠️  WARNING: This will remove all claude-code files from:
   /home/user/hello-forge

Are you sure? Type 'yes' to confirm: no
Aborted.
```

### When to Use

- Switching to a different platform
- Resetting integration to start fresh
- Removing integration entirely
- Testing generation from clean state

---

## forge test

**Purpose:** Run Forge test suite.

### Usage

```bash
forge test [OPTIONS]
```

### Options

Currently runs pytest with default configuration.

### Examples

```bash
# Run all tests
forge test
```

### Output

```
============== test session starts ==============
collected 23 items

tests/test_claude_code_provider.py ✓✓✓✓✓✓✓✓✓✓✓✓✓✓
tests/test_e2e_cli.py ✓✓✓✓✓✓✓✓✓

============== 23 passed in 3.1s ==============
```

---

## Command Workflows

### Initial Setup

```bash
forge init
cd my-project
forge generate claude-code
forge validate claude-code
```

### Modify Composition

```bash
# Edit .forge/composition.yaml
nano .forge/composition.yaml

# Update integration
forge update claude-code

# Validate changes
forge validate claude-code
```

### Reset Integration

```bash
forge clean claude-code --force
forge generate claude-code
```

### Switch Projects

```bash
# Project 1
cd project1
forge generate claude-code

# Project 2
cd ../project2
forge generate claude-code
```

---

## Error Messages Reference

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Composition not found` | No `.forge/composition.yaml` | Run `forge init` |
| `Unknown provider` | Invalid provider name | Use `claude-code` |
| `Directory already exists` | Files already generated | Use `--force` or `clean` first |
| `Validation failed` | Missing or invalid files | Run `forge generate` |
| `Element not found` | Invalid element reference | Check element names in composition |

### Exit Code Summary

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Error occurred |

---

## Tips and Best Practices

### Use `--force` Carefully

The `--force` flag overwrites files without confirmation. Use it when:
- You want to reset to generated defaults
- You know you have no custom modifications
- You're testing or debugging

**Don't use it when:**
- You've made manual customizations to generated files
- You're unsure what will be overwritten

### Validate Often

```bash
# After any manual changes
forge validate claude-code

# Before committing to version control
forge validate claude-code
```

### Update vs Generate

- **Use `generate`**: First time setup, complete reset
- **Use `update`**: After composition changes, incremental updates

### Version Control

```bash
# .gitignore recommendations
.forge/memory/session/    # Ephemeral session data
.venv/                    # Virtual environment

# Commit these:
.forge/composition.yaml   # Your methodology
.forge/elements/          # Custom elements
.claude/                  # Generated integration (optional)
```

---

For more information, see:
- [WORKFLOWS.md](WORKFLOWS.md) - Common development workflows
- [../README.md](../README.md) - Project overview
- [element-types.md](element-types.md) - Element documentation
- [memory-system.md](memory-system.md) - Memory system guide
