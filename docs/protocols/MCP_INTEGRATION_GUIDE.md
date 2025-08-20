# MCP Integration Guide V2.0 (Claude Code Environment)

Model Context Protocols (MCP) are the foundation of the V2.0 integration layer, enabling shared context, persistent learning, and optimized execution within Claude Code.

## MCP Utilization Strategy

### 1. `mcp__memory__store/retrieve` (Critical)  
This tool serves two distinct purposes:

#### A. Session Management (Shared Context System - SCS)  
* **Purpose:** Maintain the state of the current session.  
* **Implementation:** Managed via `AGENT_INTEGRATION_PROTOCOL_SCS.md`. Agents sequentially update the SCS object using the session ID key.

#### B. Long-Term Knowledge Base (LTKB)  
* **Purpose:** Store persistent knowledge.  
* **Implementation:** Managed primarily by the Learning-Agent. Uses persistent keys (e.g., `LTKB_PATTERN_ERROR_{ErrorSig}`).  
* **Data Stored:** Error patterns, successful layout configurations matching the Gold Standard, node schemas, user preferences.

### 2. `mcp__code_execution` (Critical for V2.0 Optimization)  
* **Purpose:** Algorithmic Offloading—moving complex algorithms from agent prompts into dedicated Python modules.  
* **Utilization:**  
  * Used by `Layout-Refiner` for AABB collision resolution (`collision_detection.py`).  
  * Used by `Reroute-Engineer` for Data Bus routing (`data_bus_router.py`).  
  * Used by `Workflow-Serializer` for validation (`json_validator.py`).  
* **Requirement:** Agents MUST use this tool for designated tasks, passing data from the SCS to the module (in `./code_modules/`) and integrating the results back into the SCS.

### 3. `mcp__web-fetch__fetch` / `google_search`  
* **Purpose:** Retrieve external data or discover assets.  
* **Utilization:** Invoked by the Node-Curator and Asset-Finder. Results should be cached in the LTKB.