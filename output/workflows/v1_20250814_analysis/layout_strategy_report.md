# Engineering Layout Strategy Report
## Wan 2.1 - Seamless Loop Workflow v1.2

### Executive Summary
This layout strategy implements a professional engineering drawing approach with:
- **1500px horizontal spacing** between major stages
- **600px vertical separation** for parallel processes
- **5 dedicated data bus lanes** for clean routing
- **8 vertical routing channels** with nested sub-channels
- **Strict orthogonal (90°) routing** - no splines or diagonals

### Key Design Decisions

#### 1. Spacing Strategy (1500-2000px Recommended)
- **Horizontal Stage Gap**: 1500px - provides ample room for routing channels
- **Vertical Parallel Gap**: 600px - separates two-pass sampling clearly
- **Bus Lane Spacing**: 200px - prevents visual congestion
- **Node Minimum**: 80px - ensures readable labels

#### 2. Data Bus Architecture
Located above main workflow area for clean access:
- **MODEL_BUS** (Y: -2400): Routes model data across 10 nodes
- **CLIP_BUS** (Y: -2200): Handles text encoding connections
- **VAE_BUS** (Y: -2000): Distributes VAE to decode points
- **IMAGE_BUS** (Y: -1800): Manages image flow between stages
- **CONDITIONING_BUS** (Y: -1600): Routes conditioning data

#### 3. Vertical Processing Zones
Eight zones create clear workflow progression:
1. **Input Zone** (X: -2000): All loaders grouped
2. **Model Processing** (X: -1400 to -400): Sequential LoRA chain
3. **Conditioning** (X: -800 to -200): Text encoding
4. **Sampling** (X: -200 to 400): Two-pass system
5. **Decode** (X: 500 to 800): VAE operations
6. **Frame Processing** (X: 1200 to 2200): RIFE interpolation
7. **Preview** (X: 2300 to 2900): Quick outputs
8. **Final Output** (X: 3300 to 4300): Full quality save

#### 4. Orthogonal Routing Rules
All connections follow engineering standards:
- Exit nodes horizontally to nearest channel
- Use bus lanes for distances > 1000px
- Drop vertically at destination X
- Add reroute nodes at every 90° turn
- Maintain 40px spacing between parallel routes

### Problem Resolutions

#### Long Connection Management
Previous issues with 1400px+ connections resolved by:
- Dedicated bus lanes eliminate diagonal sprawl
- Breakout points at key X-coordinates
- Clean vertical drops to targets

#### Sampling Area Congestion
Two-pass sampling previously overlapped, now:
- Pass 1: Y range -2600 to -2000
- Pass 2: Y range -1900 to -1300
- 100px buffer zone prevents overlap

#### Nested Channel Implementation
Complex areas use sub-channels:
```
Main Channel (X: 0) - Sampling Zone
├── Sub-channel -20: Sigma connections
├── Sub-channel 0: Main sampler flow
└── Sub-channel +20: CFG guide connections
```

### Stage Layout Details

| Stage | X Range | Y Range | Node Count | Purpose |
|-------|---------|---------|------------|---------|
| Input | -2000 to -1600 | -2600 to -1400 | 4 | Model/CLIP/VAE/Image loaders |
| Model Pipeline | -1400 to -400 | -2600 to -1800 | 7 | LoRA chain and enhancements |
| Conditioning | -800 to -200 | -1700 to -1200 | 4 | Positive/negative prompts |
| Sampling Pass 1 | -200 to 400 | -2600 to -2000 | 6 | First generation pass |
| Sampling Pass 2 | -200 to 400 | -1900 to -1300 | 3 | Refinement pass |
| Frame Processing | 1200 to 2200 | -1700 to -900 | 13 | RIFE interpolation system |
| Final Output | 3300 to 4300 | -2600 to -1000 | 6 | Full quality renders |

### Implementation Priority
1. **Critical**: Position nodes in defined stages
2. **Critical**: Create bus lanes at exact Y positions
3. **High**: Route MODEL/VAE connections first (most complex)
4. **High**: Implement sampling zone sub-channels
5. **Medium**: Add reroute nodes at turns
6. **Low**: Fine-tune 20px grid alignment

### Success Metrics
- ✓ No overlapping long connections
- ✓ Clear visual hierarchy left-to-right
- ✓ Parallel processes vertically separated
- ✓ All routing at 90° angles
- ✓ Professional engineering aesthetic
- ✓ 1500px+ spacing prevents cramping

### Next Steps
This layout strategy is ready for:
1. Reroute-Engineer to implement bus routing
2. Layout-Refiner to apply collision detection
3. Group-Coordinator to create visual clusters

The engineering approach ensures scalability for complex workflows while maintaining professional clarity.