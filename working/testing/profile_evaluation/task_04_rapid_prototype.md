# Task 04: Rapid Prototype

## Task Information

**Task ID**: task_04_rapid_prototype
**Category**: Prototyping and exploration
**Complexity**: Low-Medium
**Estimated Duration**: 1-2 hours
**Last Updated**: 2025-11-09

## Objective

Build a working prototype of a **Pomodoro timer CLI** to validate the concept before investing in full development.

## Context

Someone suggested building a Pomodoro timer for the team. Before committing to a full implementation, you need a quick prototype to:
- Validate the basic concept works
- Get feedback on UX
- Explore technical feasibility
- Decide if it's worth building properly

This tests:
- Speed over perfection
- Pragmatic decision-making
- Tolerance for quick-and-dirty code
- Knowing when "good enough" is good enough

## Requirements

### Must Have (MVP)
1. Start a 25-minute work session
2. Alert when time is up (sound or visual)
3. Track number of pomodoros completed
4. Basic commands: `start`, `status`, `stats`

### Nice to Have (If Time)
- 5-minute break timer
- Persistent stats (across sessions)
- Customizable duration
- Desktop notifications

### Explicitly Out of Scope (For Prototype)
- Full test coverage
- Perfect error handling
- Configuration file
- Multiple concurrent timers
- Fancy UI

## Success Criteria

1. **Functional Success**:
   - Works well enough to demo
   - Core use case (25 min timer) functions
   - Doesn't crash on basic usage

2. **Speed Success**:
   - Built in under 2 hours
   - "Done" means "demo-able" not "production-ready"

3. **Process Success**:
   - Shortcuts were taken intentionally
   - Trade-offs were clear
   - Focus stayed on validation, not perfection

4. **Decision Success**:
   - Can now decide: build it properly, modify approach, or abandon

## Starting Materials

Nothing! Quick prototype from scratch.

**Expected usage**:
```bash
$ pomodoro start
🍅 Pomodoro started! 25:00 remaining...
Focus on your task.

$ pomodoro status
🍅 15:32 remaining in current pomodoro

$ pomodoro stats
📊 Pomodoros completed today: 3
```

## Expected Profile Differences

### Default Profile (Minimalist)
- **Expected approach**:
  - Single file, ~100 lines
  - Use `time.sleep()` and simple countdown
  - Print to console for notifications
  - Maybe store count in a temp file
  - No tests (it's a prototype!)

- **Time estimate**: 45-90 minutes

- **Key characteristics**:
  - Fastest path to working demo
  - Comfortable with hacky solutions
  - Focus on "can we demo this in an hour?"
  - Perfect fit for this task

### Waterfall Profile (Phase-Gate)
- **Expected approach**:
  - Even a prototype needs some planning
  - Quick requirements doc (10-15 min)
  - Architecture sketch
  - Implementation
  - Basic testing
  - Still more structured than default

- **Time estimate**: 1.5-2 hours

- **Key characteristics**:
  - Can't help but plan a little
  - May include more features than necessary
  - Cleaner code structure even for prototype
  - Tension between "quick" and "proper"

### Mathematical-Elegance Profile (Formal Methods)
- **Expected approach**:
  - Specify what "a pomodoro" formally means
  - Type-safe time handling
  - Pure functions for logic
  - May still write some tests
  - Struggle with "quick and dirty"

- **Time estimate**: 2-3 hours

- **Key characteristics**:
  - Hard time writing bad code
  - May over-engineer even prototype
  - Types prevent errors (even in prototype)
  - Least suited profile for this task

## Evaluation Criteria

### Time Metrics
- [ ] Time to first working demo
- [ ] Total time spent
- [ ] How much time on "extras"

### Process Metrics
- [ ] Lines of code
- [ ] Number of files
- [ ] Tests written (if any)
- [ ] Features implemented

### Quality Metrics
- [ ] Does it work for demo?
- [ ] How "hacky" is it?
- [ ] Could it survive light use?

### Cognitive Metrics
- [ ] Comfort with quick-and-dirty
- [ ] Where did you draw the quality line?
- [ ] What shortcuts were taken?
- [ ] What was the first thing you built?

## Documentation Requirements

Document in `results/<profile-name>/task_04/`:

1. **approach.md**:
   - Shortcuts taken
   - What you skipped and why
   - How you decided "done"

2. **timeline.md**:
   - Time to first working version
   - Time on "extras"
   - Total time

3. **artifacts/**:
   - The prototype code
   - Demo output/screenshot

4. **metrics.json**:
```json
{
  "time_to_first_demo_minutes": 0,
  "total_time_minutes": 0,
  "lines_of_code": 0,
  "number_of_files": 0,
  "tests_written": 0,
  "features_implemented": ["start", "status"],
  "shortcuts_taken": ["no persistence", "no tests", "..."]
}
```

5. **reflection.md**:
   - Was this profile a good fit for prototyping?
   - Where did you struggle with "good enough"?
   - Did you over-engineer or under-engineer?

## Notes

- This task deliberately favors speed over quality
- Default profile should excel here
- Waterfall and mathematical-elegance may struggle
- Watch for: inability to ship "bad" code
- The point is validation, not production code

## Prototype Quality Spectrum

**Too Quick** (unusable):
- Doesn't actually work
- Can't demo
- Crashes immediately

**Just Right** (prototype):
- Works for demo
- Has obvious limitations
- Good enough to decide next steps

**Too Polished** (over-engineering):
- Perfect code structure
- Comprehensive tests
- Production-ready error handling
- Missed the point of "prototype"

## Example Implementation (Default Profile)

```python
#!/usr/bin/env python3
import time
import sys
from datetime import datetime, timedelta

# Quick and dirty: store state in a temp file
STATE_FILE = "/tmp/pomodoro_state.txt"
STATS_FILE = "/tmp/pomodoro_stats.txt"

def start():
    end_time = datetime.now() + timedelta(minutes=25)
    with open(STATE_FILE, 'w') as f:
        f.write(end_time.isoformat())
    print("🍅 Pomodoro started! 25:00 remaining...")
    print("Focus on your task.")

def status():
    try:
        with open(STATE_FILE, 'r') as f:
            end_time = datetime.fromisoformat(f.read().strip())
        remaining = end_time - datetime.now()
        if remaining.total_seconds() > 0:
            mins, secs = divmod(int(remaining.total_seconds()), 60)
            print(f"🍅 {mins}:{secs:02d} remaining")
        else:
            print("✅ Pomodoro complete!")
            # Increment stats (hacky)
            count = 0
            try:
                with open(STATS_FILE, 'r') as f:
                    count = int(f.read())
            except:
                pass
            with open(STATS_FILE, 'w') as f:
                f.write(str(count + 1))
    except FileNotFoundError:
        print("No active pomodoro")

def stats():
    try:
        with open(STATS_FILE, 'r') as f:
            count = int(f.read())
        print(f"📊 Pomodoros completed: {count}")
    except:
        print("📊 Pomodoros completed: 0")

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'status'
    {'start': start, 'status': status, 'stats': stats}.get(cmd, status)()
```

**This is intentionally hacky!** That's the point of a prototype.

## References

- Pomodoro Technique: https://francescocirillo.com/products/the-pomodoro-technique
- Similar tools: `pomo`, `pomofocus`
