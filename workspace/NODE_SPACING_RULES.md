# CRITICAL NODE SPACING RULES - MUST FOLLOW

## THE PROBLEM (RECURRING ISSUE)
User has complained DAY AFTER DAY, SESSION AFTER SESSION about overlapping nodes.
This is the #1 complaint that MUST be fixed.

## MINIMUM SPACING REQUIREMENTS (NON-NEGOTIABLE)

### Vertical Spacing (REFINED - User Feedback 2025-08-31):
- **OPTIMAL**: 100-150px between node bottoms and next node tops
- **SAFE MINIMUM**: 80px (tighter is acceptable, user confirmed)
- **CALCULATION**: Next Y = Previous Y + Node Height + 100px
- **Example**: 
  - Node 1: pos [100, 100], size [315, 98] 
  - Node 2: pos [100, 298] (was 448, now tighter)
- **NOTE**: 250px was TOO MUCH - can be tightened considerably
  
### Horizontal Spacing:
- **MINIMUM**: 500px between columns
- **CALCULATION**: Next X = Previous X + Node Width + 500px
- **Example**:
  - Column 1: X = 100 (width 315)
  - Column 2: X = 915 (NOT 415!)

### Node Size Ranges (MUST ACCOUNT FOR):
- **Small nodes**: 200x50px (labels, primitives)
- **Medium nodes**: 315x100px (loaders, encode)
- **Large nodes**: 400x300px (samplers, displays)
- **Extra large**: 400x400px (preview images)

## PROPER SPACING EXAMPLE:

```
Column 1 (X=100):
- Node 1: Y=100 (height 98)
- Node 2: Y=348 (100 + 98 + 250)
- Node 3: Y=648 (348 + 100 + 250)

Column 2 (X=615):  // 100 + 315 + 200
- Node 4: Y=100
- Node 5: Y=400
- Node 6: Y=700

Column 3 (X=1230): // 615 + 315 + 300
- Node 7: Y=100
- Node 8: Y=500
```

## GROUP BOUNDARIES:
- **Padding**: 50px minimum on ALL sides
- **Formula**: 
  - Group X = Min Node X - 50
  - Group Y = Min Node Y - 50
  - Group Width = (Max Node X + Node Width) - Group X + 50
  - Group Height = (Max Node Y + Node Height) - Group Y + 50

## VALIDATION CHECKLIST:
- [ ] No node Y positions closer than 250px (accounting for height)
- [ ] No column X positions closer than 500px (accounting for width)
- [ ] All groups have 50px padding from contained nodes
- [ ] Preview images have extra space (400px height)
- [ ] Samplers have extra space (334px height typical)

## PNG WORKFLOW EXTRACTION:
User's workflows are embedded in PNGs. Extract and compare to ensure proper spacing.

## THIS IS CRITICAL:
If nodes overlap, the workflow is UNUSABLE. This has been happening for too long.
ALWAYS err on the side of TOO MUCH space rather than too little.

When in doubt: ADD MORE SPACE!