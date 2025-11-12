# Forge CLI Usage Demo

This document demonstrates the complete workflow for using Forge to create compositions and generate Claude Code integrations.

## Installation

```bash
cd forge
pip install -e .
```

## Available Commands

```bash
forge                        # Show help
forge init                   # Initialize new project
forge add                    # Add elements to project
forge generate [provider]    # Generate platform files
forge validate [provider]    # Validate platform files
forge update [provider]      # Update platform files
forge clean [provider]       # Remove platform files
forge version                # Show version
```

## Complete Workflow Example

### Step 1: View Available Commands

```bash
$ forge

Forge CLI - A Composable AI Development System

Usage:
  forge init              Initialize a new Forge project (interactive wizard)
  forge add               Add elements to current project
  forge generate [PROVIDER] Generate AI platform files from composition
  forge validate [PROVIDER] Validate platform files against composition
  forge update [PROVIDER]   Update platform files when composition changes
  forge clean [PROVIDER]    Remove generated platform files
  forge version           Show version information

Examples:
  forge init                      # Start the interactive wizard
  forge add                       # Add elements to project
  forge generate claude-code      # Generate .claude/ directory
  forge generate claude-code -f   # Force overwrite existing files
  forge validate claude-code      # Check if .claude/ matches composition

Available Providers:
  claude-code    Claude Code integration (.claude/ directory)

Learn more:
  https://github.com/yourorg/forge
```

### Step 2: Create a New Project

Option A: Use the interactive wizard (recommended for first-time users):

```bash
$ forge init

🔨 Forge Project Wizard
============================================================

Welcome to Forge!

Forge is a composable AI development system. This wizard will help you:
  • Choose guiding principles for your project
  • Select development tools
  • Configure memory storage
  • Create your first composition

Let's get started!

▶ Project Information

Project name [my-project]: demo-app
✓ Created project directory: /path/to/demo-app

▶ Loading Available Elements

✓ Found 2 principles

▶ Choose Guiding Principles

Principles define your project's philosophy and values.
They guide decision-making throughout development.

Select principles to guide your project:
(Select as many as you like)

  1. ruthless-minimalism
     Ship the simplest thing that could possibly work, then adapt based on real needs

  2. coevolution
     Specifications and code are conversation partners that inform each other

Your selection: 1 2
✓ Selected 2 principles: ruthless-minimalism, coevolution

▶ Memory Configuration

Memory provider [file]:
Memory storage path [.forge/memory]:
✓ Configured file memory at .forge/memory

▶ Creating Composition

Composition name [demo-app]:
Description: My demo application
✓ Saved composition to .forge/composition.yaml

▶ Initializing Memory

✓ Memory initialized successfully

▶ Creating Documentation

✓ Created README.md

🎉 Project Initialized!
============================================================

Your Forge project is ready!

📁 Project: /path/to/demo-app
📝 Composition: demo-app
💾 Memory: file (.forge/memory)
🎯 Principles: ruthless-minimalism, coevolution

Next steps:

  1. cd demo-app
  2. Review README.md for more information
  3. Customize .forge/composition.yaml as needed
  4. Start building!

Happy forging! 🔨
```

Option B: Create manually:

```bash
mkdir my-project
cd my-project
mkdir -p .forge

cat > .forge/composition.yaml <<EOF
composition:
  name: my-project
  type: preset
  version: 1.0.0
  description: My custom project

elements:
  principles:
    - ruthless-minimalism
    - coevolution
  agents:
    - code-reviewer
  tools:
    - scaffold
  hooks:
    SessionStart: session-logger

settings:
  memory:
    provider: file
    config:
      base_path: .forge/memory
EOF
```

### Step 3: Generate Claude Code Integration

```bash
$ forge generate claude-code

📁 Project: /path/to/my-project
🔨 Provider: claude-code

▶ Loaded composition: my-project
  • 2 principles
  • 1 agents
  • 1 tools
  • 1 hooks

▶ Generating claude-code files...

✓ Generation complete!

📝 Created 5 files:
  • .claude/agents/code-reviewer.md
  • .claude/commands/scaffold.md
  • .claude/tools/hook_sessionstart.py
  • .claude/settings.json
  • .claude/README.md

🎉 Done! Your AI platform files are ready.
```

### Step 4: Inspect Generated Files

```bash
$ tree .claude/
.claude/
├── README.md
├── agents
│   └── code-reviewer.md
├── commands
│   └── scaffold.md
├── settings.json
└── tools
    └── hook_sessionstart.py

$ cat .claude/agents/code-reviewer.md
---
name: code-reviewer
description: "Reviews code for quality, security, and best practices"
model: inherit
role: "code_reviewer"
---

You are an expert code reviewer focused on quality, security, and maintainability.

When reviewing code:
1. Check for security vulnerabilities
2. Assess code quality and readability
3. Identify potential bugs or edge cases
4. Suggest improvements for maintainability
5. Ensure adherence to best practices

Provide constructive, actionable feedback.

$ cat .claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash",
      "TodoWrite",
      "WebFetch"
    ],
    "deny": [],
    "defaultMode": "bypassPermissions",
    "additionalDirectories": [
      ".forge",
      ".data"
    ]
  },
  "enableAllProjectMcpServers": false,
  "enabledMcpjsonServers": [],
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/tools/hook_sessionstart.py",
            "timeout": 3000
          }
        ]
      }
    ]
  }
}
```

### Step 5: Validate Integration

```bash
$ forge validate claude-code

📁 Project: /path/to/my-project
🔨 Provider: claude-code

▶ Validating claude-code files...

✓ Validation passed!
```

### Step 6: Modify Composition

Edit `.forge/composition.yaml` to add more elements:

```yaml
elements:
  principles:
    - ruthless-minimalism
    - coevolution
  agents:
    - code-reviewer
    - bug-hunter          # NEW
  tools:
    - scaffold
    - deploy              # NEW
  hooks:
    SessionStart: session-logger
```

### Step 7: Update Generated Files

```bash
$ forge update claude-code

📁 Project: /path/to/my-project
🔨 Provider: claude-code

▶ Loaded composition: my-project
  • 2 principles
  • 2 agents
  • 2 tools
  • 1 hooks

▶ Updating claude-code files...

✓ Update complete!

📝 Created 2 files:
  • .claude/agents/bug-hunter.md
  • .claude/commands/deploy.md

🔄 Updated 2 files:
  • .claude/settings.json
  • .claude/README.md

🎉 Done! Your AI platform files have been updated.
```

### Step 8: Using with Claude Code

Now when you open this project in Claude Code, it will automatically load:

- **Agents** from `.claude/agents/`
- **Commands** as `/scaffold`, `/deploy`, etc.
- **Hooks** that trigger on events

Example usage in Claude Code:

```
# Use an agent
Can you review this code for security issues?
[Claude Code invokes code-reviewer agent via Task tool]

# Use a command
/scaffold python --name my-module

# Hooks run automatically
[SessionStart hook logs session start to .forge/logs/]
```

### Step 9: Clean Up (Optional)

Remove all generated files:

```bash
$ forge clean claude-code

📁 Project: /path/to/my-project
🔨 Provider: claude-code

⚠️  WARNING: This will remove all claude-code files from:
   /path/to/my-project

Are you sure? Type 'yes' to confirm: yes

▶ Cleaning claude-code files...

✓ Clean complete!

🗑️  Removed 7 files:
  • .claude/README.md
  • .claude/settings.json
  • .claude/agents/code-reviewer.md
  • .claude/agents/bug-hunter.md
  • .claude/commands/scaffold.md
  • .claude/commands/deploy.md
  • .claude/tools/hook_sessionstart.py

🎉 Done! AI platform files have been removed.
```

## Advanced Usage

### Force Overwrite

Regenerate files even if they exist:

```bash
forge generate claude-code --force
# or
forge generate claude-code -f
```

### Specify Project Directory

Work with projects outside current directory:

```bash
forge generate claude-code --project-dir /path/to/project
# or
forge generate claude-code -d /path/to/project
```

### Quick Validation

```bash
forge validate claude-code && echo "✓ Valid" || echo "✗ Invalid"
```

### Update Workflow

```bash
# Edit composition
vim .forge/composition.yaml

# Validate changes
forge validate claude-code

# Update generated files
forge update claude-code

# Commit changes
git add .forge/ .claude/
git commit -m "feat: Add bug-hunter agent and deploy tool"
```

## Composition Patterns

### Minimal Setup

```yaml
composition:
  name: minimal
  type: preset
  version: 1.0.0

elements:
  principles:
    - ruthless-minimalism
  agents: []
  tools: []
  hooks: {}

settings:
  memory:
    provider: file
    config:
      base_path: .forge/memory
```

### Full Stack Development

```yaml
composition:
  name: full-stack
  type: preset
  version: 1.0.0

elements:
  principles:
    - ruthless-minimalism
    - coevolution
  agents:
    - code-reviewer
    - database-architect
    - api-designer
  tools:
    - scaffold
    - migrate
    - deploy
  hooks:
    SessionStart: session-logger
    PostToolUse: code-formatter
    PreCompact: transcript-saver

settings:
  memory:
    provider: file
    config:
      base_path: .forge/memory
  agent_orchestration:
    mode: sequential
    max_parallel: 3
```

### Security-Focused

```yaml
composition:
  name: security-focused
  type: preset
  version: 1.0.0

elements:
  principles:
    - security-first
    - coevolution
  agents:
    - security-guardian
    - code-reviewer
    - vulnerability-scanner
  tools:
    - security-audit
    - dependency-check
  hooks:
    PreCommit: security-scan

settings:
  memory:
    provider: file
    config:
      base_path: .forge/memory
```

## Troubleshooting

### Issue: "Composition not found"

**Solution**: Make sure you're in a directory with `.forge/composition.yaml`:

```bash
ls .forge/composition.yaml
# or
forge init  # to create a new project
```

### Issue: ".claude/ directory already exists"

**Solution**: Use `--force` to overwrite:

```bash
forge generate claude-code --force
```

### Issue: "Unknown provider: xyz"

**Solution**: Check available providers:

```bash
forge  # Shows available providers in help text
```

Currently supported:
- `claude-code`

### Issue: Validation warnings

**Solution**: Either update composition or regenerate files:

```bash
# Option 1: Update composition to match files
vim .forge/composition.yaml

# Option 2: Regenerate files from composition
forge update claude-code --force
```

## Tips & Best Practices

1. **Version Control**: Commit both `.forge/` and `.claude/` directories

   ```bash
   git add .forge/ .claude/
   git commit -m "feat: Add Forge composition and Claude Code integration"
   ```

2. **Regular Validation**: Run validate after manual edits

   ```bash
   forge validate claude-code
   ```

3. **Composition as Source of Truth**: Edit composition, then update

   ```bash
   vim .forge/composition.yaml
   forge update claude-code
   ```

4. **Use Force Sparingly**: Only use `--force` when intentional

5. **Document Changes**: Keep README.md updated with composition changes

6. **Test Integration**: Verify generated files work in Claude Code

## Next Steps

- [Create Custom Elements](./docs/element-types.md)
- [Understand Providers](./docs/providers/README.md)
- [Claude Code Integration Guide](./docs/providers/claude-code.md)
- [Memory System](./docs/memory-system.md)
- [Contribute](./CONTRIBUTING.md)

---

**Happy Forging! 🔨**
