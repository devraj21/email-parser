#!/usr/bin/env python3
"""
Configuration Manager for Data Ingestion System

Handles loading, validation, and management of JSON configuration files
for templates, column mappings, and file processing rules.
"""

import json
import os
import re
import glob
from typing import Dict, List, Any, Optional, Tuple
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ConfigurationManager:
    """
    Manages configuration files for the data ingestion system.
    """
    
    def __init__(self, config_dir: str = "config"):
        """
        Initialize configuration manager.
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = config_dir
        self.templates_config = None
        self.file_mappings_config = None
        self._load_configurations()
    
    def _load_configurations(self):
        """Load all configuration files."""
        try:
            # Load templates configuration
            templates_path = os.path.join(self.config_dir, "templates_config.json")
            if os.path.exists(templates_path):
                with open(templates_path, 'r') as f:
                    self.templates_config = json.load(f)
                logger.info(f"Loaded templates configuration from {templates_path}")
            else:
                logger.warning(f"Templates configuration not found at {templates_path}")
                
            # Load file mappings configuration
            mappings_path = os.path.join(self.config_dir, "file_mappings.json")
            if os.path.exists(mappings_path):
                with open(mappings_path, 'r') as f:
                    self.file_mappings_config = json.load(f)
                logger.info(f"Loaded file mappings configuration from {mappings_path}")
            else:
                logger.warning(f"File mappings configuration not found at {mappings_path}")
                
        except Exception as e:
            logger.error(f"Error loading configurations: {e}")
            raise
    
    def get_template_config(self, template_name: str) -> Optional[Dict[str, Any]]:
        """
        Get configuration for a specific template.
        
        Args:
            template_name: Name of the template
            
        Returns:
            Template configuration dictionary or None if not found
        """
        if not self.templates_config:
            return None
        return self.templates_config.get("templates", {}).get(template_name)
    
    def get_available_templates(self) -> List[str]:
        """Get list of available template names."""
        if not self.templates_config:
            return []
        return list(self.templates_config.get("templates", {}).keys())
    
    def get_column_mappings(self, template_name: str) -> Dict[str, Any]:
        """
        Get column mappings for a specific template.
        
        Args:
            template_name: Name of the template
            
        Returns:
            Column mappings dictionary
        """
        if not self.templates_config:
            return {}
        return self.templates_config.get("column_mappings", {}).get(template_name, {})
    
    def resolve_file_template(self, file_path: str) -> str:
        """
        Determine which template should be used for a given file.
        
        Args:
            file_path: Path to the input file
            
        Returns:
            Template name to use for this file
        """
        if not self.file_mappings_config:
            return self.file_mappings_config.get("default_template", "standard")
        
        file_path = os.path.normpath(file_path)
        
        # Check specific file overrides first
        overrides = self.file_mappings_config.get("specific_file_overrides", {}).get("overrides", {})
        for pattern, template in overrides.items():
            if file_path.endswith(os.path.normpath(pattern)) or file_path == os.path.normpath(pattern):
                logger.info(f"File {file_path} matched specific override: {template}")
                return template
        
        # Check file mapping patterns
        for mapping in self.file_mappings_config.get("file_mappings", []):
            if not mapping.get("enabled", True):
                continue
                
            # Check if file matches any input patterns
            for pattern in mapping.get("input_patterns", []):
                if self._match_pattern(file_path, pattern):
                    # Check if file should be excluded
                    excluded = False
                    for exclude_pattern in mapping.get("exclude_patterns", []):
                        if self._match_pattern(file_path, exclude_pattern):
                            excluded = True
                            break
                    
                    if not excluded:
                        logger.info(f"File {file_path} matched pattern {pattern}, using template: {mapping['template']}")
                        return mapping["template"]
        
        # Try auto-detection if enabled
        if self.file_mappings_config.get("auto_detection", {}).get("enabled", False):
            detected_template = self._auto_detect_template(file_path)
            if detected_template:
                logger.info(f"Auto-detected template for {file_path}: {detected_template}")
                return detected_template
        
        # Return default template
        default_template = self.file_mappings_config.get("default_template", "standard")
        logger.info(f"Using default template for {file_path}: {default_template}")
        return default_template
    
    def _match_pattern(self, file_path: str, pattern: str) -> bool:
        """
        Check if a file path matches a glob pattern.
        
        Args:
            file_path: File path to check
            pattern: Glob pattern
            
        Returns:
            True if file matches pattern
        """
        try:
            # Handle different pattern types
            if '*' in pattern or '?' in pattern:
                # Use glob-style matching
                matched_files = glob.glob(pattern)
                return any(os.path.normpath(file_path) == os.path.normpath(matched) for matched in matched_files)
            else:
                # Direct string matching
                return os.path.normpath(pattern) in os.path.normpath(file_path)
        except Exception as e:
            logger.warning(f"Error matching pattern {pattern} against {file_path}: {e}")
            return False
    
    def _auto_detect_template(self, file_path: str) -> Optional[str]:
        """
        Attempt to auto-detect template based on file content.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Detected template name or None
        """
        try:
            import pandas as pd
            
            # Try to read file and examine structure
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, nrows=0)  # Just read headers
            elif file_path.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path, nrows=0)  # Just read headers
            else:
                return None
            
            columns = [str(col).lower() for col in df.columns]
            column_count = len(columns)
            
            # Check detection rules
            for rule in self.file_mappings_config.get("auto_detection", {}).get("detection_rules", []):
                template = rule["template"]
                conditions = rule["conditions"]
                
                # Check required columns
                required_columns = [col.lower() for col in conditions.get("required_columns", [])]
                if required_columns and not all(any(req in col for col in columns) for req in required_columns):
                    continue
                
                # Check column count range
                col_range = conditions.get("column_count_range", [0, 1000])
                if not (col_range[0] <= column_count <= col_range[1]):
                    continue
                
                return template
                
        except Exception as e:
            logger.warning(f"Error during auto-detection for {file_path}: {e}")
        
        return None
    
    def get_output_folder(self, file_path: str, template_name: str) -> str:
        """
        Get the appropriate output folder for a file.
        
        Args:
            file_path: Input file path
            template_name: Template being used
            
        Returns:
            Output folder path
        """
        # Check if file has specific mapping with output folder
        for mapping in self.file_mappings_config.get("file_mappings", []):
            if not mapping.get("enabled", True):
                continue
            
            if mapping["template"] == template_name:
                for pattern in mapping.get("input_patterns", []):
                    if self._match_pattern(file_path, pattern):
                        return mapping.get("output_folder", f"output/{template_name}")
        
        # Default output folder
        return f"output/{template_name}"
    
    def flatten_column_mappings(self, template_name: str) -> Dict[str, List[str]]:
        """
        Flatten hierarchical column mappings into a single dictionary.
        
        Args:
            template_name: Name of the template
            
        Returns:
            Flattened column mappings
        """
        mappings = self.get_column_mappings(template_name)
        flattened = {}
        
        def _flatten_dict(d: Dict[str, Any], prefix: str = ""):
            for key, value in d.items():
                if isinstance(value, dict) and not isinstance(value, list):
                    _flatten_dict(value, prefix)
                elif isinstance(value, list):
                    flattened[key] = value
        
        _flatten_dict(mappings)
        return flattened
    
    def get_processing_rules(self) -> Dict[str, Any]:
        """Get processing rules from configuration."""
        if not self.templates_config:
            return {}
        return self.templates_config.get("processing_rules", {})
    
    def validate_configuration(self) -> List[str]:
        """
        Validate the loaded configuration.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if not self.templates_config:
            errors.append("Templates configuration not loaded")
            return errors
        
        if not self.file_mappings_config:
            errors.append("File mappings configuration not loaded")
            return errors
        
        # Validate templates exist
        templates = self.templates_config.get("templates", {})
        if not templates:
            errors.append("No templates defined in configuration")
        
        # Validate template files exist
        for template_name, config in templates.items():
            template_file = config.get("template_file")
            if template_file and not os.path.exists(template_file):
                errors.append(f"Template file not found for '{template_name}': {template_file}")
        
        # Validate file mappings reference valid templates (only for enabled mappings)
        for mapping in self.file_mappings_config.get("file_mappings", []):
            if mapping.get("enabled", True):  # Only validate enabled mappings
                template_name = mapping.get("template")
                if template_name and template_name not in templates:
                    errors.append(f"File mapping references unknown template: {template_name}")
        
        return errors
    
    def create_template_config(self, template_name: str, template_config: Dict[str, Any]) -> bool:
        """
        Add a new template configuration.
        
        Args:
            template_name: Name for the new template
            template_config: Template configuration dictionary
            
        Returns:
            True if successful
        """
        try:
            if not self.templates_config:
                self.templates_config = {"version": "1.0", "templates": {}, "column_mappings": {}}
            
            self.templates_config["templates"][template_name] = template_config
            
            # Save back to file
            templates_path = os.path.join(self.config_dir, "templates_config.json")
            with open(templates_path, 'w') as f:
                json.dump(self.templates_config, f, indent=2)
            
            logger.info(f"Added new template configuration: {template_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating template configuration: {e}")
            return False
    
    def reload_configurations(self):
        """Reload configuration files from disk."""
        logger.info("Reloading configuration files")
        self._load_configurations()


def create_default_configs():
    """Create default configuration files if they don't exist."""
    config_dir = "config"
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    # Check if we need to create default configs
    templates_path = os.path.join(config_dir, "templates_config.json")
    mappings_path = os.path.join(config_dir, "file_mappings.json")
    
    if not os.path.exists(templates_path) or not os.path.exists(mappings_path):
        print(f"Creating default configuration files in {config_dir}/")
        # The files were already created above, so just log this
        print("Configuration files created successfully!")
        print("Edit the files to customize templates and file mappings for your needs.")


if __name__ == "__main__":
    # Test the configuration manager
    create_default_configs()
    config_manager = ConfigurationManager()
    
    # Validate configuration
    errors = config_manager.validate_configuration()
    if errors:
        print("Configuration validation errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Configuration validation passed!")
    
    # Test template resolution
    test_files = [
        "examples/Batchload files/Group 1.xls",
        "examples/Change files/AON.xls",
        "examples/Change files/Benifex Dental.csv"
    ]
    
    for test_file in test_files:
        template = config_manager.resolve_file_template(test_file)
        output_folder = config_manager.get_output_folder(test_file, template)
        print(f"File: {test_file}")
        print(f"  Template: {template}")
        print(f"  Output: {output_folder}")
        print()