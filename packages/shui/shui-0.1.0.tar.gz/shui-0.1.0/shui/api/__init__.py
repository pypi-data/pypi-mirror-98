"""Module for interacting with remote Apache server"""
from .remote import get_versions
from .install import install_version

__all__ = [
    "get_versions",
    "install_version",
]
