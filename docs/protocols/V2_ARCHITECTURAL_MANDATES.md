# V2.0 Architectural Mandates

This document outlines the fundamental architectural shifts required for Version 2.0, addressing the systemic failures of V1.0 and optimizing for the Claude Code environment.

## 1. The Shared Context System (SCS)

**V1.0 Failure:** Siloed agents, integration errors.  
**V2.0 Mandate:** Implement a central data repository using MCP Memory (`mcp__memory__store/retrieve`).  
- **Requirement:** All agents MUST communicate exclusively through the SCS as defined in `AGENT_INTEGRATION_PROTOCOL_SCS.md`.

## 2. Enforced Agentic Pipelines

**V1.0 Failure:** Orchestrator bypassed pipelines, causing inconsistency.  
**V2.0 Mandate:** The operational pipelines in `CLAUDE_V2.md` must be hard-coded and non-skippable.

## 3. Strict Delegation (The "Coordinator" Principle)

**V1.0 Failure:** Orchestrator acted as a "doer."  
**V2.0 Mandate:** The Orchestrator's role is strictly limited to coordination, delegation, user interaction, and SCS management.

## 4. Algorithmic Offloading (Claude Code Optimization)

**V1.0 Failure:** Complex logic embedded in prompts, leading to fragility and poor performance.  
**V2.0 Mandate:** Offload complex, computationally intensive algorithms to dedicated Python modules.  
- **Implementation:** Modules stored in `./code_modules/`.  
- **Execution:** Invoked by agents using `mcp__code_execution`.  
- **Requirement:** Agents (like Layout-Refiner, Reroute-Engineer) MUST use this mechanism for core processing (e.g., collision detection, routing algorithms).

## 5. Integrated Feedback Loops and Active Learning

**V1.0 Failure:** System did not learn; Learning-Agent inactive.  
**V2.0 Mandate:** Integrate the Learning-Agent into the core execution loop (The Learning Wrapper).  
- **Requirement:** All successes and failures MUST trigger the Learning-Agent to update the Long-Term Knowledge Base (via MCP).

## 6. Standardization Enforcement

**V1.0 Failure:** Inconsistent output quality; failure to match the Gold Standard.  
**V2.0 Mandate:** Introduce the `Templating-Enforcer` agent.  
- **Requirement:** This agent validates the final output against the aesthetic and structural rules defined in `GOLD_STANDARD_ANALYSIS.md`.