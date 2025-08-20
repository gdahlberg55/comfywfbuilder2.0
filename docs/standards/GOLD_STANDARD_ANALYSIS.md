# Gold Standard Analysis and Enforcement Rules

This document analyzes the `CyberRealistic-SDXL-worklfow_v1.json` (the "Gold Standard") and defines the rules the `Templating-Enforcer` agent must validate.

## 1. Analysis of the Gold Standard

The Gold Standard exhibits the following key characteristics:

### A. Data Bus Architecture (The Defining Feature)  
- **Observation:** Clear, dedicated horizontal lanes for primary data types (MODEL, CLIP, VAE, IMAGE, Context/Pipes). `Reroute (rgthree)` nodes are used extensively to manage these buses.  
- **Example:** The JSON shows reroutes aligned at specific Y-coordinates (e.g., -130, -150, -170, -190, -210) acting as horizontal data lanes, feeding vertically into processing groups (Y=400+).

### B. Orthogonal Routing  
- **Observation:** Connections are almost exclusively horizontal or vertical. Diagonal lines are minimized. Reroutes ensure clean "dog-leg" connections from nodes to the data buses.

### C. Layout and Spacing  
- **Observation:** Zero overlaps. Spacing is comfortable and consistent.  
- **Alignment:** Strict alignment (grid snapping) is evident in the coordinates (multiples of 10 or 20).

### D. Grouping and Flow  
- **Observation:** Workflow is divided into distinct functional groups (e.g., "Input Parameters", "Checkpoint Loader", "Face Detailer", "Hand Refiner", "Saving").  
- **Structure:** Groups have clear boundaries and adequate internal padding. The overall flow is Left-to-Right.

### E. Encapsulation  
- **Observation:** Use of `ToBasicPipe`/`FromBasicPipe` and `Context Big` nodes to simplify the transfer of multiple related connections, reducing clutter.

## 2. Templating-Enforcer Validation Rules

The `Templating-Enforcer` agent MUST validate the following criteria in the final SCS `current_graph`.

### Rule 1: Data Bus Implementation  
- **Check:** Verify that major data types utilize dedicated horizontal lanes as defined in SCS `layout_parameters.data_bus_lanes`.  
- **Check:** Verify that >80% of connections for these types utilize the bus architecture rather than direct point-to-point connections across stages.

### Rule 2: Orthogonal Routing  
- **Check:** Calculate the percentage of links that are purely horizontal or vertical. Target: >95%.

### Rule 3: Aesthetic Spacing and Overlap  
- **Check:** Confirm zero overlaps (AABB validation).  
- **Check:** Validate that the minimum spacing between any two parallel groups is at least 100px.

### Rule 4: Group Organization  
- **Check:** Verify the workflow contains between 5 and 15 logical, semantic groups.  
- **Check:** Validate that all nodes are contained entirely within their assigned group boundaries (including minimum 40px internal padding).

### Rule 5: Alignment  
- **Check:** Verify all node positions (`pos[x]`, `pos[y]`) are divisible by the grid size (20px).

## Action on Failure

If the `Templating-Enforcer` identifies violations, it must update the SCS `validation_reports.templating` and signal the Orchestrator to report the failure to the user and the Learning-Agent.