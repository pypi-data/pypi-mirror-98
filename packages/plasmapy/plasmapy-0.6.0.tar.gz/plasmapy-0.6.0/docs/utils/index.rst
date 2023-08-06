.. py:module:: plasmapy.utils

.. _plasmapy-utils:

*****************************************
Core package utilities (`plasmapy.utils`)
*****************************************

.. currentmodule:: plasmapy.utils

Introduction
============

The `~plasmapy.utils` subpackage contains functionality that is needed
across multiple subpackages or does not fit nicely in any other subpackage.
Functionality contained in `~plasmapy.utils` includes:

 * Warnings and exceptions used in PlasmaPy, such as
   `~plasmapy.utils.exceptions.RelativityWarning` or
   `~plasmapy.utils.exceptions.PhysicsError`.
 * Decorators we use for reusable physical `~astropy.units.Quantity`
   computation and checking, such as
   `~plasmapy.utils.decorators.validate_quantities`
   and `~plasmapy.utils.decorators.check_relativistic`.
 * Helper utilities for importing and testing packages.

Reference/API
=============

.. automodapi:: plasmapy.utils.decorators
.. automodapi:: plasmapy.utils.exceptions
.. automodapi:: plasmapy.utils.code_repr
.. automodapi:: plasmapy.utils.pytest_helpers
