# MCP Tool Mapping Documentation v2.0

This document outlines the MCP (Model Context Protocol) tools and standard Claude Code tools available to ComfyUI Workflow Generator agents and their specific use cases.

## ⚠️ IMPORTANT: Tool Availability in Claude Code

### ✅ ACTUALLY Available MCP Servers
Based on real-world testing in Claude Code environment:

### 1. brave-search
- **Tool**: `mcp__brave-search__search`
- **Purpose**: Web searching for models, LoRAs, custom nodes, and documentation
- **Used by**: asset-finder agent

### 2. web-fetch
- **Tool**: `mcp__web-fetch__fetch`
- **Purpose**: Fetching web content, particularly ComfyUI API documentation
- **Used by**: node-curator, node-verification agents
- **Primary endpoint**: ComfyUI /object_info API

### ❌ NOT Available in Claude Code
- `mcp__playwright-mcp-server__*` - NOT AVAILABLE
- `Windows-MCP tools` - NOT AVAILABLE
- `desktop-commander` - NOT AVAILABLE
- Any extension-based MCP servers - NOT AVAILABLE

### 4. memory
- **Tool**: `mcp__memory__store`, `mcp__memory__retrieve`
- **Purpose**: Persistent memory for caching node schemas and learned patterns
- **Potential use**: learning-agent, node-verification

### 5. code_execution (via MCP)
- **Tool**: `mcp__code_execution`
- **Purpose**: Execute Python code for algorithms
- **Used by**: layout-strategist, layout-refiner, reroute-engineer, graph-analyzer

## Standard Claude Code Tools

In addition to MCP tools, agents have access to standard Claude Code tools:

### File System Tools
- **Read**: Read files
- **Write**: Write new files
- **Edit**: Modify existing files
- **MultiEdit**: Multiple edits in one operation
- **Glob**: Find files by pattern
- **Grep**: Search within files
- **LS**: List directory contents

### Web Tools
- **WebSearch**: Search the web
- **WebFetch**: Fetch web content (alternative to MCP)

### System Tools
- **Bash**: Execute shell commands (restricted)
- **Task**: Delegate to other agents
- **TodoWrite**: Task management

## Enhanced Tool Usage by Agent (v2.0)

### Agents with Web Access:
- **asset-finder**: `mcp__brave-search__search`, `WebSearch`, `WebFetch`
- **node-curator**: `mcp__web-fetch__fetch`, `WebSearch`
- **node-verification**: `mcp__web-fetch__fetch`, `Read`
- **workflow-researcher**: `WebSearch`, `WebFetch`, `mcp__brave-search__search`
- **prompt-crafter**: `WebSearch` (for prompt techniques)
- **learning-agent**: `WebSearch` (for best practices)

### Agents with Code Execution:
- **graph-analyzer**: `mcp__code_execution`, `Read`, `Write`
- **layout-strategist**: `mcp__code_execution`, `mcp__memory__store/retrieve`
- **reroute-engineer**: `mcp__code_execution` (data_bus_router.py)
- **layout-refiner**: `mcp__code_execution` (collision_detection.py)
- **group-coordinator**: `mcp__memory__retrieve`, `Edit`
- **workflow-serializer**: `mcp__code_execution` (json_validator.py), `Write`
- **visualizer**: `mcp__code_execution`, `Write`
- **workflow-validator**: `mcp__code_execution`, `Read`, `Write`
- **memory-monitor**: `mcp__memory__retrieve`, `Bash` (restricted)
- **workflow-chunker**: `mcp__code_execution`, `Read`, `Write`
- **learning-agent**: `mcp__memory__store/retrieve`, `WebSearch`

### Agents with File Management:
- **logger**: `Write`, `Read`
- **issue-tracker**: `Read`, `Edit`, `Write`
- **nomenclature-specialist**: `MultiEdit`, `mcp__memory__store`
- **workflow-serializer**: `Write`, `Edit`
- **templating-enforcer**: `Read`, `Write`

## Tool Invocation Patterns

### Searching for Assets:
```
mcp__brave-search__search({
  "query": "SDXL LoRA anime style civitai"
})
```

### Fetching ComfyUI Node Schema:
```
mcp__web-fetch__fetch({
  "url": "http://localhost:8188/object_info",
  "method": "GET"
})
```

### Alternative for Screenshots:
```python
# Since playwright is not available in Claude Code:
# Ask user to take screenshot manually
print("Please take a screenshot using Win+Shift+S")
print("Then paste directly into chat or save and provide path")
```

### Code Execution for Layout:
```
code_execution({
  "language": "python",
  "code": "# Calculate node positions using topological sort..."
})
```

## Tool Access Recommendations Summary

### Security Levels by Agent Type
1. **Level 1 - Read Only**: Node-Verification (initial)
2. **Level 2 - Memory Access**: Most analytical agents
3. **Level 3 - File Modification**: Serializer, Logger, Issue-Tracker
4. **Level 4 - Code Execution**: Layout-*, Graph-Engineer, Validators
5. **Level 5 - Web Access**: Asset-Finder, Workflow-Researcher
6. **Level 6 - System Access**: Memory-Monitor, Logger
7. **Level 7 - Full Delegation**: Orchestrator only

### New Agent: Workflow-Researcher
**Purpose**: Learn from successful online workflows
**Key Tools**:
- `WebSearch` - Search workflow platforms
- `WebFetch` - Fetch workflow details
- `mcp__brave-search__search` - Multi-source search
- `mcp__memory__store` - Store patterns
- `mcp__code_execution` - Analyze structures

**Target Platforms**:
- Civitai (models & workflows)
- OpenArt (artistic workflows)
- GitHub (technical workflows)
- Reddit (community discussions)
- HuggingFace (model cards)

## Implementation Benefits

1. **Efficiency**: Agents only load needed tools
2. **Security**: Minimal access reduces risk
3. **Performance**: Faster agent initialization
4. **Clarity**: Clear agent responsibilities
5. **Learning**: Workflow-Researcher brings community insights

## Notes

1. The orchestrator (CLAUDE.md) coordinates all agent invocations
2. Agents can only access tools listed in their frontmatter
3. MCP tools are prefixed with `mcp__[server-name]__[action]`
4. Standard Claude Code tools don't require prefixes
5. Tool failures should be caught and reported to learning-agent
6. Total agents: 24 (23 original + workflow-researcher)
7. See AGENT_TOOL_ACCESS_MATRIX.md for complete mappings

---
*Updated: 2025-08-17*
*Version: 2.0*