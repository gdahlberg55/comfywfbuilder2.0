# V2.0 Algorithmic Upgrades Checklist

This document details the specific technical upgrades required for V2.0, based on the V1.0 audit. Complex algorithms MUST be implemented in `./code_modules/` and invoked via `mcp__code_execution`.

## 1. Layout-Refiner: AABB Collision Detection

- **V1.0 Flaw:** Point-based collision detection guaranteed overlaps.  
- **V2.0 Upgrade:** Implement AABB (Axis-Aligned Bounding Box) collision detection.  
- **Implementation:** `./code_modules/collision_detection.py`.  
- **Requirement:** Must account for full dimensions of nodes AND groups, plus mandatory padding (min 80px). Must use iterative refinement until convergence.

## 2. Reroute-Engineer: Data Bus Architecture

- **V1.0 Flaw:** "Spaghetti" connections; lack of systematic routing.  
- **V2.0 Upgrade:** Implement a Lane-Based Data Bus System (as seen in Gold Standard).  
- **Implementation:** `./code_modules/data_bus_router.py`.  
- **Requirement:** Reserve horizontal lanes (defined in SCS). Reroute nodes must align strictly to these lanes using orthogonal connections.

## 3. Layout-Strategist: Dynamic Spacing & Bus Definition

- **V1.0 Flaw:** Hardcoded static spacing.  
- **V2.0 Upgrade:** Implement Dynamic Spacing Calculation and define initial Y-coordinates for Data Buses.  
- **Requirement:** Spacing calculated based on SCS data (Node count, User preferences, Workflow type).

## 4. Nomenclature-Specialist: Context-Aware Naming

- **V1.0 Flaw:** Generic titles.  
- **V2.0 Upgrade:** Implement Context-Aware, Parameterized Naming.  
- **Requirement:** Format: `(ExecutionOrder) [Category] Purpose (KeyParameters)`.

## 5. Workflow-Serializer: Format Validation and Auto-Fixing

- **V1.0 Flaw:** Produced invalid JSON (e.g., `bounding_box` instead of `bounding`).  
- **V2.0 Upgrade:** Implement Strict Format Templates and Auto-Fixing.  
- **Implementation:** `./code_modules/json_validator.py`.  
- **Requirement:** Validate against the ComfyUI schema before writing. Auto-correct known issues.

## 6. Group-Coordinator: Accurate Bounding Boxes

- **V1.0 Flaw:** Incorrect bounding box calculations; incorrect colors.  
- **V2.0 Upgrade:** Implement Dimension-Aware Bounding Box Calculation and Dynamic Color Loading.  
- **Requirement:** Calculate bounds using true extent (position + dimension) plus padding. MUST load colors dynamically from `COLOR_SCHEME.md`.