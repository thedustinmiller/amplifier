#!/usr/bin/env python3
"""Test ElementLoader caching performance."""

import sys
import time
from pathlib import Path

forge_root = Path(__file__).parent
sys.path.insert(0, str(forge_root / "src"))

from forge.core.element import ElementLoader, ElementType


def test_cache_performance():
    """Test that caching improves load times."""
    elements_dir = forge_root / "elements"
    loader = ElementLoader([elements_dir])

    print("Testing ElementLoader Cache Performance")
    print("=" * 80)

    # First load (cold cache)
    start = time.time()
    element1 = loader.load("coevolution", ElementType.PRINCIPLE)
    first_load_time = time.time() - start

    # Second load (cached)
    start = time.time()
    element2 = loader.load("coevolution", ElementType.PRINCIPLE)
    cached_load_time = time.time() - start

    print(f"\nFirst load (cold):   {first_load_time*1000:.2f} ms")
    print(f"Second load (cache): {cached_load_time*1000:.2f} ms")
    print(f"Speedup:            {first_load_time/cached_load_time:.1f}x")

    # Verify they're the same object
    if element1 is element2:
        print("\n✓ Cache returns same object (efficient)")
    else:
        print("\n✗ Cache returns different object (inefficient)")

    # Test cache key distinction
    print("\n" + "=" * 80)
    print("Testing Cache Key Distinction")
    print("=" * 80)

    # Load with type specified
    element_typed = loader.load("coevolution", ElementType.PRINCIPLE)

    # Load without type specified
    element_any = loader.load("coevolution", None)

    print(f"\nWith type specified: {element_typed.name}")
    print(f"Without type (any):  {element_any.name}")

    if element_typed is not element_any:
        print("✓ Cache distinguishes between typed and untyped loads")
    else:
        print("⚠ Cache does not distinguish (may cause issues)")

    # Check cache size
    print("\n" + "=" * 80)
    print("Cache Inspection")
    print("=" * 80)
    print(f"\nCache entries: {len(loader._cache)}")
    for key in loader._cache.keys():
        print(f"  - {key}")


if __name__ == "__main__":
    test_cache_performance()
