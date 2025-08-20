"""
JSON Validator Module for ComfyUI Workflow Layout
Version 2.0 - Validates and auto-fixes ComfyUI workflow JSON structure
"""

import json
from typing import Dict, List, Any, Tuple, Optional, Union

# Type aliases for clarity
NodeT = Dict[str, Any]
LinkT = List[Any]  # [id, from_node, from_slot, to_node, to_slot, type]
GroupT = Dict[str, Any]
WorkflowT = Dict[str, Any]
SCS = Dict[str, Any]


class JSONValidator:
    """Validates and auto-fixes ComfyUI workflow JSON structure"""
    
    # Valid color codes from COLOR_SCHEME.md
    VALID_COLORS = {
        '#355335': 'Loaders (Green)',
        '#353553': 'Conditioning (Blue)',
        '#533535': 'Sampling (Red)',
        '#535335': 'Latent Operations (Yellow)',
        '#453553': 'Post-Processing (Purple)',
        '#444444': 'Utility (Black/Dark Gray)',
        '#534535': 'Control Networks (Orange)',
        '#355353': 'Image Input/Output (Teal)',
        '#533545': 'Custom Nodes (Pink)'
    }
    
    # Node type to color mapping for auto-fixing
    NODE_TYPE_COLORS = {
        'CheckpointLoaderSimple': '#355335',
        'VAELoader': '#355335',
        'LoraLoader': '#355335',
        'CLIPLoader': '#355335',
        'CLIPTextEncode': '#353553',
        'ConditioningCombine': '#353553',
        'ConditioningSetArea': '#353553',
        'KSampler': '#533535',
        'KSamplerAdvanced': '#533535',
        'SamplerCustom': '#533535',
        'VAEEncode': '#535335',
        'VAEDecode': '#535335',
        'LatentUpscale': '#535335',
        'EmptyLatentImage': '#535335',
        'ImageUpscaleWithModel': '#453553',
        'ImageScale': '#453553',
        'ImageComposite': '#453553',
        'PrimitiveNode': '#444444',
        'Note': '#444444',
        'Reroute': '#444444',
        'IntegerInput': '#444444',
        'ControlNetApply': '#534535',
        'ControlNetLoader': '#534535',
        'LoadImage': '#355353',
        'SaveImage': '#355353',
        'PreviewImage': '#355353'
    }
    
    def __init__(self):
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.auto_fixes: List[Dict[str, Any]] = []
        self.validation_summary: Dict[str, Any] = {}
    
    def _add_error(self, severity: str, location: str, message: str, fix_applied: bool = False):
        """Add an error or warning to the tracking lists"""
        entry = {
            'severity': severity,
            'location': location,
            'message': message,
            'fix_applied': fix_applied
        }
        
        if severity == 'error':
            self.errors.append(entry)
        elif severity == 'warning':
            self.warnings.append(entry)
            
        if fix_applied:
            self.auto_fixes.append(entry)
    
    def _fix_node_properties(self, node: NodeT) -> bool:
        """Fix missing required node properties"""
        fixed = False
        node_id = node.get('id', 'unknown')
        
        # Check and fix required properties
        if 'flags' not in node:
            node['flags'] = {}
            self._add_error('error', f'node_{node_id}', 
                          f"Node {node_id} missing 'flags' property - added empty flags", True)
            fixed = True
            
        if 'order' not in node:
            node['order'] = 0
            self._add_error('error', f'node_{node_id}', 
                          f"Node {node_id} missing 'order' property - set to 0", True)
            fixed = True
            
        if 'mode' not in node:
            node['mode'] = 0
            self._add_error('error', f'node_{node_id}', 
                          f"Node {node_id} missing 'mode' property - set to 0", True)
            fixed = True
            
        if 'properties' not in node:
            node['properties'] = {}
            # Try to set Node name for S&R if possible
            if 'type' in node:
                node['properties']['Node name for S&R'] = node['type']
            self._add_error('error', f'node_{node_id}', 
                          f"Node {node_id} missing 'properties' property - added default", True)
            fixed = True
            
        # Fix outputs slot_index
        if 'outputs' in node:
            for i, output in enumerate(node['outputs']):
                if 'slot_index' not in output:
                    output['slot_index'] = i
                    self._add_error('error', f'node_{node_id}_output_{i}', 
                                  f"Node {node_id} output missing 'slot_index' - set to {i}", True)
                    fixed = True
                    
        return fixed
    
    def _fix_group_properties(self, group: GroupT, index: int) -> bool:
        """Fix group property issues"""
        fixed = False
        group_title = group.get('title', f'Group_{index}')
        
        # Fix bounding_box -> bounding
        if 'bounding_box' in group and 'bounding' not in group:
            group['bounding'] = group['bounding_box']
            del group['bounding_box']
            self._add_error('error', f'group_{index}', 
                          f"Group '{group_title}' uses 'bounding_box' - changed to 'bounding'", True)
            fixed = True
        elif 'bounding' not in group:
            # Add default bounding if missing
            group['bounding'] = [0, 0, 400, 300]
            self._add_error('error', f'group_{index}', 
                          f"Group '{group_title}' missing 'bounding' - added default", True)
            fixed = True
            
        # Validate and fix color
        color = group.get('color')
        if color:
            if color not in self.VALID_COLORS:
                # Try to infer color from title or set default
                new_color = '#444444'  # Default to utility color
                title_lower = group_title.lower()
                
                if 'loader' in title_lower or 'model' in title_lower:
                    new_color = '#355335'
                elif 'condition' in title_lower or 'prompt' in title_lower:
                    new_color = '#353553'
                elif 'sampl' in title_lower:
                    new_color = '#533535'
                elif 'latent' in title_lower:
                    new_color = '#535335'
                elif 'post' in title_lower or 'process' in title_lower:
                    new_color = '#453553'
                elif 'control' in title_lower:
                    new_color = '#534535'
                elif 'image' in title_lower or 'input' in title_lower or 'output' in title_lower:
                    new_color = '#355353'
                    
                group['color'] = new_color
                self._add_error('warning', f'group_{index}', 
                              f"Group '{group_title}' invalid color '{color}' - changed to '{new_color}'", True)
                fixed = True
        
        return fixed
    
    def _validate_link_structure(self, link: LinkT, index: int) -> bool:
        """Validate link has correct structure"""
        if len(link) != 6:
            self._add_error('error', f'link_{index}', 
                          f"Link {index} has {len(link)} elements instead of 6 - cannot auto-fix", False)
            return False
        return True
    
    def _check_reroute_connections(self, workflow: WorkflowT) -> None:
        """Check for disconnected reroute nodes"""
        # Build connection maps
        input_connections = {}  # node_id -> list of incoming links
        output_connections = {}  # node_id -> list of outgoing links
        
        for link in workflow.get('links', []):
            if len(link) >= 4:
                source_node = link[1]
                target_node = link[3]
                
                if source_node not in output_connections:
                    output_connections[source_node] = []
                output_connections[source_node].append(link)
                
                if target_node not in input_connections:
                    input_connections[target_node] = []
                input_connections[target_node].append(link)
        
        # Check reroute nodes
        for node in workflow.get('nodes', []):
            if node.get('type') == 'Reroute':
                node_id = node.get('id')
                
                if node_id not in input_connections:
                    self._add_error('warning', f'reroute_{node_id}', 
                                  f"Reroute node {node_id} has no input connections", False)
                    
                if node_id not in output_connections:
                    self._add_error('warning', f'reroute_{node_id}', 
                                  f"Reroute node {node_id} has no output connections", False)
    
    def _check_duplicate_ids(self, workflow: WorkflowT) -> bool:
        """Check for duplicate node IDs"""
        node_ids = []
        for node in workflow.get('nodes', []):
            node_id = node.get('id')
            if node_id is not None:
                node_ids.append(node_id)
                
        if len(node_ids) != len(set(node_ids)):
            self._add_error('error', 'workflow', 
                          "Duplicate node IDs detected - cannot auto-fix", False)
            return False
        return True
    
    def validate_and_fix(self, scs_data: SCS) -> Dict[str, Any]:
        """
        Main validation and auto-fix function
        
        Args:
            scs_data: Shared Context System data containing workflow
            
        Returns:
            Validation results with auto-fixed issues and final JSON
        """
        # Reset tracking lists
        self.errors = []
        self.warnings = []
        self.auto_fixes = []
        
        # Extract workflow from SCS
        workflow = scs_data.get('workflow_state', {}).get('current_graph', {})
        if not workflow:
            return {
                'success': False,
                'error': 'No workflow found in SCS data',
                'validation_summary': {},
                'errors': [],
                'warnings': [],
                'auto_fixes': [],
                'fixed_workflow': None
            }
        
        # Make a deep copy for fixing
        import copy
        fixed_workflow = copy.deepcopy(workflow)
        
        # Track statistics
        total_nodes = len(fixed_workflow.get('nodes', []))
        total_links = len(fixed_workflow.get('links', []))
        total_groups = len(fixed_workflow.get('groups', []))
        
        # 1. Validate and fix nodes
        nodes_fixed = 0
        for node in fixed_workflow.get('nodes', []):
            if self._fix_node_properties(node):
                nodes_fixed += 1
        
        # 2. Validate and fix groups
        groups_fixed = 0
        for i, group in enumerate(fixed_workflow.get('groups', [])):
            if self._fix_group_properties(group, i):
                groups_fixed += 1
        
        # 3. Validate links (cannot auto-fix structural issues)
        valid_links = 0
        for i, link in enumerate(fixed_workflow.get('links', [])):
            if self._validate_link_structure(link, i):
                valid_links += 1
        
        # 4. Check for disconnected reroutes
        self._check_reroute_connections(fixed_workflow)
        
        # 5. Check for duplicate IDs
        has_unique_ids = self._check_duplicate_ids(fixed_workflow)
        
        # Determine overall validity
        is_valid = len(self.errors) == 0
        
        # Create validation summary
        self.validation_summary = {
            'total_nodes': total_nodes,
            'total_links': total_links,
            'total_groups': total_groups,
            'errors_count': len(self.errors),
            'warnings_count': len(self.warnings),
            'auto_fixes_count': len(self.auto_fixes),
            'nodes_fixed': nodes_fixed,
            'groups_fixed': groups_fixed,
            'valid_links': valid_links,
            'is_valid': is_valid
        }
        
        # Update SCS with fixed workflow
        updated_scs = copy.deepcopy(scs_data)
        updated_scs['workflow_state']['current_graph'] = fixed_workflow
        
        return {
            'success': True,
            'validation_summary': self.validation_summary,
            'errors': self.errors,
            'warnings': self.warnings,
            'auto_fixes': self.auto_fixes,
            'is_valid': is_valid,
            'fixed_workflow': fixed_workflow,
            'scs_data': updated_scs
        }


def main(scs_data: SCS) -> Dict[str, Any]:
    """
    Entry point for MCP code execution.
    Returns the status wrapper shape that the calling agent expects.
    """
    try:
        # Initialize validator
        validator = JSONValidator()
        
        # Perform validation and auto-fixing
        result = validator.validate_and_fix(scs_data)
        
        # Extract key information for return
        validation_summary = result.get('validation_summary', {})
        
        return {
            'success': result['success'],
            'is_valid': result.get('is_valid', False),
            'validation_summary': validation_summary,
            'errors': result.get('errors', []),
            'warnings': result.get('warnings', []),
            'auto_fixes': result.get('auto_fixes', []),
            'total_issues_fixed': validation_summary.get('auto_fixes_count', 0),
            'scs_data': result.get('scs_data', scs_data)
        }
        
    except Exception as e:
        # On failure, return consistent shape
        return {
            'success': False,
            'error': str(e),
            'is_valid': False,
            'validation_summary': {
                'total_nodes': 0,
                'total_links': 0,
                'total_groups': 0,
                'errors_count': 0,
                'warnings_count': 0,
                'auto_fixes_count': 0
            },
            'errors': [],
            'warnings': [],
            'auto_fixes': [],
            'total_issues_fixed': 0,
            'scs_data': scs_data
        }