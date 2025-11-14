# Environment Manager Documentation

Generated: 2025-11-14

## Overview

`environment-manager` is the core component that handles the lifecycle of Claude Code remote sessions. It's a compiled Go binary that manages the containerized environment where Claude Code runs.

## Binary Information

**Location**: `/usr/local/bin/environment-manager`

**Type**: ELF 64-bit LSB executable, x86-64, dynamically linked

**Version**: staging-856163973

**Build Info**:
- Includes debug symbols (not stripped)
- BuildID: d33e39643effa11e8435973a2bca063d8e7b5028

## Operating Modes

The environment-manager can operate in two modes:

1. **Poll Mode**: Long-polls the container API waiting for new sessions
2. **Run Mode**: Directly connects to a session with known credentials

## Commands

### Main Command

```
environment-manager [command]
```

### Available Subcommands

- `completion` - Generate autocompletion script for specified shell
- `help` - Help about any command
- `task-run` - Start with existing session credentials

## task-run Command

This is the primary command used in Claude Code Web sessions (as seen in `ps aux` output).

### Description

Connects directly to the API with an existing session ID and token. Can optionally use a local JSON environment file to bypass API environment fetch.

### Usage

```bash
environment-manager task-run [flags]
```

### Flags

#### Session Management
- `--session string` - ID of the session to manage (required)
- `--session-mode string` - Session mode: 'new' (default), 'resume' (skip git clone and setup scripts), 'setup-only' (exit after setup) (default: "new")
- `--stdin` - Read combined startup context and environment configuration JSON from stdin (can bypass API environment fetch)

#### Authentication & Organization
- `--environment-id string` - Environment ID for API calls (required for BYOC)
- `--organization-uuid string` - Organization UUID for API calls (required for BYOC)

#### Tool Configuration
- `--allowed-tools string` - Comma-separated list of allowed tools for Claude (e.g., 'Bash,Edit,Write,MultiEdit,Agent,Glob,Grep,LS,View,Search,NotebookEdit,NotebookRead,TodoRead,TodoWrite')

#### Git Configuration
- `--git-mode string` - Git mode: 'http-proxy' (default, uses local git proxy) or 'mcp' (uses MCP git server) (default: "http-proxy")

#### Debugging & Logging
- `--debug` - Enable debug mode (sets CLAUDE_CODE_DEBUG environment variable)
- `--log-level string` - Log level: debug, info, warn, error (default: "info")
- `--verbose-claude-logs` - Enable verbose logging of Claude Code output to console (automatically enabled with --local-testing)

#### Development & Testing
- `--local-testing` - Disable Claude Code WebSocket connections and git configuration (run in standalone mode for local testing)

#### Upgrades
- `--upgrade-claude-code` - Upgrade Claude Code to the latest version before starting (default: true)

### stdin JSON Format

When using `--stdin`, provide a JSON object with the following structure:

```json
{
  "startup_context": {
    "sources": [...],
    "cwd": "..."
  },
  "environment": {
    "environment_type": "...",
    "version": "...",
    ...
  },
  "auth": [
    {
      "type": "github_app",
      "url": "github.com",
      "token": "ghs_..."
    }
  ]
}
```

## Current Session Usage

From the process list (`docs/process-list.txt`), the current session is running:

```bash
/usr/local/bin/environment-manager task-run \
  --stdin \
  --session session_019AbtVVtPRKXvRtM8W9LRow \
  --session-mode resume \
  --upgrade-claude-code=False
```

### Analysis of Current Flags

- `--stdin` - Configuration provided via stdin (from parent process)
- `--session session_019AbtVVtPRKXvRtM8W9LRow` - This specific session ID
- `--session-mode resume` - Resuming existing session (skipping git clone and setup)
- `--upgrade-claude-code=False` - Not upgrading Claude Code during this session

## Related Environment Variables

As seen in `docs/environment-details.md`, environment-manager sets several environment variables:

- `CLAUDE_CODE_SESSION_ID=session_019AbtVVtPRKXvRtM8W9LRow`
- `CLAUDE_CODE_VERSION=2.0.34`
- `CLAUDE_CODE_CONTAINER_ID=container_01SC7spAP38p8tyUuGuUuC2J--claude_code_remote--ragged-pretty-weary-apples`
- `CLAUDE_CODE_REMOTE=true`
- `CLAUDE_CODE_DEBUG=true` (debug mode enabled in current session)

## Architecture Insights

### Process Hierarchy

From `ps aux` output:

```
process_api (PID 1)
└── bash (PID 19)
    └── environment-manager (PID 21)
        └── claude (PID 33)
```

### Resource Usage

- Memory: ~56MB RSS (0.4% of 13GB available)
- CPU: Minimal when idle
- Manages the entire Claude Code session lifecycle

### Git Integration

The environment-manager handles git operations through:
- Local HTTP proxy (default mode, `--git-mode http-proxy`)
- Or MCP git server (`--git-mode mcp`)

Current session uses HTTP proxy mode with authentication tokens passed through the proxy configuration.

## Key Responsibilities

Based on flags and environment variables, environment-manager:

1. **Session Lifecycle**: Creates, resumes, and manages Claude Code sessions
2. **Environment Setup**: Configures the containerized environment
3. **Git Integration**: Manages git authentication and operations
4. **Tool Permissions**: Controls which Claude Code tools are available
5. **Logging & Debug**: Provides logging and debug capabilities
6. **Upgrades**: Can upgrade Claude Code versions between sessions

## See Also

- Main environment documentation: `docs/environment-details.md`
- Process list: `docs/process-list.txt`
- Claude CLI behavior: `docs/claude-cli-recursive-test.md`
