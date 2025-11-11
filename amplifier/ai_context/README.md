# 🤖 AI Context

Reference materials and supporting documentation for AI-assisted development.

## Organization

### Core Philosophy
- **core/** - Core development philosophy (symlinked to AGENTS.md for single source of truth)
  - `AGENTS.md` → Points to root AGENTS.md
  - `IMPLEMENTATION_PHILOSOPHY.md` → Points to root AGENTS.md (backwards compatibility)
  - `MODULAR_DESIGN_PHILOSOPHY.md` → Points to root AGENTS.md (backwards compatibility)

### Design Resources
- **design/** - Design-specific philosophy and frameworks
  - `DESIGN-FRAMEWORK.md` - Comprehensive design framework
  - `DESIGN-VISION.md` - Design vision and approach
  - `DESIGN-PHILOSOPHY.md` - Design philosophy
  - `DESIGN-PRINCIPLES.md` - Core design principles

### Reference Materials
- **reference/** - External library documentation and references
- **claude_code/** - Claude Code platform documentation (cached for offline use)
  - Includes CLI reference, hooks, subagents, SDK documentation

### Tool-Specific Context
- **tools/** - Context files for specific tools
  - `module_generator/` - Module generation specifications

### Generated Content
- **generated/** - Auto-generated project file roll-ups for LLM consumption

## Usage

Most AI sessions should load from the root `AGENTS.md` file, which serves as the single source of truth for development philosophy. The files in this directory provide supporting context and specialized knowledge.

See `profiles/` for profile-based development methodologies that compose these materials in different ways.
