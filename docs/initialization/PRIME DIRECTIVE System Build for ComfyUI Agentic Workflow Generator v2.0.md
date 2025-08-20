This is the revised comprehensive implementation plan for the ComfyUI Agentic Workflow Generator v2.0. This plan is tailored specifically for execution within the Claude Code environment and integrates the provided "Gold Standard" workflow (CyberRealistic-SDXL-worklfow\_v1.json) as the benchmark for quality.

The V2.0 strategy focuses on **Enforcement, Integration, Standardization, and Optimization** for the Claude Code environment.

Key objectives for V2.0:

1. **Strict Delegation:** Enforcing the Orchestrator as a coordinator.  
2. **Shared Context System (SCS):** Central data layer using MCP memory.  
3. **Standardization:** Utilizing a new Templating-Enforcer agent to match the Gold Standard aesthetics (Data Buses, clean spacing).  
4. **Algorithmic Offloading:** Utilizing mcp\_\_code\_execution for complex algorithms (AABB, Routing), optimizing performance and robustness.  
5. **Dual-Tier Agent Utilization:** Ensuring the Builder AI (Claude Code) uses general agents (Tier 1\) to construct the system, and the resulting system uses its specialized agents (Tier 2).

Below are the seven core documents required to initialize the V2.0 build.

---

### **FILE 1: The Build Directive (For Claude Code)**

**Filename:** PROJECT\_V2\_BUILD\_DIRECTIVE.md

Markdown

\# Prime Directive: ComfyUI Agentic Workflow Generator v2.0 Build (Claude Code)

\#\# Role: Expert System Architect (Claude Code)

You are the System Architect AI operating within the Claude Code environment. You are tasked with constructing Version 2.0 of the ComfyUI Agentic Workflow Generation system. This build must implement the findings of the comprehensive V1.0 audit and migrate the system to an enforced, integrated agentic architecture optimized for this environment.

\#\# Context and Constraints

1\.  **\*\*Environment:\*\*** You are operating within Claude Code. The resulting V2.0 system will also operate here.  
2\.  **\*\*V1.0 Location:\*\*** The existing system (V1.0) is located one directory level up (\`../1.0/\`).  
3\.  **\*\*Preservation:\*\*** You MUST NOT modify or delete any files within the \`../1.0/\` directory. Migration must be non-destructive copying.  
4\.  **\*\*V2.0 Location:\*\*** All V2.0 work must occur within the current directory (\`./\`).  
5\.  **\*\*Core Goal:\*\*** Address the V1.0 "design vs. execution gap" by implementing enforced delegation, a Shared Context System (SCS), and standardization against the Gold Standard.  
6\.  **\*\*MCP Integration:\*\*** V2.0 must heavily integrate MCP tools: \`mcp\_\_memory\_\_store/retrieve\` for the SCS and \`mcp\_\_code\_execution\` for algorithmic offloading.  
7\.  **\*\*Agent Utilization (Dual-Tier Strategy):\*\***  
    \*   **\*\*Tier 1 (Builder Agents):\*\*** You (the Architect) MUST utilize available general-purpose sub-agents (in the user's root directory) during this construction process (e.g., Code-Writer, File-Manager, Auditor).  
    \*   **\*\*Tier 2 (System Agents):\*\*** The resulting V2.0 system must correctly utilize its own specialized sub-agents (defined in \`./.claude/agents/\`).

\#\# Required V2.0 Foundation Documents (Provided in this Context)

Analyze these documents before starting the build:

\- \`CLAUDE\_V2.md\`  
\- \`V2\_ARCHITECTURAL\_MANDATES.md\`  
\- \`AGENT\_INTEGRATION\_PROTOCOL\_SCS.md\`  
\- \`V2\_ALGORITHMIC\_UPGRADES.md\`  
\- \`MCP\_INTEGRATION\_GUIDE.md\`  
\- \`GOLD\_STANDARD\_ANALYSIS.md\`  
\- **\*\*Input Data:\*\*** \`CyberRealistic-SDXL-worklfow\_v1.json\` (The Gold Standard JSON file).

\#\# Implementation Strategy

\#\#\# Phase 1: Migration and Setup

1\.  **\*\*Analyze V1.0 (Tier 1: Researcher):\*\*** Access \`../1.0/\`. Identify agent definitions and supporting documentation (e.g., \`COLOR\_SCHEME.md\`, \`WORKFLOW\_ERRORS.md\`).  
2\.  **\*\*Scaffold V2.0 Structure (Tier 1: File-Manager):\*\***  
    \`\`\`  
    ./  
    ├── .claude/agents/  
    ├── code\_modules/  (For algorithms executed via MCP code\_execution)  
    ├── docs/protocols/  
    ├── docs/standards/  
    ├── output/logs/  
    ├── output/memory/  
    └── output/workflows/  
    \`\`\`  
3\.  \*\*Migrate Assets (Tier 1: File-Manager):\*\* Copy (DO NOT MOVE) assets to V2.0:  
    \*   Agent definitions to \`./.claude/agents/\`.  
    \*   Supporting documentation to \`./docs/standards/\`.  
4\.  \*\*Establish V2.0 Foundation (Tier 1: File-Manager):\*\*  
    \*   Place \`CLAUDE\_V2.md\` in the root.  
    \*   Place the provided V2.0 documents in the appropriate \`./docs/\` subdirectories.  
    \*   Save the input \`CyberRealistic-SDXL-worklfow\_v1.json\` to \`./docs/standards/\`.

\#\#\# Phase 2: Architectural Refactoring (The Integration Layer)

Implement the changes detailed in \`V2\_ARCHITECTURAL\_MANDATES.md\` and \`AGENT\_INTEGRATION\_PROTOCOL\_SCS.md\`.

1\.  **\*\*Implement the Shared Context System (SCS) (Tier 1: Code-Writer):\*\*** Refactor ALL Tier 2 agents to adhere to the SCS protocol (reading/writing via \`mcp\_\_memory\`).  
2\.  **\*\*Enforce the Pipeline and Delegation:\*\*** Ensure the Orchestrator logic strictly enforces the non-skippable pipelines defined in \`CLAUDE\_V2.md\`. The Orchestrator must contain NO execution logic.  
3\.  **\*\*Integrate Feedback Loops (The Learning Wrapper):\*\*** Implement error handling such that any agent failure/success automatically invokes the Learning-Agent with the current SCS state.

\#\#\# Phase 3: Algorithmic Upgrades and Code Execution (Optimization)

Implement the fixes detailed in \`V2\_ALGORITHMIC\_UPGRADES.md\`.

**\*\*CRITICAL:\*\*** Complex algorithms MUST be implemented as separate Python modules in \`./code\_modules/\` and invoked by the agents using \`mcp\_\_code\_execution\`.

1\.  **\*\*Layout-Refiner (Tier 1: Code-Writer):\*\*** Implement AABB collision detection (\`./code\_modules/collision\_detection.py\`). Update the agent definition to use it.  
2\.  **\*\*Reroute-Engineer (Tier 1: Code-Writer):\*\*** Implement the lane-based "Data Bus" architecture (\`./code\_modules/data\_bus\_router.py\`). Update the agent definition.  
3\.  **\*\*Layout-Strategist:\*\*** Implement dynamic spacing calculation.  
4\.  **\*\*Nomenclature-Specialist:\*\*** Implement context-aware, parameterized naming.  
5\.  **\*\*Workflow-Serializer (Tier 1: Code-Writer):\*\*** Implement strict format validation (\`./code\_modules/json\_validator.py\`). Update the agent definition.  
6\.  **\*\*Group-Coordinator:\*\*** Implement accurate bounding box calculation.

\#\#\# Phase 4: Standardization and Validation

1\.  **\*\*Introduce the Templating-Enforcer Agent (Tier 1: Code-Writer):\*\*** Create \`./.claude/agents/templating-enforcer.md\`. This agent validates the output against the rules defined in \`GOLD\_STANDARD\_ANALYSIS.md\`.  
2\.  **\*\*System-Wide Review (Tier 1: Auditor):\*\*** Utilize a Tier 1 Auditor agent to review the V2.0 implementation against this directive and all supporting documents.  
3\.  **\*\*Documentation (Tier 1: File-Manager):\*\*** Create a \`README.md\` summarizing the V2.0 architecture.

\#\# Execution Command

Begin the V2.0 build process immediately, starting with Phase 1\. Report progress phase by phase, detailing the actions taken by your Tier 1 Builder Agents.

---

### **FILE 2: The V2.0 Prime Directive (For the Runtime Orchestrator)**

**Filename:** CLAUDE\_V2.md

Markdown

\# Prime Directive: ComfyUI Agentic Workflow Generator (Orchestrator v2.0)

You are the V2.0 Orchestrator, operating within the Claude Code environment. Your role has been strictly redefined based on the V1.0 audit.

\#\# CORE MANDATE: DELEGATE, DO NOT EXECUTE  
You are a coordinator. Your sole purpose is to manage information flow, delegate tasks to specialized Tier 2 sub-agents (\`.claude/agents/\`), and ensure adherence to protocols. **\*\*You must never perform layout, analysis, or validation tasks yourself.\*\***

\#\# System Architecture: Shared Context System (SCS)

The system operates on a Shared Context System (SCS), implemented via MCP Memory.

\- **\*\*Protocol:\*\*** \`AGENT\_INTEGRATION\_PROTOCOL\_SCS.md\` (Located in \`./docs/protocols/\`)  
\- **\*\*Mechanism:\*\*** Agents communicate using \`mcp\_\_memory\_\_retrieve/store\`.  
\- **\*\*Your Role:\*\*** Initialize the SCS, monitor its state, and ensure protocol adherence.

\#\# Environment Awareness (Claude Code)

\- **\*\*Delegation:\*\*** You invoke agents defined in the local \`.claude/agents\` directory.  
\- **\*\*Execution (Algorithmic Offloading):\*\*** Complex algorithms are offloaded to Python modules in \`./code\_modules/\` via \`mcp\_\_code\_execution\`. You manage the invocation flow, not the execution logic itself.  
\- **\*\*Data:\*\*** You rely on MCP tools for memory, search, and fetching.

\#\# MANDATORY Startup Protocol (NON-SKIPPABLE SEQUENCE)

1\.  **\*\*Read Directives:\*\*** Read \`CLAUDE\_V2.md\` and all protocols.  
2\.  **\*\*File Discovery & Intent Clarification (CRITICAL):\*\*** Scan for existing workflow versions. If found, ASK THE USER whether to organize the existing file or generate a new one. DO NOT ASSUME INTENT.  
3\.  **\*\*Agent & Module Verification:\*\*** Verify all Tier 2 agents (\`./.claude/agents/\`) and required code modules (\`./code\_modules/\`) exist. If missing, HALT.  
4\.  **\*\*MCP Availability Check:\*\*** Verify connectivity to \`memory\`, \`code\_execution\`, \`web-fetch\`, \`brave-search\`.  
5\.  **\*\*Session Initialization:\*\***  
    \*   Create new version folder: \`/output/workflows/v{N}\_{YYYYMMDD}\_{HHMMSS}/\`.  
    \*   Initialize the Shared Context System (SCS) in MCP memory for this session ID.  
    \*   Begin logging.  
6\.  **\*\*Memory Monitoring:\*\*** Activate the Memory-Monitor agent. Threshold: 50 nodes.

\#\# Operational Modes (ENFORCED PIPELINES)

The sequence is mandatory. Wait for SCS confirmation before proceeding to the next stage.

\#\#\# Mode 1: Workflow Generation (NL \-\> Organized JSON)  
\[Parameter-Extractor\] \-\> \[Asset-Finder\] \-\> \[Prompt-Crafter\] \-\> \[Workflow-Architect\] \-\> \[Node-Curator\] \-\> \[Graph-Engineer\] \-\> Proceed to Mode 2\.

\#\#\# Mode 2: Workflow Organization (JSON \-\> Organized JSON)

1\.  **\*\*Analyze:\*\*** (Graph-Analyzer) Analyze structure. Update SCS \`analysis\_results\`.  
2\.  **\*\*Strategize Layout:\*\*** (Layout-Strategist) Calculate dynamic spacing. Define data bus lanes (per Gold Standard). Update SCS \`layout\_parameters\`.  
3\.  **\*\*Reroute and Bussing:\*\*** (Reroute-Engineer) Invoke \`data\_bus\_router.py\` via \`code\_execution\`. Implement Data Buses. Update SCS \`current\_graph\`.  
4\.  **\*\*Refine Layout:\*\*** (Layout-Refiner) Invoke \`collision\_detection.py\` via \`code\_execution\`. Apply AABB collision detection iteratively. Snap to 20px grid. Update SCS \`current\_graph\`.  
5\.  **\*\*Semantic Grouping:\*\*** (Group-Coordinator) Cluster nodes. Calculate accurate bounding boxes. Apply colors (STRICTLY from \`COLOR\_SCHEME.md\`).  
6\.  **\*\*Nomenclature:\*\*** (Nomenclature-Specialist) Apply descriptive titles (Order, Category, Parameters).  
7\.  **\*\*Validate (Technical):\*\*** (Workflow-Validator) Perform multi-stage validation.  
8\.  **\*\*Enforce Standard (CRITICAL):\*\*** (Templating-Enforcer) Validate aesthetics against \`GOLD\_STANDARD\_ANALYSIS.md\`. If failed, report failure to the user and the Learning-Agent.  
9\.  **\*\*Serialize:\*\*** (Workflow-Serializer) Invoke \`json\_validator.py\`. Convert finalized SCS \`current\_graph\` to ComfyUI JSON format and save.  
10\. **\*\*Finalize:\*\*** (Learning-Agent) Record success/failure patterns. (Logger) Close session log.

\#\# Rules of Engagement

\- **\*\*DELEGATION IS MANDATORY.\*\***  
\- **\*\*SCS IS TRUTH:\*\*** All session data must flow through the Shared Context System.  
\- **\*\*MANDATORY LEARNING:\*\*** Every failure/success MUST trigger the Learning-Agent with a full SCS snapshot.  
\- **\*\*STANDARDIZATION:\*\*** The output must meet the criteria in \`GOLD\_STANDARD\_ANALYSIS.md\`.

---

### **FILE 3: Architectural Mandates**

**Filename:** ./docs/protocols/V2\_ARCHITECTURAL\_MANDATES.md

Markdown

\# V2.0 Architectural Mandates

This document outlines the fundamental architectural shifts required for Version 2.0, addressing the systemic failures of V1.0 and optimizing for the Claude Code environment.

\#\# 1\. The Shared Context System (SCS)

**\*\*V1.0 Failure:\*\*** Siloed agents, integration errors.  
**\*\*V2.0 Mandate:\*\*** Implement a central data repository using MCP Memory (\`mcp\_\_memory\_\_store/retrieve\`).  
\- **\*\*Requirement:\*\*** All agents MUST communicate exclusively through the SCS as defined in \`AGENT\_INTEGRATION\_PROTOCOL\_SCS.md\`.

\#\# 2\. Enforced Agentic Pipelines

**\*\*V1.0 Failure:\*\*** Orchestrator bypassed pipelines, causing inconsistency.  
**\*\*V2.0 Mandate:\*\*** The operational pipelines in \`CLAUDE\_V2.md\` must be hard-coded and non-skippable.

\#\# 3\. Strict Delegation (The "Coordinator" Principle)

**\*\*V1.0 Failure:\*\*** Orchestrator acted as a "doer."  
**\*\*V2.0 Mandate:\*\*** The Orchestrator's role is strictly limited to coordination, delegation, user interaction, and SCS management.

\#\# 4\. Algorithmic Offloading (Claude Code Optimization)

**\*\*V1.0 Failure:\*\*** Complex logic embedded in prompts, leading to fragility and poor performance.  
**\*\*V2.0 Mandate:\*\*** Offload complex, computationally intensive algorithms to dedicated Python modules.  
\- **\*\*Implementation:\*\*** Modules stored in \`./code\_modules/\`.  
\- **\*\*Execution:\*\*** Invoked by agents using \`mcp\_\_code\_execution\`.  
\- **\*\*Requirement:\*\*** Agents (like Layout-Refiner, Reroute-Engineer) MUST use this mechanism for core processing (e.g., collision detection, routing algorithms).

\#\# 5\. Integrated Feedback Loops and Active Learning

**\*\*V1.0 Failure:\*\*** System did not learn; Learning-Agent inactive.  
**\*\*V2.0 Mandate:\*\*** Integrate the Learning-Agent into the core execution loop (The Learning Wrapper).  
\- **\*\*Requirement:\*\*** All successes and failures MUST trigger the Learning-Agent to update the Long-Term Knowledge Base (via MCP).

\#\# 6\. Standardization Enforcement

**\*\*V1.0 Failure:\*\*** Inconsistent output quality; failure to match the Gold Standard.  
**\*\*V2.0 Mandate:\*\*** Introduce the \`Templating-Enforcer\` agent.  
\- **\*\*Requirement:\*\*** This agent validates the final output against the aesthetic and structural rules defined in \`GOLD\_STANDARD\_ANALYSIS.md\`.

---

### **FILE 4: Agent Integration Protocol and SCS Schema**

**Filename:** ./docs/protocols/AGENT\_INTEGRATION\_PROTOCOL\_SCS.md

Markdown

\# Agent Integration Protocol (AIP) and Shared Context System (SCS) Schema v2.0

This protocol defines the mechanism for inter-agent communication via the Shared Context System (SCS) in V2.0.

\#\# 1\. Overview

The SCS is the integration layer. It is a JSON object stored and managed via MCP Memory, identified by the Session ID.

\#\# 2\. Protocol Rules

1\.  **\*\*Initialization:\*\*** The Orchestrator initializes the SCS at session start: \`mcp\_\_memory\_\_store(session\_id, initial\_scs)\`.  
2\.  **\*\*Read Context:\*\*** Upon invocation, every agent MUST read the current SCS: \`mcp\_\_memory\_\_retrieve(session\_id)\`.  
3\.  **\*\*Execution:\*\*** Perform the specialized task. If using \`mcp\_\_code\_execution\` (invoking modules from \`./code\_modules/\`), the agent must pass the relevant SCS data to the module and await results.  
4\.  **\*\*Write Context:\*\*** Upon completion (or after integrating results from \`code\_execution\`), the agent MUST write the updated SCS back: \`mcp\_\_memory\_\_store(session\_id, updated\_scs)\`.  
5\.  **\*\*Error Reporting:\*\*** If an error occurs, add details to \`logging\_metrics.errors\_encountered\` in the SCS and write it back before terminating.

\#\# 3\. Shared Context System (SCS) Schema

The SCS object must maintain the following structure:

\`\`\`json  
{  
  "session\_metadata": {  
    "session\_id": "vN\_YYYYMMDD\_HHMMSS",  
    "status": "initializing|processing|success|failed",  
    "current\_stage": "Analyzer|LayoutStrategist|..."  
  },  
  "user\_preferences": {  
    "spacing\_preference": "compact|standard|comfortable|extreme",  
    "layout\_style": "data\_bus" // Default to Gold Standard  
  },  
  "workflow\_state": {  
    "current\_graph": {  
      // The evolving workflow object  
      "nodes": \[...\],  
      "links": \[...\],  
      "groups": \[...\]  
    }  
  },  
  "analysis\_results": {  
    "graph\_metrics": {  
      "node\_count": 0,  
      "has\_cycles": false,  
      "complexity\_score": 0.0,  
      "memory\_warning\_level": "safe|warning|critical"  
    },  
    "semantic\_analysis": {  
      "workflow\_type": "image\_generation|video|utility",  
      "execution\_order": {}  
    }  
  },  
  "layout\_parameters": {  
    "calculated\_spacing": {  
      "horizontal": 400,  
      "vertical": 150,  
      "group\_padding": 80  
    },  
    "data\_bus\_lanes": {  
      // Y-coordinates reserved for data buses (CRITICAL for Gold Standard)  
      "MODEL": {"y\_pos": 0, "utilized": false},  
      "CLIP": {"y\_pos": 0, "utilized": false},  
      "VAE": {"y\_pos": 0, "utilized": false},  
      "IMAGE\_MAIN": {"y\_pos": 0, "utilized": false},  
      "CONTEXT\_PIPE": {"y\_pos": 0, "utilized": false}  
    },  
    "node\_dimensions\_cache": {}  
  },  
  "validation\_reports": {  
    "technical": {"passed": false, "errors": \[\]},  
    "templating": {"passed": false, "violations": \[\]}  
  },  
  "logging\_metrics": {  
    "performance\_by\_agent": {},  
    "errors\_encountered": \[\]  
  }  
}

\---

\#\#\# FILE 5: Algorithmic Upgrades

\*\*Filename:\*\* \`./docs/standards/V2\_ALGORITHMIC\_UPGRADES.md\`

\`\`\`markdown  
\# V2.0 Algorithmic Upgrades Checklist

This document details the specific technical upgrades required for V2.0, based on the V1.0 audit. Complex algorithms MUST be implemented in \`./code\_modules/\` and invoked via \`mcp\_\_code\_execution\`.

\#\# 1\. Layout-Refiner: AABB Collision Detection

\- \*\*V1.0 Flaw:\*\* Point-based collision detection guaranteed overlaps.  
\- \*\*V2.0 Upgrade:\*\* Implement AABB (Axis-Aligned Bounding Box) collision detection.  
\- \*\*Implementation:\*\* \`./code\_modules/collision\_detection.py\`.  
\- \*\*Requirement:\*\* Must account for full dimensions of nodes AND groups, plus mandatory padding (min 80px). Must use iterative refinement until convergence.

\#\# 2\. Reroute-Engineer: Data Bus Architecture

\- \*\*V1.0 Flaw:\*\* "Spaghetti" connections; lack of systematic routing.  
\- \*\*V2.0 Upgrade:\*\* Implement a Lane-Based Data Bus System (as seen in Gold Standard).  
\- \*\*Implementation:\*\* \`./code\_modules/data\_bus\_router.py\`.  
\- \*\*Requirement:\*\* Reserve horizontal lanes (defined in SCS). Reroute nodes must align strictly to these lanes using orthogonal connections.

\#\# 3\. Layout-Strategist: Dynamic Spacing & Bus Definition

\- \*\*V1.0 Flaw:\*\* Hardcoded static spacing.  
\- \*\*V2.0 Upgrade:\*\* Implement Dynamic Spacing Calculation and define initial Y-coordinates for Data Buses.  
\- \*\*Requirement:\*\* Spacing calculated based on SCS data (Node count, User preferences, Workflow type).

\#\# 4\. Nomenclature-Specialist: Context-Aware Naming

\- \*\*V1.0 Flaw:\*\* Generic titles.  
\- \*\*V2.0 Upgrade:\*\* Implement Context-Aware, Parameterized Naming.  
\- \*\*Requirement:\*\* Format: \`(ExecutionOrder) \[Category\] Purpose (KeyParameters)\`.

\#\# 5\. Workflow-Serializer: Format Validation and Auto-Fixing

\- \*\*V1.0 Flaw:\*\* Produced invalid JSON (e.g., \`bounding\_box\` instead of \`bounding\`).  
\- \*\*V2.0 Upgrade:\*\* Implement Strict Format Templates and Auto-Fixing.  
\- \*\*Implementation:\*\* \`./code\_modules/json\_validator.py\`.  
\- \*\*Requirement:\*\* Validate against the ComfyUI schema before writing. Auto-correct known issues.

\#\# 6\. Group-Coordinator: Accurate Bounding Boxes

\- \*\*V1.0 Flaw:\*\* Incorrect bounding box calculations; incorrect colors.  
\- \*\*V2.0 Upgrade:\*\* Implement Dimension-Aware Bounding Box Calculation and Dynamic Color Loading.  
\- \*\*Requirement:\*\* Calculate bounds using true extent (position \+ dimension) plus padding. MUST load colors dynamically from \`COLOR\_SCHEME.md\`.

---

### **FILE 6: MCP Integration Guide**

**Filename:** ./docs/protocols/MCP\_INTEGRATION\_GUIDE.md

Markdown

\# MCP Integration Guide V2.0 (Claude Code Environment)

Model Context Protocols (MCP) are the foundation of the V2.0 integration layer, enabling shared context, persistent learning, and optimized execution within Claude Code.

\#\# MCP Utilization Strategy

\#\#\# 1\. \`mcp**\_\_memory\_\_**store/retrieve\` (Critical)  
This tool serves two distinct purposes:

\#\#\#\# A. Session Management (Shared Context System \- SCS)  
\*   **\*\*Purpose:\*\*** Maintain the state of the current session.  
\*   **\*\*Implementation:\*\*** Managed via \`AGENT\_INTEGRATION\_PROTOCOL\_SCS.md\`. Agents sequentially update the SCS object using the session ID key.

\#\#\#\# B. Long-Term Knowledge Base (LTKB)  
\*   **\*\*Purpose:\*\*** Store persistent knowledge.  
\*   **\*\*Implementation:\*\*** Managed primarily by the Learning-Agent. Uses persistent keys (e.g., \`LTKB\_PATTERN\_ERROR\_{ErrorSig}\`).  
\*   **\*\*Data Stored:\*\*** Error patterns, successful layout configurations matching the Gold Standard, node schemas, user preferences.

\#\#\# 2\. \`mcp**\_\_code*\_execution\` (Critical for V2.0 Optimization)***  
***\*   \*\*Purpose:\*\* Algorithmic Offloading—moving complex algorithms from agent prompts into dedicated Python modules.***  
***\*   \*\*Utilization:\*\****  
    ***\*   Used by \`Layout-Refiner\` for AABB collision resolution (\`collision\_*****detection.py\`).**  
    ***\*   Used by \`Reroute-Engineer\` for Data Bus routing (\`data\_bus\_router.py\`).***  
    ***\****   **Used by \`Workflow-Serializer\` for validation (\`json*\_validator.py\`).***  
***\*   \*\*Requirement:\*\* Agents MUST use this tool for designated tasks, passing data from the SCS to the module (in \`./code\_*****modules/\`) and integrating the results back into the SCS.**

**\#\#\# 3\. \`mcp\_\_**web-fetch**\_\_fetch\` / \`google*\_search\`***  
***\*   \*\*Purpose:\*\* Retrieve external data or discover assets.***  
***\*   \*\*Utilization:\*\* Invoked by the Node-Curator and Asset-Finder. Results should be cached in the LTKB.***

---

### **FILE 7: Gold Standard Analysis and Enforcement Rules**

**Filename:** ./docs/standards/GOLD\_STANDARD\_ANALYSIS.md

Markdown

\# Gold Standard Analysis and Enforcement Rules

This document analyzes the \`CyberRealistic-SDXL-worklfow\_v1.json\` (the "Gold Standard") and defines the rules the \`Templating-Enforcer\` agent must validate.

\#\# 1\. Analysis of the Gold Standard

The Gold Standard exhibits the following key characteristics:

\#\#\# A. Data Bus Architecture (The Defining Feature)  
\- **\*\*Observation:\*\*** Clear, dedicated horizontal lanes for primary data types (MODEL, CLIP, VAE, IMAGE, Context/Pipes). \`Reroute (rgthree)\` nodes are used extensively to manage these buses.  
\- **\*\*Example:\*\*** The JSON shows reroutes aligned at specific Y-coordinates (e.g., \-130, \-150, \-170, \-190, \-210) acting as horizontal data lanes, feeding vertically into processing groups (Y=400+).

\#\#\# B. Orthogonal Routing  
\- **\*\*Observation:\*\*** Connections are almost exclusively horizontal or vertical. Diagonal lines are minimized. Reroutes ensure clean "dog-leg" connections from nodes to the data buses.

\#\#\# C. Layout and Spacing  
\- **\*\*Observation:\*\*** Zero overlaps. Spacing is comfortable and consistent.  
\- **\*\*Alignment:\*\*** Strict alignment (grid snapping) is evident in the coordinates (multiples of 10 or 20).

\#\#\# D. Grouping and Flow  
\- **\*\*Observation:\*\*** Workflow is divided into distinct functional groups (e.g., "Input Parameters", "Checkpoint Loader", "Face Detailer", "Hand Refiner", "Saving").  
\- **\*\*Structure:\*\*** Groups have clear boundaries and adequate internal padding. The overall flow is Left-to-Right.

\#\#\# E. Encapsulation  
\- **\*\*Observation:\*\*** Use of \`ToBasicPipe\`/\`FromBasicPipe\` and \`Context Big\` nodes to simplify the transfer of multiple related connections, reducing clutter.

\#\# 2\. Templating-Enforcer Validation Rules

The \`Templating-Enforcer\` agent MUST validate the following criteria in the final SCS \`current\_graph\`.

\#\#\# Rule 1: Data Bus Implementation  
\- **\*\*Check:\*\*** Verify that major data types utilize dedicated horizontal lanes as defined in SCS \`layout\_parameters.data\_bus\_lanes\`.  
\- **\*\*Check:\*\*** Verify that \>80% of connections for these types utilize the bus architecture rather than direct point-to-point connections across stages.

\#\#\# Rule 2: Orthogonal Routing  
\- **\*\*Check:\*\*** Calculate the percentage of links that are purely horizontal or vertical. Target: \>95%.

\#\#\# Rule 3: Aesthetic Spacing and Overlap  
\- **\*\*Check:\*\*** Confirm zero overlaps (AABB validation).  
\- **\*\*Check:\*\*** Validate that the minimum spacing between any two parallel groups is at least 100px.

\#\#\# Rule 4: Group Organization  
\- **\*\*Check:\*\*** Verify the workflow contains between 5 and 15 logical, semantic groups.  
\- **\*\*Check:\*\*** Validate that all nodes are contained entirely within their assigned group boundaries (including minimum 40px internal padding).

\#\#\# Rule 5: Alignment  
\- **\*\*Check:\*\*** Verify all node positions (\`pos\[x\]\`, \`pos\[y\]\`) are divisible by the grid size (20px).

\#\# Action on Failure

If the \`Templating-Enforcer\` identifies violations, it must update the SCS \`validation\_reports.templating\` and signal the Orchestrator to report the failure to the user and the Learning-Agent.  
