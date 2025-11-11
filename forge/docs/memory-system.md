# Memory System

The memory system is **pluggable** - start simple with files, scale to graphs/vectors/relational as needed.

## Design Philosophy

### Why Pluggable?
Different projects have different memory needs:
- **Prototypes**: Simple file-based memory
- **Production**: Relational database with transactions
- **AI-heavy**: Vector store for semantic search
- **Complex domains**: Graph database for relationships

One size doesn't fit all. Start simple, upgrade when needed.

### Core Abstraction
All memory providers implement the same interface. Swap providers without changing elements.

## Architecture

```
┌─────────────────────────────────────────────┐
│ Elements (Tools, Agents, Hooks)             │
│ ↓ use                                       │
├─────────────────────────────────────────────┤
│ Memory Interface (Abstract)                 │
│ - get(), set(), query(), search()           │
│ - Scope-aware (session/project/global)      │
│ ↓ delegates to                              │
├─────────────────────────────────────────────┤
│ Memory Providers (Pluggable)                │
│ - FileProvider (simple)                     │
│ - GraphProvider (relationships)             │
│ - VectorProvider (semantic)                 │
│ - RelationalProvider (structured)           │
│ - HybridProvider (best of all)              │
└─────────────────────────────────────────────┘
```

## Memory Interface

### Core Protocol

```python
from typing import Protocol, Optional, List, Dict, Any
from enum import Enum
from dataclasses import dataclass

class Scope(Enum):
    """Memory scopes with different lifetimes."""
    SESSION = "session"    # Current working context (ephemeral)
    PROJECT = "project"    # Project-specific (persistent)
    GLOBAL = "global"      # Cross-project (permanent)

@dataclass
class MemoryEntry:
    """Memory entry with metadata."""
    key: str
    value: str
    scope: Scope
    timestamp: int
    tags: List[str]
    metadata: Dict[str, Any]

class MemoryProvider(Protocol):
    """Abstract memory provider interface."""

    async def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize provider with configuration."""
        ...

    async def get(self, key: str, scope: Scope) -> Optional[MemoryEntry]:
        """Retrieve value by key within scope."""
        ...

    async def set(
        self,
        key: str,
        value: str,
        scope: Scope,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Store value with key in scope."""
        ...

    async def query(
        self,
        pattern: str,
        scope: Scope,
        limit: Optional[int] = None
    ) -> List[MemoryEntry]:
        """Query entries matching pattern.

        Pattern syntax:
        - "prefix:*" - All keys starting with "prefix:"
        - "*:suffix" - All keys ending with ":suffix"
        - "key" - Exact match
        - "tag:tagname" - All entries with tag
        """
        ...

    async def search(
        self,
        semantic: str,
        scope: Scope,
        limit: int = 10,
        threshold: float = 0.7
    ) -> List[tuple[MemoryEntry, float]]:
        """Semantic search (requires vector support).

        Returns entries with similarity scores.
        Raises NotImplementedError if provider doesn't support vectors.
        """
        ...

    async def delete(self, key: str, scope: Scope) -> bool:
        """Delete entry by key."""
        ...

    async def clear(self, scope: Scope) -> int:
        """Clear all entries in scope. Returns count deleted."""
        ...

    async def close(self) -> None:
        """Close provider and release resources."""
        ...
```

### Extended Interface (Optional)

Providers can optionally implement advanced features:

```python
class AdvancedMemoryProvider(MemoryProvider):
    """Extended capabilities for advanced providers."""

    async def relate(
        self,
        from_key: str,
        to_key: str,
        relation_type: str,
        scope: Scope
    ) -> None:
        """Create relationship between entries (graph providers)."""
        ...

    async def traverse(
        self,
        start_key: str,
        relation_type: str,
        scope: Scope,
        max_depth: int = 3
    ) -> List[List[MemoryEntry]]:
        """Traverse relationships (graph providers)."""
        ...

    async def transaction(self) -> "Transaction":
        """Begin transaction (relational providers)."""
        ...

    async def index(self, field: str, scope: Scope) -> None:
        """Create index for faster queries."""
        ...
```

## Memory Scopes

### Session Scope
**Lifetime**: Current session only
**Purpose**: Working context, temporary state
**Cleared**: When session ends

**Use cases**:
- Current task context
- Temporary notes
- Intermediate results
- Agent state

**Example**:
```python
# Store current task
await memory.set(
    key="current_task",
    value="Implementing user authentication",
    scope=Scope.SESSION
)

# Retrieve later in session
task = await memory.get("current_task", Scope.SESSION)
```

### Project Scope
**Lifetime**: Project duration
**Purpose**: Project-specific knowledge
**Cleared**: When project deleted

**Use cases**:
- Project decisions
- Architecture notes
- Implementation patterns
- Team conventions

**Example**:
```python
# Store decision
await memory.set(
    key="decision:auth-strategy",
    value="Using JWT with refresh tokens because...",
    scope=Scope.PROJECT,
    tags=["decision", "authentication"]
)

# Query all decisions
decisions = await memory.query("decision:*", Scope.PROJECT)
```

### Global Scope
**Lifetime**: Permanent
**Purpose**: Cross-project learnings
**Cleared**: Never (user must explicitly delete)

**Use cases**:
- Reusable patterns
- Common mistakes
- Tool knowledge
- General learnings

**Example**:
```python
# Store learning
await memory.set(
    key="learning:async-file-io",
    value="Always use aiofiles for async file operations. Regular open() blocks.",
    scope=Scope.GLOBAL,
    tags=["python", "async", "io"]
)

# Search across all projects
learnings = await memory.search(
    semantic="file operations async python",
    scope=Scope.GLOBAL
)
```

## Memory Providers

### FileProvider
**Purpose**: Simple file-based storage
**Best for**: Prototypes, small projects, getting started

**Structure**:
```
.forge/memory/
├── session/
│   └── {session_id}/
│       └── {key}.json
├── project/
│   ├── {key}.json
│   └── _index.json
└── global/
    ├── {key}.json
    └── _index.json
```

**Configuration**:
```yaml
memory:
  provider: file
  config:
    base_path: .forge/memory
    compression: true
    max_file_size: 1MB
```

**Implementation**:
```python
from forge.memory import MemoryProvider, Scope, MemoryEntry
import json
from pathlib import Path
from typing import Optional, List

class FileProvider(MemoryProvider):
    """File-based memory provider."""

    def __init__(self):
        self.base_path: Optional[Path] = None

    async def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize file provider."""
        self.base_path = Path(config.get("base_path", ".forge/memory"))
        self.base_path.mkdir(parents=True, exist_ok=True)

        # Create scope directories
        for scope in Scope:
            (self.base_path / scope.value).mkdir(exist_ok=True)

    async def get(self, key: str, scope: Scope) -> Optional[MemoryEntry]:
        """Get entry from file."""
        file_path = self._key_to_path(key, scope)
        if not file_path.exists():
            return None

        async with aiofiles.open(file_path, 'r') as f:
            data = json.loads(await f.read())
            return MemoryEntry(**data)

    async def set(
        self,
        key: str,
        value: str,
        scope: Scope,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Store entry to file."""
        entry = MemoryEntry(
            key=key,
            value=value,
            scope=scope,
            timestamp=int(time.time()),
            tags=tags or [],
            metadata=metadata or {}
        )

        file_path = self._key_to_path(key, scope)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(file_path, 'w') as f:
            await f.write(json.dumps(asdict(entry), indent=2))

        # Update index
        await self._update_index(entry)

    def _key_to_path(self, key: str, scope: Scope) -> Path:
        """Convert key to file path."""
        safe_key = key.replace(":", "_").replace("/", "_")
        return self.base_path / scope.value / f"{safe_key}.json"

    async def query(
        self,
        pattern: str,
        scope: Scope,
        limit: Optional[int] = None
    ) -> List[MemoryEntry]:
        """Query entries by pattern."""
        # Load index
        index = await self._load_index(scope)

        # Match pattern
        matches = []
        for entry_data in index:
            if self._matches_pattern(entry_data["key"], pattern):
                matches.append(MemoryEntry(**entry_data))

        # Limit results
        if limit:
            matches = matches[:limit]

        return matches

    async def search(
        self,
        semantic: str,
        scope: Scope,
        limit: int = 10,
        threshold: float = 0.7
    ) -> List[tuple[MemoryEntry, float]]:
        """Semantic search not supported in file provider."""
        raise NotImplementedError(
            "FileProvider doesn't support semantic search. "
            "Use VectorProvider for semantic capabilities."
        )
```

**Pros**:
- Simple to understand
- No external dependencies
- Easy to inspect (JSON files)
- Version control friendly

**Cons**:
- No semantic search
- Linear query performance
- No relationships
- No transactions

### GraphProvider
**Purpose**: Relationship-based storage
**Best for**: Complex domains, interconnected concepts

**Technology**: Neo4j, ArangoDB, or similar

**Structure**:
```
Nodes: Memory entries
Edges: Relationships between entries
Properties: Tags, metadata, timestamps
```

**Configuration**:
```yaml
memory:
  provider: graph
  config:
    url: bolt://localhost:7687
    username: neo4j
    password: secret
    database: forge
```

**Capabilities**:
```python
# Store with relationships
await memory.set("decision:auth", "Use JWT", Scope.PROJECT)
await memory.set("implementation:jwt-service", "Created", Scope.PROJECT)

# Create relationship
await memory.relate(
    from_key="decision:auth",
    to_key="implementation:jwt-service",
    relation_type="IMPLEMENTS",
    scope=Scope.PROJECT
)

# Traverse relationships
implementations = await memory.traverse(
    start_key="decision:auth",
    relation_type="IMPLEMENTS",
    scope=Scope.PROJECT
)
```

**Pros**:
- Rich relationships
- Complex queries
- Pattern matching
- Flexible schema

**Cons**:
- External dependency
- Learning curve
- Overkill for simple projects

### VectorProvider
**Purpose**: Semantic search and similarity
**Best for**: AI-heavy workflows, large knowledge bases

**Technology**: Pinecone, Weaviate, ChromaDB, or similar

**Structure**:
```
Vectors: Embeddings of values
Metadata: Keys, scopes, tags
Index: Optimized for similarity search
```

**Configuration**:
```yaml
memory:
  provider: vector
  config:
    url: https://api.pinecone.io
    api_key: secret
    index: forge-memory
    embedding_model: openai/text-embedding-3-small
    dimensions: 1536
```

**Capabilities**:
```python
# Store with automatic embedding
await memory.set(
    key="pattern:async-file-io",
    value="Always use aiofiles for async file operations...",
    scope=Scope.GLOBAL
)

# Semantic search
results = await memory.search(
    semantic="How do I do async file operations in Python?",
    scope=Scope.GLOBAL,
    limit=5,
    threshold=0.8
)

for entry, score in results:
    print(f"[{score:.2f}] {entry.key}: {entry.value}")
```

**Pros**:
- Semantic search
- Similarity matching
- Scales to millions
- AI-native

**Cons**:
- External dependency
- Cost (embeddings)
- Eventual consistency
- Less precise queries

### RelationalProvider
**Purpose**: Structured queries and transactions
**Best for**: Production systems, audit requirements

**Technology**: PostgreSQL, SQLite, MySQL

**Structure**:
```sql
CREATE TABLE memory (
    id SERIAL PRIMARY KEY,
    key VARCHAR(255) NOT NULL,
    value TEXT NOT NULL,
    scope VARCHAR(50) NOT NULL,
    timestamp BIGINT NOT NULL,
    tags TEXT[],
    metadata JSONB,
    UNIQUE(key, scope)
);

CREATE INDEX idx_memory_scope ON memory(scope);
CREATE INDEX idx_memory_key ON memory(key);
CREATE INDEX idx_memory_tags ON memory USING GIN(tags);
```

**Configuration**:
```yaml
memory:
  provider: relational
  config:
    url: postgresql://user:pass@localhost:5432/forge
    pool_size: 10
    ssl: require
```

**Capabilities**:
```python
# Transactional updates
async with memory.transaction() as txn:
    await txn.set("counter", "1", Scope.PROJECT)
    await txn.set("status", "active", Scope.PROJECT)
    await txn.commit()

# Complex queries
results = await memory.query(
    pattern="decision:* WHERE tags @> ARRAY['architecture']",
    scope=Scope.PROJECT
)
```

**Pros**:
- ACID transactions
- Complex queries
- Mature ecosystem
- Well understood

**Cons**:
- Schema management
- Less flexible
- External dependency

### HybridProvider
**Purpose**: Combine best of multiple providers
**Best for**: Production systems that need everything

**Structure**:
```
┌─────────────────────────────────────┐
│ HybridProvider                      │
│ ↓ delegates to                      │
├─────────────────────────────────────┤
│ FileProvider     (cache)            │
│ RelationalProvider (source of truth)│
│ VectorProvider  (semantic search)   │
│ GraphProvider   (relationships)     │
└─────────────────────────────────────┘
```

**Configuration**:
```yaml
memory:
  provider: hybrid
  config:
    cache:
      provider: file
      ttl: 3600
    storage:
      provider: relational
      url: postgresql://...
    search:
      provider: vector
      url: https://pinecone.io/...
    relationships:
      provider: graph
      url: bolt://neo4j:7687
```

**Routing**:
- `get()`, `set()`, `delete()` → Storage provider
- `search()` → Search provider (if available)
- `relate()`, `traverse()` → Relationships provider (if available)
- All reads check cache first

**Pros**:
- Best of all worlds
- Optimized for each operation
- Graceful degradation

**Cons**:
- Complexity
- Many dependencies
- Consistency challenges

## Memory Patterns

### Decision Log
```python
async def log_decision(
    memory: MemoryProvider,
    decision: str,
    rationale: str,
    alternatives: List[str]
):
    """Log architectural decision."""
    timestamp = int(time.time())
    key = f"decision:{timestamp}"

    await memory.set(
        key=key,
        value=json.dumps({
            "decision": decision,
            "rationale": rationale,
            "alternatives": alternatives
        }),
        scope=Scope.PROJECT,
        tags=["decision", "architecture"]
    )
```

### Learning Capture
```python
async def capture_learning(
    memory: MemoryProvider,
    topic: str,
    insight: str,
    context: str
):
    """Capture learning for future reference."""
    key = f"learning:{topic.replace(' ', '-')}"

    await memory.set(
        key=key,
        value=insight,
        scope=Scope.GLOBAL,
        tags=["learning", topic],
        metadata={"context": context}
    )
```

### Context Loading
```python
async def load_session_context(
    memory: MemoryProvider,
    session_id: str
) -> Dict[str, Any]:
    """Load relevant context for session."""
    # Get recent project activity
    recent_project = await memory.query(
        pattern="*",
        scope=Scope.PROJECT,
        limit=10
    )

    # Get relevant global learnings
    recent_global = await memory.query(
        pattern="learning:*",
        scope=Scope.GLOBAL,
        limit=5
    )

    return {
        "recent_project": [e.value for e in recent_project],
        "relevant_learnings": [e.value for e in recent_global]
    }
```

## Migration Between Providers

### Export
```python
async def export_memory(
    provider: MemoryProvider,
    output_path: str
):
    """Export all memory to JSON."""
    export_data = {
        "version": "1.0",
        "timestamp": int(time.time()),
        "scopes": {}
    }

    for scope in Scope:
        entries = await provider.query("*", scope)
        export_data["scopes"][scope.value] = [
            asdict(entry) for entry in entries
        ]

    async with aiofiles.open(output_path, 'w') as f:
        await f.write(json.dumps(export_data, indent=2))
```

### Import
```python
async def import_memory(
    provider: MemoryProvider,
    input_path: str
):
    """Import memory from JSON."""
    async with aiofiles.open(input_path, 'r') as f:
        data = json.loads(await f.read())

    for scope_name, entries in data["scopes"].items():
        scope = Scope(scope_name)
        for entry_data in entries:
            await provider.set(
                key=entry_data["key"],
                value=entry_data["value"],
                scope=scope,
                tags=entry_data.get("tags"),
                metadata=entry_data.get("metadata")
            )
```

## Configuration

### Per-Project
`.forge/config.yaml`:
```yaml
memory:
  provider: file
  config:
    base_path: .forge/memory
```

### Global Default
`~/.forge/config.yaml`:
```yaml
memory:
  provider: hybrid
  config:
    storage:
      provider: relational
      url: postgresql://localhost/forge
    search:
      provider: vector
      url: http://localhost:8000
```

### Runtime Override
```bash
forge init --memory-provider vector
forge session start --memory-config memory.yaml
```

## Summary

The pluggable memory system provides:
- **Simple start**: File-based provider for prototypes
- **Scale when needed**: Graph, vector, relational for production
- **Best of both**: Hybrid provider combines multiple backends
- **Smooth migration**: Export/import between providers
- **Scope isolation**: Session/project/global separation

Start simple. Scale when needed. No lock-in.
