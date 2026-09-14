"""
Grover's Algorithm Modular Package.

Provides dynamic oracle construction, diffuser generation, and end-to-end
Grover search execution via Qiskit.
"""

from .oracle import build_oracle
from .diffuser import build_diffuser
from .grover import GroverSearch

__all__ = ["build_oracle", "build_diffuser", "GroverSearch"]