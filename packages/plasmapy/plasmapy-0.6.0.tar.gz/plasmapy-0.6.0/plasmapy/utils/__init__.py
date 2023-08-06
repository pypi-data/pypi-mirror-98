"""
Package of functions and classes used to develop clean, readable, and informative
code.
"""
__all__ = [
    "CouplingWarning",
    "PhysicsError",
    "PhysicsWarning",
    "PlasmaPyError",
    "PlasmaPyWarning",
    "RelativityError",
    "RelativityWarning",
    "decorators",
    "exceptions",
    "roman",
]

from plasmapy.utils import (
    code_repr,
    datatype_factory_base,
    decorators,
    exceptions,
    roman,
)
from plasmapy.utils.exceptions import (
    CouplingWarning,
    PhysicsError,
    PhysicsWarning,
    PlasmaPyError,
    PlasmaPyWarning,
    RelativityError,
    RelativityWarning,
)

try:
    from plasmapy.utils import pytest_helpers
except ModuleNotFoundError:
    # pytest is not a hard dependency, so only import pytest_helpers if pytest
    # is installed
    pass
