# Claude Code Agent Configuration

## Project: ComfyUI Workflow Builder v2.0

This configuration file registers all agents for the ComfyUI Workflow Builder v2.0 system.

## Agents

### Orchestration
- id: orchestrator
  path: .claude/agents/orchestrator.md
  autoload: true
  description: Master coordinator managing all sub-agents for ComfyUI workflow generation and organization

### Workflow Generation Pipeline (Mode 1)
- id: parameter-extractor
  path: .claude/agents/parameter-extractor.md
  autoload: true
  description: Extracts workflow parameters from natural language descriptions

- id: asset-finder
  path: .claude/agents/asset-finder.md
  autoload: true
  description: Searches for models, LoRAs, custom nodes

- id: prompt-crafter
  path: .claude/agents/prompt-crafter.md
  autoload: true
  description: Refines and optimizes prompts for ComfyUI workflows

- id: workflow-architect
  path: .claude/agents/workflow-architect.md
  autoload: true
  description: Designs high-level workflow architecture and structure

- id: node-curator
  path: .claude/agents/node-curator.md
  autoload: true
  description: Selects, configures, and optimizes ComfyUI nodes for specific workflow requirements

- id: graph-engineer
  path: .claude/agents/graph-engineer.md
  autoload: true
  description: Builds and optimizes the workflow graph structure

### Workflow Organization Pipeline (Mode 2)
- id: graph-analyzer
  path: .claude/agents/graph-analyzer.md
  autoload: true
  description: Analyzes workflow graphs to identify issues, optimize performance, and ensure correctness

- id: layout-strategist
  path: .claude/agents/layout-strategist.md
  autoload: true
  description: Plans and optimizes the visual layout of workflow nodes with SCS integration and dynamic spacing calculation

- id: reroute-engineer
  path: .claude/agents/reroute-engineer.md
  autoload: true
  description: Manages connection routing and reroute nodes using data bus routing algorithms via SCS and Python modules

- id: layout-refiner
  path: .claude/agents/layout-refiner.md
  autoload: true
  description: Refines and polishes workflow layouts using collision detection algorithms via SCS and Python modules

- id: group-coordinator
  path: .claude/agents/group-coordinator.md
  autoload: true
  description: Organizes nodes into logical groups for better workflow structure

- id: nomenclature-specialist
  path: .claude/agents/nomenclature-specialist.md
  autoload: true
  description: Standardizes naming conventions for nodes, groups, and workflows

- id: workflow-serializer
  path: .claude/agents/workflow-serializer.md
  autoload: true
  description: Converts workflow structures into valid ComfyUI JSON format

- id: workflow-validator
  path: .claude/agents/workflow-validator.md
  autoload: true
  description: Validates workflow structure and ensures correctness

### Support Agents
- id: node-verification
  path: .claude/agents/node-verification.md
  autoload: true
  description: Verifies node availability, compatibility, and correct implementation in workflows

- id: memory-monitor
  path: .claude/agents/memory-monitor.md
  autoload: true
  description: Tracks and optimizes workflow memory usage and performance

- id: workflow-chunker
  path: .claude/agents/workflow-chunker.md
  autoload: true
  description: Splits large workflows into manageable chunks for processing

- id: visualizer
  path: .claude/agents/visualizer.md
  autoload: true
  description: Creates visual representations and documentation of ComfyUI workflows

- id: learning-agent
  path: .claude/agents/learning-agent.md
  autoload: true
  description: Learns from workflow patterns and provides optimization insights

- id: logger
  path: .claude/agents/logger.md
  autoload: true
  description: Manages logging and generation history

- id: templating-enforcer
  path: .claude/agents/templating-enforcer.md
  autoload: true
  description: Ensures workflows follow standardized templates and patterns

## Integration Notes

These agents integrate with:
- **SCS (Shared Context System)**: Via mcp__memory__retrieve/store
- **Python Modules**: Via mcp__code_execution
  - collision_detection.py (layout-refiner)
  - data_bus_router.py (reroute-engineer)
  - Additional modules as required

## Tool Requirements

Valid tools that agents can use:
- Basic Claude Code tools: Read, Write, Edit, MultiEdit, Bash, Glob, Grep, LS
- MCP tools (when configured): mcp__memory__retrieve, mcp__memory__store, mcp__code_execution
- Other specialized MCP tools: mcp__web-fetch__fetch, mcp__brave-search__search, mcp__playwright-mcp-server__screenshot, mcp__playwright-mcp-server__navigate

## Agent Colors (for visualization)
- Orchestrator: #9C27B0 (Purple)
- Workflow Generation: #2196F3 (Blue)
- Workflow Organization: #4CAF50 (Green)
- Support Agents: #FF9800 (Orange)