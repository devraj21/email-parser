#!/usr/bin/env python3
"""
Convenience script to run the Configuration-Driven Data Ingestion CLI

This script provides easy access to the new structured data ingestion system
that uses JSON configuration files for template and column mapping definitions.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_ingestion.cli import main

if __name__ == "__main__":
    main()
