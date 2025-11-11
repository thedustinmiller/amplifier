"""
Tests for element system.
"""

import tempfile
from pathlib import Path

from forge.core.element import Element, ElementType, ElementMetadata


def test_element_creation():
    """Test creating an element."""
    element = Element(
        metadata=ElementMetadata(
            name="test-principle",
            type=ElementType.PRINCIPLE,
            version="1.0.0",
            description="Test principle",
            author="test",
            tags=["test"],
        ),
        content="This is a test principle."
    )

    assert element.name == "test-principle"
    assert element.type == ElementType.PRINCIPLE
    assert element.version == "1.0.0"
    assert element.content == "This is a test principle."


def test_element_serialization():
    """Test element to/from dict."""
    element = Element(
        metadata=ElementMetadata(
            name="test",
            type=ElementType.PRINCIPLE,
            version="1.0.0"
        ),
        content="Test content"
    )

    # To dict
    data = element.to_dict()
    assert data["metadata"]["name"] == "test"
    assert data["content"] == "Test content"

    # From dict
    element2 = Element.from_dict(data)
    assert element2.name == "test"
    assert element2.content == "Test content"


def test_element_file_io():
    """Test saving/loading elements."""
    with tempfile.TemporaryDirectory() as tmpdir:
        element_dir = Path(tmpdir) / "test-element"
        element_dir.mkdir()

        # Create element
        element = Element(
            metadata=ElementMetadata(
                name="test",
                type=ElementType.PRINCIPLE,
                version="1.0.0"
            ),
            content="Test principle content"
        )

        # Save
        element_file = element_dir / "element.yaml"
        element.save_to_file(element_file)

        # Verify files exist
        assert element_file.exists()
        assert (element_dir / "test.md").exists()

        # Load
        loaded = Element.load_from_file(element_file)
        assert loaded.name == "test"
        assert loaded.type == ElementType.PRINCIPLE
        assert loaded.content == "Test principle content"
