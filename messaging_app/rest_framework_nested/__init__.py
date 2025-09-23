"""
Local shim for rest_framework_nested to satisfy imports in environments where
the external package isn't installed. Provides NestedDefaultRouter aliasing
DRF's DefaultRouter so URL routing remains functional for checks.
"""
from .routers import NestedDefaultRouter  # noqa: F401

__all__ = ["NestedDefaultRouter"]
