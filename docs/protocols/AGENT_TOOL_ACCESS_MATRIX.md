# Agent Tool Access Matrix v2.0

## Purpose
Define specific tool access permissions for each agent to enhance their capabilities while maintaining security and efficiency.

## Tool Categories

### 🔍 Search & Discovery Tools
- `WebSearch` - Search for workflows, nodes, techniques
- `WebFetch` - Fetch specific pages/documentation
- `Grep` - Search within codebase
- `Glob` - Find files by pattern
- `LS` - List directory contents

### 💾 Data Management Tools
- `Read` - Read files
- `Write` - Write new files
- `Edit` - Modify existing files
- `MultiEdit` - Multiple edits in one operation

### 🧠 Intelligence Tools
- `mcp__memory__store` - Store in shared memory
- `mcp__memory__retrieve` - Retrieve from shared memory
- `mcp__brave-search__search` - Search for models, LoRAs
- `mcp__web-fetch__fetch` - Fetch API schemas
- `mcp__code_execution` - Execute Python code

### 🔧 System Tools
- `Bash` - Execute shell commands (restricted)
- `Task` - Delegate to other agents
- `TodoWrite` - Task management

---

## Agent Tool Mappings

### 1. Parameter-Extractor
**Purpose**: Extract parameters from user requests
**Recommended Tools**:
- ✅ `Read` - Read user input files
- ✅ `mcp__memory__store` - Store extracted parameters
- ✅ `Grep` - Search for parameter patterns
- ✅ `WebSearch` - Search for parameter documentation
**Rationale**: Needs to analyze text and store structured data

### 2. Asset-Finder
**Purpose**: Search for models, LoRAs, custom nodes
**Recommended Tools**:
- ✅ `mcp__brave-search__search` - Primary search tool
- ✅ `WebSearch` - Search model repositories
- ✅ `WebFetch` - Fetch model details
- ✅ `mcp__memory__store` - Cache found assets
- ✅ `Read` - Read local asset lists
**Rationale**: Core function is searching and cataloging external resources

### 3. Prompt-Crafter
**Purpose**: Optimize prompts with triggers
**Recommended Tools**:
- ✅ `WebSearch` - Search for prompt techniques
- ✅ `mcp__memory__retrieve` - Get stored prompts
- ✅ `mcp__memory__store` - Store optimized prompts
- ✅ `Read` - Read prompt templates
**Rationale**: Needs access to prompt databases and techniques

### 4. Workflow-Architect
**Purpose**: Design workflow structure
**Recommended Tools**:
- ✅ `mcp__memory__retrieve` - Get parameters and assets
- ✅ `mcp__memory__store` - Store architecture
- ✅ `Read` - Read workflow templates
- ✅ `WebSearch` - Search for workflow patterns
- ✅ `mcp__code_execution` - Run design algorithms
**Rationale**: Central design role requires broad data access

### 5. Node-Curator
**Purpose**: Select appropriate ComfyUI nodes
**Recommended Tools**:
- ✅ `mcp__web-fetch__fetch` - Fetch node schemas
- ✅ `WebSearch` - Search node documentation
- ✅ `mcp__memory__store` - Cache node info
- ✅ `Read` - Read node libraries
- ✅ `Grep` - Search node definitions
**Rationale**: Must access and analyze node specifications

### 6. Graph-Engineer
**Purpose**: Wire node connections
**Recommended Tools**:
- ✅ `mcp__memory__retrieve` - Get workflow structure
- ✅ `mcp__memory__store` - Store graph data
- ✅ `mcp__code_execution` - Run graph algorithms
- ✅ `Write` - Save graph files
**Rationale**: Needs to manipulate graph structures programmatically

### 7. Graph-Analyzer
**Purpose**: Analyze workflow topology
**Recommended Tools**:
- ✅ `Read` - Read workflow files
- ✅ `mcp__code_execution` - Run analysis algorithms
- ✅ `mcp__memory__store` - Store analysis results
- ✅ `Write` - Generate analysis reports
**Rationale**: Heavy computational analysis requires code execution

### 8. Layout-Strategist
**Purpose**: Plan optimal layout with data buses
**Recommended Tools**:
- ✅ `mcp__memory__retrieve` - Get graph data
- ✅ `mcp__code_execution` - Run layout algorithms
- ✅ `mcp__memory__store` - Store layout parameters
- ✅ `Write` - Save layout plans
**Rationale**: Complex spatial calculations need algorithmic support

### 9. Reroute-Engineer
**Purpose**: Implement orthogonal routing
**Recommended Tools**:
- ✅ `mcp__code_execution` - Run routing algorithms
- ✅ `mcp__memory__retrieve` - Get layout data
- ✅ `mcp__memory__store` - Store routing data
- ✅ `Edit` - Modify workflow connections
**Rationale**: Routing algorithms are computationally intensive

### 10. Layout-Refiner
**Purpose**: Resolve collisions via AABB
**Recommended Tools**:
- ✅ `mcp__code_execution` - Run collision detection
- ✅ `mcp__memory__retrieve` - Get current layout
- ✅ `mcp__memory__store` - Store refined layout
- ✅ `MultiEdit` - Apply multiple position adjustments
**Rationale**: Collision detection requires complex calculations

### 11. Group-Coordinator
**Purpose**: Create semantic groups
**Recommended Tools**:
- ✅ `mcp__memory__retrieve` - Get workflow data
- ✅ `Read` - Read grouping rules
- ✅ `mcp__memory__store` - Store group definitions
- ✅ `Edit` - Update workflow groups
**Rationale**: Needs to analyze and modify workflow structure

### 12. Nomenclature-Specialist
**Purpose**: Apply descriptive naming
**Recommended Tools**:
- ✅ `mcp__memory__retrieve` - Get workflow elements
- ✅ `MultiEdit` - Rename multiple elements
- ✅ `mcp__memory__store` - Store naming mappings
- ✅ `Read` - Read naming conventions
**Rationale**: Batch renaming operations require multi-edit

### 13. Workflow-Validator
**Purpose**: Technical validation
**Recommended Tools**:
- ✅ `Read` - Read workflow files
- ✅ `mcp__code_execution` - Run validation scripts
- ✅ `Write` - Generate validation reports
- ✅ `mcp__memory__store` - Store validation results
**Rationale**: Validation requires programmatic checks

### 14. Templating-Enforcer
**Purpose**: Gold Standard validation
**Recommended Tools**:
- ✅ `Read` - Read gold standard templates
- ✅ `mcp__memory__retrieve` - Get workflow data
- ✅ `Write` - Generate compliance reports
- ✅ `WebFetch` - Fetch latest standards
**Rationale**: Must compare against authoritative templates

### 15. Workflow-Serializer
**Purpose**: JSON format conversion
**Recommended Tools**:
- ✅ `mcp__memory__retrieve` - Get final workflow
- ✅ `mcp__code_execution` - Run serialization
- ✅ `Write` - Save JSON files
- ✅ `Edit` - Fix formatting issues
**Rationale**: Format conversion needs precise control

### 16. Learning-Agent
**Purpose**: Pattern recognition and improvement
**Recommended Tools**:
- ✅ `mcp__memory__store` - Store learned patterns
- ✅ `mcp__memory__retrieve` - Analyze patterns
- ✅ `Read` - Read historical data
- ✅ `Write` - Update knowledge base
- ✅ `WebSearch` - Search for best practices
**Rationale**: Learning requires broad data access and storage

### 17. Logger
**Purpose**: Session and audit logging
**Recommended Tools**:
- ✅ `Write` - Write log files
- ✅ `Read` - Read existing logs
- ✅ `mcp__memory__retrieve` - Get session data
- ✅ `Bash` - Check system status (restricted)
**Rationale**: Logging needs file system access

### 18. Memory-Monitor
**Purpose**: Resource usage tracking
**Recommended Tools**:
- ✅ `mcp__memory__retrieve` - Monitor memory state
- ✅ `Bash` - Check system resources (restricted)
- ✅ `Write` - Generate resource reports
- ✅ `mcp__code_execution` - Calculate metrics
**Rationale**: System monitoring requires OS-level access

### 19. Node-Verification
**Purpose**: Schema validation
**Recommended Tools**:
- ✅ `mcp__web-fetch__fetch` - Fetch node schemas
- ✅ `Read` - Read node definitions
- ✅ `mcp__code_execution` - Validate schemas
- ✅ `Write` - Generate verification reports
**Rationale**: Schema validation needs external data

### 20. Visualizer
**Purpose**: Preview generation
**Recommended Tools**:
- ✅ `mcp__memory__retrieve` - Get workflow data
- ✅ `mcp__code_execution` - Generate visualizations
- ✅ `Write` - Save preview images
- ✅ `WebFetch` - Fetch rendering libraries
**Rationale**: Visualization requires computational rendering

### 21. Workflow-Chunker
**Purpose**: Large workflow handling
**Recommended Tools**:
- ✅ `Read` - Read large workflows
- ✅ `mcp__code_execution` - Split algorithms
- ✅ `Write` - Save chunks
- ✅ `mcp__memory__store` - Track chunk relationships
**Rationale**: Chunking requires algorithmic processing

### 22. Issue-Tracker
**Purpose**: Maintains KNOWN_ISSUES_TRACKER.md
**Recommended Tools**:
- ✅ `Read` - Read issue tracker
- ✅ `Edit` - Update issues
- ✅ `WebSearch` - Search for solutions
- ✅ `Write` - Create issue reports
**Rationale**: Issue management needs file manipulation

### 23. Orchestrator
**Purpose**: Master coordinator
**Recommended Tools**:
- ✅ `Task` - Delegate to all agents
- ✅ `mcp__memory__store` - Initialize SCS
- ✅ `mcp__memory__retrieve` - Monitor SCS
- ✅ `TodoWrite` - Manage task lists
- ✅ `Read` - Read protocols
**Rationale**: Coordination role, not execution

---

## 🌐 NEW AGENT: Workflow-Researcher

### Purpose
Analyze successful online workflows to extract patterns, techniques, and innovations for continuous improvement.

### Core Capabilities
- Search popular workflow sharing platforms
- Analyze high-rated workflows
- Extract novel techniques and patterns
- Learn from community best practices
- Monitor trending workflow styles

### Recommended Tools
- ✅ `WebSearch` - Search workflow platforms
- ✅ `WebFetch` - Fetch workflow details
- ✅ `mcp__brave-search__search` - Search multiple sources
- ✅ `mcp__memory__store` - Store discovered patterns
- ✅ `mcp__code_execution` - Analyze workflow structures
- ✅ `Write` - Generate insight reports
- ✅ `Task` - Delegate to Learning-Agent

### Target Platforms
1. **Civitai** - Model and workflow sharing
2. **OpenArt** - AI art workflows
3. **GitHub** - ComfyUI workflow repositories
4. **Reddit** - r/comfyui, r/StableDiffusion
5. **Discord** - ComfyUI community servers
6. **HuggingFace** - Model cards with workflows

### Analysis Criteria
- ⭐ Star/Like count
- 💬 Comment engagement
- 🔄 Fork/Remix count
- 📈 View count
- 🏆 Featured/Curated status
- 📅 Recency (trending vs established)

### Workflow-Researcher Agent Definition
```yaml
name: workflow-researcher
version: 2.0
purpose: Learn from successful online workflows
capabilities:
  - Search workflow platforms for highly-rated examples
  - Analyze workflow patterns and techniques
  - Extract innovative node combinations
  - Identify trending styles and methods
  - Report insights to Learning-Agent
  
search_queries:
  - "ComfyUI workflow {stars:>100}"
  - "StableDiffusion workflow popular"
  - "innovative ComfyUI techniques"
  - "trending AI art workflows {date:recent}"
  
analysis_pipeline:
  1. Search for high-performing workflows
  2. Fetch workflow JSON/details
  3. Parse and analyze structure
  4. Extract unique patterns
  5. Compare with existing knowledge
  6. Store new insights
  7. Generate improvement recommendations

output_format:
  insights:
    - pattern_name: string
    - description: string
    - popularity_score: float
    - complexity: low|medium|high
    - applicable_to: [workflow_types]
    - implementation_guide: string
```

---

## Tool Access Security Levels

### Level 1: Read-Only
- Can only read existing data
- No modification capabilities
- Agents: Node-Verification, Graph-Analyzer (initial phase)

### Level 2: Memory Access
- Read + Shared memory access
- Can store/retrieve from SCS
- Agents: Most analytical agents

### Level 3: File Modification
- Memory + File write/edit
- Can create and modify files
- Agents: Serializer, Logger, Issue-Tracker

### Level 4: Code Execution
- File + Algorithm execution
- Can run Python modules
- Agents: Layout-*, Graph-Engineer, Validators

### Level 5: Web Access
- Code + External web access
- Can search and fetch online
- Agents: Asset-Finder, Workflow-Researcher

### Level 6: System Access
- Web + Limited shell commands
- Restricted system operations
- Agents: Memory-Monitor, Logger

### Level 7: Full Delegation
- All tools + Task delegation
- Can invoke other agents
- Agents: Orchestrator only

---

## Implementation Guidelines

### Tool Initialization
```python
# Each agent should initialize with specific tools
agent_tools = {
    "parameter-extractor": ["Read", "mcp__memory__store", "Grep"],
    "asset-finder": ["mcp__brave-search__search", "WebSearch", "WebFetch"],
    # ... etc
}
```

### Rate Limiting
- Web searches: Max 10 per minute
- API calls: Max 100 per hour
- File writes: Max 50 per session
- Code execution: Max 30 seconds per run

### Error Handling
- All agents must handle tool failures gracefully
- Fallback strategies for unavailable tools
- Report tool issues to Issue-Tracker

### Monitoring
- Log all tool usage
- Track success/failure rates
- Optimize tool allocation based on usage patterns

---

## Benefits of Tool Specialization

1. **Efficiency**: Agents only load needed tools
2. **Security**: Minimal access reduces risk
3. **Performance**: Faster agent initialization
4. **Clarity**: Clear agent responsibilities
5. **Scalability**: Easy to add new tools/agents
6. **Debugging**: Easier to trace tool usage

---

## Future Enhancements

### Proposed New Tools
1. **ImageAnalyzer** - Analyze generated images
2. **WorkflowDiff** - Compare workflow versions
3. **PerformanceProfiler** - Measure workflow efficiency
4. **CommunityConnector** - Interface with forums/Discord
5. **ModelAnalyzer** - Analyze model capabilities

### Proposed New Agents
1. **Workflow-Optimizer** - Optimize for performance
2. **Style-Specialist** - Apply artistic styles
3. **Compatibility-Checker** - Ensure node compatibility
4. **Documentation-Generator** - Auto-generate docs
5. **Workflow-Translator** - Convert between formats

---

*Last Updated: 2025-08-17*
*Version: 2.0*
*Status: PROPOSED*