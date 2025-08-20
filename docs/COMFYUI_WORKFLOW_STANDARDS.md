# ComfyUI Workflow Standards - Complete Reference

## Current Version: 2.0
**Last Updated**: 2025-08-17

## Core Documents Reference
- **CLAUDE.md** - Prime directive and orchestrator rules
- **WORKFLOW_SPACING_RULES.md** - Node positioning and group clearance
- **NOTE_NODE_PLACEMENT_STRATEGY.md** - Note placement logic
- **COLOR_SCHEME.md** - Group color standards
- **FILE_ORGANIZATION_PROTOCOL.md** - Naming and versioning

## 1. Node Positioning Standards

### Micro-Spacing (NEW)
- **2px gap** between directly adjacent nodes (prevents visual merging)
- Applied both horizontally and vertically
- Creates subtle visual separation

### Group Header Clearance
- **35px minimum** clearance from group top boundary
- Group headers are ~25-30px tall
- Formula: `Node_Y = Group_Y + 35`

### Standard Spacing Grid
```
Horizontal: 50-80px (+ 2px micro-gap)
Vertical:   20-70px (+ 2px micro-gap)
Group gaps: 20-40px
```

## 2. Node Naming Standards

### Node Titles
- Use **original/technical names** (e.g., "UNETLoader", "CLIPTextEncode")
- No step numbers in node titles
- Keep node type identifiable

### Group Titles
- Include step ranges: "STEP 1-3: MODELS"
- Use caps for clarity
- Keep concise

### Note Nodes
- Title stays as "Note"
- Content uses emoji + category (🔵 MODELS)
- Thin profile (30px height)

## 3. Layout Variants

### Compact Layout (Current Default)
- **Spacing**: 50-80px horizontal, 20-70px vertical
- **Notes**: Thin (30px) between groups
- **Density**: High
- **Use Case**: Standard workflows

### Future Layouts (Planned)
- **Extended**: Side notes, verbose instructions
- **Professional**: No notes, maximum density
- **Spacious**: 100-150px spacing for clarity

## 4. Color Standards

### Group Colors (from COLOR_SCHEME.md)
```
Models/Loading: #3f789e (Blue)
Inputs:         #b58b2a (Orange)
Conditioning:   #84a96e (Green)
Generation:     #a1309b (Purple)
Processing:     #8b4c9b (Violet)
Output:         #b06634 (Brown)
```

### Note Colors
- Match associated group color
- Use lighter shade for visibility
- Maintain contrast

## 5. Workflow Organization

### Left-to-Right Flow
1. Models/Loading (leftmost)
2. Inputs
3. Conditioning/Prompts
4. Generation/Sampling
5. Processing
6. Output/Save (rightmost)

### Vertical Stacking
- Similar operations stack vertically
- Positive above negative prompts
- Multiple inputs stack top-down

## 6. File Naming Convention
```
v{version}_{date}_{name}_{variant}.json
Example: v13_20250817_outfit_changer_compact.json
```

### Directory Structure
```
output/workflows/v{N}_{YYYYMMDD}_{name}/
├── {workflow}_compact.json      # Compact layout
├── {workflow}_extended.json     # Extended layout (future)
├── metadata.json                # Workflow metadata
└── README.md                    # Documentation
```

## 7. Quality Checklist

### Pre-Release
- [ ] 35px group header clearance
- [ ] 2px micro-gaps between nodes
- [ ] No overlapping elements
- [ ] Proper color coding
- [ ] Clear left-to-right flow
- [ ] Note nodes properly placed
- [ ] Original node names used
- [ ] Step numbers in group titles

### Validation
- [ ] Links properly connected
- [ ] All required properties present
- [ ] Groups have "bounding" property
- [ ] Nodes have slot_index defined
- [ ] Version number incremented

## 8. Best Practices

### Do's
✅ Add 2px micro-spacing between adjacent nodes
✅ Use original node type names
✅ Place thin notes between groups
✅ Include step numbers in group titles
✅ Follow color scheme exactly
✅ Test workflow before finalizing

### Don'ts
❌ Place nodes touching group headers
❌ Use custom names for standard nodes
❌ Create gaps larger than 100px
❌ Mix color schemes
❌ Overlap any elements

## 9. Implementation Priority

1. **Essential** (Must Have)
   - Proper spacing (including 2px gaps)
   - No overlaps
   - Clear flow
   - Working connections

2. **Important** (Should Have)
   - Color coding
   - Step numbering
   - Note guidance
   - Clean organization

3. **Nice to Have** (Could Have)
   - Multiple layout variants
   - Extended documentation
   - Visual previews

## 10. Version Control

### Version Increment Rules
- Major: New workflow type
- Minor: Significant reorganization
- Patch: Spacing/positioning fixes

### Change Log Format
```
v13: Added 2px micro-spacing
v12: Professional organization
v11: FLUX integration
```

## References
All standards derive from and must comply with:
- CLAUDE.md (Prime Directive)
- WORKFLOW_SPACING_RULES.md
- NOTE_NODE_PLACEMENT_STRATEGY.md
- COLOR_SCHEME.md
- FILE_ORGANIZATION_PROTOCOL.md

---
*This document represents the complete, current standards for ComfyUI workflow creation as of v2.0*