#!/usr/bin/env python3
"""
File Cleanup and Organization Script
Version: 2.0
Purpose: Automated file organization following FILE_ORGANIZATION_PROTOCOL.md
"""

import os
import shutil
import json
from datetime import datetime, timedelta
from pathlib import Path
import re
from typing import List, Dict, Tuple

class FileOrganizer:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.archive_dir = self.base_path / "archive"
        self.temp_dir = self.base_path / "temp"
        self.output_dir = self.base_path / "output"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report = []
        
    def initialize_directories(self):
        """Create required directory structure"""
        directories = [
            self.archive_dir,
            self.archive_dir / "workflows",
            self.archive_dir / "code",
            self.archive_dir / "docs",
            self.output_dir / "debug",
            self.output_dir / "errors",
            self.temp_dir / "tests"
        ]
        
        for dir_path in directories:
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                self.report.append(f"Created directory: {dir_path}")
    
    def cleanup_temp_files(self, hours: int = 24):
        """Remove temporary files older than specified hours"""
        if not self.temp_dir.exists():
            return
        
        cutoff = datetime.now() - timedelta(hours=hours)
        cleaned = 0
        
        for file_path in self.temp_dir.glob("temp_*"):
            if file_path.is_file():
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if mtime < cutoff:
                    file_path.unlink()
                    cleaned += 1
                    self.report.append(f"Deleted temp file: {file_path.name}")
        
        self.report.append(f"Cleaned {cleaned} temporary files")
    
    def archive_old_workflows(self, days: int = 30):
        """Archive workflows older than specified days"""
        workflow_dir = self.output_dir / "workflows"
        if not workflow_dir.exists():
            return
        
        cutoff = datetime.now() - timedelta(days=days)
        archived = 0
        
        for version_dir in workflow_dir.iterdir():
            if version_dir.is_dir() and version_dir.name.startswith("v"):
                # Extract date from directory name (v1_20250814_175944)
                match = re.match(r"v\d+_(\d{8})_", version_dir.name)
                if match:
                    dir_date = datetime.strptime(match.group(1), "%Y%m%d")
                    if dir_date < cutoff:
                        dest = self.archive_dir / "workflows" / version_dir.name
                        shutil.move(str(version_dir), str(dest))
                        archived += 1
                        self.report.append(f"Archived workflow: {version_dir.name}")
        
        self.report.append(f"Archived {archived} old workflows")
    
    def organize_root_files(self):
        """Move misplaced files from root to appropriate directories"""
        patterns = {
            r".*_workflow.*\.json$": "archive/workflows",
            r".*_nodes.*\.json$": "archive/workflows",
            r".*_graph.*\.json$": "archive/workflows",
            r".*_layout.*\.json$": "archive/workflows",
            r".*_grouped.*\.json$": "archive/workflows",
            r".*_validation.*\.json$": "archive/workflows",
            r"temp_.*": "temp",
            r".*_request\.json$": "temp",
            r"invoke_.*\.py$": "archive/code",
            r"analyze_.*\.py$": "archive/code",
            r"create_.*\.py$": "archive/code",
            r"prepare_.*\.py$": "archive/code",
            r"run_.*\.py$": "archive/code",
            r"apply_.*\.py$": "archive/code",
            r"remove_.*\.py$": "archive/code"
        }
        
        moved = 0
        for file_path in self.base_path.iterdir():
            if file_path.is_file():
                for pattern, dest_dir in patterns.items():
                    if re.match(pattern, file_path.name):
                        dest = self.base_path / dest_dir / file_path.name
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(file_path), str(dest))
                        moved += 1
                        self.report.append(f"Moved {file_path.name} to {dest_dir}")
                        break
        
        self.report.append(f"Organized {moved} root files")
    
    def rename_inconsistent_files(self):
        """Rename files to follow naming conventions"""
        renames = []
        
        # Check workflow directories
        workflow_dir = self.output_dir / "workflows"
        if workflow_dir.exists():
            for version_dir in workflow_dir.iterdir():
                if version_dir.is_dir():
                    for file_path in version_dir.glob("*.json"):
                        # Check for proper naming
                        if not re.match(r".*_v\d+_\d{8}_\d{6}_.*\.json$", file_path.name):
                            # Try to extract version from parent dir
                            version_match = re.match(r"(v\d+_\d{8}_\d{6})", version_dir.name)
                            if version_match:
                                version = version_match.group(1)
                                base_name = file_path.stem
                                new_name = f"{base_name}_{version}.json"
                                new_path = file_path.parent / new_name
                                if not new_path.exists():
                                    file_path.rename(new_path)
                                    renames.append((file_path.name, new_name))
        
        self.report.append(f"Renamed {len(renames)} files to follow conventions")
        for old, new in renames[:5]:  # Show first 5 renames
            self.report.append(f"  {old} -> {new}")
    
    def consolidate_duplicate_files(self):
        """Identify and consolidate duplicate files"""
        duplicates = {}
        
        for file_path in self.base_path.rglob("*.json"):
            if file_path.is_file():
                size = file_path.stat().st_size
                key = (file_path.name, size)
                if key not in duplicates:
                    duplicates[key] = []
                duplicates[key].append(file_path)
        
        consolidated = 0
        for key, paths in duplicates.items():
            if len(paths) > 1:
                # Keep the newest file, archive others
                paths.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                keeper = paths[0]
                for dup in paths[1:]:
                    archive_path = self.archive_dir / "duplicates" / dup.name
                    archive_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(dup), str(archive_path))
                    consolidated += 1
                    self.report.append(f"Archived duplicate: {dup.name}")
        
        self.report.append(f"Consolidated {consolidated} duplicate files")
    
    def generate_inventory(self):
        """Generate file inventory report"""
        inventory = {
            "workflows": 0,
            "agents": 0,
            "modules": 0,
            "docs": 0,
            "temp": 0,
            "total": 0
        }
        
        # Count files by category
        if (self.output_dir / "workflows").exists():
            inventory["workflows"] = sum(1 for _ in (self.output_dir / "workflows").rglob("*.json"))
        
        if (self.base_path / ".claude/agents").exists():
            inventory["agents"] = sum(1 for _ in (self.base_path / ".claude/agents").iterdir())
        
        if (self.base_path / "code_modules").exists():
            inventory["modules"] = sum(1 for _ in (self.base_path / "code_modules").glob("*.py"))
        
        if (self.base_path / "docs").exists():
            inventory["docs"] = sum(1 for _ in (self.base_path / "docs").rglob("*.md"))
        
        if self.temp_dir.exists():
            inventory["temp"] = sum(1 for _ in self.temp_dir.glob("*"))
        
        inventory["total"] = sum(v for k, v in inventory.items() if k != "total")
        
        return inventory
    
    def save_report(self):
        """Save cleanup report"""
        report_dir = self.output_dir / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = report_dir / f"cleanup_report_{self.timestamp}.md"
        
        with open(report_file, "w") as f:
            f.write(f"# File Cleanup Report\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Actions Taken\n")
            for line in self.report:
                f.write(f"- {line}\n")
            
            f.write("\n## File Inventory\n")
            inventory = self.generate_inventory()
            for category, count in inventory.items():
                f.write(f"- {category.capitalize()}: {count}\n")
        
        print(f"Report saved to: {report_file}")
        return report_file
    
    def run_cleanup(self, dry_run: bool = False):
        """Run complete cleanup process"""
        print("Starting file cleanup and organization...")
        print(f"Base path: {self.base_path.absolute()}")
        
        if dry_run:
            print("DRY RUN MODE - No files will be modified")
            self.report.append("DRY RUN MODE - No actual changes made")
        
        # Initialize directory structure
        self.initialize_directories()
        
        if not dry_run:
            # Perform cleanup operations
            self.cleanup_temp_files()
            self.archive_old_workflows()
            self.organize_root_files()
            self.rename_inconsistent_files()
            self.consolidate_duplicate_files()
        
        # Generate and save report
        report_file = self.save_report()
        
        # Print summary
        print("\n" + "="*50)
        print("CLEANUP SUMMARY")
        print("="*50)
        for line in self.report[-5:]:  # Show last 5 actions
            print(f"- {line}")
        
        inventory = self.generate_inventory()
        print(f"\nTotal files: {inventory['total']}")
        print(f"Report saved: {report_file}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="File cleanup and organization script")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying files")
    parser.add_argument("--path", default=".", help="Base path to clean (default: current directory)")
    parser.add_argument("--temp-hours", type=int, default=24, help="Hours before temp files are deleted (default: 24)")
    parser.add_argument("--archive-days", type=int, default=30, help="Days before workflows are archived (default: 30)")
    
    args = parser.parse_args()
    
    organizer = FileOrganizer(args.path)
    organizer.run_cleanup(dry_run=args.dry_run)


if __name__ == "__main__":
    main()