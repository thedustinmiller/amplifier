# Pomodoro Timer CLI - Initial Spec Sketch

**Status**: Draft (Coevolution Iteration 1)
**Created**: 2025-11-12
**Principle**: Ruthless Minimalism + Coevolution

## Core Need
Users need a simple way to time focused work sessions (25 min Pomodoros) from the command line.

## MVP User Stories (Ruthlessly Minimal)

### P1: Start a Timer
As a user, I want to start a 25-minute timer so I can focus on work.

**Acceptance**:
- Run `pomodoro start`
- See confirmation that timer started
- Timer runs for 25 minutes

### P2: Check Status
As a user, I want to see how much time remains so I know when to take a break.

**Acceptance**:
- Run `pomodoro status`
- See time remaining in current pomodoro
- See helpful message if no timer running

### P3: Track Completion
As a user, I want to see how many pomodoros I completed so I feel accomplished.

**Acceptance**:
- Run `pomodoro stats`
- See count of completed pomodoros
- Count persists across terminal sessions

## Functional Requirements (Minimal)

- **FR-001**: System MUST start a 25-minute countdown timer
- **FR-002**: System MUST show remaining time when asked
- **FR-003**: System MUST track completed pomodoros count
- **FR-004**: System MUST notify user when timer completes
- **FR-005**: System MUST persist stats across sessions

## Success Criteria

- **SC-001**: User can start timer in under 5 seconds
- **SC-002**: User can check status at any time
- **SC-003**: Stats persist after closing terminal
- **SC-004**: Works on first run without setup

## Out of Scope (For Prototype)

- Break timers
- Customizable durations
- Desktop notifications
- Multiple concurrent timers
- Configuration files
- Full test coverage
- Fancy UI

## Implementation Discovery Points

These will be resolved during prototyping (coevolution):
- How to persist state? [File-based, temp directory]
- How to notify completion? [Print to console, maybe bell]
- How to handle timer in background? [User must check status]
- Error handling depth? [Basic only]

## Notes

This spec will evolve as we build. Starting minimal to ship fast.
