"""
Invoke the Workflow Serializer agent with json_validator.py
"""

import json
import sys
import os
from datetime import datetime

# Add code_modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'code_modules'))

# Import the json_validator module
from json_validator import main as validate_json

def invoke_workflow_serializer(workflow_path):
    """
    Invokes the workflow-serializer agent process
    """
    print(f"[Workflow Serializer] Starting serialization process for: {workflow_path}")
    
    # Load the workflow
    try:
        with open(workflow_path, 'r') as f:
            workflow_data = json.load(f)
        print(f"[Workflow Serializer] Successfully loaded workflow with {len(workflow_data.get('nodes', []))} nodes")
    except Exception as e:
        print(f"[ERROR] Failed to load workflow: {e}")
        return None
    
    # Prepare SCS data structure as expected by json_validator
    scs_data = {
        'workflow_state': {
            'current_graph': workflow_data
        }
    }
    
    # Call the json_validator main function
    print("[Workflow Serializer] Invoking json_validator.py for validation and fixes...")
    result = validate_json(scs_data)
    
    # Process results
    if result['success']:
        print(f"[Workflow Serializer] Validation complete:")
        print(f"  - Valid: {result['is_valid']}")
        print(f"  - Total issues fixed: {result['total_issues_fixed']}")
        print(f"  - Errors: {len(result['errors'])}")
        print(f"  - Warnings: {len(result['warnings'])}")
        
        # Extract the fixed workflow
        fixed_workflow = result['scs_data']['workflow_state']['current_graph']
        
        # Create output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = f"output/workflows/v7_{timestamp}_serialized"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the serialized workflow
        output_path = os.path.join(output_dir, "workflow_serialized.json")
        with open(output_path, 'w') as f:
            json.dump(fixed_workflow, f, indent=2)
        print(f"[Workflow Serializer] Saved serialized workflow to: {output_path}")
        
        # Save validation report
        report_path = os.path.join(output_dir, "serialization_report.json")
        report = {
            'timestamp': timestamp,
            'source_workflow': workflow_path,
            'validation_summary': result['validation_summary'],
            'errors': result['errors'],
            'warnings': result['warnings'],
            'auto_fixes': result['auto_fixes']
        }
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"[Workflow Serializer] Saved validation report to: {report_path}")
        
        # Print detailed report
        print("\n[Workflow Serializer] Detailed Report:")
        print(f"  Validation Summary: {json.dumps(result['validation_summary'], indent=4)}")
        
        if result['errors']:
            print("\n  Errors:")
            for error in result['errors']:
                print(f"    - [{error['location']}] {error['message']} (Fixed: {error['fix_applied']})")
                
        if result['warnings']:
            print("\n  Warnings:")
            for warning in result['warnings']:
                print(f"    - [{warning['location']}] {warning['message']}")
                
        if result['auto_fixes']:
            print("\n  Auto-fixes Applied:")
            for fix in result['auto_fixes']:
                print(f"    - [{fix['location']}] {fix['message']}")
        
        return output_path
    else:
        print(f"[ERROR] Validation failed: {result.get('error', 'Unknown error')}")
        return None


if __name__ == "__main__":
    # Default to the latest nomenclature-applied workflow
    workflow_path = "output/workflows/v6_20250815_145203_nomenclature_applied/outfit_variation_named.json"
    
    if len(sys.argv) > 1:
        workflow_path = sys.argv[1]
    
    result = invoke_workflow_serializer(workflow_path)
    if result:
        print(f"\n[SUCCESS] Workflow serialization complete: {result}")
    else:
        print("\n[FAILED] Workflow serialization failed")