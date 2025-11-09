# Test Results

This directory stores results from profile evaluation tests.

## Structure

```
results/
├── default/                    # Results using default profile
│   ├── task_01/
│   │   ├── approach.md        # How the task was approached
│   │   ├── timeline.md        # Timeline of work
│   │   ├── artifacts/         # Code, docs, etc. produced
│   │   ├── metrics.json       # Quantitative metrics
│   │   └── reflection.md      # Reflection on the process
│   ├── task_02/
│   └── ...
├── waterfall/                  # Results using waterfall profile
│   └── ...
├── mathematical-elegance/      # Results using mathematical-elegance profile
│   └── ...
├── profile-editor/            # Results using profile-editor profile
│   └── ...
└── comparison_reports/        # Cross-profile comparisons
    ├── task_01_comparison.md
    └── ...
```

## How to Document Results

After completing a task:

1. **Create task directory** (if not exists):
   ```bash
   mkdir -p results/<profile>/task_XX
   cd results/<profile>/task_XX
   ```

2. **Document your approach** (`approach.md`):
   - What philosophy guided you?
   - What decisions did you make?
   - Why did you make them?

3. **Record timeline** (`timeline.md`):
   - When did you start?
   - What were the key milestones?
   - How much time on each phase?

4. **Save artifacts** (`artifacts/`):
   - The actual code/docs you created
   - Screenshots if applicable
   - Any supporting materials

5. **Capture metrics** (`metrics.json`):
   - Follow the structure in the task spec
   - Quantitative data for comparison

6. **Reflect** (`reflection.md`):
   - What went well?
   - What was challenging?
   - Would you use this profile again?
   - What did you learn?

## Comparison Reports

After completing the same task with multiple profiles:

1. **Create comparison** (`comparison_reports/task_XX_comparison.md`)
2. **Compare**:
   - Approaches taken
   - Time spent
   - Quality of results
   - Appropriateness for task

3. **Analyze**:
   - Which profile was best suited?
   - What were the key differences?
   - What did we learn?

## Analysis

Use the data in this directory to:
- Choose the right profile for your work
- Understand profile tradeoffs
- Improve profiles over time
- Validate that profiles actually shape behavior

## Template Files

See parent directory for template structures:
- `task_template.md` - How tasks are structured
- Individual task files for specific requirements
