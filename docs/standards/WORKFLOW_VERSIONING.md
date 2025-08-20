# Workflow Versioning and Memory System

## Directory Structure

```
output/
├── workflows/              # Versioned workflow outputs
│   ├── v1_YYYYMMDD_HHMMSS/
│   │   ├── workflow.json   # Final workflow
│   │   ├── metadata.json   # Generation metadata
│   │   └── preview.png     # Visual preview
│   └── v2_YYYYMMDD_HHMMSS/
├── logs/                   # Generation logs
│   ├── YYYYMMDD/
│   │   └── generation_HHMMSS.log
└── memory/                 # MCP memory persistence
    ├── node_cache.json     # Cached node schemas
    ├── patterns.json       # Learned patterns
    └── history.json        # Generation history
```

## Versioning System

Each workflow generation creates a new versioned folder:
- **Format**: `v{N}_{YYYYMMDD}_{HHMMSS}`
- **N**: Incremental version number for the day
- **YYYYMMDD**: Date stamp
- **HHMMSS**: Time stamp

## Metadata Structure

Each generation includes metadata.json:
```json
{
  "version": "v1_20250809_143000",
  "timestamp": "2025-08-09T14:30:00Z",
  "request": {
    "type": "generation|organization",
    "input": "user's original request",
    "parameters": {...}
  },
  "agents_invoked": ["parameter-extractor", "asset-finder", ...],
  "execution_time": 45.2,
  "node_count": 25,
  "group_count": 5,
  "validation_status": "passed",
  "memory_usage": "35MB"
}
```

## Memory MCP Integration

The system uses MCP memory server for:

1. **Node Cache** (`mcp__memory__store/retrieve`)
   - Caches ComfyUI node schemas
   - Reduces API calls
   - Updates on new discoveries

2. **Pattern Learning**
   - Common workflow patterns
   - Successful configurations
   - User preferences

3. **Generation History**
   - Complete audit trail
   - Performance metrics
   - Error patterns

## Logging System

Detailed logs for each generation:
```
[2025-08-09 14:30:00] INFO: Starting workflow generation v1
[2025-08-09 14:30:01] INFO: Invoking parameter-extractor
[2025-08-09 14:30:02] DEBUG: Extracted parameters: {...}
[2025-08-09 14:30:03] INFO: Invoking asset-finder
[2025-08-09 14:30:10] INFO: Found 3 compatible models
...
[2025-08-09 14:30:45] SUCCESS: Workflow generated and validated
```

## Benefits

1. **No Lost Work**: Every generation is preserved
2. **Easy Comparison**: Compare versions side-by-side
3. **Audit Trail**: Complete history of all generations
4. **Learning**: System improves from past generations
5. **Debugging**: Detailed logs for troubleshooting