# Agent Integration Protocol (AIP) and Shared Context System (SCS) Schema v2.0

This protocol defines the mechanism for inter-agent communication via the Shared Context System (SCS) in V2.0.

## 1. Overview

The SCS is the integration layer. It is a JSON object stored and managed via MCP Memory, identified by the Session ID.

## 2. Protocol Rules

1. **Initialization:** The Orchestrator initializes the SCS at session start: `mcp__memory__store(session_id, initial_scs)`.  
2. **Read Context:** Upon invocation, every agent MUST read the current SCS: `mcp__memory__retrieve(session_id)`.  
3. **Execution:** Perform the specialized task. If using `mcp__code_execution` (invoking modules from `./code_modules/`), the agent must pass the relevant SCS data to the module and await results.  
4. **Write Context:** Upon completion (or after integrating results from `code_execution`), the agent MUST write the updated SCS back: `mcp__memory__store(session_id, updated_scs)`.  
5. **Error Reporting:** If an error occurs, add details to `logging_metrics.errors_encountered` in the SCS and write it back before terminating.

## 3. Shared Context System (SCS) Schema

The SCS object must maintain the following structure:

```json
{
  "session_metadata": {
    "session_id": "vN_YYYYMMDD_HHMMSS",
    "status": "initializing|processing|success|failed",
    "current_stage": "Analyzer|LayoutStrategist|..."
  },
  "user_preferences": {
    "spacing_preference": "compact|standard|comfortable|extreme",
    "layout_style": "data_bus"
  },
  "workflow_state": {
    "current_graph": {
      "nodes": [...],
      "links": [...],
      "groups": [...]
    }
  },
  "analysis_results": {
    "graph_metrics": {
      "node_count": 0,
      "has_cycles": false,
      "complexity_score": 0.0,
      "memory_warning_level": "safe|warning|critical"
    },
    "semantic_analysis": {
      "workflow_type": "image_generation|video|utility",
      "execution_order": {}
    }
  },
  "layout_parameters": {
    "calculated_spacing": {
      "horizontal": 400,
      "vertical": 150,
      "group_padding": 80
    },
    "data_bus_lanes": {
      "MODEL": {"y_pos": 0, "utilized": false},
      "CLIP": {"y_pos": 0, "utilized": false},
      "VAE": {"y_pos": 0, "utilized": false},
      "IMAGE_MAIN": {"y_pos": 0, "utilized": false},
      "CONTEXT_PIPE": {"y_pos": 0, "utilized": false}
    },
    "node_dimensions_cache": {}
  },
  "validation_reports": {
    "technical": {"passed": false, "errors": []},
    "templating": {"passed": false, "violations": []}
  },
  "logging_metrics": {
    "performance_by_agent": {},
    "errors_encountered": []
  }
}
```