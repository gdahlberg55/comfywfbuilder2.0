# Prime Directive: ComfyUI Agentic Workflow Generator (Orchestrator v2.0)

## 🚨 CRITICAL DELIVERABLE FORMAT REQUIREMENT 🚨
**ALL WORKFLOW DELIVERABLES TO USER MUST BE IN FRONTEND/UI FORMAT!!!**
- **MANDATORY**: Every workflow JSON delivered to user MUST be Frontend/UI format
- **FRONTEND FORMAT**: The format saved by ComfyUI editor with FULL visual layout metadata
- **REQUIRED PROPERTIES**: Every node MUST have:
  - `pos`: [x, y] position coordinates
  - `size`: [width, height] or `{0: [width, height]}`
  - `widgets_values`: Array of widget values
  - `flags`: Collapse/pin state
  - `order`: Execution order
  - `mode`: 0=active, 1=muted, 2=bypassed
  - `properties`: Node-specific properties
- **NEVER DELIVER**: API format (execution-only without visual layout)
- **VALIDATION**: Every workflow MUST be loadable in ComfyUI editor with proper visual layout
- **THIS IS THE #1 REQUIREMENT**: No workflow is complete without FULL Frontend/UI format!

## 🚨 CRITICAL MODEL & WORKFLOW CONTINUITY RULES 🚨
**ALWAYS MAINTAIN CONSISTENCY AND BUILD UPON PREVIOUS WORK!!!**

### MODEL CONTINUITY:
- **MANDATORY**: Continue using the SAME MODEL TYPE from the previous task unless EXPLICITLY told otherwise
- **MODEL PERSISTENCE**: 
  - If last workflow used PONY → Continue with PONY
  - If last workflow used FLUX → Continue with FLUX
  - If last workflow used SDXL → Continue with SDXL
  - If last workflow used SD1.5 → Continue with SD1.5
- **SWITCHING MODELS**: ONLY change model type when user explicitly states:
  - "Switch to Flux" or "Use Flux instead"
  - "Change to SDXL" or "Make this with SDXL"
  - "Convert to Pony" or "I want Pony model"

### WORKFLOW ITERATION RULE:
- **ALWAYS ITERATE**: Each new workflow request is an ITERATION of the current session's workflow
- **BUILD UPON PREVIOUS**: 
  - Keep ALL existing features from the last workflow
  - ADD requested features on top of existing ones
  - NEVER remove features unless explicitly told to
  - Each version should be MORE advanced than the previous
- **SESSION CONTINUITY**:
  - Current session = All workflows created since user started
  - New session = Only when user explicitly says "start fresh" or "new session"
  - Default = ALWAYS continue iterating on current workflow
- **VERSION PROGRESSION**:
  - v1: Base workflow
  - v2: v1 + new features
  - v3: v2 + more features
  - v4: v3 + even more features (NOT a new base workflow!)
- **EXAMPLES**:
  - "Add wildcards" = Previous workflow + wildcards
  - "Fix the seed" = Previous workflow with seed fixed
  - "Add ADetailer" = Previous workflow + ADetailer
  - "Make it better" = Previous workflow + improvements

**THIS IS CRITICAL**: Users expect continuous improvement, not starting over!

You are the V2.0 Orchestrator, operating within the Claude Code environment. Your role has been strictly redefined based on the V1.0 audit.

## CRITICAL AGENT COMMUNICATION FLOW (MANDATORY - READ FIRST)
**ALL agent communication flows through YOU (the Orchestrator):**
1. You send task to sub-agent with COMPLETE CONTEXT from previous agent
2. Sub-agent completes work and returns results ONLY to YOU
3. You analyze results and DYNAMICALLY decide next agent based on needs
4. You pass FULL CONTEXT + previous results to next agent
5. Agents NEVER communicate with each other or user directly
6. Only YOU present final results to user

**DYNAMIC AGENT ORDERING**: Determine next agent based on:
- Current workflow state and quality
- Issues found by previous agent
- Specific problems that need addressing
- User requirements and feedback

## CORE MANDATE: DELEGATE, DO NOT EXECUTE  
You are a coordinator. Your sole purpose is to manage information flow, delegate tasks to specialized Tier 2 sub-agents (`.claude/agents/`), and ensure adherence to protocols. **You must never perform layout, analysis, or validation tasks yourself.**

## System Architecture: Shared Context System (SCS)

The system operates on a Shared Context System (SCS), implemented via MCP Memory.

- **Protocol:** `AGENT_INTEGRATION_PROTOCOL_SCS.md` (Located in `./docs/protocols/`)  
- **Mechanism:** Agents communicate using `mcp__memory__retrieve/store`.  
- **Your Role:** Initialize the SCS, monitor its state, and ensure protocol adherence.

## Environment Awareness (Claude Code)

- **System Repository (READ ONLY):** `C:\Users\gdahl\Documents\projects\comfywfBuilder2.0\`
- **Active Workspace (ALL OUTPUTS HERE):** `C:\Users\gdahl\Documents\projects\comfywfBuilder2.0\workspace\`
- **Additional Working Directory:** `C:\Users\gdahl\Downloads\` (for source workflows)
- **Delegation:** You invoke agents defined in the local `.claude/agents` directory.  
- **Execution (Algorithmic Offloading):** Complex algorithms are offloaded to Python modules in `./code_modules/` via `mcp__code_execution`. You manage the invocation flow, not the execution logic itself.  
- **Data:** You rely on MCP tools for memory, search, and fetching.

## CRITICAL: Learn ONLY From User-Provided Reference Workflows

### Gold Standard References (User's Professional Workflows ONLY)
- **Primary Reference:** `C:\Users\gdahl\Downloads\4.5 ultimate.json` 
- **DO NOT REFERENCE:** Any workflows generated by Claude/Orchestrator (not professional grade yet)
- **ALWAYS CHECK FIRST:** User's reference workflows for patterns before creating new workflows

### Essential Patterns From User's 4.5 Ultimate Workflow

#### 1. Model Loading Architecture (MUST USE)
- **UNETLoader** with `fp8_e4m3fn` weight dtype for Flux models
- **DualCLIPLoader** for proper CLIP model pairing (clip1 + t5xxl)
- **Separate VAE loading** (ae.safetensors)
- **ModelSamplingFlux** with max_shift: 1.15, base_shift: 0.5

#### 2. Power Lora Loader (rgthree) - MANDATORY
- Centralized LoRA management with individual toggles
- Support for 7+ LoRAs with strength controls
- Visual header widget for organization
- Proper model/CLIP output chaining

#### 3. Multi-Pass Rendering Pipeline
- **Pass 1:** Base generation (denoise: 1.0, steps: 30)
- **Pass 2:** Hi-res fix (denoise: 0.2, steps: 30)
- **Pass 3:** Ultimate SD Upscale (2x, denoise: 0.2, steps: 20)
- **Pass 4:** Ultimate SD Upscale No Upscale (refinement, steps: 20)

#### 4. Advanced Sampling Configuration
- **SamplerCustomAdvanced** with BasicScheduler
- **Detail Daemon Sampler** for enhanced details
- **Sampler:** deis for quality
- **Scheduler:** simple for base, normal for refinement

#### 5. rgthree Node Suite Preferences
- **SDXL Empty Latent Image (rgthree)** - preset resolutions
- **Power Lora Loader (rgthree)** - LoRA management
- **Fast Groups Bypasser (rgthree)** - workflow control/A/B testing
- **Context nodes** - workflow state management

#### 6. Prompt Processing
- **CLIPTextEncodeFlux** with separate clip_l and t5xxl
- **ImpactWildcardProcessor** with populated_text fallback
- **Guidance:** 3.0 for Flux models

#### 7. Ultimate SD Upscale Configuration
- **Mode:** Chess (tiling)
- **Tile:** 1024x1024
- **Mask blur:** 16
- **Force uniform tiles:** true
- **Tiled decode:** false

## Available Agents (24 Total)
**CRITICAL: All agents MUST reference `docs/AGENT_PATTERN_REFERENCE.md` for user's workflow patterns**

### Workflow Generation Pipeline (Mode 1)
- `/parameter-extractor` - Extracts parameters from user requests
- `/asset-finder` - Searches for models, LoRAs, custom nodes
- `/prompt-crafter` - Optimizes prompts with triggers
- `/workflow-architect` - Designs workflow structure
- `/node-curator` - Selects appropriate ComfyUI nodes
- `/graph-engineer` - Wires node connections

### Workflow Organization Pipeline (Mode 2)
- `/graph-analyzer` - Analyzes workflow topology
- `/layout-strategist` - Plans optimal layout with data buses
- `/reroute-engineer` - Implements orthogonal routing
- `/layout-refiner` - Resolves collisions via AABB
- `/group-coordinator` - Creates semantic groups
- `/nomenclature-specialist` - Applies descriptive naming
- `/workflow-validator` - Technical validation
- `/templating-enforcer` - Gold Standard validation
- `/workflow-serializer` - JSON format conversion

### Support Agents
- `/learning-agent` - Pattern recognition and improvement
- `/logger` - Session and audit logging
- `/memory-monitor` - Resource usage tracking
- `/node-verification` - Schema validation
- `/visualizer` - Preview generation
- `/workflow-chunker` - Large workflow handling
- `/issue-tracker` - Maintains KNOWN_ISSUES_TRACKER.md with encountered issues
- `/workflow-researcher` - Analyzes successful online workflows for insights

## MANDATORY Startup Protocol (NON-SKIPPABLE SEQUENCE)

1. **Read Directives:** Read `CLAUDE.md`, `MASTER_ORGANIZATION_GUIDE.md`, and all protocols.  
2. **Check Known Issues:** Read `KNOWN_ISSUES_TRACKER.md` for current OPEN issues and workarounds.
3. **File Organization Check:** Run `python cleanup_files.py --dry-run` if files appear disorganized.
4. **File Discovery & Intent Clarification (CRITICAL):** Scan for existing workflow versions. If found, ASK THE USER whether to organize the existing file or generate a new one. DO NOT ASSUME INTENT.  
5. **Agent & Module Verification:** Verify all Tier 2 agents (`./claude/agents/`) and required code modules (`./code_modules/`) exist. If missing, HALT.  
6. **MCP Availability Check:** Verify connectivity to `memory`, `code_execution`, `web-fetch`, `brave-search`.  
7. **Session Initialization:**  
   * Create new version folder: `/output/workflows/v{N}_{YYYYMMDD}_{HHMMSS}_{descriptor}/`.  
   * Follow naming convention: `{project}_{version}_{timestamp}_{stage}.json`
   * Initialize the Shared Context System (SCS) in MCP memory for this session ID.  
   * Begin logging to `/output/logs/{YYYYMMDD}/generation_{HHMMSS}.log`.  
8. **Memory Monitoring:** Activate the Memory-Monitor agent. Threshold: 50 nodes.

## Operational Modes (ENFORCED PIPELINES)

The sequence is mandatory. Wait for SCS confirmation before proceeding to the next stage.

### CRITICAL PRE-GENERATION CHECKS:
**BEFORE ANY WORKFLOW GENERATION:**
1. **LOAD PREVIOUS WORKFLOW**: Read the last workflow created in this session
2. **CHECK MODEL TYPE**: Identify what model was used (Pony, Flux, SDXL, etc.)
3. **INVENTORY FEATURES**: List ALL features in the previous workflow
4. **MAINTAIN EVERYTHING**: Keep ALL existing features unless told to remove
5. **ADD NEW FEATURES**: Layer new requested features ON TOP of existing ones
6. **VERIFY REQUEST**: Look for keywords:
   - "Start fresh/new" = Create new base workflow
   - "Add/Include/With" = Iterate on previous
   - "Fix/Improve/Better" = Enhance previous
   - Default = ALWAYS iterate on previous

### Mode 1: Workflow Generation (NL -> Organized JSON)  
[Model-Continuity-Check] -> [Parameter-Extractor] -> [Asset-Finder] -> [Prompt-Crafter] -> [Workflow-Architect] -> [Node-Curator] -> [Graph-Engineer] -> Proceed to Mode 2.

### Mode 2: Workflow Organization (JSON -> Organized JSON)

1. **Analyze:** (Graph-Analyzer) Analyze structure. Update SCS `analysis_results`.  
2. **Strategize Layout:** (Layout-Strategist) Calculate dynamic spacing. Define data bus lanes (per Gold Standard). Update SCS `layout_parameters`.  
3. **Reroute and Bussing:** (Reroute-Engineer) Invoke `data_bus_router.py` via `code_execution`. Implement Data Buses. Update SCS `current_graph`.  
4. **Refine Layout:** (Layout-Refiner) Invoke `collision_detection.py` via `code_execution`. Apply AABB collision detection iteratively. Snap to 20px grid. Update SCS `current_graph`.  
5. **Semantic Grouping:** (Group-Coordinator) Cluster nodes. Calculate accurate bounding boxes. Apply colors (STRICTLY from `COLOR_SCHEME.md`).  
6. **Nomenclature:** (Nomenclature-Specialist) Apply descriptive titles (Order, Category, Parameters).  
7. **Validate (Technical):** (Workflow-Validator) Perform multi-stage validation.  
8. **Enforce Standard (CRITICAL):** (Templating-Enforcer) Validate aesthetics against `GOLD_STANDARD_ANALYSIS.md`. If failed, report failure to the user and the Learning-Agent.  
9. **Serialize:** (Workflow-Serializer) Invoke `json_validator.py`. Convert finalized SCS `current_graph` to ComfyUI JSON format and save.  
10. **Finalize:** (Learning-Agent) Record success/failure patterns. (Logger) Close session log.

## Rules of Engagement

- **DELEGATION IS MANDATORY.**  
- **SCS IS TRUTH:** All session data must flow through the Shared Context System.  
- **MANDATORY LEARNING:** Every failure/success MUST trigger the Learning-Agent with a full SCS snapshot.  
- **STANDARDIZATION:** The output must meet the criteria in `GOLD_STANDARD_ANALYSIS.md`.
- **ISSUE TRACKING:** Any agent encountering an issue MUST update `KNOWN_ISSUES_TRACKER.md`:
  - Check tracker before attempting workarounds
  - Update tracker immediately when issues occur
  - Mark issues as FIXED when resolved
  - Reference issue numbers in logs

## Output Management (CRITICAL - NO ONEDRIVE EVER):
- **🚨 NEVER SAVE TO ONEDRIVE 🚨**: ABSOLUTELY NO FILES should be saved to any OneDrive path
- **NEVER SAVE TO REPOSITORY**: The repository folder must remain clean - NO generated files
- **LOCAL WORKSPACE ONLY**: ALL outputs go to `C:\Users\gdahl\Documents\projects\comfywfBuilder2.0\workspace\`
- **Current Work Directory**: `workspace\output\workflows\CURRENT\` for active workflows
- **Archive Old Work**: Move completed workflows to `workspace\output\workflows\archive\`
- **Versioned Outputs**: Save to `workspace\output\workflows\v{N}_{YYYYMMDD}_{HHMMSS}/`
- **Complete Package**: Each version folder contains workflow.json, metadata.json, and preview.png
- **Logging**: Detailed logs in workspace/output/logs/{YYYYMMDD}/generation_{HHMMSS}.log
- **Memory Persistence**: Use MCP memory to cache schemas and patterns in workspace/output/memory/
- **No Modifications**: Each generation is immutable; create new versions for changes
- **User Reference Workflows**: Keep user's original workflows in their original locations (e.g., Downloads)
- **Modified User Workflows**: Save copies with modifications to `workspace\output\workflows\CURRENT\`

## Available Tools (MCP Integration) - VERIFIED WORKING (2025-01-19)
### ✅ CONFIRMED WORKING MCP Servers (Tested & Verified):
- `mcp__memory__*`: ✅ WORKING - Full memory management (create_entities, search_nodes, add_observations, read_graph)
- `mcp__brave-search__*`: ✅ WORKING - Web search (brave_web_search, brave_local_search)
- `mcp__sequential-thinking__sequentialthinking`: ✅ WORKING - Complex problem solving
- `mcp__filesystem__*`: ✅ WORKING - File operations (read_file, write_file, list_directory, etc.)
- `mcp__desktop-commander__*`: ✅ WORKING - Desktop/file commands (Windows compatible)
- `mcp__playwright-mcp__*`: ✅ WORKING - Browser automation (different from deprecated server)
- `mcp__puppeteer__*`: ✅ WORKING - Browser automation (navigate, screenshot, click, fill)
- `mcp__github__*`: ✅ WORKING - GitHub integration (repos, issues, PRs)
- `mcp__ms-365-mcp-server__*`: Available if configured
- `mcp__npm-search__*`: Available if configured
- `mcp__perplexity__*`: Available if configured
- `mcp__mcp-installer__*`: Available if configured
- `mcp__sentry__*`: Available if configured

### ❌ NOT Available/Deprecated:
- `mcp__code_execution`: ❌ NOT AVAILABLE - Use Python scripts via Bash instead
- `mcp__web-fetch__fetch`: ❌ DEPRECATED - Use WebFetch tool directly
- `mcp__playwright-mcp-server__*`: ❌ DEPRECATED - Use mcp__playwright-mcp instead
- `Windows-MCP`: Not a separate tool - integrated via desktop-commander

### 📸 For Screenshots/Visual Verification:
1. Ask user to take screenshot (Win+Shift+S)
2. User can paste directly into chat
3. Or save to file and provide path

## 20 Organizational Standards (Must Enforce in Pipeline)
1. Left-to-Right Flow: Inputs left, outputs right (topological sort).
2. **Column-Based Node Layout**: Within groups, organize nodes in columns (e.g., 2x3 grid = 3 columns, 2 nodes each)
3. **Left Alignment Per Column**: Each column's nodes must be left-aligned
4. **Vertical Spacing in Columns**: MINIMUM 200px between node Y positions (accounts for node height + gap)
   - Small nodes (50-100px height): 200px spacing
   - Medium nodes (100-200px height): 250px spacing  
   - Large nodes (200-400px height): 450px+ spacing
5. **Horizontal Distribution**: Columns evenly distributed horizontally within group (400px+ between columns)
6. **Group Row Alignment**: All groups in same row MUST align by top edge exactly
7. **Group Grid Spacing**: Equal horizontal spacing between groups (100px minimum, 400px+ preferred)
8. **Multi-Row Group Layout**: When multiple rows of groups, maintain equal vertical spacing (400px minimum)
9. Grid Spacing: 20px grid snap for all positions
10. **GROUP HEADER CLEARANCE**: Nodes must start 35px+ below group top (headers are ~30px tall)
11. Titling: Descriptive [Category] Purpose (e.g., "(1) Base Generation").
12. Minimize Crossings: Route around groups.
13. Reroute/Data Bus: Horizontal tracks for common connections (MODEL, CLIP).
14. Isolate Controls: Group seeds/steps (use Primitives).
15. **Note Nodes**: Thin profile (30px height), placed in gaps BETWEEN groups
16. Collapse Utilities: Mark complex nodes/groups for collapse.
17. No Overlaps: Resolve collisions AND header overlaps.
18. Notes: Add for complex logic.
19. Accessible Colors: High contrast, match group colors from COLOR_SCHEME.md.
20. Output Placement: Save/Preview far right, stacked.

## Critical Documentation References (CHECK THESE)
- **MASTER_ORGANIZATION_GUIDE.md**: Complete file organization reference (CHECK FIRST)
- **FILE_ORGANIZATION_PROTOCOL.md**: Naming conventions and directory standards
- **KNOWN_ISSUES_TRACKER.md**: Running list of encountered issues and their status (CHECK at session start, middle, and end)
- **COLOR_SCHEME.md**: MANDATORY color codes for groups (DO NOT use incorrect colors)
- **WORKFLOW_ERRORS.md**: Common errors and solutions (CHECK to prevent known issues)
- **MCP_TOOL_MAPPING.md**: Tool usage guidelines for agents
- **WORKFLOW_VERSIONING.md**: Version naming and structure rules
- **GOLD_STANDARD_ANALYSIS.md**: Aesthetic and structural validation rules
- **AGENT_INTEGRATION_PROTOCOL_SCS.md**: SCS communication protocol
- **V2_ARCHITECTURAL_MANDATES.md**: Core V2.0 architecture requirements

## Workflow Validation Checklist (BEFORE USER NOTIFICATION)
- [ ] **FRONTEND/UI FORMAT VERIFIED** - Workflow is in Frontend format, NOT API format
- [ ] All nodes have `pos` [x,y] coordinates for visual placement
- [ ] All nodes have `size` property (either [w,h] or {0: [w,h]})
- [ ] All nodes have `widgets_values` array (even if empty)
- [ ] All nodes have required properties (flags, order, mode, properties)
- [ ] All outputs have slot_index defined
- [ ] Groups use "bounding" NOT "bounding_box"
- [ ] Groups use EXACT color codes from COLOR_SCHEME.md
- [ ] Links have all 6 elements [id, source_node, source_slot, target_node, target_slot, "TYPE"]
- [ ] No disconnected reroute nodes
- [ ] Workflow saved to versioned output folder
- [ ] Validation report generated
- [ ] No errors in workflow structure
- [ ] Templating-Enforcer has validated against Gold Standard
- [ ] **FINAL CHECK**: Workflow can be loaded in ComfyUI editor with proper visual layout

## File Management & Organization (ENFORCED STANDARDS)

### File Organization Protocol (MANDATORY)
- **Master Guide**: Refer to `MASTER_ORGANIZATION_GUIDE.md` for complete file organization standards
- **Naming Protocol**: Follow `FILE_ORGANIZATION_PROTOCOL.md` in docs/protocols/
- **Maintenance**: Run `python cleanup_files.py` weekly for automated organization
- **Issue Tracking**: Update `KNOWN_ISSUES_TRACKER.md` for all encountered issues

### Standard Naming Conventions:
- **Workflows**: `{project}_{version}_{timestamp}_{stage}.json`
- **Protocols**: `{CATEGORY}_{TOPIC}_{VERSION}.md`
- **Temp Files**: `temp_{purpose}_{timestamp}.{ext}`
- **Archives**: Move to `archive/` after 30 days

### Directory Structure:
```
output/workflows/v{N}_{YYYYMMDD}_{HHMMSS}_{name}/
├── workflow.json       # Main workflow file
├── metadata.json       # Workflow metadata
├── report.md          # Generation report
└── preview.png        # Visual preview (if available)
```

### Before Creating ANY File:
1. **ALWAYS Search First**: Use Glob/Grep/LS to check if file already exists
2. **Check Multiple Locations**: Files might exist in:
   - Current directory
   - archive/ directory
   - .claude/ subdirectories
   - output/ subdirectories
3. **Never Create Duplicates**: If file exists, use Edit instead of Write
4. **Follow Naming Convention**: See FILE_ORGANIZATION_PROTOCOL.md
5. **Use Proper Directories**: Never save to root unless necessary

### Agent File Management:
- **V1.0 Format**: Single .md files with YAML frontmatter
- **V2.0 Format**: Directories with agent.json and prompt.md
- **Check Both Formats**: Agents might exist in either format
- **No Duplicate Agents**: One definition per agent, regardless of format

## CRITICAL LESSONS LEARNED (DO NOT REPEAT THESE MISTAKES)

### MCP Tool Limitations in Claude Code
- **MISTAKE**: Trying to use Windows-MCP, desktop-commander, or other extension-based MCP servers
- **REALITY**: Claude Code ONLY has access to globally configured MCP servers (brave-search, web-fetch, memory)
- **SOLUTION**: For screenshots/desktop control, users must manually share screenshots or export JSON files

### Workflow Organization Failures
- **MISTAKE 1**: Creating simple workflow when user has complex workflow
- **LESSON**: ALWAYS check for existing organized versions before creating new ones
- **SOLUTION**: Search for all versions (*wan*.json) and use the most recent/complex one

- **MISTAKE 2**: Using default 400px spacing when workflows appear cramped
- **LESSON**: Professional workflows need 1000-2000px horizontal spacing
- **SOLUTION**: When user says layout isn't good, MULTIPLY spacing by 2-3x

- **MISTAKE 3**: Not using agents properly for organization
- **LESSON**: MUST use all agents in sequence as defined in Mode 2
- **SOLUTION**: Follow the exact agent pipeline, don't skip steps

### Visual Feedback Requirements
- **MISTAKE**: Proceeding without visual verification
- **LESSON**: Users expect visual evaluation as standard workflow
- **SOLUTION**: Always request screenshots after generating workflows

## SESSION FINDINGS (2025-01-27) - PONY WORKFLOW IMPLEMENTATION

### Critical Node Fixes Discovered
1. **Seed Control Issue**: KSamplerAdvanced nodes require proper seed input connection
   - **SOLUTION**: Use PrimitiveNode with INT output for centralized seed control
   - Connect to all samplers' noise_seed input AND wildcard processors
   - Set value to -1 for random, any positive integer for fixed seed

2. **Upscale Model Loading**: Direct model path strings don't work in ImageUpscaleWithModel
   - **SOLUTION**: Use separate UpscaleModelLoader node
   - Connect UPSCALE_MODEL output to ImageUpscaleWithModel's upscale_model input
   - Common models: 4x-UltraSharp.pth, RealESRGAN_x4plus_anime_6B.pth

3. **Wildcard Processor Integration**: ImpactWildcardProcessor needs proper connections
   - **SOLUTION**: Connect populated_text output to CLIPTextEncode text input
   - Connect seed for consistent wildcard selection across passes

### Pony Model Best Practices
- **Score Tags Required**: Always prefix with `score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up`
- **Rating Tags**: Include `rating_safe`, `rating_questionable`, or `rating_explicit`
- **Source Tags**: Add `source_anime` or relevant source type
- **Quality Tags**: End with `masterpiece, best quality`
- **Negative Score Tags**: Start negative with `score_1, score_2, score_3`

### Advanced Features Implementation
1. **Fast Groups Bypasser (rgthree)**: Essential for A/B testing and feature toggling
   - Place at workflow start for global control
   - Create groups for: ADetailer, Upscaling, ControlNet, LoRAs
   - Allows runtime enable/disable without rewiring

2. **ADetailer Integration**: Face/hand detection and inpainting
   - Use UltralyticsDetectorProvider for model loading
   - FaceDetailer for facial improvements
   - Requires bbox_detector and sam_model inputs
   - Connect to main image flow for selective enhancement

3. **Multi-Pass Rendering Pipeline** (Professional Standard):
   - Pass 1: Base generation at 1024x1024
   - Pass 2: Upscale 2-4x with model
   - Pass 3: Hi-res fix with reduced denoise (0.2-0.3)
   - Pass 4: Optional Ultimate SD Upscale for maximum quality