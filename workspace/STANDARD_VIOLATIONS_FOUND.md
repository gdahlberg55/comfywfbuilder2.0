# Standard Violations Found During Cleanup
Date: 2025-08-31

## Naming Convention Violations

### STANDARD REQUIREMENT:
`{project}_{version}_{timestamp}_{stage}.json`

### FILES NOT FOLLOWING STANDARD:

#### 1. Missing Version Numbers:
- `consistent_character_ultimate.json` → Should be: `consistent_character_v1_20250828_2318_ultimate.json`
- `illustrious_lora_upscale_professional.json` → Should be: `illustrious_lora_v1_20250827_1404_upscale_professional.json`
- `seamless_loop_original.json` → Should be: `seamless_loop_v1_20250827_1324_original.json`

#### 2. Inconsistent Version Placement:
- `flux_creative_nsfw_diamond_20250127.json` → Should be: `flux_v1_20250127_1016_creative_nsfw_diamond.json`
- `flux_nsfw_grid_layout_20250127.json` → Should be: `flux_v1_20250127_1117_nsfw_grid_layout.json`

#### 3. Missing Timestamps (HHMMSS):
- All flux files have date but missing time: `20250127` should be `20250127_HHMMSS`
- Example: `flux_nsfw_organized_upscale_20250127.json` → `flux_v1_20250127_1101_nsfw_organized_upscale.json`

#### 4. Inconsistent Naming Patterns:
- Some use `workflow` suffix, others don't
- `pony_ultimate_upscale_workflow.json` vs `pony_ultimate_wan21_adetailer.json`
- Should consistently be: `pony_v1_TIMESTAMP_feature.json`

## Root Directory Violations (Fixed by Cleanup):

### FILES THAT WERE IN ROOT (Should be in subdirectories):
1. `metadata.json` (multiple versions) - Should have been in versioned folders
2. `workflow.json` - Generic name without context
3. `parameters.json` - Should be workflow-specific
4. `illustrious_xl_optimized_workflow.json` - Was in root instead of workspace

## Directory Structure Violations:

### MISSING VERSIONED FOLDERS:
- Workflows saved directly to `CURRENT/` instead of:
  ```
  workspace/output/workflows/v{N}_{YYYYMMDD}_{HHMMSS}_{descriptor}/
  ├── workflow.json
  ├── metadata.json
  └── report.md
  ```

### NO METADATA OR REPORTS:
- Each workflow should have accompanying:
  - `metadata.json` with generation details
  - `report.md` with validation results
  - `preview.png` if possible

## Other Issues Found:

1. **No automatic versioning**: When creating iterations (v2, v3), not incrementing properly
2. **Missing stage descriptors**: Files should indicate stage (base, refined, organized, etc.)
3. **Inconsistent separators**: Mix of underscores and lack of clear separation
4. **No archive rotation**: Old files staying in CURRENT instead of moving to archive/

## Recommendations for Future:

1. **ENFORCE NAMING AT GENERATION TIME**:
   ```python
   filename = f"{project}_v{version}_{timestamp}_{stage}.json"
   # Example: flux_v1_20250831_143022_base.json
   ```

2. **CREATE VERSIONED FOLDERS**:
   ```
   workspace/output/workflows/v1_20250831_143022_flux_base/
   ```

3. **ALWAYS GENERATE METADATA**:
   - Track model used
   - Track generation parameters
   - Track agent pipeline used

4. **USE CONSISTENT STAGES**:
   - base
   - refined
   - organized
   - ultimate
   - experimental

5. **AUTO-INCREMENT VERSIONS**:
   - Check existing versions before saving
   - Increment automatically

This document should be referenced when generating new workflows to ensure standards are followed from the start.