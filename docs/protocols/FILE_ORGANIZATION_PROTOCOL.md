# File Organization Protocol v2.0

## Purpose
This protocol establishes standardized file naming conventions, directory structures, and version control practices for the ComfyUI Agentic Workflow Generator v2.0 system.

## Directory Structure

### Root Level Organization
```
comfywfBuilder2.0/
├── .claude/                 # Claude-specific configurations
│   ├── agents/              # Agent definitions
│   └── settings.local.json  # Local settings
├── code_modules/            # Python algorithmic modules
├── docs/                    # Documentation
│   ├── audits/             # System audits and reviews
│   ├── initialization/     # Initialization docs
│   ├── protocols/          # System protocols
│   ├── reports/            # Generated reports
│   └── standards/          # Standards and templates
├── output/                  # All generated outputs
│   ├── logs/               # Session logs
│   ├── memory/             # MCP memory persistence
│   ├── semantic_groups/    # Group analysis outputs
│   └── workflows/          # Generated workflows
├── temp/                    # Temporary working files
├── archive/                 # Archived/deprecated files
└── CLAUDE.md               # Prime directive
```

## Naming Conventions

### 1. Workflow Files
```
Pattern: {project}_{version}_{timestamp}_{stage}.json
Example: outfit_changer_v1_20250817_143022_final.json

Stages:
- raw        : Initial unorganized workflow
- analyzed   : After graph analysis
- layout     : After layout strategy
- routed     : After data bus routing
- refined    : After collision refinement
- grouped    : After semantic grouping
- named      : After nomenclature
- validated  : After validation
- final      : Production-ready
```

### 2. Protocol & Documentation Files
```
Pattern: {CATEGORY}_{TOPIC}_{VERSION}.md
Example: PROTOCOL_FILE_ORGANIZATION_V2.md

Categories:
- PROTOCOL   : System protocols
- STANDARD   : Standards and templates
- AUDIT      : Audit reports
- REPORT     : Generated reports
- GUIDE      : User guides
- TRACKER    : Issue/feature trackers
```

### 3. Code Modules
```
Pattern: {function}_{component}.py
Example: collision_detection.py, data_bus_router.py

Rules:
- Use snake_case
- Be descriptive but concise
- Include component type
```

### 4. Agent Files
```
Pattern: {agent-name}.md or {agent-name}/
Example: workflow-validator.md or workflow-validator/

Structure for v2.0 agents:
workflow-validator/
├── agent.json     # Agent configuration
├── prompt.md      # Agent prompt
└── README.md      # Agent documentation
```

### 5. Temporary Files
```
Pattern: temp_{purpose}_{timestamp}.{ext}
Example: temp_validation_20250817_143022.json

Rules:
- Always prefix with "temp_"
- Include timestamp
- Delete after session
```

### 6. Archive Files
```
Pattern: archive_{original_name}_{archive_date}.{ext}
Example: archive_workflow_v1_20250817.json

Rules:
- Move to archive/ directory
- Preserve original name
- Add archive date
```

## Version Control Protocol

### Workflow Versioning
```
v{major}_{date}_{time}_{descriptor}/
v1_20250817_143022_outfit_changer/
├── workflow.json          # Main workflow
├── metadata.json          # Workflow metadata
├── report.md             # Generation report
└── preview.png           # Visual preview
```

### Semantic Versioning for Code
```
Major.Minor.Patch
2.1.3

Major: Breaking changes
Minor: New features
Patch: Bug fixes
```

### Timestamp Format
```
Standard: YYYYMMDD_HHMMSS
Example:  20250817_143022

Use for:
- Directory names
- File timestamps
- Log entries
```

## File Cleanup Rules

### Session Files (Delete After Session)
- `temp_*.json`
- `*_request.json` (unless in active use)
- Duplicate validation reports
- Intermediate workflow states

### Archive Candidates (Move to archive/)
- Workflows older than 30 days
- Deprecated code modules
- Old protocol versions
- Failed generation attempts

### Permanent Files (Never Delete)
- CLAUDE.md (Prime Directive)
- Active protocol files
- Gold standard templates
- Agent definitions
- Code modules in use

## Troubleshooting File Locations

### Debug Files
```
Location: output/debug/{date}/
Pattern:  debug_{component}_{timestamp}.log
Example:  debug_serializer_20250817_143022.log
```

### Error Reports
```
Location: output/errors/{date}/
Pattern:  error_{component}_{error_code}_{timestamp}.json
Example:  error_validator_E001_20250817_143022.json
```

### Test Files
```
Location: temp/tests/
Pattern:  test_{feature}_{timestamp}.json
Example:  test_routing_20250817_143022.json
```

## Implementation Checklist

### Immediate Actions
- [ ] Create archive/ directory
- [ ] Create output/debug/ directory
- [ ] Create output/errors/ directory
- [ ] Move old files to archive/
- [ ] Rename inconsistent files
- [ ] Delete temporary files
- [ ] Update agent file structures

### Ongoing Maintenance
- [ ] Run cleanup script weekly
- [ ] Archive old workflows monthly
- [ ] Review and update protocols quarterly
- [ ] Maintain KNOWN_ISSUES_TRACKER.md

## Automated Cleanup Script

```python
# cleanup.py - Run weekly
import os
import shutil
from datetime import datetime, timedelta

def cleanup_temp_files():
    """Remove temporary files older than 24 hours"""
    temp_dir = "temp/"
    cutoff = datetime.now() - timedelta(hours=24)
    # Implementation here

def archive_old_workflows():
    """Archive workflows older than 30 days"""
    workflow_dir = "output/workflows/"
    archive_dir = "archive/workflows/"
    cutoff = datetime.now() - timedelta(days=30)
    # Implementation here

def consolidate_duplicates():
    """Identify and consolidate duplicate files"""
    # Implementation here

if __name__ == "__main__":
    cleanup_temp_files()
    archive_old_workflows()
    consolidate_duplicates()
```

## Compliance Monitoring

### Weekly Review
- Check for non-compliant file names
- Verify directory structure integrity
- Clean temporary files
- Update file inventory

### Monthly Audit
- Archive old workflows
- Review protocol compliance
- Update documentation
- Generate compliance report

## Quick Reference

### Valid File Patterns
✅ `outfit_changer_v1_20250817_143022_final.json`
✅ `PROTOCOL_FILE_ORGANIZATION_V2.md`
✅ `collision_detection.py`
✅ `temp_validation_20250817_143022.json`

### Invalid File Patterns
❌ `workflow.json` (no version/timestamp)
❌ `test.py` (too generic)
❌ `NewWorkflow.json` (wrong case, no version)
❌ `my-file.txt` (hyphens instead of underscores)

## Related Documents
- WORKFLOW_VERSIONING.md
- KNOWN_ISSUES_TRACKER.md
- V2_ARCHITECTURAL_MANDATES.md
- AGENT_INTEGRATION_PROTOCOL_SCS.md

---
*Last Updated: 2025-08-17*
*Version: 2.0*
*Status: ACTIVE*