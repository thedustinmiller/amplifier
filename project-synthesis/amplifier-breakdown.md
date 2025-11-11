# Amplifier: Complete Project Breakdown

## Executive Summary

**Amplifier** is a **metacognitive AI development system** that transforms Claude Code from a simple coding assistant into a supercharged development platform. It multiplies human capability through AI partnership by providing memory, specialized agents, executable methodologies, and automatic quality assurance—all while remaining technology-agnostic and non-prescriptive.

**Core Innovation**: The system makes development methodology itself **mutable, explicit, and subject to continuous improvement** through composable profiles.

---

## 1. Vision and Purpose

### The Problem
"I have more ideas than time to try them out" - Human exploration is fundamentally sequential while possibilities expand exponentially.

### The Solution
**Multiply human capability** by removing the bottleneck. The constraint isn't AI capability—it's that vanilla AI lacks:
- Your domain knowledge
- Patterns from previous work
- Context across projects
- Ability to work in parallel

### The Transformation
- **Today**: Explore 1-2 solutions sequentially
- **With Amplifier**: Explore 20 solutions simultaneously in parallel
- **Result**: AI executes while humans direct and decide

### Technology-Agnostic Foundation
Critical principle: Not married to any specific AI. Built for Claude Code today, but the value is in:
- Knowledge base (portable)
- Patterns (reusable)
- Workflows (transferable)
- Accumulated learnings (permanent)

Tomorrow's AI platform can leverage all of this.

---

## 2. Architecture

### The Four-Layer Stack

```
┌─────────────────────────────────────────────────────────┐
│ Layer 5: USER INTERFACE                                 │
│ Commands: /ultrathink-task, /ddd:*, /profile-*         │
├─────────────────────────────────────────────────────────┤
│ Layer 4: ORCHESTRATION                                  │
│ 25+ Specialized Agents (parallel/sequential execution)  │
├─────────────────────────────────────────────────────────┤
│ Layer 3: AUTOMATION                                     │
│ Hooks: SessionStart, PreToolUse, PostToolUse           │
├─────────────────────────────────────────────────────────┤
│ Layer 2: CONTEXT                                        │
│ Memory: CLAUDE.md, AGENTS.md, DISCOVERIES.md          │
├─────────────────────────────────────────────────────────┤
│ Layer 1: CORE                                           │
│ Claude Code SDK                                         │
└─────────────────────────────────────────────────────────┘
```

### Hub-and-Spoke Model

**CLAUDE.md** acts as the central hub with spokes extending to:
- **AGENTS.md** - Shared project philosophy
- **Commands** - Executable methodologies
- **Hooks** - Event-driven automation
- **Subagents** - Specialized intelligence
- **DISCOVERIES.md** - Evolutionary learning

### Modular "Bricks & Studs" Architecture

**Philosophy**: Build self-contained "bricks" with clear "studs" (public contracts)

**Core Principles**:
1. **Ruthless Simplicity** - KISS, minimize abstractions, start minimal
2. **Emergent Design** - Structure emerges from solving real problems
3. **Architectural Integrity with Minimal Implementation** - Pattern benefits, simpler code
4. **Regenerate, Don't Patch** - Rewrite whole bricks from specs instead of line-editing

---

## 3. The Profiles System: Cognitive Prostheses

### Revolutionary Concept

Profiles are **cognitive prostheses** that shape how you think about development. They make the development process:
- **Explicit** - Philosophy is documented
- **Mutable** - You can switch approaches
- **Compositional** - Profiles reuse components
- **Self-improving** - Subject to its own processes

### Included Profiles

#### **default** - Ruthless Minimalism & Emergent Design
- **Timeline**: Ships in 4 hours with 150 lines of code
- **Guiding Question**: "What's the simplest thing that could work?"
- **Approach**: Defers 10+ features until pain is real
- **Tradeoffs**: Speed/adaptability vs. upfront certainty
- **Philosophy**: Start minimal, let structure emerge

#### **waterfall** - Sequential Phase-Based Development
- **Timeline**: 29 weeks to production with 500+ pages of docs
- **Guiding Question**: "What requirements must be gathered?"
- **Approach**: 7 sequential phases with formal gates
- **Tradeoffs**: Predictability/compliance vs. adaptability/speed
- **Philosophy**: Complete each phase before proceeding

#### **mathematical-elegance** - Formal Methods & Provable Correctness
- **Timeline**: Months with proofs, provable correctness
- **Guiding Question**: "What properties must we prove?"
- **Approach**: Types encode invariants, make illegal states unrepresentable
- **Tradeoffs**: Correctness/elegance vs. time to market
- **Philosophy**: Formal verification, mathematical rigor

#### **profile-editor** - Meta-Cognitive Process Design
- **Purpose**: Makes the system subject to its own processes
- **Capabilities**: Analyzes, compares, and refines profiles
- **Innovation**: Creates the meta-cognitive loop

### How Profiles Work

1. **Selection**: `.claude/active-profile` symlink points to current profile
2. **Configuration**: Each profile's `config.yaml` defines:
   - Imported commands/agents (from shared library: `@commands/`, `@agents/`)
   - Local commands/agents (profile-specific)
   - Philosophy documents to load
   - Settings and preferences
3. **Loading**: Philosophy documents loaded at session start shape AI's thinking
4. **Composition**: Profiles reference shared resources, avoiding duplication

### Empirical Validation

Testing with **identical tasks** produced **dramatically different cognitive patterns**:

| Profile | First Action | Timeline | Approach |
|---------|-------------|----------|----------|
| default | Code minimal MVP | 4 hours | "What's simplest?" |
| waterfall | Ask 40+ requirements questions | 18 weeks to first code | "What must we gather?" |
| mathematical-elegance | Write formal logic `∀ u ∈ Users...` | Months | "What must we prove?" |

**Conclusion**: Profiles fundamentally shape cognitive patterns, not just outputs.

---

## 4. Memory System

### Core Memory Files

#### CLAUDE.md (`/home/user/amplifier/amplifier/CLAUDE.md`)
- **Role**: Auto-loaded foundation with cascade imports
- **Content**:
  - Project overview
  - Architecture explanation
  - Import directives for other memory files
  - Session initialization context
- **Impact**: Ensures every session starts with complete context

#### AGENTS.md (`/home/user/amplifier/amplifier/AGENTS.md`)
- **Role**: Single source of truth for development philosophy
- **Content**:
  - Shared guidelines across all agents
  - Development principles
  - Quality standards
  - Communication patterns
- **Impact**: Consistency across all specialized agents

#### DISCOVERIES.md (`/home/user/amplifier/amplifier/DISCOVERIES.md`)
- **Role**: Evolutionary memory—learnings from past work
- **Content**:
  - Non-obvious problems and solutions
  - DevContainer setup patterns
  - LLM response handling patterns
  - Cloud sync file I/O errors and retries
  - Tool generation pattern failures
- **Impact**: System doesn't repeat mistakes; learns from experience

### Memory Benefits

1. **Context Persistence** - Knowledge survives session boundaries
2. **Accumulated Learning** - Compounds across projects
3. **Shared Intelligence** - All agents benefit from discoveries
4. **Portable Knowledge** - Can migrate to new AI platforms

---

## 5. Agent Ecosystem (25+ Specialized Agents)

### Development Agents
- **zen-architect** - Minimalist design perspective
- **modular-builder** - Composable system construction
- **bug-hunter** - Error detection and analysis
- **test-coverage** - Comprehensive testing strategies

### Knowledge Synthesis Agents
- **concept-extractor** - Identifies key concepts from content
- **insight-synthesizer** - Combines perspectives into coherent insights
- **tension-keeper** - Identifies and preserves productive tensions

### Design Agents
- **animation-choreographer** - Motion and timing design
- **art-director** - Visual design direction
- **component-designer** - UI component architecture

### Meta Agent
- **amplifier-cli-architect** - Expert on hybrid code/AI patterns
- **profile-editor** - Analyzes and refines development methodologies

### Orchestration Strategies

**Sequential**: Architecture → Implementation → Review
- Use when: Context builds progressively
- Benefit: Each agent builds on previous work

**Parallel**: Multiple independent perspectives simultaneously
- Use when: Need diverse viewpoints
- Benefit: Speed and diversity of thought
- Example: zen-architect + bug-hunter + test-coverage running concurrently

**Fork-and-Merge**: Agents fork context, work independently, return essentials
- Use when: Context space is constrained
- Benefit: Conserves context, focuses on key insights

---

## 6. Command System: Executable Methodologies

### Meta-Commands
- **/ultrathink-task** - Orchestrates multi-agent workflows with TodoWrite tracking
- **/prime** - Loads philosophical context
- **/profile-switch** - Changes development methodology on the fly

### Workflow Commands
- **/ddd:1-plan** through **/ddd:5-finish** - Document-driven development stages
- **/create-plan** - Generate implementation plans
- **/execute-plan** - Execute planned work
- **/review-changes** - Quality review of modifications

### Quality Commands
- **/review-code-at-path** - Targeted code review
- **/test-webapp-ui** - UI testing workflows
- **/commit** - Intelligent git commit with context awareness

### Command Benefits
1. **Encapsulated Expertise** - Best practices encoded in reusable commands
2. **Consistent Execution** - Same approach every time
3. **Composable** - Commands can invoke other commands
4. **Profile-Specific** - Different profiles can include different commands

---

## 7. Hook Infrastructure: Invisible Automation

### Session Lifecycle Hooks

**SessionStart**
- Memory system initialization
- Profile loading
- Context preparation
- Environment validation

**Stop**
- State saving
- Cleanup operations
- Session summary generation

### Tool Interaction Hooks

**PreToolUse**
- Subagent logging
- Context validation
- Permission checks

**PostToolUse**
- Quality checks
- Comprehensive tracking
- Error detection
- Learning capture

### Hook Benefits
1. **Automatic Quality Assurance** - No manual intervention
2. **Comprehensive Logging** - Complete audit trail
3. **State Persistence** - Work survives interruptions
4. **Zero Cognitive Overhead** - Invisible to user

---

## 8. CCSDK Toolkit: Code for Structure, AI for Intelligence

### Location
`/home/user/amplifier/amplifier/amplifier/ccsdk_toolkit/`

### Core Pattern
**"Code for structure, AI for intelligence"**
- Python provides: Type safety, async handling, file I/O, retry logic
- AI provides: Domain logic, decision-making, content generation

### Key Components

**Async Wrapper**
- Handles Claude Code SDK async/await complexity
- Manages session lifecycle
- Provides clean synchronous-feeling API

**Session Persistence**
- Saves state between invocations
- Supports resume/retry
- Handles interruptions gracefully

**Structured Logging**
- Rich terminal output
- Progress tracking
- Error reporting

**Defensive Patterns**
- `retry_with_feedback` - LLM parsing with retry
- `isolate_prompt` - Prevent prompt injection
- `parse_llm_json` - Robust JSON extraction
- File I/O with cloud sync retries

### Example Scenarios

**blog-writer**
- Transform ideas into polished posts matching your style
- Learns from existing posts
- Reviews itself for accuracy and style
- Built from one conversation describing the thinking process

**tips-synthesizer**
- Transform scattered tips into comprehensive guides
- Multi-stage pipeline: extract → organize → synthesize → review → refine
- State management with resumability

**article-illustrator**
- Generate contextual AI illustrations for markdown
- 4-stage pipeline with resume capability
- Multi-API support (GPT-Image-1, DALL-E, Imagen)

---

## 9. Meta-Development Approach

### The Metacognitive Recipe Pattern

Instead of coding implementations, you describe **how to think through the problem**:

**Example Recipe**:
1. "First, understand the author's style from their writings"
2. "Then draft content matching that style"
3. "Review the draft for accuracy against sources"
4. "Get user feedback and refine"

**Key Insight**: You describe the **thinking process**; Amplifier handles:
- async/await complexity
- Retry logic
- State management
- File I/O
- Error handling

### The Meta-Cognitive Loop

```
┌─────────────────────────────────────────────┐
│ 1. Work in a profile (default/waterfall/etc)│
│                    ↓                         │
│ 2. Notice patterns (what works? friction?)  │
│                    ↓                         │
│ 3. Switch to profile-editor                 │
│                    ↓                         │
│ 4. Analyze and refine the process itself    │
│                    ↓                         │
│ 5. Switch back with improved methodology    │
│                    ↓                         │
│ 6. Repeat → continuous improvement          │
└─────────────────────────────────────────────┘
```

**Result**: Development methodology becomes **subject to the same rigor as your code**.

### The Amplification Formula

```
Base Claude Code
  × Memory System
  × Agent Network
  × Commands
  × Hooks
  × Integration
= 10,000x+ Capability Multiplication
```

Not additive features—**multiplicative synergy**.

---

## 10. Design Philosophy Integration

### Nine Design Dimensions
1. **Style** - Visual identity and aesthetic
2. **Motion** - Animation and transitions
3. **Voice** - Tone and communication
4. **Space** - Layout and proximity
5. **Color** - Palette and meaning
6. **Typography** - Font hierarchy and readability
7. **Proportion** - Scale and relationships
8. **Texture** - Surface and materiality
9. **Body** - Physical embodiment

### Five Design Pillars

#### 1. Purpose Drives Execution
Understand **why** before perfecting **how**. Purpose gives work meaning and direction.

#### 2. Craft Embeds Care
300ms timing isn't arbitrary—it's human perception science. Details matter.

#### 3. Constraints Enable Creativity
Strategic limitations **channel** rather than restrict. Constraints focus creativity.

#### 4. Intentional Incompleteness
You provide: Purpose and meaning
AI provides: Execution and implementation
**Together**: Meaningful work

#### 5. Design for Humans
Real people with diverse needs, not abstract users. Accessibility and inclusivity matter.

### AI Era Insight
When AI handles execution, **sensibility becomes the differentiating input**:
- Your values
- Cultural context
- Intention and purpose
- What makes work meaningful

---

## 11. Testing and Validation

### Profile Evaluation Suite
**Location**: `/home/user/amplifier/amplifier/testing/profile_evaluation/`

**Purpose**: Empirical profile comparison through standardized tasks

**Metrics**:
- **Time**: Setup, planning, implementation, total
- **Process**: Question count, iteration cycles, phases
- **Quality**: Test coverage, error handling, documentation
- **Cognitive**: Decision points, methodology adherence

**Value**:
- Longitudinal analysis
- Methodology validation
- Objective profile comparison
- Continuous improvement feedback

### 10 Standardized Tasks
Diverse scenarios covering:
- Simple utilities
- API integrations
- Data processing
- UI components
- Complex workflows

**Usage**: Run same task across different profiles to observe cognitive pattern differences.

---

## 12. Key Strengths

### 1. Non-Prescriptive by Design
No "one size fits all"—context determines the right approach:
- Startups/prototypes → **default** (minimalism, speed)
- Regulated domains → **waterfall** (predictability, compliance)
- Safety-critical → **mathematical-elegance** (provable correctness)

### 2. Composable Profiles
Mix and match components:
- Shared commands library (`@commands/`)
- Shared agents library (`@agents/`)
- Profile-specific customizations
- Flexible philosophy documents

### 3. Meta-Development Capability
The system can improve its own processes:
- **profile-editor** edits profiles
- Discoveries feed back into methodology
- Continuous evolution based on experience

### 4. Technology-Agnostic Foundation
Built for portability:
- Knowledge base is markdown (portable)
- Patterns are conceptual (reusable)
- Workflows are methodology (transferable)
- Not locked to Claude Code

### 5. Memory That Compounds
Knowledge accumulates across projects:
- DISCOVERIES.md captures learnings
- Patterns become reusable
- Quality improves over time
- Experience is preserved

### 6. Parallel Exploration
Run 20 explorations simultaneously:
- Different agents on same problem
- Different approaches in parallel
- Rapid iteration
- Human directs, AI executes

---

## 13. Current Project Structure

```
amplifier/
├── CLAUDE.md                    # Central hub - auto-loaded
├── AGENTS.md                    # Shared philosophy
├── DISCOVERIES.md               # Evolutionary memory
├── PROFILES_SYSTEM.md          # Profile documentation
├── AMPLIFIER_VISION.md         # Vision and purpose
├── ROADMAP.md                  # Future directions
│
├── profiles/                    # Profile definitions
│   ├── default/
│   │   ├── config.yaml         # Profile configuration
│   │   ├── philosophy/         # Methodology documents
│   │   ├── commands/           # Profile-specific commands
│   │   └── agents/             # Profile-specific agents
│   ├── waterfall/
│   ├── mathematical-elegance/
│   └── profile-editor/
│
├── tools/                       # Shared tools library
│   ├── commands/               # @commands/ imports
│   └── agents/                 # @agents/ imports
│
├── amplifier/ccsdk_toolkit/    # Python toolkit
│   ├── core/                   # Session, models, utils
│   ├── cli/                    # CLI builders
│   ├── config/                 # Configuration
│   ├── defensive/              # Defensive patterns
│   └── examples/               # Working examples
│
├── ai_context/                 # AI reference documentation
│   ├── design/                 # Design philosophy
│   ├── core/                   # Core concepts
│   └── claude_code/            # Claude Code specifics
│
├── ai_working/                 # Working area
│   └── decisions/              # Decision logs
│
└── testing/
    └── profile_evaluation/     # Profile testing suite
```

---

## 14. Key Documentation Files

### Core Vision
- **AMPLIFIER_VISION.md** - Problem, solution, transformation
- **PROFILES_SYSTEM.md** - Profile architecture and philosophy
- **PROFILES_TESTING_RESULTS.md** - Empirical validation

### Philosophy
- **ai_context/DESIGN-PHILOSOPHY.md** - Overall design approach
- **ai_context/DESIGN-PRINCIPLES.md** - Guiding principles
- **ai_context/IMPLEMENTATION_PHILOSOPHY.md** - Implementation approach
- **ai_context/MODULAR_DESIGN_PHILOSOPHY.md** - Bricks and studs

### Technical
- **amplifier/ccsdk_toolkit/README.md** - Toolkit overview
- **amplifier/ccsdk_toolkit/DEVELOPER_GUIDE.md** - Development guide
- **amplifier/ccsdk_toolkit/defensive/PATTERNS.md** - Defensive patterns

### Reference
- **ai_context/claude_code/** - Complete Claude Code documentation
- **ai_context/reference/LLM_API_LOOKUP.md** - LLM API reference

---

## 15. The Amplifier Difference

### What Makes Amplifier Unique

1. **Metacognitive Operating System**
   - Not just a tool—a cognitive framework
   - Makes methodology itself mutable
   - System can improve its own processes

2. **Non-Prescriptive Flexibility**
   - Multiple coexisting methodologies
   - Choose based on context
   - No "one right way"

3. **Composable Architecture**
   - Mix and match components
   - Shared libraries reduce duplication
   - Easy to extend and customize

4. **Memory That Persists**
   - Knowledge survives sessions
   - Learnings compound over time
   - Portable across AI platforms

5. **Parallel AI Orchestration**
   - 20 simultaneous explorations
   - Sequential, parallel, or fork-merge
   - Massive capability multiplication

6. **Technology Agnostic**
   - Not locked to Claude Code
   - Portable knowledge base
   - Future-proof architecture

---

## 16. Use Cases

### Startup Development
- **Profile**: default (ruthless minimalism)
- **Benefit**: Ship MVP in hours, validate quickly
- **Pattern**: Minimal code, emergent design

### Enterprise Software
- **Profile**: waterfall (sequential phases)
- **Benefit**: Predictability, compliance, documentation
- **Pattern**: Formal requirements, phase gates

### Safety-Critical Systems
- **Profile**: mathematical-elegance (formal methods)
- **Benefit**: Provable correctness, formal verification
- **Pattern**: Types as proofs, impossible states prevented

### Process Improvement
- **Profile**: profile-editor (meta-cognitive)
- **Benefit**: Analyze and refine development methodology
- **Pattern**: Meta-development, continuous improvement

### Research and Exploration
- **Tool**: Multi-agent parallel exploration
- **Benefit**: Explore 20 solutions simultaneously
- **Pattern**: AI executes, human directs and synthesizes

---

## 17. Future Directions (from ROADMAP.md)

### Planned Enhancements
- Additional methodology profiles (Lean, Scrum, Kanban)
- Enhanced profile composition mechanisms
- Improved meta-cognitive loop automation
- Broader AI platform support
- Community profile sharing
- Advanced analytics on profile effectiveness

### Research Areas
- Optimal agent orchestration patterns
- Memory system optimization
- Profile discovery from natural work patterns
- Automated methodology adaptation

---

## Conclusion

**Amplifier is not a development tool—it's a cognitive operating system for AI-assisted software development.**

It transforms the fundamental equation:
- **Before**: Sequential exploration, limited by human execution time
- **After**: Parallel exploration at AI speed, limited only by human direction

The profiles system makes development methodology:
- **Explicit** - Written down, not implicit
- **Mutable** - Changeable based on context
- **Compositional** - Built from reusable components
- **Self-improving** - Subject to its own meta-cognitive processes

**The real product isn't the code—it's the capacity to think clearly about building software while making that thinking process itself subject to continuous improvement.**
