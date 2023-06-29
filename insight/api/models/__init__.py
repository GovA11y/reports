# __init__.py
# Relative Path: insight/api/models/__init__.py
from .axe import ScanData, Rule, Test
from .targets import Domain, Url
from .orgs import Entity


__all__ = ["ScanData", "Rule", "Test", "Domain", "Url", "Entity"]