# ComfyUI Agentic Workflow Generator v2.0

A sophisticated multi-agent system for generating and organizing ComfyUI workflows, built on Claude Code with enforced architectural patterns and Gold Standard aesthetics.

## 🚀 What's New in V2.0

### Core Improvements
- **Shared Context System (SCS)**: Centralized data layer using MCP Memory for seamless agent communication
- **Enforced Delegation**: Orchestrator strictly coordinates, never executes
- **Algorithmic Offloading**: Complex algorithms moved to Python modules via `mcp__code_execution`
- **Gold Standard Validation**: New Templating-Enforcer agent ensures aesthetic excellence
- **AABB Collision Detection**: Proper bounding box collision resolution (replacing V1.0's point-based system)
- **Data Bus Architecture**: Horizontal routing lanes for clean, organized workflows

## 📋 System Architecture

### Three-Layer Architecture

1. **Orchestration Layer** (`CLAUDE.md`)
   - Pure coordinator role
   - Manages agent pipeline execution
   - Handles SCS initialization and monitoring

2. **Agent Layer** (`.claude/agents/`)
   - 22 specialized agents (21 from V1.0 + Templating-Enforcer)
   - All agents use SCS protocol for communication
   - Strict input/output contracts via MCP Memory

3. **Algorithm Layer** (`code_modules/`)
   - `collision_detection.py`: AABB collision resolution
   - `data_bus_router.py`: Orthogonal routing implementation
   - `json_validator.py`: Format validation and auto-fixing

### Key V2.0 Principles

1. **Delegation is Mandatory**: Orchestrator never performs tasks
2. **SCS is Truth**: All data flows through Shared Context System
3. **Standardization is Enforced**: Gold Standard validation is non-negotiable
4. **Learning is Active**: All outcomes trigger the Learning-Agent

## 🛠️ Installation & Setup

### Prerequisites
- Claude Code environment
- MCP servers configured:
  - `mcp__memory__store/retrieve`
  - `mcp__code_execution`
  - `mcp__brave-search__search`
  - `mcp__web-fetch__fetch`

### Quick Start
1. Ensure you're in the V2.0 directory
2. The system will auto-initialize on first run
3. All agents and modules are pre-configured

## 📚 Core Components

### Agents (22 Total)

#### Workflow Generation Pipeline
- `parameter-extractor`: Parses natural language requests
- `asset-finder`: Searches for models, LoRAs, custom nodes
- `prompt-crafter`: Optimizes prompts with triggers
- `workflow-architect`: Designs workflow structure
- `node-curator`: Selects appropriate ComfyUI nodes
- `graph-engineer`: Wires node connections

#### Workflow Organization Pipeline
- `graph-analyzer`: Analyzes workflow topology
- `layout-strategist`: Plans optimal layout with data buses
- `reroute-engineer`: Implements orthogonal routing
- `layout-refiner`: Resolves collisions via AABB
- `group-coordinator`: Creates semantic groups
- `nomenclature-specialist`: Applies descriptive naming
- `workflow-validator`: Technical validation
- `templating-enforcer`: Gold Standard validation (NEW)
- `workflow-serializer`: JSON format conversion

#### Support Agents
- `learning-agent`: Pattern recognition and improvement
- `logger`: Session and audit logging
- `memory-monitor`: Resource usage tracking
- `node-verification`: Schema validation
- `visualizer`: Preview generation
- `workflow-chunker`: Large workflow handling

### Python Modules

#### collision_detection.py
- AABB collision detection with 80px minimum padding
- Grid snapping to 50px
- Iterative resolution with metrics tracking

#### data_bus_router.py
- Creates horizontal lanes at negative Y coordinates
- Generates reroute nodes for clean routing
- Ensures >95% orthogonal connections

#### json_validator.py
- Validates ComfyUI JSON structure
- Auto-fixes common V1.0 errors
- Ensures proper group colors from COLOR_SCHEME.md

## 🔄 Operational Modes

### Mode 1: Natural Language → Workflow
```
User Input → Parameter Extraction → Asset Discovery → 
Prompt Crafting → Architecture → Node Selection → 
Graph Engineering → [Proceed to Mode 2]
```

### Mode 2: JSON → Organized JSON
```
Graph Analysis → Layout Strategy → Data Bus Routing →
Collision Resolution → Grouping → Naming → 
Technical Validation → Gold Standard Check → 
Serialization → Output
```

## 📐 Gold Standard Compliance

The system enforces these aesthetic standards:

1. **Data Bus Architecture**: Horizontal lanes for major data types
2. **Orthogonal Routing**: >95% horizontal/vertical connections
3. **Zero Overlaps**: AABB collision detection ensures spacing
4. **Semantic Groups**: 5-15 logical groups with proper colors
5. **Grid Alignment**: All positions snap to 50px grid

## 🎨 15 Organizational Standards

1. Left-to-Right Flow
2. Vertical Stacking
3. Grid Spacing (50px grid, 80px minimum)
4. Grouping/Color Coding
5. Descriptive Titling
6. Minimize Crossings
7. Reroute/Data Bus Usage
8. Isolate Controls
9. Consistent Scaling
10. Collapse Utilities
11. No Overlaps
12. Add Notes
13. Handle Disconnected Components
14. Accessible Colors
15. Output Placement

## 📁 Directory Structure

```
comfywfBuilder2.0/
├── .claude/
│   └── agents/          # 22 specialized agents
├── code_modules/        # Python algorithmic modules
├── docs/
│   ├── protocols/       # SCS and integration protocols
│   └── standards/       # Color schemes, error guides
├── output/
│   ├── workflows/       # Versioned outputs
│   ├── logs/           # Session logs
│   └── memory/         # Persistent storage
├── CLAUDE.md           # Orchestrator directive
└── README.md           # This file
```

## 🚦 MCP Tool Usage

### ✅ Available in Claude Code
- `mcp__memory__store/retrieve`: SCS and long-term knowledge
- `mcp__code_execution`: Algorithmic module execution
- `mcp__brave-search__search`: Asset discovery
- `mcp__web-fetch__fetch`: Schema retrieval

### ❌ NOT Available
- Screenshot tools
- Desktop control
- Extension-based MCP servers

## 🔍 Troubleshooting

### Common Issues

1. **"Agent not found"**
   - Ensure all agents exist in `.claude/agents/`
   - Check agent names match exactly

2. **"SCS communication failure"**
   - Verify MCP memory server is running
   - Check session_id format

3. **"Module execution failed"**
   - Ensure Python modules have `main()` function
   - Check input/output format matches SCS schema

## 📈 Performance Metrics

V2.0 improvements over V1.0:
- **Zero overlaps** (vs frequent collisions)
- **>95% orthogonal routing** (vs spaghetti connections)
- **100% Gold Standard compliance** (vs inconsistent quality)
- **Deterministic outcomes** (vs variable results)

## 🤝 Contributing

When adding new agents or modules:
1. Follow SCS protocol for all communication
2. Use algorithmic offloading for complex logic
3. Ensure Gold Standard compliance
4. Update relevant documentation

## 📜 License

[Specify your license here]

## 🙏 Acknowledgments

Built on learnings from V1.0 audit and inspired by the CyberRealistic-SDXL Gold Standard workflow.