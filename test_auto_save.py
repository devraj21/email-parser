#!/usr/bin/env python3
"""
Test script to demonstrate auto-save functionality
Creates sample outputs in organized directories
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and show results"""
    print(f"\n🔍 {description}")
    print(f"Running: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Success!")
            if result.stdout.strip():
                # Show first few lines of output
                lines = result.stdout.strip().split('\n')
                for line in lines[:10]:
                    print(f"  {line}")
                if len(lines) > 10:
                    print(f"  ... ({len(lines) - 10} more lines)")
        else:
            print("❌ Failed!")
            print(f"Error: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    """Test auto-save functionality"""
    print("🚀 Testing Email Parser Auto-Save Functionality")
    print("=" * 60)
    
    # Activate venv prefix
    python_cmd = ["python", "email_cli.py"]
    
    # Test 1: Entity extraction with auto-save
    run_command(
        python_cmd + [
            "extract-entities",
            "--text", "Contact sales@company.com or call (555) 123-4567. Meeting on 03/15/2024, budget $75,000. Visit https://company.com",
            "--auto-save",
            "--format", "json",
            "--quiet"
        ],
        "Entity extraction with auto-save"
    )
    
    # Test 2: Entity extraction with patterns
    run_command(
        python_cmd + [
            "extract-entities", 
            "--text", "Email info@support.com for help. Phone: +1-800-555-0199. Due: 12/25/2024",
            "--show-patterns",
            "--auto-save",
            "--format", "json"
        ],
        "Entity extraction with patterns and auto-save"
    )
    
    # Test 3: Demo with auto-save (if it supported it)
    run_command(
        python_cmd + ["demo", "--type", "basic", "--quiet"],
        "Demo functionality"
    )
    
    # Show output directory contents
    print(f"\n📁 Output Directory Contents:")
    print("=" * 40)
    
    output_dir = Path("output")
    if output_dir.exists():
        for subdir in ["emails", "analysis", "entities", "reports"]:
            subdir_path = output_dir / subdir
            if subdir_path.exists():
                files = list(subdir_path.glob("*.json"))
                print(f"\n📂 {subdir}/")
                if files:
                    for file in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True):
                        size = file.stat().st_size
                        print(f"  📄 {file.name} ({size} bytes)")
                else:
                    print("  (empty)")
    else:
        print("Output directory not found")
    
    print(f"\n✅ Auto-save test complete!")
    print("Check the output/ directory for organized results.")

if __name__ == "__main__":
    main()