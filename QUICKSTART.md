# Quickstart Guide

Get up and running with Forge in 10 minutes.

## What You'll Learn

- Install Forge and verify it works
- Initialize your first project with the interactive wizard
- Generate Claude Code integration
- Understand the project structure
- Make your first modifications

## Prerequisites

Before you begin, ensure you have:

- **Python 3.10 or higher** - Check with `python --version` or `python3 --version`
- **uv** (recommended) or pip - Fast Python package installer

### Install uv (if needed)

```bash
# Unix/macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or use pip
pip install uv
```

## Step 1: Install Forge

```bash
# Clone or navigate to the repository
cd /path/to/amplifier/forge

# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # Unix/macOS
# or
.venv\Scripts\activate     # Windows

# Install Forge
uv pip install -e .
```

**Expected output:**
```
Successfully installed forge-ai-0.1.0
```

## Step 2: Verify Installation

```bash
forge version
```

**Expected output:**
```
Forge version 0.1.0
```

```bash
forge
```

**Expected output:**
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
...
```

## Step 3: Create Your First Project

Choose between the **interactive wizard** (recommended for beginners) or **manual setup** (for advanced users).

### Option A: Interactive Wizard (Recommended)

```bash
# Navigate to where you want to create your project
cd ~/projects

# Run the wizard
forge init
```

**Follow the prompts:**

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
(Select as many as you like)

  1. ruthless-minimalism
     Ship the simplest thing that could possibly work, then adapt

  2. coevolution
     Specifications and code are conversation partners

Your selection: 1 2
✓ Selected 2 principles: ruthless-minimalism, coevolution

▶ Memory Configuration

Memory provider [file]:
Memory storage path [.forge/memory]:
✓ Configured file memory at .forge/memory

▶ Creating Composition

Composition name [hello-forge]:
Description [Development composition for hello-forge]: My first Forge project
✓ Saved composition to .forge/composition.yaml

▶ Initializing Memory

✓ Memory initialized successfully

🎉 Project Initialized!
============================================================

Your Forge project is ready!

📁 Project: /home/user/projects/hello-forge
📝 Composition: hello-forge
💾 Memory: file (.forge/memory)
🎯 Principles: ruthless-minimalism, coevolution

Next steps:
  1. cd hello-forge
  2. Review .forge/composition.yaml
  3. Start building!
```

### Option B: Manual Setup

```bash
# Create project directory
mkdir hello-forge && cd hello-forge

# Create Forge directory
mkdir -p .forge

# Create composition file
cat > .forge/composition.yaml <<'EOF'
composition:
  name: hello-forge
  type: preset
  version: 1.0.0
  description: My first Forge project

elements:
  principles:
    - ruthless-minimalism
    - coevolution
  constitutions: []
  tools: []
  agents: []
  templates: []
  hooks: {}
  queries: []

settings:
  memory:
    provider: file
    config:
      base_path: .forge/memory
  agent_orchestration:
    mode: sequential
    max_parallel: 3
  tool_defaults: {}
EOF

echo "✓ Project initialized manually"
```

## Step 4: Explore Your Project

```bash
cd hello-forge

# View project structure
tree -L 3 .
```

**You should see:**
```
.
└── .forge
    ├── composition.yaml
    └── memory
        ├── global
        ├── project
        └── session
```

**View your composition:**
```bash
cat .forge/composition.yaml
```

**Output:**
```yaml
composition:
  name: hello-forge
  type: preset
  version: 1.0.0
  description: My first Forge project

elements:
  principles:
    - ruthless-minimalism
    - coevolution
  # ... more configuration
```

## Step 5: Generate Claude Code Integration

If you're using Claude Code, generate the integration files:

```bash
forge generate claude-code
```

**Expected output:**
```
🔨 Generating Claude Code integration...

✓ Created directory: .claude
✓ Created directory: .claude/agents
✓ Created directory: .claude/commands
✓ Created directory: .claude/tools
✓ Generated settings.json
✓ Generated README.md

✓ Generation complete!

Created 5 files in .claude/
```

**Verify the files:**
```bash
ls -la .claude/
```

**Output:**
```
.claude/
├── agents/
├── commands/
├── tools/
├── settings.json
└── README.md
```

## Step 6: Validate Integration

```bash
forge validate claude-code
```

**Expected output:**
```
🔨 Validating Claude Code integration...

✓ Found .claude/ directory
✓ Found settings.json
✓ Found README.md
✓ Validated agents/
✓ Validated commands/
✓ Validated tools/

✓ Validation passed!
```

## Step 7: Make Your First Modification

### Add a Tool to Your Composition

```bash
# Edit the composition file
nano .forge/composition.yaml  # or vim, code, etc.
```

**Add the scaffold tool:**
```yaml
elements:
  principles:
    - ruthless-minimalism
    - coevolution
  tools:
    - scaffold  # Add this line
```

**Save and update Claude Code integration:**
```bash
forge update claude-code
```

**Expected output:**
```
🔨 Updating Claude Code integration...

✓ Updated settings.json
✓ Updated README.md
✓ Updated tools/ (1 tool added)

✓ Update complete!
```

**Verify the new tool:**
```bash
ls .claude/tools/
```

**Output:**
```
scaffold.md
```

## What's Next?

### Learn About Elements

Explore available elements in the Forge repository:

```bash
cd /path/to/amplifier/forge
ls elements/
```

**Available element types:**
- `principle/` - Guiding principles like ruthless-minimalism, coevolution
- `tool/` - Executable tools like scaffold, commit helpers
- `agent/` - Specialized agents like code-reviewer
- `template/` - Document templates for specs, plans, tasks

**Read an element:**
```bash
cat elements/principle/ruthless-minimalism/ruthless-minimalism.md
```

### Create a Custom Element

```bash
cd hello-forge

# Create a custom principle
mkdir -p .forge/elements/principle/my-principle

# Create element metadata
cat > .forge/elements/principle/my-principle/element.yaml <<'EOF'
metadata:
  name: my-principle
  type: principle
  version: 1.0.0
  description: My custom guiding principle
  tags: [custom]

dependencies:
  principles: []
EOF

# Create element content
cat > .forge/elements/principle/my-principle/my-principle.md <<'EOF'
# Principle: My Custom Principle

## Core Tenet
Always write clear, concise code that others can understand.

## Motivation
Code is read more often than written. Clarity beats cleverness.

## Implications
- Use descriptive variable names
- Add comments for complex logic
- Prefer simple solutions over clever ones
- Write code for humans, not machines
EOF

# Add to your composition
nano .forge/composition.yaml
# Add "- my-principle" to the principles list

# Update integration
forge update claude-code
```

### Try Different Memory Providers

The file provider is great for getting started, but you can upgrade:

```yaml
# In .forge/composition.yaml
settings:
  memory:
    provider: relational  # or graph, vector
    config:
      url: postgresql://localhost/mydb
```

### Explore Common Workflows

See [forge/docs/WORKFLOWS.md](forge/docs/WORKFLOWS.md) for detailed workflows:

- Rapid prototyping
- Test-driven development
- Specification-driven development
- Documentation-first development

### Use with Claude Code

If you generated the Claude Code integration:

1. Open your project in Claude Code
2. The `.claude/` directory is automatically loaded
3. Principles guide Claude's behavior
4. Tools and agents are available as commands
5. Memory persists across conversations

**Example Claude Code workflow:**
```bash
# In Claude Code chat
"I want to scaffold a new Python web service"

# Claude will use:
# - ruthless-minimalism principle → suggest minimal implementation
# - coevolution principle → create both spec sketch and initial code
# - scaffold tool → generate basic project structure
# - memory → remember this decision for future sessions
```

## Troubleshooting

### "Command not found: forge"

**Solution:** Activate your virtual environment first:
```bash
source /path/to/amplifier/forge/.venv/bin/activate
```

### "Composition not found"

**Solution:** Make sure you're in a directory with `.forge/composition.yaml`:
```bash
# Check current directory
ls -la .forge/

# Or initialize a new project
forge init
```

### "No elements found"

**Solution:** Forge looks for elements in these locations (in order):
1. `.forge/elements/` (project-local)
2. Package installation path

**Verify element discovery:**
```bash
python3 << 'EOF'
from forge.utils import get_element_search_paths
print("Search paths:", get_element_search_paths())
EOF
```

### Permission Errors

**Solution:** Ensure the `.forge/memory` directory is writable:
```bash
chmod -R 755 .forge/
```

## Quick Reference

### Essential Commands

```bash
forge                    # Show help
forge version            # Show version
forge init               # Create new project (wizard)
forge generate claude-code  # Generate Claude Code files
forge validate claude-code  # Validate generated files
forge update claude-code    # Update after composition changes
forge clean claude-code     # Remove generated files
```

### Project Structure

```
your-project/
├── .forge/
│   ├── composition.yaml       # Your methodology definition
│   ├── memory/                # Persistent context
│   │   ├── session/          # Ephemeral (current session)
│   │   ├── project/          # Project-specific
│   │   └── global/           # Cross-project learnings
│   └── elements/             # Custom elements (optional)
└── .claude/                   # Generated Claude Code integration
    ├── agents/               # AI agent definitions
    ├── commands/             # Slash commands
    ├── tools/                # Available tools
    ├── settings.json         # Claude Code settings
    └── README.md             # Integration documentation
```

### Key Files

- **`.forge/composition.yaml`** - Defines your methodology (elements + settings)
- **`.claude/settings.json`** - Claude Code configuration
- **`.forge/memory/`** - Persistent memory across sessions

## Next Steps

1. **Read the full documentation**: [README.md](README.md) for system overview
2. **Understand testing**: [TESTING.md](TESTING.md) for test structure
3. **Explore commands**: [forge/docs/COMMANDS.md](forge/docs/COMMANDS.md) for detailed command reference
4. **Learn workflows**: [forge/docs/WORKFLOWS.md](forge/docs/WORKFLOWS.md) for common development patterns
5. **Browse elements**: [forge/ELEMENT_CATALOG.md](forge/ELEMENT_CATALOG.md) for all available elements

---

**Happy Forging! Start simple, compose freely, scale when needed.**
