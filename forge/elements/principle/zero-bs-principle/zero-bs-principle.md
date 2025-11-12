# Zero-BS Principle: No Stubs or Placeholders

Build working code only. Avoid NotImplementedError, TODO without code, mock functions, and "coming soon" features.

## What to Avoid

**Unimplemented stubs:**
```python
def important_feature():
    raise NotImplementedError("TODO: implement this")
```

**Empty TODO comments:**
```python
# TODO: Add error handling
# TODO: Optimize this later
# TODO: Make this configurable
```

**Mock implementations:**
```python
def authenticate(user):
    return True  # Mock - always succeeds
```

**Coming soon features:**
```python
# This will support OAuth2 in the future
def login(username, password):
    pass  # Basic auth only for now
```

## What to Do Instead

**Option 1: Implement it fully**
```python
def authenticate(user, password):
    hashed = hash_password(password)
    return check_hash(user, hashed)
```

**Option 2: Don't include it**
- Remove the function entirely
- Update specs to reflect actual scope
- Add to backlog for future work

**Option 3: Reduce scope**
```python
def authenticate(username, password):
    """Basic authentication only. OAuth not supported."""
    return verify_credentials(username, password)
```

## Core Philosophy

- Every function must work or not exist
- TODOs are technical debt disguised as planning
- Stubs create false confidence in completeness
- YAGNI: You aren't gonna need it (until you do)

## Enforcement

- Reduces scope to achievable functionality
- Forces honest assessment of what's ready
- Prevents shipping incomplete features
- Makes code review straightforward

## Remember

Code you don't write has no bugs. If a feature isn't ready, don't pretend it is with stubs and TODOs. Either build it fully or remove it entirely.
