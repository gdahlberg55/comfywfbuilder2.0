# Known Issues Tracker

## Purpose
Track known issues, their status, and workarounds for the ComfyUI Agentic Workflow Generator v2.0 system.

## Issue Format
```
### ISSUE-{NUMBER}: {Title}
**Status**: OPEN | IN_PROGRESS | FIXED | WONTFIX
**Severity**: CRITICAL | HIGH | MEDIUM | LOW
**Date Reported**: YYYY-MM-DD
**Date Resolved**: YYYY-MM-DD (if applicable)
**Affected Components**: List of affected components
**Description**: Brief description of the issue
**Workaround**: Temporary solution if available
**Resolution**: Final fix applied (if resolved)
```

---

## Active Issues

### ISSUE-001: MCP Tools Not Available in Claude Code
**Status**: OPEN
**Severity**: HIGH
**Date Reported**: 2025-08-14
**Affected Components**: MCP Integration, Desktop Control
**Description**: Windows-MCP, desktop-commander, and playwright servers not available in Claude Code environment
**Workaround**: Request users to manually take screenshots (Win+Shift+S) and paste into chat
**Resolution**: Pending - Use alternative approaches

### ISSUE-002: File Naming Inconsistencies
**Status**: FIXED
**Severity**: MEDIUM
**Date Reported**: 2025-08-16
**Date Resolved**: 2025-08-17
**Affected Components**: File Organization, Version Control
**Description**: Inconsistent file naming patterns across project causing confusion
**Workaround**: Manual renaming during sessions
**Resolution**: Implemented FILE_ORGANIZATION_PROTOCOL.md and cleanup_files.py script

### ISSUE-003: Workflow Spacing Too Narrow
**Status**: OPEN
**Severity**: MEDIUM
**Date Reported**: 2025-08-15
**Affected Components**: Layout-Strategist, Layout-Refiner
**Description**: Default 400px spacing appears cramped in complex workflows
**Workaround**: Multiply spacing by 2-3x for professional layouts (1000-2000px)
**Resolution**: Pending - Update default spacing in Layout-Strategist

### ISSUE-004: Groups Using Wrong Property Name
**Status**: OPEN
**Severity**: HIGH
**Date Reported**: 2025-08-15
**Affected Components**: Group-Coordinator, Workflow-Serializer
**Description**: Some workflows use "bounding_box" instead of correct "bounding" property
**Workaround**: Check and rename property during validation
**Resolution**: Pending - Update Group-Coordinator to use correct property

---

## Fixed Issues

### ISSUE-005: Duplicate Agent Creation
**Status**: FIXED
**Severity**: HIGH
**Date Reported**: 2025-08-14
**Date Resolved**: 2025-08-15
**Affected Components**: Agent Management
**Description**: System creating duplicate agents due to not checking existing files
**Workaround**: Search comprehensively before creating agents
**Resolution**: Added file existence checks in initialization protocol

### ISSUE-006: Wrong Workflow Selection
**Status**: FIXED
**Severity**: CRITICAL
**Date Reported**: 2025-08-16
**Date Resolved**: 2025-08-17
**Affected Components**: File Discovery, Intent Clarification
**Description**: System selecting wrong workflow file during organization
**Workaround**: Explicitly specify which workflow to use
**Resolution**: Added mandatory intent clarification step in startup protocol

---

## Monitoring

### Issues Under Investigation
- Collision detection algorithm performance on large workflows (>100 nodes)
- Memory usage optimization for MCP storage
- Data bus routing efficiency for complex connections

### Recurring Patterns
1. **File Organization**: Need consistent enforcement of naming conventions
2. **Visual Spacing**: Users consistently request more spacing in layouts
3. **MCP Limitations**: Multiple attempts to use unavailable MCP tools

---

## Improvement Suggestions

### HIGH Priority
1. Implement dynamic spacing calculation based on workflow complexity
2. Create automated validation for group property names
3. Add pre-flight check for MCP tool availability

### MEDIUM Priority
1. Enhance file discovery with fuzzy matching
2. Implement workflow complexity analyzer
3. Add visual preview generation capability

### LOW Priority
1. Create workflow diff tool for version comparison
2. Add workflow compression for storage optimization
3. Implement workflow template library

---

## Update Log
- 2025-08-17: Created initial tracker, added 6 issues
- 2025-08-17: Fixed ISSUE-002 (File Naming) and ISSUE-006 (Wrong Workflow)
- 2025-08-17: Added improvement suggestions and monitoring section

---

*Last Updated: 2025-08-17*
*Next Review: 2025-08-24*