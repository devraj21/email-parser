"""
Data Ingestion Module

A configuration-driven system for processing Excel/CSV files and mapping them 
to standardized templates. Supports multiple template types with intelligent
column mapping and data transformation.
"""

from .config_manager import ConfigurationManager, create_default_configs
from .mapper import ConfigurableDataIngestionMapper

__version__ = "2.0.0"
__all__ = [
    "ConfigurationManager",
    "ConfigurableDataIngestionMapper", 
    "create_default_configs"
]
