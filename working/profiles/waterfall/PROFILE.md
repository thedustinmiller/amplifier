# Waterfall Profile: Sequential Phase-Based Development

## Philosophy at a Glance

**This profile embodies traditional waterfall methodology: thorough upfront planning, sequential phases with gates, and comprehensive documentation before implementation.**

### Core Tenets

1. **Requirements First**
   - Fully specify requirements before design
   - Get stakeholder sign-off at each phase
   - Changes require formal change management
   - "Measure twice, cut once"

2. **Phase-Gate Structure**
   - Each phase completes before the next begins
   - Gates require approval to proceed
   - Deliverables are well-defined and reviewed
   - Progress is measured by phase completion

3. **Comprehensive Documentation**
   - Requirements specifications
   - Design documents
   - Test plans created before coding
   - Traceability matrices maintained

4. **Risk Through Planning**
   - Identify risks upfront
   - Plan mitigation strategies
   - Minimize surprises during implementation
   - Predictability over adaptability

### When to Use This Profile

**Use this profile when:**
- Requirements are well-understood and stable
- Cost of changes is very high (hardware integration, regulations)
- Multiple teams need detailed coordination
- Stakeholders require predictability and formal approvals
- You're in a regulated domain (medical, aerospace, defense)
- Fixed-price contracts demand upfront estimates
- Team is geographically distributed with limited communication

**Consider alternatives when:**
- Requirements are uncertain or evolving rapidly (try `default` or `agile`)
- You need to learn by building (try `exploratory-research`)
- Speed to market is critical (try `lean-startup`)
- Cost of change is low (pure software, no hardware)

### Phase Structure

This profile enforces sequential phases:

1. **Requirements Analysis**
   - Gather and document all requirements
   - Create requirements specification document
   - Stakeholder review and sign-off
   - Gate: Requirements Approval

2. **System Design**
   - High-level architecture
   - Database schema design
   - Interface specifications
   - Design review and approval
   - Gate: Design Approval

3. **Detailed Design**
   - Module specifications
   - API contracts
   - Data structures and algorithms
   - Design walkthrough
   - Gate: Detailed Design Approval

4. **Implementation**
   - Code according to detailed design
   - Unit testing
   - Code reviews
   - Integration
   - Gate: Implementation Complete

5. **Testing**
   - System testing against requirements
   - Integration testing
   - User acceptance testing
   - Defect tracking and resolution
   - Gate: Testing Complete

6. **Deployment**
   - Production deployment
   - User training
   - Documentation delivery
   - Post-deployment support
   - Gate: Deployment Successful

7. **Maintenance**
   - Bug fixes
   - Change requests through formal process
   - Version management

### Key Commands

This profile includes phase-specific commands:
- `/waterfall:1-requirements` - Requirements gathering and specification
- `/waterfall:2-design` - System and detailed design
- `/waterfall:3-implement` - Implementation phase
- `/waterfall:4-test` - Testing phase
- `/waterfall:5-deploy` - Deployment phase
- `/gate-review` - Formal gate review and approval
- `/change-request` - Formal change management
- `/traceability-matrix` - Maintain requirements traceability

### Key Agents

- **requirements-analyst** - Elicit and document requirements
- **systems-architect** - High-level architecture design
- **qa-planner** - Test plan creation and management
- **change-manager** - Formal change control process
- **documentation-specialist** - Comprehensive documentation
- **gate-reviewer** - Phase gate approval assessment

Plus imported from shared library:
- @agents/api-contract-designer
- @agents/database-architect
- @agents/test-coverage
- @agents/security-guardian

### Philosophy Documents

This profile loads:
1. `WATERFALL_METHODOLOGY.md` - Detailed methodology description
2. `PHASE_GATE_CHECKLIST.md` - Requirements for each gate
3. `CHANGE_MANAGEMENT_PROCESS.md` - How to handle changes
4. This `PROFILE.md` - Quick reference

### Design Principles

- **Plan the work, work the plan** - Discipline over flexibility
- **Complete before proceeding** - Don't skip phases
- **Documentation is deliverable** - Not an afterthought
- **Traceability is mandatory** - Requirements → Design → Code → Tests
- **Change is expensive** - Formal process for changes
- **Risk through analysis** - Understand risks before building

### Tradeoffs This Profile Makes

**Gains**:
- Predictability - Timeline and budget estimation
- Coordination - Multiple teams know what to expect
- Documentation - Comprehensive specifications
- Risk management - Identified upfront
- Stakeholder confidence - Formal approvals
- Regulatory compliance - Audit trail

**Sacrifices**:
- Adaptability - Hard to change course
- Speed - Long time before working software
- Learning - Can't adjust based on implementation learnings
- Efficiency - May build wrong thing correctly
- Innovation - Rigid process discourages exploration
- Developer satisfaction - Can feel bureaucratic

### Cultural Notes

This profile draws from:
- **Traditional engineering** - Civil, mechanical engineering practices
- **Project management** - PMBOK, PMP methodology
- **Systems engineering** - V-model, NASA processes
- **Regulated industries** - FDA, FAA, ISO standards

### Anti-patterns to Avoid

- **Waterfall theater** - Going through motions without real planning
- **Analysis paralysis** - Perfect requirements before starting
- **Big bang integration** - Integrating everything at the end
- **Late testing** - Waiting until implementation complete
- **Change resistance** - Refusing necessary changes due to process
- **Documentation over communication** - Docs substitute for talking

### When Waterfall Actually Works

Waterfall gets unfairly maligned, but it's genuinely appropriate when:

1. **Requirements are truly stable** - Building to a fixed specification (e.g., medical device to FDA standard)
2. **Cost of change is prohibitive** - Hardware/firmware integration where changes are expensive
3. **Multiple vendors must coordinate** - Contract-based development with clear interfaces
4. **Regulatory requires upfront validation** - Must prove design before building
5. **Team expertise is in planning** - Organization culture and skills match waterfall

The key is honest assessment: Do these conditions actually apply to your situation?

### Hybrid Approaches

This profile can be adapted:
- **Mini-waterfalls** - Apply waterfall within short iterations
- **Staged delivery** - Waterfall per feature, but incremental releases
- **Critical path only** - Apply rigor to high-risk components only
- **Documentation as needed** - Formal docs where required, informal elsewhere

---

## How This Profile Works

When this profile is active:
1. Session starts by loading methodology documents
2. Commands enforce sequential phase progression
3. Gate reviews required before phase transitions
4. Agents guide thorough documentation and planning
5. Change requests go through formal process
6. Traceability is maintained throughout

This creates a **cognitive prosthesis for systematic planning** - it helps you think through the entire system before building, using AI to handle the mechanics of documentation and traceability while you focus on completeness and correctness.

Use this profile when predictability matters more than adaptability.
