# ComfyUI Workflow Spacing Rules

## Group Header Clearance
**CRITICAL**: Nodes must NEVER overlap with group title bars (headers)

### Group Header Specifications
- Group headers in ComfyUI have a darker colored title bar at the top
- Standard header height: ~25-30 pixels
- The header color is always darker than the group body color

### Node Positioning Rules

#### 1. Vertical Spacing from Group Headers
- **Minimum clearance**: 35px from top of group bounding box
- **Formula**: First node Y position = Group_Y + 35
- **Example**: If group starts at Y:120, first node should be at Y:155 minimum

#### 2. Note Nodes Between Groups
- **Position**: Place note nodes in the gap BETWEEN groups
- **Size**: Make them thin (30px height) to fit in gaps
- **Placement**: 
  - At bottom of previous group
  - At top of next group
  - Centered in gap if space allows

#### 3. Standard Spacing Values
- **Group header clearance**: 35px minimum
- **Node to node vertical**: 20-70px (with 2px micro-gap between adjacent nodes)
- **Node to node horizontal**: 50-80px (with 2px micro-gap)
- **Micro-spacing**: 2px between directly adjacent nodes (prevents visual merging)
- **Group to group gap**: 20-40px
- **Note node height**: 30px (thin profile)

## Visual Example
```
┌─────────────────────┐ ← Group 1 Header (darker color)
│     Group Title     │
├─────────────────────┤ ← Header bottom
│                     │ ← 35px clearance zone
│   [First Node]      │ ← Node starts here
│                     │
└─────────────────────┘
     [Note Node]       ← Thin note in gap
┌─────────────────────┐ ← Group 2 Header
│     Group Title     │
├─────────────────────┤
│                     │
│   [First Node]      │
```

## Implementation Checklist
- [ ] All nodes start at least 35px below group header
- [ ] Note nodes are 30px height or less
- [ ] Note nodes positioned in gaps between groups
- [ ] No node overlaps with any group header
- [ ] Groups have appropriate padding for headers

## Color Coordination
- Note node colors should match their associated group
- Use lighter shade for note body
- Keep text concise to fit thin profile

## Updates Required
When creating any workflow:
1. Calculate group bounding box
2. Add 35px to Y for first node position
3. Place note nodes strategically in gaps
4. Verify no header overlaps before finalizing