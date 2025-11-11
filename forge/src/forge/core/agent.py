"""
Agent base class for Forge.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class Agent(ABC):
    """Base class for agents.

    Agents provide specialized intelligence and perspective.
    """

    @abstractmethod
    async def process(self, **kwargs) -> Dict[str, Any]:
        """Process input and provide perspective.

        Args:
            **kwargs: Agent-specific arguments

        Returns:
            Dictionary with agent outputs
        """
        pass
