# Agent Tool Assignments v2.0

## Philosophy
Each agent gets ONLY the tools needed for their specific role. This prevents:
- Accidental file corruption
- Scope creep
- Security issues
- Performance overhead

## Core Tool Categories

### Read-Only Tools (Information Gathering)
- Read, Glob, Grep, LS
- Safe for most agents

### Modification Tools (Change State)
- Write, Edit, MultiEdit
- Only for agents that produce outputs

### Execution Tools (Run Code)
- Bash, BashOutput, KillBash
- Only for agents running Python modules

### Memory Tools (SCS Communication)
- create_entities, search_nodes, etc.
- All agents need these for SCS

### Web Tools (External Data)
- brave_web_search, WebFetch
- Only for research agents

### Thinking Tools (Complex Logic)
- sequentialthinking
- Most agents benefit from this

## Agent-Specific Assignments

### Orchestrator
```yaml
tools:
  - Read          # Read workflows and configs
  - Glob          # Find files
  - Grep          # Search patterns
  - LS            # List directories
  - TodoWrite     # Manage task pipeline
  - sequentialthinking  # Complex coordination
  - All memory tools    # Manages entire SCS
```

### Parameter-Extractor
```yaml
tools:
  - sequentialthinking  # Parse complex NL
  - create_entities     # Store parameters
  - search_nodes        # Find existing params
```

### Asset-Finder
```yaml
tools:
  - brave_web_search    # Find models online
  - WebFetch           # Get model details
  - create_entities    # Cache findings
  - search_nodes       # Check cache first
```

### Prompt-Crafter
```yaml
tools:
  - sequentialthinking  # Craft optimized prompts
  - perplexity_ask     # Research prompt techniques
  - create_entities    # Store prompts
  - search_nodes       # Find trigger words
```

### Workflow-Architect
```yaml
tools:
  - Read               # Analyze example workflows
  - sequentialthinking # Design architecture
  - create_entities    # Store design
  - search_nodes       # Find patterns
```

### Node-Curator
```yaml
tools:
  - Read              # Read node schemas
  - Glob              # Find node definitions
  - Grep              # Search node properties
  - create_entities   # Store node selections
  - search_nodes      # Find compatible nodes
```

### Graph-Engineer
```yaml
tools:
  - sequentialthinking # Connection logic
  - create_entities    # Store graph
  - create_relations   # Store connections
  - search_nodes       # Find nodes to connect
```

### Graph-Analyzer
```yaml
tools:
  - Read              # Read workflows
  - sequentialthinking # Analysis logic
  - create_entities   # Store analysis
  - search_nodes      # Find patterns
```

### Layout-Strategist
```yaml
tools:
  - sequentialthinking # Calculate spacing
  - create_entities    # Store layout params
  - search_nodes       # Get current positions
```

### Reroute-Engineer
```yaml
tools:
  - Bash              # Run data_bus_router.py
  - create_entities   # Store routing
  - search_nodes      # Get connections
```

### Layout-Refiner
```yaml
tools:
  - Bash              # Run collision_detection.py
  - create_entities   # Store refined positions
  - search_nodes      # Get current layout
```

### Group-Coordinator
```yaml
tools:
  - sequentialthinking # Grouping logic
  - create_entities    # Store groups
  - search_nodes       # Find related nodes
```

### Nomenclature-Specialist
```yaml
tools:
  - sequentialthinking # Naming conventions
  - create_entities    # Store names
  - search_nodes       # Get current names
```

### Workflow-Validator
```yaml
tools:
  - Read              # Read workflows
  - Bash              # Run validation.py
  - create_entities   # Store results
  - search_nodes      # Get workflow data
```

### Templating-Enforcer
```yaml
tools:
  - Read              # Read Gold Standard
  - sequentialthinking # Compare standards
  - create_entities   # Store compliance
  - search_nodes      # Get workflow
```

### Workflow-Serializer
```yaml
tools:
  - Write             # Create JSON files
  - create_directory  # Version folders
  - Bash              # Run json_validator.py
  - search_nodes      # Get final graph
```

### Learning-Agent
```yaml
tools:
  - Read              # Read patterns
  - Write             # Update patterns
  - Edit              # Modify patterns
  - All memory tools  # Complete access for learning
  - sequentialthinking # Pattern recognition
```

### Logger
```yaml
tools:
  - Write             # Create logs
  - create_directory  # Log folders
  - create_entities   # Log to memory
  - search_nodes      # Get session data
```

### Memory-Monitor
```yaml
tools:
  - Bash              # Check system memory
  - create_entities   # Store metrics
  - search_nodes      # Track usage
```

### Visualizer
```yaml
tools:
  - Write             # Create preview files
  - playwright_screenshot # If available
  - search_nodes      # Get workflow data
```

### Workflow-Researcher
```yaml
tools:
  - brave_web_search  # Find workflows
  - WebFetch          # Analyze workflows
  - Write             # Create reports
  - create_entities   # Store findings
  - search_nodes      # Check existing research
```

### Issue-Tracker
```yaml
tools:
  - Read              # Read tracker file
  - Edit              # Update tracker
  - MultiEdit         # Batch updates
  - create_entities   # Store in memory
  - search_nodes      # Find issues
```

### Node-Verification
```yaml
tools:
  - Read              # Read schemas
  - Grep              # Search definitions
  - create_entities   # Store verification
  - search_nodes      # Find node info
```

### Workflow-Chunker
```yaml
tools:
  - Read              # Read large workflows
  - Write             # Write chunks
  - create_entities   # Store chunk map
  - search_nodes      # Track chunks
```

## Security Principles

1. **Least Privilege**: Only grant what's absolutely necessary
2. **Read Before Write**: Agents that write must be able to read
3. **No Cross-Domain Access**: Web agents don't get file system access
4. **Audit Trail**: All modifications through memory tools
5. **Validation Required**: Write access requires validation capability

## Tool Denial Reasons

### Why Most Agents DON'T Get Write/Edit:
- Prevents accidental corruption
- Forces proper pipeline flow
- Maintains single responsibility
- Ensures validation before output

### Why Most Agents DON'T Get Bash:
- Security risk
- Performance overhead
- Most don't need execution
- Python modules are specific to certain agents

### Why Most Agents DON'T Get Web Tools:
- Rate limiting concerns
- Most work with local data
- Prevents external dependencies
- Focused responsibilities

## Implementation Notes

1. Tools are defined in each agent's YAML frontmatter
2. Orchestrator validates tool access before delegation
3. Unauthorized tool use triggers error
4. All agents MUST have memory access for SCS
5. Consider adding `dry_run` mode for testing