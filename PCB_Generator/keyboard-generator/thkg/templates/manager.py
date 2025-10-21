"""Template cache and management system."""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict
from thkg.templates.models import CircuitTemplate, TemplateMetadata, Component, Connection


class TemplateManager:
    """Manage cached circuit templates."""
    
    def __init__(self, cache_dir: Optional[Path] = None):
        """Initialize template manager.
        
        Args:
            cache_dir: Directory for template cache (default: thkg/templates/cache)
        """
        if cache_dir is None:
            cache_dir = Path(__file__).parent / "cache"
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.templates: Dict[str, CircuitTemplate] = {}
        self.metadata: Dict[str, TemplateMetadata] = {}
        
        # Load existing templates from cache
        self._load_all_from_cache()
    
    def list_templates(self) -> List[str]:
        """List all cached template names.
        
        Returns:
            List of template names
        """
        return list(self.templates.keys())
    
    def get_template(self, name: str) -> Optional[CircuitTemplate]:
        """Get a template by name.
        
        Args:
            name: Template name
            
        Returns:
            Template or None if not found
        """
        # Try memory first
        if name in self.templates:
            return self.templates[name]
        
        # Try loading from disk
        return self.load_from_cache(name)
    
    def cache_template(self, template: CircuitTemplate, save_to_disk: bool = True):
        """Cache a template for future use.
        
        Args:
            template: Template to cache
            save_to_disk: Whether to save to disk (default: True)
        """
        self.templates[template.name] = template
        
        if save_to_disk:
            self._save_to_disk(template)
    
    def cache_templates(self, templates: List[CircuitTemplate]):
        """Cache multiple templates.
        
        Args:
            templates: List of templates to cache
        """
        for template in templates:
            self.cache_template(template)
    
    def load_from_cache(self, name: str) -> Optional[CircuitTemplate]:
        """Load a template from disk cache.
        
        Args:
            name: Template name
            
        Returns:
            Template or None if not found
        """
        cache_file = self.cache_dir / f"{name}.json"
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
            
            template = self._deserialize_template(data)
            self.templates[name] = template
            return template
            
        except Exception as e:
            print(f"Error loading template {name}: {e}")
            return None
    
    def _load_all_from_cache(self):
        """Load all templates from cache directory."""
        if not self.cache_dir.exists():
            return
        
        for cache_file in self.cache_dir.glob("*.json"):
            name = cache_file.stem
            self.load_from_cache(name)
    
    def _save_to_disk(self, template: CircuitTemplate):
        """Save template to disk.
        
        Args:
            template: Template to save
        """
        cache_file = self.cache_dir / f"{template.name}.json"
        
        try:
            data = self._serialize_template(template)
            
            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving template {template.name}: {e}")
    
    def _serialize_template(self, template: CircuitTemplate) -> dict:
        """Serialize template to dictionary.
        
        Args:
            template: Template to serialize
            
        Returns:
            Dictionary representation
        """
        return {
            'name': template.name,
            'type': template.type,
            'source_project': template.source_project,
            'version': template.version,
            'description': template.description,
            'notes': template.notes,
            'components': [
                {
                    'reference': c.reference,
                    'value': c.value,
                    'footprint': c.footprint,
                    'library': c.library,
                    'symbol': c.symbol,
                    'position': c.position,
                    'rotation': c.rotation,
                    'properties': c.properties,
                }
                for c in template.components
            ],
            'connections': [
                {
                    'net_name': conn.net_name,
                    'pins': conn.pins,
                }
                for conn in template.connections
            ],
            'input_pins': template.input_pins,
            'output_pins': template.output_pins,
            'power_nets': template.power_nets,
        }
    
    def _deserialize_template(self, data: dict) -> CircuitTemplate:
        """Deserialize template from dictionary.
        
        Args:
            data: Dictionary representation
            
        Returns:
            CircuitTemplate object
        """
        components = [
            Component(
                reference=c['reference'],
                value=c['value'],
                footprint=c['footprint'],
                library=c['library'],
                symbol=c['symbol'],
                position=tuple(c['position']) if c['position'] else None,
                rotation=c['rotation'],
                properties=c['properties'],
            )
            for c in data['components']
        ]
        
        connections = [
            Connection(
                net_name=conn['net_name'],
                pins=[tuple(pin) for pin in conn['pins']],
            )
            for conn in data['connections']
        ]
        
        return CircuitTemplate(
            name=data['name'],
            type=data['type'],
            source_project=data['source_project'],
            version=data['version'],
            components=components,
            connections=connections,
            input_pins=data.get('input_pins', {}),
            output_pins=data.get('output_pins', {}),
            power_nets=data.get('power_nets', {}),
            description=data.get('description', ''),
            notes=data.get('notes', ''),
        )
    
    def get_templates_by_type(self, template_type: str) -> List[CircuitTemplate]:
        """Get all templates of a specific type.
        
        Args:
            template_type: Type of template ('mcu', 'usb', etc.)
            
        Returns:
            List of matching templates
        """
        return [t for t in self.templates.values() if t.type == template_type]
    
    def get_templates_by_project(self, project_name: str) -> List[CircuitTemplate]:
        """Get all templates from a specific project.
        
        Args:
            project_name: Source project name
            
        Returns:
            List of matching templates
        """
        return [t for t in self.templates.values() if t.source_project == project_name]
    
    def clear_cache(self):
        """Clear all cached templates from memory and disk."""
        self.templates.clear()
        self.metadata.clear()
        
        # Delete cache files
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
    
    def get_cache_stats(self) -> dict:
        """Get statistics about cached templates.
        
        Returns:
            Dictionary with cache statistics
        """
        by_type = {}
        by_project = {}
        
        for template in self.templates.values():
            by_type[template.type] = by_type.get(template.type, 0) + 1
            by_project[template.source_project] = by_project.get(template.source_project, 0) + 1
        
        return {
            'total': len(self.templates),
            'by_type': by_type,
            'by_project': by_project,
        }
