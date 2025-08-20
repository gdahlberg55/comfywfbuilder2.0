# MCP Usage Guidelines for Agents

## Core Principles

### 1. Memory (SCS) Usage
**Pattern**: Store Early, Retrieve Often
```python
# Good: Check cache before expensive operations
existing = search_nodes("model:SDXL")
if not existing:
    result = brave_web_search("SDXL model")
    create_entities(result)

# Bad: Duplicate searches without caching
result1 = brave_web_search("SDXL model")
result2 = brave_web_search("SDXL model")  # Wasteful!
```

### 2. Structured Data in Memory
**Pattern**: Use consistent entity types
```yaml
Entity Types:
  - workflow_parameter
  - node_selection
  - layout_position
  - validation_result
  - learned_pattern
  - asset_reference
```

### 3. Web Search Optimization
**Pattern**: Batch related searches
```python
# Good: Single search with comprehensive query
results = brave_web_search("ComfyUI SDXL LoRA trigger words site:civitai.com")

# Bad: Multiple narrow searches
search1 = brave_web_search("SDXL")
search2 = brave_web_search("LoRA")
search3 = brave_web_search("trigger words")
```

### 4. Sequential Thinking Usage
**When to Use**:
- Breaking down complex requirements (>3 steps)
- Evaluating multiple solutions
- Making architectural decisions
- Pattern matching across examples

**When NOT to Use**:
- Simple lookups
- Direct transformations
- Single-step operations

## Agent-Specific MCP Patterns

### Workflow-Architect (Opus)
```yaml
MCP Flow:
  1. sequentialthinking: Break down requirements
  2. search_nodes: Find similar architectures
  3. create_entities: Store design decisions
  4. create_relations: Map component relationships
```

### Asset-Finder
```yaml
MCP Flow:
  1. search_nodes: Check cache first
  2. brave_web_search: Find models/LoRAs
  3. WebFetch: Get detailed specs
  4. create_entities: Cache for reuse
```

### Graph-Analyzer (Opus)
```yaml
MCP Flow:
  1. sequentialthinking: Identify analysis strategy
  2. search_nodes: Get workflow structure
  3. create_relations: Map dependencies
  4. create_entities: Store bottlenecks/issues
```

### Learning-Agent (Opus)
```yaml
MCP Flow:
  1. search_nodes: Retrieve session history
  2. sequentialthinking: Extract patterns
  3. create_entities: Store new patterns
  4. add_observations: Enhance existing patterns
```

### Workflow-Researcher (Opus)
```yaml
MCP Flow:
  1. brave_web_search: Find trending workflows
  2. WebFetch: Download workflow JSON
  3. sequentialthinking: Analyze innovations
  4. create_entities: Store techniques
```

## Memory Schema Standards

### Entity Structure
```json
{
  "name": "unique_identifier",
  "entityType": "category",
  "observations": [
    "fact_1",
    "fact_2"
  ]
}
```

### Relation Structure
```json
{
  "from": "entity_1",
  "to": "entity_2",
  "relationType": "connects_to|depends_on|triggers|..."
}
```

## Error Handling

### Rate Limiting
```python
try:
    result = brave_web_search(query)
except RateLimitError:
    # Fall back to cache
    cached = search_nodes(query)
    if cached:
        return cached
    else:
        wait_and_retry()
```

### Memory Conflicts
```python
# Always check before creating
existing = search_nodes(f"name:{entity_name}")
if existing:
    add_observations(entity_name, new_data)
else:
    create_entities(entity_data)
```

## Performance Guidelines

### 1. Cache Everything
- Models/LoRAs found → Store permanently
- Workflow patterns → Store with tags
- Validation results → Store for comparison

### 2. Batch Operations
```python
# Good: Single memory operation
create_entities([entity1, entity2, entity3])

# Bad: Multiple calls
create_entities([entity1])
create_entities([entity2])
create_entities([entity3])
```

### 3. Use Relations for Complex Data
Instead of storing everything in observations:
```python
# Good: Structured relations
create_entities([{"name": "node_1", "type": "KSampler"}])
create_entities([{"name": "node_2", "type": "VAEDecode"}])
create_relations([{"from": "node_1", "to": "node_2", "type": "latent_flow"}])

# Bad: Everything in observations
create_entities([{
    "name": "workflow",
    "observations": ["node_1 connects to node_2", "node_1 is KSampler", ...]
}])
```

## Best Practices

### 1. Session Management
- Initialize session entity at start
- Update session with milestones
- Close session with summary

### 2. Search Before Store
- Always check if data exists
- Update rather than duplicate
- Use consistent naming

### 3. Fail Gracefully
- Cache fallbacks for web searches
- Default values for missing data
- Log failures to memory

### 4. Clean Up
- Remove temporary entities
- Archive old sessions
- Compress repetitive data

## Model-Specific Guidelines

### Opus Agents (Complex Reasoning)
- Use sequentialthinking for ALL multi-step decisions
- Store reasoning chains in memory
- Reference previous thoughts in new analysis

### Standard Agents (Focused Tasks)
- Direct tool usage without overthinking
- Quick memory lookups
- Efficient single-purpose execution

## Integration with SCS

All agents MUST:
1. Read SCS state on start
2. Update SCS after each operation
3. Pass full context to next agent
4. Never assume SCS state

## Monitoring & Debugging

Track in memory:
- Tool usage counts
- Error frequencies
- Performance metrics
- Success patterns

This enables Learning-Agent to optimize the system over time.