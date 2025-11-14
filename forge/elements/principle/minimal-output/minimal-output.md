# Principle: Minimal Output

## Core Tenet
Show only essential information. Reduce noise, maximize signal. Respect the user's attention and time.

## Motivation
Information overload is real. When output is verbose, important details get buried in noise. Experienced users know what they need—they want results, not explanations. Every unnecessary word is friction.

The cost of verbosity:
- Time spent reading irrelevant details
- Mental energy parsing noise from signal
- Important information lost in clutter
- Slower feedback loops
- Cognitive fatigue

Less output means:
- Faster comprehension
- Clearer focus on what matters
- Higher velocity workflows
- Reduced mental load
- More efficient iteration

## Implications

### Show Only What's Needed
- Output the result, not the process
- Skip explanations for obvious actions
- Omit "working on it" status updates
- Suppress successful operation confirmations
- Report only errors and key decisions

### Optimize for Scanning
- Use structured output (tables, lists, JSON)
- Put important information first
- Use visual hierarchy (headers, indentation)
- Group related information
- Make it greppable

### Assume Expertise
- Skip teaching moments
- Don't explain common concepts
- Assume familiarity with tools and patterns
- Trust the user to ask if confused
- Provide depth only on request

### Actionable Over Comprehensive
- What changed? (not why it was changed)
- What failed? (not how the system works)
- What's next? (not what just happened)
- What requires action? (not what succeeded)

## Trade-offs

### What You Gain
- **Speed**: Less to read means faster iteration
- **Focus**: Signal stands out clearly
- **Efficiency**: High information density
- **Velocity**: Minimal friction in workflows
- **Clarity**: Important details aren't buried

### What You Sacrifice
- **Learning**: Less explanation means less teaching
- **Transparency**: Decision rationale hidden
- **Debuggability**: Less context for troubleshooting
- **Collaboration**: Teammates may lack context
- **Onboarding**: Harder for newcomers to follow

## Conflicts

### Incompatible Principles
- **detailed-explanation**: Prefers comprehensive output
- **comprehensive-documentation**: Values explicit knowledge
- **user-confirmation** (when verbose): May include too much context

### Compatible Principles
- **ruthless-minimalism**: Both value simplicity and reduction
- **fast-iteration**: Speed benefits from concise communication
- **autonomous-execution**: Both minimize interruptions

## Examples

### Code Review
**Minimal Output**:
```
Refactored auth: bcrypt, split authenticate(), indexed email.
Breaking change: requires migration. Run: ./migrate.py
```

**Detailed** (for contrast):
```
I'm refactoring the authentication flow for three reasons:
1. Security: bcrypt hashing vs plain text
2. Maintainability: broke 200-line function into smaller units
3. Performance: O(n) → O(1) lookups with email index

[... 20 more lines of explanation ...]
```

### Error Reporting
**Minimal Output**:
```
✗ user_test.py:42 - Timezone mismatch
  Fix: Use timezone.utc
  Docs: docs/guidelines.md#timezones
```

**Detailed** (for contrast):
```
The test is failing because of a timezone mismatch:

File: tests/user_test.py, line 42
Error: AssertionError: expected '2025-11-14 10:00:00' but got '2025-11-14 15:00:00'

Root cause: The test creates a timestamp in UTC but the comparison uses
local time (EST = UTC-5). [... 15 more lines ...]
```

### Build Output
**Minimal Output**:
```
✓ Tests passed (47/47)
✓ Built in 2.3s
→ localhost:3000
```

**Detailed** (for contrast):
```
Running test suite...
  ✓ test_user_authentication (0.05s)
  ✓ test_password_hashing (0.03s)
  ✓ test_session_creation (0.04s)
  [... 44 more lines ...]
All 47 tests passed in 1.2s

Building production bundle...
  Compiling TypeScript...
  Bundling with webpack...
  Minifying JavaScript...
  Optimizing assets...
  [... 10 more lines ...]
Build completed successfully in 2.3s

Server running at http://localhost:3000
```

### Git Operations
**Minimal Output**:
```
3 files changed
Created: feat/rate-limiting @ a3f9c21
```

**Detailed** (for contrast):
```
Staged changes:
  M src/api/views.py (added rate limiting decorator)
  M requirements.txt (added django-redis-ratelimit==2.0.0)
  A tests/test_rate_limiting.py (added comprehensive test suite)

Created new branch: feat/rate-limiting
Base: main @ 4ee6108
HEAD: a3f9c21 "Add rate limiting to API endpoints"

Next steps:
- Run tests: pytest tests/test_rate_limiting.py
- Manual test: scripts/test_rate_limit.sh
- Create PR: gh pr create
```

### Search Results
**Minimal Output**:
```
authenticate() - 3 files:
  src/auth/login.py:45
  src/auth/session.py:78
  tests/auth_test.py:23
```

**Detailed** (for contrast):
```
Searching for 'authenticate()' across the codebase...

Found 3 matches in 3 files:

1. src/auth/login.py, line 45:
   def authenticate(email: str, password: str) -> Optional[User]:
   Context: Main authentication function used by login endpoint

2. src/auth/session.py, line 78:
   if not authenticate(email, request.POST['password']):
   Context: Session creation flow calls authenticate to verify credentials

3. tests/auth_test.py, line 23:
   result = authenticate('test@example.com', 'password123')
   Context: Test suite for authentication functionality

To see more context, use: grep -A 5 -B 5 'authenticate' <file>
```

### API Response
**Minimal Output**:
```json
{"status": "ok", "id": 1234}
```

**Detailed** (for contrast):
```json
{
  "status": "ok",
  "message": "User created successfully",
  "data": {
    "id": 1234,
    "email": "user@example.com",
    "created_at": "2025-11-14T10:00:00Z",
    "email_verified": false,
    "profile_complete": false
  },
  "meta": {
    "request_id": "req_abc123",
    "processing_time_ms": 45,
    "rate_limit_remaining": 99,
    "rate_limit_reset": 1731585600
  }
}
```

## When to Use

### Good For
- Experienced developers who know the system
- High-velocity workflows (rapid iteration)
- Production operations (focus on errors)
- Repetitive tasks (minimal friction)
- Command-line tools (machine-parseable)
- Status dashboards (essential metrics only)
- CI/CD pipelines (failures matter, successes don't)

### Bad For
- Learning environments (users need context)
- Debugging complex issues (require rich context)
- Onboarding new team members
- Collaborative projects with diverse expertise
- Regulated environments (require audit trails)
- Teaching and mentoring

## Quotes

> "Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away." — Antoine de Saint-Exupéry

> "Brevity is the soul of wit." — William Shakespeare

> "Omit needless words." — Strunk & White

> "Less is more." — Ludwig Mies van der Rohe

> "The most valuable thing you can make is a mistake—you can't learn anything from being perfect." — Adam Osborne

## Related Patterns

- **Unix Philosophy**: Do one thing well, compose with others
- **Progressive Disclosure**: Show basics first, details on demand
- **Just-in-Time Information**: Provide context when needed
- **Signal vs Noise**: Maximize information relevance
- **Cognitive Load Theory**: Reduce mental burden

## Evolution

This principle doesn't mean "hide everything always." It means:

1. **Know your audience**: Experts need less, beginners need more
2. **Optimize for common case**: Show what's usually needed
3. **Make depth available**: Verbose flags (-v, --debug) for details
4. **Progressive disclosure**: Summary first, drill down as needed
5. **Context-aware**: Errors need more info than successes

The right level of concision depends on:
- User expertise (senior developers vs newcomers)
- Task type (production fix vs exploration)
- Failure mode (errors need context, success doesn't)
- Tool category (automation vs debugging)
- Frequency (one-off vs repeated operations)

Examples of progressive disclosure:

**Default (minimal)**:
```
✗ Build failed
```

**Verbose (-v)**:
```
✗ Build failed: TypeScript compilation error in src/auth.ts:45
```

**Debug (--debug)**:
```
✗ Build failed

Compilation error details:
  File: src/auth.ts:45
  Error: TS2345: Argument of type 'string' is not assignable to parameter of type 'number'

  Code:
    43 | function authenticate(userId: number) {
    44 |   const user = getUser(userId);
    45 |   return verifyPassword(userId, password);
       |                         ^^^^^^

  Expected: number
  Received: string

  Fix: Convert userId to number or change parameter type
```

Adapt the verbosity to the situation while respecting the user's time and attention.
