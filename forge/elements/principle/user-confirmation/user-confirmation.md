# Principle: User Confirmation

## Core Tenet
Request user approval before taking significant actions. Transparency and control over automated decisions.

## Motivation

Not all automation is desirable. Sometimes the user wants to understand what's happening, learn from the process, or maintain control over important decisions. Confirmation provides checkpoints for review and course correction.

**Why Confirmation Matters**:
- Prevents unwanted actions
- Creates learning opportunities
- Builds trust through transparency
- Allows course correction
- Gives user final say
- Reduces anxiety about automation

**The Cost of Unchecked Automation**:
- Unwanted changes at scale
- Lost learning opportunities
- User disconnection from process
- Difficult to reverse batch operations
- Trust erosion from surprises
- Reduced sense of ownership

## Implications

### Approval Checkpoints
- Present plan before execution
- Show what will change
- Explain reasoning
- Request explicit approval
- Allow modifications to plan
- Respect "no" answers

### Transparency First
- Explain what agent will do
- Show intermediate results
- Display decision rationale
- Highlight risks and trade-offs
- Provide enough context for informed decisions
- Surface assumptions

### Granular Control
- Allow approval per-item or batch
- Enable partial approval
- Support "approve all similar"
- Provide filtering and preview
- Allow rollback after review
- Give user veto power

### Educational Interaction
- Explain approach and alternatives
- Show reasoning process
- Answer questions before proceeding
- Teach through interaction
- Build user expertise over time

## Trade-offs

### What You Gain
- **Control**: User maintains authority
- **Safety**: Catch mistakes before they propagate
- **Learning**: User sees and understands process
- **Trust**: Transparency builds confidence
- **Flexibility**: Easy to change direction
- **Ownership**: User feels engaged

### What You Sacrifice
- **Speed**: Waiting for approvals slows progress
- **Efficiency**: Human becomes bottleneck
- **Scale**: Can't handle large batch operations
- **Availability**: Work stops when user unavailable
- **Flow**: Interruptions break concentration

## Conflicts

### Incompatible Principles
- **autonomous-execution**: Agent acts without approval
- **batch-processing**: Requires automated bulk operations
- **minimal-output**: Showing plans takes communication
- **fast-iteration**: Approvals slow down cycles

### Compatible Principles
- **detailed-explanation**: Both favor transparency
- **learning-focused**: Confirmation creates teaching moments
- **conservative-approach**: Both prioritize safety
- **user-control**: Both keep user in charge

## Examples

### Code Refactoring

**User Confirmation Approach**:
```markdown
Agent: "I found 47 API endpoints that could be converted to async/await.
Here's my plan:

Phase 1: Convert simple endpoints (23 endpoints)
- GET /users
- GET /posts
- POST /login
- ... [show all]

Phase 2: Convert complex endpoints with dependencies (15 endpoints)
- POST /checkout (depends on payment service)
- GET /analytics (complex queries)
- ... [show all]

Phase 3: Convert remaining endpoints (9 endpoints)
- Legacy endpoints that may need manual review

Estimated time: 2 hours
Risks: May need to adjust error handling patterns

Shall I proceed with Phase 1?"

User: "Yes, but skip the legacy endpoints for now."

Agent: "Understood. Converting 38 endpoints (Phases 1 & 2 only)."

[After Phase 1]
Agent: "Phase 1 complete (23 endpoints converted).
All tests passing. Here's what changed: [summary]

Proceed with Phase 2?"

User: "Show me the changes first."

[Agent shows diff summary]

User: "Looks good, proceed."
```

### Database Changes

**User Confirmation**:
```sql
-- Agent proposes changes
Agent: "I need to modify the users table.

Proposed changes:
1. ADD COLUMN last_login TIMESTAMP
2. ADD INDEX idx_users_email ON users(email)
3. ALTER COLUMN status SET DEFAULT 'active'

Impact:
- Table will be locked briefly (~5 seconds estimated)
- Current rows: 10,847
- Existing indexes: 2
- New index will use ~2MB space

Risk assessment:
- Low risk: Non-destructive changes
- Downtime: < 10 seconds
- Reversible: Yes

Migration SQL:
```sql
BEGIN;

ALTER TABLE users
ADD COLUMN last_login TIMESTAMP;

CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

ALTER TABLE users
ALTER COLUMN status SET DEFAULT 'active';

COMMIT;
```

Rollback plan available if needed.

Approve migration?"

User: "Use CREATE INDEX CONCURRENTLY to avoid locking."

Agent: "Good catch. Updated migration:

CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

This will take longer (~30 seconds) but won't lock the table.

Proceed?"

User: "Yes."
```

### Dependency Updates

**User Confirmation**:
```markdown
Agent: "Found 12 dependency updates available:

Critical security updates:
✗ express: 4.17.1 → 4.18.2 (CVE-2022-24999)
✗ jsonwebtoken: 8.5.1 → 9.0.0 (CVE-2022-23529)

Major version updates (breaking changes possible):
⚠ react: 17.0.2 → 18.2.0
⚠ typescript: 4.9.0 → 5.3.0

Minor updates (should be safe):
✓ eslint: 8.45.0 → 8.56.0
✓ jest: 29.5.0 → 29.7.0
... [6 more]

Recommendation:
1. Apply security updates immediately
2. Test major updates in separate branch
3. Apply minor updates as batch

Which would you like to proceed with?"

User: "Security updates now, create branch for major updates."

Agent: "Applying security updates to main branch...
Creating branch 'update-major-deps' for react and typescript.

For main branch:
- express: 4.17.1 → 4.18.2
- jsonwebtoken: 8.5.1 → 9.0.0

Run tests after update?"

User: "Yes."

Agent: "Tests complete: ✓ All passing

Commit message:
'security: Update express and jsonwebtoken for CVE fixes'

Commit and push?"

User: "Commit only, I'll push after review."

Agent: "Committed. SHA: abc123def"
```

### File Deletion

**User Confirmation**:
```markdown
Agent: "Found 347 unused files:

Test files for deleted features: 89 files
- test/features/old-auth/*.test.js (23 files)
- test/features/beta-ui/*.test.js (31 files)
... [see full list]

Old migration scripts: 143 files
- migrations/2022/*.sql (143 files, from over 1 year ago)

Deprecated documentation: 67 files
- docs/old-api/*.md (67 files)

Unused assets: 48 files
- public/old-images/*.png (48 files)

Total space: 23.4 MB

These files haven't been accessed in >6 months and reference deleted code.

Actions:
[ ] Delete all
[ ] Review list first
[ ] Delete by category
[ ] Cancel

What would you like to do?"

User: "Review test files and old migrations, but delete deprecated docs and assets."

Agent: "Deleting:
- docs/old-api/ (67 files, 3.2 MB)
- public/old-images/ (48 files, 18.1 MB)

Total: 115 files, 21.3 MB

Proceed?"

User: "Yes."

Agent: "Deleted 115 files.

Would you like to review the test files (89 files) and migrations (143 files)?"

User: "Show me test files first."

Agent: [Shows categorized list with last-accessed dates]
```

## When to Use

### Good For
- Learning new codebase or technology
- High-stakes changes (production, database)
- First-time tasks
- Exploratory work
- When user wants transparency
- Building trust with new agent
- Regulatory/compliance requirements
- Irreversible operations
- Security-sensitive changes

### Bad For
- Routine, repetitive tasks
- Well-established trust
- Time-sensitive operations
- Batch processing
- When user is unavailable
- Trusted, low-risk operations
- User wants to focus elsewhere

## Practices

### Effective Confirmation Requests

**Good Confirmation**:
```markdown
What: Convert 23 API endpoints to async/await
Why: Improve performance and enable concurrent operations
How: Replace function declarations with async, add await to DB calls
Impact: Tests may need updating, existing code unaffected
Risk: Low - fully backward compatible
Time: ~1 hour
Rollback: Easy - each endpoint is independent

Approve?
```

**Poor Confirmation**:
```markdown
"Make some changes to the API?"
```

### Batch Approval Patterns
```markdown
Agent: "Found 50 linting issues. How would you like to proceed?

[ ] Show all issues
[ ] Fix all automatically
[ ] Fix by category (imports: 23, spacing: 15, naming: 12)
[ ] Show first 10 issues

Choose an option:"

User: "Fix by category - start with imports."

Agent: "Fixing import issues (23 files affected).
Preview changes? [Y/n]"

User: "n"

Agent: "Fixed 23 import issues. All tests passing.

Next category: spacing (15 issues).
Auto-fix these too? [Y/n]"

User: "Yes to all remaining."

Agent: "Fixing spacing (15) and naming (12) issues... Done.
Total: 50 issues fixed across 38 files."
```

### Graduated Autonomy
```markdown
# Build trust over time

Session 1: Confirm everything
Agent: "Update import?"
User: "Yes"
Agent: "Update another similar import?"
User: "Yes"

Session 2: Batch similar actions
Agent: "Found 15 similar imports. Update all? [Y/n]"
User: "Yes"

Session 3: Automatic with summary
Agent: "Updated 15 imports. [Review changes]"

Session 4+: Fully autonomous (user opted in)
Agent: [Just fixes imports, mentions in summary]
```

### Decision Documentation
```markdown
# Track user decisions for consistency

User approved:
- Auto-fix linting issues (2025-11-14)
- Update minor dependencies without asking (2025-11-10)
- Use async/await pattern for new endpoints (2025-11-08)

User requires confirmation:
- Database schema changes
- Dependency major version updates
- File deletions
- Production deployments
```

## Anti-Patterns

### Confirmation Overload
Asking for approval on every tiny decision.
**Fix**: Batch similar decisions, remember preferences.

### Insufficient Context
"Proceed? [Y/n]" with no explanation.
**Fix**: Always explain what, why, impact, and risk.

### Fake Confirmations
Asking but ignoring the answer.
**Fix**: Respect user decisions, adjust plans accordingly.

### No Escape Hatch
Can't cancel or modify once approved.
**Fix**: Allow rollback, provide stop mechanisms.

## Quotes

> "With great power comes great responsibility." — Uncle Ben

> "Trust, but verify." — Ronald Reagan

> "The user is always right." — User experience principle

> "Consent is not the absence of 'no', it's the presence of 'yes'." — Consent principle

## Related Patterns

- **Two-Phase Commit**: Plan, then execute
- **Preview Before Action**: Show changes before applying
- **Dry Run**: Simulate without side effects
- **Approval Workflow**: Structured review process
- **Undo/Redo**: Easy reversal of actions

## Progression

Confirmation can adapt to user trust:

1. **Paranoid Mode**: Confirm every action
2. **Standard Mode**: Confirm significant actions
3. **Trusted Mode**: Confirm only risky actions
4. **Autonomous Mode**: Just report what was done

Users can move between modes based on task, context, and confidence.

## Success Metrics

You're using user confirmation well when:
- User feels in control
- Surprises are rare
- Confirmation requests have sufficient context
- User can make informed decisions
- Approvals don't feel burdensome
- Trust is building over time
- User learns from interactions
- Course corrections are easy
