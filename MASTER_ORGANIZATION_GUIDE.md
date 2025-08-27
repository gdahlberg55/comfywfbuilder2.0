# Master Organization Guide
## ComfyUI Agentic Workflow Generator v2.0

### Quick Start
This guide provides comprehensive organization standards for all project files, naming conventions, and maintenance procedures.

---

## 📁 Directory Structure

```
comfywfBuilder2.0/
├── 🔧 .claude/                    # Claude-specific configurations
│   ├── agents/                    # Agent definitions (23 agents)
│   └── settings.local.json        # Local Claude settings
│
├── 🐍 code_modules/               # Python algorithmic modules
│   ├── collision_detection.py     # AABB collision algorithms
│   ├── data_bus_router.py        # Orthogonal routing
│   ├── json_validator.py         # ComfyUI JSON validation
│   └── workflow_reorganizer.py   # Layout organization
│
├── 📚 docs/                       # Documentation hub
│   ├── audits/                   # System audits and reviews
│   ├── initialization/           # Startup procedures
│   ├── protocols/                # System protocols (ACTIVE)
│   ├── reports/                  # Generated reports
│   └── standards/                # Templates and standards
│       ├── WORKFLOW_LAYOUT_STANDARDS.md  # Layout specifications
│       ├── GOLD_STANDARD_ANALYSIS.md     # Validation criteria
│       └── COLOR_SCHEME.md               # Group color codes
│
├── 📦 output/                     # All generated outputs
│   ├── debug/                    # Debug logs by date
│   ├── errors/                   # Error reports by date
│   ├── logs/                     # Session logs
│   ├── memory/                   # MCP persistence
│   ├── reports/                  # Cleanup reports
│   ├── semantic_groups/          # Group analysis
│   └── workflows/                # Generated workflows
│       └── v{N}_{date}_{time}_{name}/
│
├── 🗑️ temp/                      # Temporary files (24hr TTL)
│   └── tests/                    # Test files
│
├── 📦 archive/                    # Archived files (30+ days)
│   ├── workflows/                # Old workflows
│   ├── code/                     # Deprecated scripts
│   ├── docs/                     # Old documentation
│   └── duplicates/               # Duplicate files
│
└── 📋 Root Files
    ├── CLAUDE.md                 # Prime Directive (NEVER DELETE)
    ├── MASTER_ORGANIZATION_GUIDE.md # This file
    ├── KNOWN_ISSUES_TRACKER.md   # Active issues
    └── cleanup_files.py          # Maintenance script
```

---

## 📝 Naming Conventions

### Workflows
```
Pattern: {project}_{version}_{timestamp}_{stage}.json
Example: flux_nsfw_perfect_spacing_20250127.json

Layout Requirements:
- Column-based organization within groups
- 200px+ vertical spacing between nodes (no overlaps)
- 400px+ horizontal spacing between columns
- Groups aligned by top edge in rows
- 20px grid snap for all positions
```

### Documentation
```
Pattern: {CATEGORY}_{TOPIC}_{VERSION}.md
Example: PROTOCOL_FILE_ORGANIZATION_V2.md
```

### Code Modules
```
Pattern: {function}_{component}.py
Example: collision_detection.py
```

### Temporary Files
```
Pattern: temp_{purpose}_{timestamp}.{ext}
Example: temp_validation_20250817_143022.json
```

---

## 🔄 Version Control

### Workflow Versions
```
Directory: v{major}_{YYYYMMDD}_{HHMMSS}_{descriptor}/
Contents:
  - workflow.json       # Main workflow
  - metadata.json       # Workflow metadata
  - report.md          # Generation report
  - preview.png        # Visual preview (if available)
```

### Timestamp Standard
```
Format: YYYYMMDD_HHMMSS
Example: 20250817_143022
```

---

## 🧹 Maintenance Procedures

### Daily Tasks
- [ ] Delete temp files older than 24 hours
- [ ] Check for naming convention violations
- [ ] Review error logs

### Weekly Tasks
- [ ] Run `python cleanup_files.py`
- [ ] Update KNOWN_ISSUES_TRACKER.md
- [ ] Archive completed workflows
- [ ] Validate workflow layouts against WORKFLOW_LAYOUT_STANDARDS.md

### Monthly Tasks
- [ ] Archive workflows older than 30 days
- [ ] Consolidate duplicate files
- [ ] Review and update protocols
- [ ] Generate compliance report

---

## 🚀 Quick Commands

### Run Cleanup
```bash
# Preview changes (dry run)
python cleanup_files.py --dry-run

# Execute cleanup
python cleanup_files.py

# Custom settings
python cleanup_files.py --temp-hours 48 --archive-days 60
```

### Check File Compliance
```bash
# Find non-compliant files
find . -name "*.json" | grep -v "_v[0-9]_[0-9]{8}_"

# List temp files
ls temp/temp_*

# Count workflows
find output/workflows -name "*.json" | wc -l
```

---

## ⚠️ Critical Files (NEVER DELETE)

1. **CLAUDE.md** - Prime Directive
2. **Active Protocol Files** (docs/protocols/)
3. **Agent Definitions** (.claude/agents/)
4. **Code Modules** (code_modules/)
5. **Gold Standard Templates** (docs/standards/)

---

## 📊 File Categories

### Production Files
- Location: `output/workflows/*/final.json`
- Retention: Permanent
- Backup: Required

### Development Files
- Location: `temp/`, root directory
- Retention: 24-48 hours
- Backup: Not required

### Archive Files
- Location: `archive/`
- Retention: 90 days
- Backup: Optional

---

## 🔍 Troubleshooting Locations

### Debug Output
```
Path: output/debug/{YYYYMMDD}/
File: debug_{component}_{timestamp}.log
```

### Error Reports
```
Path: output/errors/{YYYYMMDD}/
File: error_{component}_{code}_{timestamp}.json
```

### Session Logs
```
Path: output/logs/{YYYYMMDD}/
File: generation_{HHMMSS}.log
```

---

## 📈 Compliance Monitoring

### Check Compliance Status
```python
# In Python
from cleanup_files import FileOrganizer
organizer = FileOrganizer()
inventory = organizer.generate_inventory()
print(f"Total files: {inventory['total']}")
```

### Generate Report
```bash
python cleanup_files.py > compliance_report.txt
```

---

## 🔗 Related Documents

- [FILE_ORGANIZATION_PROTOCOL.md](docs/protocols/FILE_ORGANIZATION_PROTOCOL.md)
- [WORKFLOW_VERSIONING.md](docs/standards/WORKFLOW_VERSIONING.md)
- [KNOWN_ISSUES_TRACKER.md](KNOWN_ISSUES_TRACKER.md)
- [V2_ARCHITECTURAL_MANDATES.md](docs/protocols/V2_ARCHITECTURAL_MANDATES.md)

---

## 📋 Checklist for New Sessions

### Session Start
- [ ] Read CLAUDE.md
- [ ] Check KNOWN_ISSUES_TRACKER.md
- [ ] Run cleanup if needed
- [ ] Create session directory

### During Session
- [ ] Follow naming conventions
- [ ] Use proper directories
- [ ] Update issue tracker
- [ ] Save to versioned folders

### Session End
- [ ] Clean temp files
- [ ] Archive old files
- [ ] Update documentation
- [ ] Run compliance check

---

*Last Updated: 2025-08-17*
*Version: 2.0*
*Status: ACTIVE*

**Remember**: Consistency in organization leads to efficiency in execution!