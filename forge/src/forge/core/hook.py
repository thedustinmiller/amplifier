"""
Hook base class for Forge.
"""

from abc import ABC
from typing import Any, Dict, Optional


class Hook(ABC):
    """Base class for hooks.

    Hooks respond to system events with automated actions.
    """

    async def on_session_start(self, **kwargs) -> Optional[Dict[str, Any]]:
        """Handle session start event."""
        pass

    async def on_session_end(self, **kwargs) -> Optional[Dict[str, Any]]:
        """Handle session end event."""
        pass

    async def on_pre_tool(self, **kwargs) -> Optional[Dict[str, Any]]:
        """Handle pre-tool execution event."""
        pass

    async def on_post_tool(self, **kwargs) -> Optional[Dict[str, Any]]:
        """Handle post-tool execution event."""
        pass

    async def on_memory_write(self, **kwargs) -> Optional[Dict[str, Any]]:
        """Handle memory write event."""
        pass

    async def on_memory_query(self, **kwargs) -> Optional[Dict[str, Any]]:
        """Handle memory query event."""
        pass
