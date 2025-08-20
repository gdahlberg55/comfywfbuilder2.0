# Compact Layout Specification

## Core Spacing Requirements

### Within Groups
- **Node to group edge**: 10-20px
- **Node to node**: 10-20px
- **Title bar clearance**: 10-20px below the group title bar
- **Never overlap**: Nodes must never overlap the group title text

### Between Groups
- **Group to group**: 10-15px horizontal and vertical

### Group Structure
- **Title Bar**: Darker shade of the group's base color (see COLOR_SCHEME.md)
- **Title Text**: White text on dark background
- **Content Area**: Where nodes are placed, starting 10-20px below title bar

### Notes Placement
(To be defined)

## Visual Example
```
┌─────────────────────────┐
│ GROUP TITLE (Dark)      │ <- Title bar (darker color)
├─────────────────────────┤
│  [10-20px gap]          │
│  ┌─────┐    ┌─────┐     │ <- Nodes start here
│  │Node1│    │Node2│     │
│  └─────┘    └─────┘     │
│  [10-20px]              │ <- Node spacing
│  ┌─────┐                │
│  │Node3│                │
│  └─────┘                │
│  [10-20px to edge]      │
└─────────────────────────┘
[10-15px gap]
┌─────────────────────────┐
│ NEXT GROUP              │
└─────────────────────────┘
```

## Key Principles
1. **Compact**: Everything close together but organized
2. **Clear Hierarchy**: Groups contain related nodes
3. **No Overlaps**: Maintain minimum spacing always
4. **Consistent**: Same spacing rules throughout workflow