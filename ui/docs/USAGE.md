# Usage Guide

How to use the ComfyUI Workflow Builder Web UI.

## Getting Started

### 1. Access the Application

Open your browser and navigate to http://localhost:5173

You should see the ComfyUI Workflow Builder interface with:
- **Left Panel**: Workflow configuration form
- **Right Panel**: Progress tracker and output viewer

### 2. Create Your First Workflow

#### Basic Workflow Generation

1. **Enter Description**: In the text area, describe your workflow in natural language
   ```
   Create a Flux workflow with LoRA support and 2-pass upscaling
   ```

2. **Select Model Type**: Choose from:
   - Flux (recommended for quality)
   - SDXL (Stable Diffusion XL)
   - Pony (Pony Diffusion)
   - SD 1.5 (Stable Diffusion 1.5)

3. **Set Resolution**: Choose width and height
   - Flux/SDXL: 1024x1024 recommended
   - SD 1.5: 512x512 recommended

4. **Click "Generate Workflow"**

#### Advanced Options

Click "Show Advanced Options" to access:

- **Sampling Steps**: Number of denoising steps (20-50 typical)
- **Include Upscaling Pass**: Add multi-pass upscaling
- **Include ADetailer**: Add face/detail enhancement

### 3. Monitor Progress

Watch the real-time progress as agents work:

**Generation Pipeline (Mode 1):**
1. Parameter Extraction
2. Asset Discovery
3. Prompt Optimization
4. Workflow Design
5. Node Selection
6. Connection Wiring

**Organization Pipeline (Mode 2):**
7. Graph Analysis
8. Layout Planning
9. Route Optimization
10. Layout Refinement
11. Group Organization
12. Naming Convention
13. Validation
14. Serialization

Each agent will show:
- ⚪ Pending (not started)
- 🔵 Running (in progress)
- ✅ Completed (finished)
- ❌ Failed (error)

### 4. Review Output

Once generation completes:

#### JSON View
- View the complete workflow JSON
- Syntax highlighted
- Read-only editor

#### Visual View (Coming Soon)
- Graphical representation of workflow
- Node connections
- Group visualization

#### Download
Click the "Download" button to save the workflow JSON file to your computer.

### 5. Import to ComfyUI

To use the generated workflow in ComfyUI:

1. Download the workflow JSON
2. Open ComfyUI in your browser
3. Drag and drop the JSON file onto ComfyUI
4. Or use "Load" button in ComfyUI

## Example Workflows

### Basic Image Generation

```
Create a simple Flux workflow for generating high-quality images
```

### Advanced Multi-Pass Rendering

```
Build a SDXL workflow with:
- Base generation at 1024x1024
- Hi-res fix pass with 0.3 denoise
- 2x upscale using Ultimate SD Upscale
- ADetailer for face enhancement
```

### LoRA-Enhanced Workflow

```
Generate a Pony workflow with:
- 3 LoRA models for style control
- Wildcard support for varied prompts
- Multi-pass rendering pipeline
- Face and hand detailer
```

### ControlNet Integration

```
Create a Flux workflow with:
- Canny edge ControlNet
- Depth map ControlNet
- Multi-pass upscaling
- Final quality refinement
```

## Workflow History

The History panel shows all previously generated workflows.

### Viewing Past Workflows

1. Click "History" tab
2. Browse workflow list
3. Click clock icon to load workflow
4. Click download icon to download
5. Click trash icon to delete

### History Features

- Workflows sorted by creation date
- Status indicators (completed/failed/processing)
- Model type badges
- Quick actions (view/download/delete)

## Tips for Better Results

### Writing Good Descriptions

**Good Examples:**
- ✅ "Create a Flux workflow with LoRA support, 2-pass upscaling, and ADetailer"
- ✅ "Build a SDXL workflow for portrait generation with face enhancement"
- ✅ "Generate a multi-pass rendering pipeline with ultimate upscale"

**Poor Examples:**
- ❌ "Make workflow" (too vague)
- ❌ "Image gen" (insufficient detail)
- ❌ Technical JSON structure (use natural language)

### Model Selection

- **Flux**: Best for quality, modern features
- **SDXL**: Good balance of quality and compatibility
- **Pony**: Specialized for certain styles
- **SD 1.5**: Maximum compatibility, lower quality

### Resolution Guidelines

| Model | Recommended | Min | Max |
|-------|-------------|-----|-----|
| Flux | 1024x1024 | 512x512 | 2048x2048 |
| SDXL | 1024x1024 | 512x512 | 2048x2048 |
| Pony | 1024x1024 | 512x512 | 1536x1536 |
| SD 1.5 | 512x512 | 256x256 | 1024x1024 |

### Upscaling Options

- **2-Pass**: Fast, good quality
- **3-Pass**: Better quality, slower
- **4-Pass**: Maximum quality, slowest

### Common Features

- **LoRA Support**: Add style/quality enhancements
- **Wildcards**: Randomize prompts
- **ADetailer**: Enhance faces and hands
- **ControlNet**: Guided generation
- **Ultimate SD Upscale**: Professional upscaling

## Keyboard Shortcuts

- `Ctrl/Cmd + Enter`: Generate workflow
- `Ctrl/Cmd + D`: Download current workflow
- `Esc`: Close modals

## Troubleshooting

### Generation Fails

1. Check description is clear and specific
2. Verify model type is appropriate
3. Check resolution is within limits
4. Review backend logs for errors

### Slow Generation

- Normal: 30-60 seconds
- Complex workflows: 1-3 minutes
- If longer: Check backend resources

### Download Issues

- Ensure generation is complete
- Check browser download settings
- Try different browser if issues persist

## Next Steps

- Experiment with different descriptions
- Try various model types
- Explore advanced options
- Import workflows into ComfyUI
- Share successful workflows

## Support

For help:
- Check [SETUP.md](SETUP.md) for installation issues
- Review [API.md](API.md) for technical details
- Consult backend logs in `logs/` directory
