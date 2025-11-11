#!/usr/bin/env python3
"""
Forge Demo - Programmatic Usage

This script demonstrates how to use Forge programmatically.
"""

import asyncio
from pathlib import Path
from forge.memory import FileProvider, Scope
from forge.core.composition import Composition, CompositionElements, CompositionSettings


async def main():
    print("🔨 Forge Demo - Programmatic Usage\n")

    # 1. Create a composition programmatically
    print("▶ Creating composition...")
    composition = Composition(
        name="demo-project",
        type="preset",
        version="1.0.0",
        description="A demo Forge composition",
        elements=CompositionElements(
            principles=["ruthless-minimalism", "coevolution"],
            tools=[],
            agents=[],
        ),
        settings=CompositionSettings(
            memory={
                "provider": "file",
                "config": {"base_path": ".forge/memory"}
            }
        )
    )

    print(f"  ✓ Created composition: {composition.name}")
    print(f"  ✓ Principles: {', '.join(composition.elements.principles)}")

    # 2. Save composition to file
    demo_dir = Path("demo-project")
    demo_dir.mkdir(exist_ok=True)
    forge_dir = demo_dir / ".forge"
    forge_dir.mkdir(exist_ok=True)

    composition_file = forge_dir / "composition.yaml"
    composition.save_to_file(composition_file)
    print(f"  ✓ Saved to: {composition_file}\n")

    # 3. Initialize memory
    print("▶ Initializing memory...")
    memory = FileProvider()
    await memory.initialize({
        "base_path": str(demo_dir / ".forge/memory"),
        "session_id": "demo"
    })
    print("  ✓ Memory initialized\n")

    # 4. Store some data
    print("▶ Storing data in memory...")

    # Project decision
    await memory.set(
        key="decision:tech-stack",
        value="Using Python + FastAPI for API, React for frontend",
        scope=Scope.PROJECT,
        tags=["decision", "architecture"]
    )
    print("  ✓ Stored decision: tech-stack")

    # Global learning
    await memory.set(
        key="learning:fastapi-async",
        value="FastAPI handles async/await natively, no need for explicit event loop",
        scope=Scope.GLOBAL,
        tags=["python", "fastapi", "async"]
    )
    print("  ✓ Stored learning: fastapi-async")

    # Session note
    await memory.set(
        key="note:current-task",
        value="Building user authentication module",
        scope=Scope.SESSION,
        tags=["task", "in-progress"]
    )
    print("  ✓ Stored note: current-task\n")

    # 5. Query memory
    print("▶ Querying memory...")

    # Get all decisions
    decisions = await memory.query("decision:*", Scope.PROJECT)
    print(f"\n  Project decisions ({len(decisions)}):")
    for entry in decisions:
        print(f"    • {entry.key}: {entry.value}")

    # Get all learnings
    learnings = await memory.query("learning:*", Scope.GLOBAL)
    print(f"\n  Global learnings ({len(learnings)}):")
    for entry in learnings:
        print(f"    • {entry.key}: {entry.value}")

    # Get session notes
    notes = await memory.query("note:*", Scope.SESSION)
    print(f"\n  Session notes ({len(notes)}):")
    for entry in notes:
        print(f"    • {entry.key}: {entry.value}")

    print()

    # 6. Query by tag
    print("▶ Querying by tag...")
    async_related = await memory.query("tag:async", Scope.GLOBAL)
    print(f"\n  Items tagged 'async' ({len(async_related)}):")
    for entry in async_related:
        print(f"    • {entry.key}: {entry.value}")

    print()

    # 7. Clean up
    await memory.close()
    print("▶ Demo complete! ✓\n")
    print(f"Project created at: {demo_dir.absolute()}")
    print(f"Explore the composition: cat {composition_file}")
    print(f"Explore memory: ls {demo_dir / '.forge/memory/project'}")


if __name__ == "__main__":
    asyncio.run(main())
