#!/usr/bin/env python3

from enum import Enum


class OSType(Enum):
    """Enumeration of supported operating system types."""
    
    MACOS = "macos"
    UBUNTU = "ubuntu"
    
    def __str__(self) -> str:
        return self.value