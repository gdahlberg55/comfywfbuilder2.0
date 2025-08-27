# Node Spacing Calculator
## Reference for Layout Agents

### Purpose
This document provides precise formulas for calculating node positions to ensure no overlaps and professional spacing.

## Node Height Reference

### Common Node Heights
```
SMALL NODES (50-100px):
- Loaders: 58-82px
- Basic nodes: 46-58px  
- Primitives: 50-80px

MEDIUM NODES (100-200px):
- Text Encode: 100-200px
- Schedulers: 106px
- CLIP nodes: 106-150px
- Wildcards: 200px

LARGE NODES (200-400px):
- Power Lora Loader: 340px
- SamplerCustomAdvanced: 326px
- KSampler: 270px

EXTRA LARGE (400px+):
- UltimateSDUpscale: 614px
- Complex processors: 400-800px
```

## Spacing Formula

### Vertical Spacing Calculation
```python
def calculate_vertical_spacing(node_heights):
    """
    Calculate Y positions for nodes in a column
    
    Args:
        node_heights: List of node heights in pixels
    
    Returns:
        List of Y positions
    """
    positions = []
    current_y = group_y + 50  # Header clearance
    
    for i, height in enumerate(node_heights):
        positions.append(current_y)
        
        # Determine gap based on node size
        if height < 100:
            gap = 200  # Small node
        elif height < 200:
            gap = 250  # Medium node
        elif height < 400:
            gap = 450  # Large node
        else:
            gap = 600  # Extra large
            
        # Next position = current + gap
        current_y += gap
    
    return positions
```

### Example Calculations

#### Model Loading Column
```
Node 1: UNETLoader (82px)
  Position: Y=80
  Next gap: 200px (small node)

Node 2: DualCLIPLoader (106px)
  Position: Y=280 (80 + 200)
  Next gap: 250px (medium node)

Node 3: VAELoader (58px)
  Position: Y=530 (280 + 250)
  Next gap: 200px (small node)

Node 4: ModelSampling (130px)
  Position: Y=730 (530 + 200)
```

#### Sampling Column
```
Node 1: SamplerCustom (326px)
  Position: Y=80
  Next gap: 450px (large node)

Node 2: VAEDecode (46px)
  Position: Y=530 (80 + 450)
```

## Horizontal Spacing

### Column Distribution
```python
def calculate_column_positions(group_x, group_width, num_columns, node_widths):
    """
    Calculate X positions for columns in a group
    
    Args:
        group_x: Group starting X
        group_width: Total group width
        num_columns: Number of columns
        node_widths: Max width per column
    
    Returns:
        List of X positions per column
    """
    padding = 20  # Edge padding
    usable_width = group_width - (2 * padding)
    
    if num_columns == 1:
        return [group_x + padding]
    
    # Calculate column spacing
    total_node_width = sum(node_widths)
    remaining_space = usable_width - total_node_width
    column_gap = remaining_space / (num_columns - 1)
    
    # Minimum 400px between columns
    column_gap = max(column_gap, 400)
    
    positions = []
    current_x = group_x + padding
    
    for width in node_widths:
        positions.append(current_x)
        current_x += width + column_gap
    
    return positions
```

## Group Sizing

### Calculate Group Bounds
```python
def calculate_group_bounds(nodes):
    """
    Calculate bounding box for a group
    
    Args:
        nodes: List of nodes with pos and size
    
    Returns:
        [x, y, width, height]
    """
    if not nodes:
        return [0, 0, 100, 100]
    
    # Find extremes
    min_x = min(n['pos'][0] for n in nodes)
    min_y = min(n['pos'][1] for n in nodes)
    max_x = max(n['pos'][0] + n['size'][0] for n in nodes)
    max_y = max(n['pos'][1] + n['size'][1] for n in nodes)
    
    # Add padding
    padding = 20
    header_space = 50
    
    return [
        min_x - padding,
        min_y - header_space,
        (max_x - min_x) + (2 * padding),
        (max_y - min_y) + header_space + padding
    ]
```

## Validation Checks

### No Overlap Check
```python
def check_no_overlaps(nodes):
    """
    Verify no nodes overlap
    
    Returns:
        List of overlapping pairs
    """
    overlaps = []
    
    for i, node1 in enumerate(nodes):
        x1, y1 = node1['pos']
        w1, h1 = node1['size']
        
        for node2 in nodes[i+1:]:
            x2, y2 = node2['pos']
            w2, h2 = node2['size']
            
            # Check AABB collision
            if (x1 < x2 + w2 and 
                x1 + w1 > x2 and
                y1 < y2 + h2 and
                y1 + h1 > y2):
                overlaps.append((node1['id'], node2['id']))
    
    return overlaps
```

## Quick Reference Table

| Node Type | Height | Min Y-Gap | Safe Y-Gap |
|-----------|--------|-----------|------------|
| Tiny (< 50px) | 46px | 150px | 200px |
| Small (50-100px) | 82px | 180px | 200px |
| Medium (100-200px) | 150px | 200px | 250px |
| Large (200-400px) | 326px | 400px | 450px |
| XL (400px+) | 614px | 550px | 600px |

## Common Patterns

### Standard 4-Node Column
```
Y=80   - Node 1 (small)
Y=280  - Node 2 (small) 
Y=480  - Node 3 (medium)
Y=730  - Node 4 (small)
```

### Mixed Size Column
```
Y=80   - Large node (326px)
Y=530  - Small node (46px)
Y=730  - Medium node (150px)
```

### Dense Packing (Not Recommended)
```
Y=80   - Node 1
Y=180  - Node 2 (100px gap - TOO CLOSE!)
Y=280  - Node 3
```

---
*Use these calculations to ensure professional, overlap-free layouts*