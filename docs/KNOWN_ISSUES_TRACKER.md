# Known Issues Tracker

This document maintains a running list of issues encountered during workflow generation and organization. Check this document at the beginning, middle, and end of each session.

## Issue Format
```
[DATE] - [STATUS] - [CATEGORY] - Issue Description
Resolution: Steps taken or workaround found
```

## Status Codes
- 🔴 OPEN - Issue unresolved
- 🟡 WORKAROUND - Temporary solution in place
- 🟢 FIXED - Issue resolved permanently

---

## Active Issues

### 🔴 OPEN - MCP Memory Access in Claude Code
**Date**: 2025-08-14
**Category**: Tool Integration
**Issue**: Cannot directly access MCP memory tools (mcp__memory__store/retrieve) from within agent execution context
**Symptoms**: 
- Commands like `mcp --name memory retrieve` fail with "command not found"
- NPX attempts to use @modelcontextprotocol/cli fail with 404 error
**Impact**: Agents cannot share data through the Shared Context System as designed
**Attempted Solutions**:
1. Direct mcp command - Failed
2. NPX with @modelcontextprotocol/cli - Failed (package not found)
3. Various command formats - All failed
**Workaround**: Store intermediate results as JSON files in versioned output folders
**Next Steps**: Need to investigate proper MCP tool invocation from agent context

### 🟡 WORKAROUND - Agent Communication Without SCS
**Date**: 2025-08-14  
**Category**: Architecture
**Issue**: Shared Context System (SCS) via MCP memory not accessible to agents
**Impact**: Agents cannot share workflow state as designed in V2.0 architecture
**Workaround**: Using file-based communication:
- Store agent outputs in `/output/workflows/v{N}_{YYYYMMDD}_{HHMMSS}/`
- Each agent reads previous agent's output file
- Maintain naming convention for traceability
**Resolution**: Functional but not as elegant as intended SCS design

### 🔴 OPEN - Windows MCP Tools Not Available
**Date**: 2025-08-14
**Category**: Tool Limitations
**Issue**: Windows-specific MCP tools (desktop-commander, Windows-MCP) not available in Claude Code
**Impact**: Cannot take automated screenshots or control desktop
**Workaround**: Request users to manually take screenshots (Win+Shift+S) and share
**Resolution**: This is a permanent limitation - update documentation

---

## Resolved Issues

### 🟢 FIXED - Duplicate Agent Creation
**Date**: 2025-08-13
**Category**: File Management
**Issue**: Agents being recreated when they already exist
**Resolution**: Added comprehensive search before creation in CLAUDE.md
**Fix Applied**: CLAUDE.md updated with "File Management Rules" section

### 🟢 FIXED - Workflow Version Confusion
**Date**: 2025-08-13
**Category**: Workflow Management  
**Issue**: Creating simple workflows when complex versions exist
**Resolution**: Added mandatory file discovery step in startup protocol
**Fix Applied**: CLAUDE.md updated with file discovery requirements

---

## Maintenance Log
- 2025-08-14 15:30 - Document created with initial issues
- [Add future updates here]

## Review Schedule
- **Beginning of session**: Check all OPEN issues
- **During session**: Update if issues encountered
- **End of session**: Review and update statuses
- **After fixes**: Update status to FIXED with resolution details