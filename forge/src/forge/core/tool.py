"""
Tool base class for Forge.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class Tool(ABC):
    """Base class for tools.

    Tools are executable capabilities that perform specific tasks.
    """

    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool.

        Args:
            **kwargs: Tool-specific arguments

        Returns:
            Dictionary with tool outputs
        """
        pass
