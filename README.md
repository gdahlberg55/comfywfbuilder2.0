# ComfyUI Workflow Builder v2.0

An agentic system for generating, organizing, and optimizing ComfyUI workflows using Claude AI and specialized sub-agents.

## 🎯 Overview

ComfyUI Workflow Builder v2.0 is a sophisticated orchestration system that transforms natural language descriptions into professionally organized ComfyUI workflows. It employs 24 specialized agents working in concert through a Shared Context System (SCS) to handle workflow generation, layout optimization, and visual organization.

## ✨ Key Features

- **Natural Language to Workflow**: Describe what you want, get a production-ready ComfyUI workflow
- **Professional Layout**: Automatic organization with proper spacing, grouping, and routing
- **Multi-Pass Rendering Support**: Built-in support for base generation, hi-res fix, and upscaling passes
- **Advanced Node Support**: Full compatibility with rgthree, Impact, Ultimate SD Upscale, and other popular node suites
- **Visual Organization**: Semantic grouping, color coding, and descriptive naming
- **Data Bus Routing**: Efficient connection management using horizontal routing lanes
- **Collision Detection**: AABB-based layout refinement to prevent node overlaps

## 🏗️ Architecture

### Core System
- **Orchestrator**: Master coordinator managing all sub-agents
- **Shared Context System (SCS)**: MCP Memory-based communication between agents
- **Python Modules**: Algorithmic components for complex operations

### Agent Pipelines

#### Mode 1: Workflow Generation (NL → JSON)
1. **Parameter Extractor** - Extracts parameters from user requests
2. **Asset Finder** - Searches for models, LoRAs, custom nodes
3. **Prompt Crafter** - Optimizes prompts with triggers
4. **Workflow Architect** - Designs workflow structure
5. **Node Curator** - Selects appropriate ComfyUI nodes
6. **Graph Engineer** - Wires node connections

#### Mode 2: Workflow Organization (JSON → Organized JSON)
1. **Graph Analyzer** - Analyzes workflow topology
2. **Layout Strategist** - Plans optimal layout with data buses
3. **Reroute Engineer** - Implements orthogonal routing
4. **Layout Refiner** - Resolves collisions via AABB
5. **Group Coordinator** - Creates semantic groups
6. **Nomenclature Specialist** - Applies descriptive naming
7. **Workflow Validator** - Technical validation
8. **Workflow Serializer** - JSON format conversion

### Support Agents
- Node Verification, Memory Monitor, Learning Agent, Logger, Visualizer, and more

## 📋 Requirements

### Claude Code Environment
- Claude Code CLI with MCP support
- Configured MCP servers:
  - `mcp__memory__*` - Memory management
  - `mcp__filesystem__*` - File operations
  - `mcp__brave-search__*` - Web search (optional)

### Python Dependencies
```bash
pip install numpy
```

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/gdahlberg55/comfywfbuilder2.0.git
cd comfywfbuilder2.0
```

2. **Set up Claude Code**
- Ensure Claude Code is installed and configured
- MCP memory server should be available

3. **Initialize the system**
```bash
claude chat
```
Then in Claude:
```
Initialize the ComfyUI Workflow Builder v2.0 system
```

4. **Generate a workflow**
```
Create a Flux workflow with LoRA support and upscaling
```

## 📁 Project Structure

```
comfywfbuilder2.0/
├── .claude/               # Agent definitions
│   └── agents/           # 24 specialized agents
├── code_modules/         # Python algorithmic modules
│   ├── collision_detection.py
│   ├── data_bus_router.py
│   └── workflow_reorganizer.py
├── docs/                 # Documentation
│   ├── protocols/       # System protocols
│   ├── standards/       # Workflow standards
│   └── initialization/  # System setup docs
├── examples/            # Example workflows
└── CLAUDE.md           # Primary directive
```

## 🎨 Workflow Standards

The system enforces professional standards including:
- Left-to-right flow (inputs → outputs)
- 20px grid snapping
- Semantic grouping with color coding
- Descriptive node naming
- Horizontal data bus routing
- Proper group header clearance (35px+)
- No node overlaps

## 📚 Documentation

- [CLAUDE.md](CLAUDE.md) - Primary system directive
- [MASTER_ORGANIZATION_GUIDE.md](MASTER_ORGANIZATION_GUIDE.md) - File organization reference
- [docs/protocols/](docs/protocols/) - System protocols and integration guides
- [docs/standards/](docs/standards/) - Workflow standards and templates

## 🤝 Contributing

Contributions are welcome! Please read the documentation thoroughly before submitting PRs.

### Development Guidelines
1. Follow the established agent architecture
2. Maintain SCS communication protocols
3. Test with various workflow types
4. Document new features thoroughly

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- ComfyUI community for the amazing framework
- rgthree for the powerful node suite
- All custom node developers whose work this system supports

## ⚠️ Note

This is an experimental system under active development. While it produces functional workflows, always review and test generated workflows before production use.

## 📧 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

**Version**: 2.0.0  
**Status**: Alpha  
**Last Updated**: January 2025