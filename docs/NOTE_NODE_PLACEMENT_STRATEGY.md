# Note Node Placement Strategy

## Core Principles
Maximize workflow clarity while minimizing wasted space

## Placement Rules

### 1. Standard Placement (Compact Workflows)
- **Between Groups**: If gap < 100px, place thin (30px) notes in gaps
- **Color Matching**: Note color matches associated group color
- **Keep Thin**: 30px height max for between-group notes

### 2. Side Placement (Large Workflows)
- **When to Use**:
  - Gap between groups would exceed 100px with note
  - Workflow has >30 nodes (vertical space precious)
  - Instructions are lengthy (>50 characters)
  
- **Positioning Logic**:
  ```
  IF node.x < workflow_centerline:
      place_note_left_side
  ELSE:
      place_note_right_side
  ```

### 3. Model Links Section
- **Dedicated Note Group**: Single tall note on side
- **Contents**:
  - Model download links (HuggingFace, Civitai)
  - File paths and versions
  - Requirements and dependencies
- **Color Coding**: Match sections or use neutral

## Layout Variants

### Compact Layout (Current)
- Notes in gaps between groups
- 30px thin profile
- Minimal text

### Extended Layout (Future)
- Side notes with detailed instructions
- Model links section
- More verbose guidance

### Professional Layout (Future)
- No notes visible (assume user expertise)
- Maximum density
- Focus on node connections

## Visual Example
```
[Left Notes]    [Main Workflow]    [Right Notes]
                     GROUP 1
   🔵 Models  ←     [Nodes]
                     
                   [Thin Note]       → 🟠 Details
                     
                     GROUP 2
                    [Nodes]
```

## Implementation Priority
1. ✅ Compact with thin notes (DONE)
2. ⬜ Side notes for large workflows
3. ⬜ Model links section
4. ⬜ Professional no-notes variant