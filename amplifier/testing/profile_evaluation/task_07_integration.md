# Task 07: Third-Party Integration

## Task Information

**Task ID**: task_07_integration
**Category**: External service integration
**Complexity**: Medium
**Estimated Duration**: 2-3 hours
**Last Updated**: 2025-11-09

## Objective

Integrate the GitHub API into an existing CLI tool to fetch and display repository statistics.

## Context

You have a CLI tool that currently only works with local Git repositories. You need to add GitHub API integration to fetch data for remote repositories. This tests:
- Reading and understanding external API documentation
- API client design decisions
- Error handling for network calls
- Testing external integrations

## Requirements

### Functional Requirements

Add a `--github` flag that:
1. Accepts a GitHub repo in `owner/repo` format
2. Fetches repository metadata (stars, forks, issues, PRs)
3. Fetches recent commit activity
4. Displays in a similar format to local analysis
5. Handles API rate limiting gracefully
6. Handles network errors and invalid repos

### Non-Functional Requirements

- Use GitHub REST API (not GraphQL, for simplicity)
- Handle authentication (optional token)
- Reasonable error messages
- Respect rate limits
- Testable (mock API calls)

## Success Criteria

1. **Functional Success**:
   - Successfully fetches GitHub data
   - Error handling works
   - Output is useful

2. **Quality Success**:
   - Clean API client design
   - Proper error handling
   - Tests with mocked API

3. **Process Success**:
   - API docs understood correctly
   - Good architectural decisions
   - Appropriate abstraction level

## Starting Materials

**Existing tool**: A simple CLI that shows local repo stats

**GitHub API endpoints needed**:
- `GET /repos/{owner}/{repo}`
- `GET /repos/{owner}/{repo}/commits`
- `GET /repos/{owner}/{repo}/issues`

**Expected usage**:
```bash
$ repo-stats --github octocat/hello-world

GitHub Repository: octocat/hello-world
Stars: 2500
Forks: 850
Open Issues: 12
Open PRs: 3

Recent Activity (last 7 days):
  - 15 commits
  - 3 contributors
  - Most active: octocat (8 commits)
```

## Expected Profile Differences

### Default Profile (Minimalist)
- **Expected approach**:
  - Direct `requests` usage
  - Minimal wrapper
  - Basic error handling
  - Simple mocking in tests

- **Time estimate**: 1.5-2 hours

### Waterfall Profile (Phase-Gate)
- **Expected approach**:
  - API client class/module
  - Adapter pattern
  - Comprehensive error handling
  - Full test coverage

- **Time estimate**: 2.5-3 hours

### Mathematical-Elegance Profile (Formal Methods)
- **Expected approach**:
  - Type-safe API client
  - Result/Option types for errors
  - Pure functions where possible
  - Property-based testing

- **Time estimate**: 2.5-3.5 hours

## Documentation Requirements

Standard structure in `results/<profile-name>/task_07/`

Include:
- API design decisions
- Error handling strategy
- Testing approach
- Time breakdown

## References

- GitHub REST API: https://docs.github.com/en/rest
- `requests` library: https://requests.readthedocs.io/
- HTTP mocking: `responses`, `httpretty`, `pytest-httpserver`
