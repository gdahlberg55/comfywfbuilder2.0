# 🚨 CRITICAL: FRONTEND/UI FORMAT REQUIREMENT 🚨

## THE #1 RULE: ALWAYS USE FRONTEND FORMAT FOR DELIVERABLES

### What is Frontend/UI Format?
The Frontend/UI format is the **COMPLETE** workflow format that ComfyUI saves when you:
- Save a workflow in the ComfyUI editor
- Embed a workflow into a PNG file
- Export from ComfyUI interface

This format contains **BOTH**:
1. **Execution Logic** - The nodes, connections, and parameters needed to run the workflow
2. **Visual Layout Metadata** - The positioning, sizing, and visual properties for the editor

### What is API Format? (NEVER USE FOR DELIVERABLES)
The API format is a stripped-down version containing ONLY execution logic:
- ❌ NO visual positioning (`pos`)
- ❌ NO node sizes (`size`)
- ❌ NO widget values array structure
- ❌ NO visual flags or properties
- ❌ CANNOT be properly loaded in ComfyUI editor
- ❌ LOSES all layout organization

## Required Properties for Frontend Format

### Every Node MUST Have:
```json
{
  "id": 1,
  "type": "LoadImage",
  "pos": [100, 200],              // REQUIRED: Visual position
  "size": [315, 314],             // REQUIRED: Node dimensions
  "flags": {},                    // REQUIRED: Collapse/pin state
  "order": 0,                     // REQUIRED: Execution order
  "mode": 0,                      // REQUIRED: 0=active, 1=muted, 2=bypassed
  "inputs": [...],                // Node connections
  "outputs": [...],               // Output slots
  "properties": {},               // Node-specific properties
  "widgets_values": [...]         // REQUIRED: Widget configuration values
}
```

### Groups MUST Have:
```json
{
  "title": "Group Title",
  "bounding": [x, y, width, height],  // NOT "bounding_box"!
  "color": "#3f789e",                 // From COLOR_SCHEME.md
  "font_size": 24,
  "flags": {}
}
```

### Links Format:
```json
[
  link_id,
  source_node_id,
  source_slot_index,
  target_node_id,
  target_slot_index,
  "TYPE_NAME"
]
```

## Visual Properties Explained

### `pos` (Position)
- **Format**: `[x, y]` where x is horizontal, y is vertical
- **Origin**: Top-left corner of the canvas
- **Purpose**: Determines where the node appears in the editor

### `size` (Dimensions)
- **Format**: Either `[width, height]` or `{0: [width, height]}`
- **Minimum**: Usually around `[200, 50]` for simple nodes
- **Purpose**: Determines the visual size of the node box

### `widgets_values` (Widget Configuration)
- **Format**: Array of values corresponding to node's widgets
- **Order**: Must match the order of widgets in the node definition
- **Example**: For LoadImage: `["image.png", "image"]`

### `flags` (Visual State)
- **collapsed**: Boolean - Is node collapsed to title bar only?
- **pinned**: Boolean - Is node pinned in place?
- **Example**: `{"collapsed": false, "pinned": false}`

### `mode` (Execution State)
- **0**: Active (normal execution)
- **1**: Muted (skip but maintain connections)
- **2**: Bypassed (pass through without processing)

## Why This Matters

### User Experience:
- ✅ Workflows open with proper visual organization
- ✅ Users can immediately understand the workflow flow
- ✅ Professional appearance with aligned nodes and groups
- ✅ Maintains the layout work done during generation

### Without Frontend Format:
- ❌ All nodes pile up at position [0, 0]
- ❌ Complete loss of visual organization
- ❌ User must manually reposition everything
- ❌ Defeats the purpose of workflow organization

## Validation Checklist

Before delivering ANY workflow to the user:

1. ✅ Verify every node has `pos` property
2. ✅ Verify every node has `size` property
3. ✅ Verify every node has `widgets_values` array
4. ✅ Verify every node has `flags`, `order`, `mode`
5. ✅ Verify groups use `bounding` not `bounding_box`
6. ✅ Test load in ComfyUI editor (or simulate)
7. ✅ Confirm visual layout is preserved

## Common Mistakes to Avoid

### ❌ WRONG - API Format:
```json
{
  "1": {
    "class_type": "LoadImage",
    "inputs": {
      "image": "example.png",
      "upload": "image"
    }
  }
}
```

### ✅ CORRECT - Frontend Format:
```json
{
  "nodes": [
    {
      "id": 1,
      "type": "LoadImage",
      "pos": [100, 200],
      "size": [315, 314],
      "flags": {},
      "order": 0,
      "mode": 0,
      "outputs": [...],
      "properties": {},
      "widgets_values": ["example.png", "image"]
    }
  ],
  "links": [...],
  "groups": [...],
  "config": {},
  "extra": {},
  "version": 0.4
}
```

## REMEMBER: 
**Every workflow delivered to the user MUST be in Frontend/UI format with COMPLETE visual layout metadata. This is NON-NEGOTIABLE!**