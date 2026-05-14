"""
CMMC Artifact Gathering Tool
Collects compliance artifacts from Windows endpoints for CMMC assessment.
"""

__version__ = "1.0.0"
__author__ = "CMMC Team"

from .gatherer import CMMCGatherer

__all__ = ["CMMCGatherer"]
