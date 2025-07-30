#!/usr/bin/env python3
"""
Simple CLI for Email Parser
"""

import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Email Parser CLI")
    parser.add_argument('command', choices=['parse', 'test'], help='Command to run')
    parser.add_argument('--path', help='Path to email file or folder')
    
    args = parser.parse_args()
    
    if args.command == 'test':
        print("Email Parser CLI is working!")
        print("To use the parser, activate the virtual environment:")
        print("  source .venv/bin/activate")
        print("  python -m src.email_parser.main")
    elif args.command == 'parse':
        if not args.path:
            print("--path is required for parse command")
            sys.exit(1)
        print(f"Would parse: {args.path}")
        print("Full parsing functionality requires activating the virtual environment.")

if __name__ == "__main__":
    main()
