"""Tests for input parsing"""

import pytest
from thkg.input import YAMLParser, KLEParser, InputValidator
from thkg.config import Configuration, Switch


def test_yaml_parser_basic():
    """Test basic YAML parsing"""
    parser = YAMLParser()
    
    # Test with minimal config
    data = {
        'keyboard': {
            'name': 'Test',
            'description': 'Test keyboard',
            'version': '1.0'
        }
    }
    
    config = parser._parse_config(data)
    assert config.name == 'Test'
    assert config.description == 'Test keyboard'


def test_kle_parser_simple():
    """Test KLE parser with simple layout"""
    parser = KLEParser()
    
    # Simple 3x3 grid
    kle_data = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"]
    ]
    
    switches, metadata = parser._parse_kle_data(kle_data)
    assert len(switches) == 9
    assert switches[0].row == 0
    assert switches[0].col == 0


def test_validator_basic():
    """Test configuration validation"""
    validator = InputValidator()
    
    # Valid config
    config = Configuration()
    config.name = "Test"
    config.layout_preset = "60-ansi"
    
    is_valid, errors = validator.validate(config)
    assert is_valid
    assert len(errors) == 0


def test_validator_missing_name():
    """Test validation with missing name"""
    validator = InputValidator()
    
    config = Configuration()
    config.name = ""
    
    is_valid, errors = validator.validate(config)
    assert not is_valid
    assert any("name" in e.lower() for e in errors)


if __name__ == '__main__':
    pytest.main([__file__])
