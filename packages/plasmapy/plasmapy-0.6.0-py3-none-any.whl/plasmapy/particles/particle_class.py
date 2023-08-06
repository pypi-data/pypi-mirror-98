"""The Particle class."""

from __future__ import annotations

__all__ = [
    "AbstractParticle",
    "AbstractPhysicalParticle",
    "CustomParticle",
    "DimensionlessParticle",
    "Particle",
    "ParticleLike",
]

import astropy.constants as const
import astropy.units as u
import json
import numpy as np
import warnings

from abc import ABC, abstractmethod
from collections import defaultdict, namedtuple
from datetime import datetime
from numbers import Integral, Real
from typing import Iterable, List, Optional, Set, Tuple, Union

from plasmapy.particles.elements import _elements, _PeriodicTable
from plasmapy.particles.exceptions import (
    ChargeError,
    InvalidElementError,
    InvalidIonError,
    InvalidIsotopeError,
    InvalidParticleError,
    MissingParticleDataError,
    MissingParticleDataWarning,
    ParticleError,
    ParticleWarning,
)
from plasmapy.particles.isotopes import _isotopes
from plasmapy.particles.parsing import (
    _dealias_particle_aliases,
    _invalid_particle_errmsg,
    _parse_and_check_atomic_input,
)
from plasmapy.particles.special_particles import (
    _antiparticles,
    _Particles,
    _special_ion_masses,
    ParticleZoo,
)
from plasmapy.utils import roman

_classification_categories = {
    "lepton",
    "antilepton",
    "fermion",
    "boson",
    "antibaryon",
    "baryon",
    "neutrino",
    "antineutrino",
    "matter",
    "antimatter",
    "stable",
    "unstable",
    "charged",
    "uncharged",
}

_periodic_table_categories = {
    "nonmetal",
    "metal",
    "alkali metal",
    "alkaline earth metal",
    "metalloid",
    "transition metal",
    "post-transition metal",
    "halogen",
    "noble gas",
    "actinide",
    "lanthanide",
}

_atomic_property_categories = {"element", "isotope", "ion"}

_specific_particle_categories = {"electron", "positron", "proton", "neutron"}

_valid_categories = (
    _periodic_table_categories
    | _classification_categories
    | _atomic_property_categories
    | _specific_particle_categories
)


def _category_errmsg(particle, category: str) -> str:
    """
    Return an error message when an attribute raises an
    `~plasmapy.particles.exceptions.InvalidElementError`,
    `~plasmapy.particles.exceptions.InvalidIonError`, or
    `~plasmapy.particles.exceptions.InvalidIsotopeError`.
    """
    article = "an" if category[0] in "aeiouAEIOU" else "a"
    errmsg = (
        f"The particle {particle} is not {article} {category}, "
        f"so this attribute is not available."
    )
    return errmsg


class AbstractParticle(ABC):
    """An abstract base class that defines the interface for particles."""

    @property
    @abstractmethod
    def mass(self) -> Union[u.Quantity, Real]:
        """Provide the particle's mass."""
        raise NotImplementedError

    @property
    @abstractmethod
    def charge(self) -> Union[u.Quantity, Real]:
        """Provide the particle's electric charge."""
        raise NotImplementedError

    @property
    def json_dict(self) -> dict:
        """
        A dictionary representation of the particle object that is JSON
        friendly (i.e. convertible to a JSON object).

        The dictionary should maintain the following format so
        `~plasmapy.particles.ParticleJSONDecoder` knows how to decoded
        the resulting JSON object.

        .. code-block:: python

            {"plasmapy_particle": {
                # string representation of the particle class
                "type": "Particle",

                # string representation of the module contains the particle class
                "module": "plasmapy.particles.particle_class",

                # date stamp of when the object was created
                "date_created": "2020-07-20 17:46:13 UTC",

                # parameters used to initialized the particle class
                "__init__": {
                    # tuple of positional arguments
                    "args": (),

                    # dictionary of keyword arguments
                    "kwargs": {},
                },
            }}

        Only the ``"__init__"`` entry should be modified by the subclass.
        """
        json_dictionary = {
            "plasmapy_particle": {
                "type": type(self).__name__,
                "module": self.__module__,
                "date_created": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                "__init__": {"args": (), "kwargs": {}},
            }
        }
        return json_dictionary

    def __bool__(self):
        """
        Raise an `~plasmapy.particles.exceptions.ParticleError` because
        particles do not have a truth value.
        """
        raise ParticleError("The truth value of a particle is not defined.")

    def json_dump(self, fp, **kwargs):
        """
        Write the particle's `json_dict` to the ``fp`` file object using
        `json.dump`.

        Parameters
        ----------
        fp: `file object <https://docs.python.org/3/glossary.html#term-file-object>`_
            Destination file object to write the JSON serialized `json_dict`.

        **kwargs:
            Any keyword accepted by `json.dump`.
        """
        return json.dump(self.json_dict, fp, **kwargs)

    def json_dumps(self, **kwargs) -> str:
        """
        Serialize the particle's `json_dict` into a JSON formatted `str`
        using `json.dumps`.

        Parameters
        ----------
        **kwargs:
            Any keyword accepted by `json.dumps`.

        Returns
        -------
        str
            JSON formatted `str`.
        """
        return json.dumps(self.json_dict, **kwargs)


class AbstractPhysicalParticle(AbstractParticle):
    """Base class for particles that are defined with physical units."""

    @property
    def _as_particle_list(self):
        # Avoid circular imports by importing here
        from plasmapy.particles.particle_collections import ParticleList

        return ParticleList([self])

    def __add__(self, other):
        return self._as_particle_list + other

    def __radd__(self, other):
        return other + self._as_particle_list

    def __mul__(self, other):
        return self._as_particle_list.__mul__(other)

    def __rmul__(self, other):
        return self._as_particle_list.__mul__(other)

    def __gt__(self, other):
        return self._as_particle_list.__gt__(other)


class Particle(AbstractPhysicalParticle):
    """
    A class for an individual particle or antiparticle.

    Parameters
    ----------
    argument : `ParticleLike`, excluding `CustomParticle` instances
        A string representing a particle, element, isotope, or ion; an
        integer representing the atomic number of an element; or a
        `Particle` instance.

    mass_numb : `int`, optional
        The mass number of an isotope or nuclide.

    Z : `int`, optional
        The integer charge of the particle.

    Raises
    ------
    `TypeError`
        For when any of the arguments or keywords is not of the required
        type.

    `~plasmapy.particles.exceptions.InvalidParticleError`
        Raised when the particle input does not correspond to a valid
        particle or is contradictory.

    `~plasmapy.particles.exceptions.InvalidElementError`
        For when an attribute is being accessed that requires
        information about an element, but the particle is not an
        element, isotope, or ion.

    `~plasmapy.particles.exceptions.InvalidIsotopeError`
        For when an attribute is being accessed that requires
        information about an isotope or nuclide, but the particle is not
        an isotope (or an ion of an isotope).

    `~plasmapy.particles.exceptions.ChargeError`
        For when either the `~plasmapy.particles.Particle.charge` or
        `~plasmapy.particles.Particle.integer_charge` attributes is
        being accessed but the charge information for the particle is
        not available.

    `~plasmapy.particles.exceptions.ParticleError`
        Raised for attempts at converting a
        `~plasmapy.particles.Particle` object to a `bool`.

    See Also
    --------
    CustomParticle
    DimensionlessParticle
    ~plasmapy.particles.particle_collections.ParticleList

    Examples
    --------
    Particles may be defined using a wide variety of aliases:

    >>> proton = Particle('p+')
    >>> electron = Particle('e-')
    >>> neutron = Particle('neutron')
    >>> deuteron = Particle('D', Z=1)
    >>> triton = Particle('T+')
    >>> alpha = Particle('He', mass_numb=4, Z=2)
    >>> positron = Particle('positron')
    >>> hydrogen = Particle(1)  # atomic number

    The `~plasmapy.particles.Particle.symbol` attribute returns the
    particle's symbol in the standard form.

    >>> positron.symbol
    'e+'

    The `~plasmapy.particles.Particle.element`,
    `~plasmapy.particles.Particle.isotope`, and
    `~plasmapy.particles.Particle.ionic_symbol` attributes provide
    the symbols for each of these different types of particles.

    >>> proton.element
    'H'
    >>> alpha.isotope
    'He-4'
    >>> deuteron.ionic_symbol
    'D 1+'

    The `~plasmapy.particles.Particle.ionic_symbol` attribute works for
    neutral atoms if charge information is available.

    >>> deuterium = Particle("D", Z=0)
    >>> deuterium.ionic_symbol
    'D 0+'

    If the particle doesn't belong to one of those categories, then
    these attributes are `None`.

    >>> positron.element is None
    True

    The attributes of a `~plasmapy.particles.Particle` instance may be used
    to test whether or not a particle is an element, isotope, or ion.

    >>> True if positron.element else False
    False
    >>> True if deuterium.isotope else False
    True
    >>> True if Particle('alpha').is_ion else False
    True

    Many of the attributes provide physical properties of a particle.

    >>> electron.integer_charge
    -1
    >>> proton.spin
    0.5
    >>> alpha.atomic_number
    2
    >>> deuteron.mass_number
    2
    >>> deuteron.binding_energy.to('MeV')
    <Quantity 2.224... MeV>
    >>> alpha.charge
    <Quantity 3.20435...e-19 C>
    >>> neutron.half_life
    <Quantity 881.5 s>
    >>> Particle('C-14').half_life.to(u.year)
    <Quantity 5730. yr>
    >>> deuteron.electron_number
    0
    >>> alpha.neutron_number
    2

    If a `~plasmapy.particles.Particle` instance represents an elementary
    particle, then the unary `~` (invert) operator may be used to
    return the particle's antiparticle.

    >>> ~positron
    Particle("e-")

    A `~plasmapy.particles.Particle` instance may be used as the first
    argument to `~plasmapy.particles.Particle`.

    >>> iron = Particle('Fe')
    >>> iron == Particle(iron)
    True
    >>> Particle(iron, mass_numb=56, Z=6)
    Particle("Fe-56 6+")

    If the previously constructed `~plasmapy.particles.Particle` instance
    represents an element, then the ``Z`` and ``mass_numb`` arguments
    may be used to specify an ion or isotope.

    >>> iron = Particle('Fe')
    >>> Particle(iron, Z=1)
    Particle("Fe 1+")
    >>> Particle(iron, mass_numb=56)
    Particle("Fe-56")

    Adding particles together will create a `~plasmapy.particles.ParticleList`,
    which is a list-like collection of particles.

    >>> proton + 2 * electron
    ParticleList(['p+', 'e-', 'e-'])

    The ``>`` operator can be used with `Particle` and/or `ParticleList`
    objects to return the nuclear reaction energy.

    >>> deuteron + triton > alpha + neutron
    <Quantity 2.81810898e-12 J>

    The `~plasmapy.particles.particle_class.Particle.categories` attribute
    and `~plasmapy.particles.particle_class.Particle.is_category` method
    may be used to find and test particle membership in categories.

    Valid particle categories include: ``'actinide'``, ``'alkali
    metal'``, ``'alkaline earth metal'``, ``'antibaryon'``,
    ``'antilepton'``, ``'antimatter'``, ``'antineutrino'``,
    ``'baryon'``, ``'boson'``, ``'charged'``, ``'electron'``,
    ``'element'``, ``'fermion'``, ``'halogen'``, ``'ion'``,
    ``'isotope'``, ``'lanthanide'``, ``'lepton'``, ``'matter'``,
    ``'metal'``, ``'metalloid'``, ``'neutrino'``, ``'neutron'``,
    ``'noble gas'``, ``'nonmetal'``, ``'positron'``,
    ``'post-transition metal'``, ``'proton'``, ``'stable'``,
    ``'transition metal'``, ``'uncharged'``, and ``'unstable'``.
    """

    def __init__(
        self, argument: ParticleLike, mass_numb: Integral = None, Z: Integral = None,
    ):
        """
        Instantiate a `~plasmapy.particles.Particle` object and set private
        attributes.
        """

        if not isinstance(argument, (Integral, np.integer, str, Particle)):
            raise TypeError(
                "The first positional argument when creating a "
                "Particle object must be either an integer, string, or "
                "another Particle object."
            )

        # If argument is a Particle instance, then we will construct a
        # new Particle instance for the same Particle (essentially a
        # copy).

        if isinstance(argument, Particle):
            argument = argument.symbol

        if mass_numb is not None and not isinstance(mass_numb, Integral):
            raise TypeError("mass_numb is not an integer")

        if Z is not None and not isinstance(Z, Integral):
            raise TypeError("Z is not an integer.")

        # For Python 3.10, change `type(None)` to `types.NoneType`
        self._attributes = defaultdict(type(None))
        attributes = self._attributes

        # Use this set to keep track of particle categories such as
        # 'lepton' for use with the is_category method later on.

        self._categories = set()
        categories = self._categories

        # If the argument corresponds to one of the case-sensitive or
        # case-insensitive aliases for particles, return the standard
        # symbol. Otherwise, return the original argument.

        particle_symbol = _dealias_particle_aliases(argument)

        if particle_symbol in _Particles.keys():  # special particles

            attributes["symbol"] = particle_symbol

            for attribute in _Particles[particle_symbol].keys():
                attributes[attribute] = _Particles[particle_symbol][attribute]

            particle_taxonomy = ParticleZoo._taxonomy_dict
            all_categories = particle_taxonomy.keys()

            for category in all_categories:
                if particle_symbol in particle_taxonomy[category]:
                    categories.add(category)

            if attributes["name"] in _specific_particle_categories:
                categories.add(attributes["name"])

            if particle_symbol == "p+":
                categories.update({"element", "isotope", "ion"})

            if mass_numb is not None or Z is not None:
                if particle_symbol == "p+" and (mass_numb == 1 or Z == 1):
                    warnings.warn(
                        "Redundant mass number or charge information.", ParticleWarning
                    )
                else:
                    raise InvalidParticleError(
                        "The keywords 'mass_numb' and 'Z' cannot be used when "
                        "creating Particle objects for special particles. To "
                        f"create a Particle object for {attributes['name']}s, "
                        f"use:  Particle({repr(attributes['particle'])})"
                    )

        else:  # elements, isotopes, and ions (besides protons)
            try:
                nomenclature = _parse_and_check_atomic_input(
                    argument, mass_numb=mass_numb, Z=Z
                )
            except Exception as exc:
                errmsg = _invalid_particle_errmsg(argument, mass_numb=mass_numb, Z=Z)
                raise InvalidParticleError(errmsg) from exc

            for key in nomenclature.keys():
                attributes[key] = nomenclature[key]

            element = attributes["element"]
            isotope = attributes["isotope"]
            ion = attributes["ion"]

            if element:
                categories.add("element")
            if isotope:
                categories.add("isotope")
            if self.element and self._attributes["integer charge"]:
                categories.add("ion")

            # Element properties

            Element = _elements[element]

            attributes["atomic number"] = Element["atomic number"]
            attributes["element name"] = Element["element name"]

            # Set the lepton number to zero for elements, isotopes, and
            # ions.  The lepton number will probably come up primarily
            # during nuclear reactions.

            attributes["lepton number"] = 0

            if isotope:

                Isotope = _isotopes[isotope]

                attributes["baryon number"] = Isotope["mass number"]
                attributes["isotope mass"] = Isotope.get("mass", None)
                attributes["isotopic abundance"] = Isotope.get("abundance", 0.0)

                if Isotope["stable"]:
                    attributes["half-life"] = np.inf * u.s
                else:
                    attributes["half-life"] = Isotope.get("half-life", None)

            if element and not isotope:
                attributes["standard atomic weight"] = Element.get("atomic mass", None)

            if ion in _special_ion_masses.keys():
                attributes["mass"] = _special_ion_masses[ion]

            attributes["periodic table"] = _PeriodicTable(
                group=Element["group"],
                period=Element["period"],
                block=Element["block"],
                category=Element["category"],
            )

            categories.add(Element["category"])

        if attributes["integer charge"] == 1:
            attributes["charge"] = const.e.si
        elif attributes["integer charge"] is not None:
            attributes["charge"] = attributes["integer charge"] * const.e.si

        if attributes["integer charge"]:
            categories.add("charged")
        elif attributes["integer charge"] == 0:
            categories.add("uncharged")

        if attributes["half-life"] is not None:
            if isinstance(attributes["half-life"], str):
                categories.add("unstable")
            elif attributes["half-life"] == np.inf * u.s:
                categories.add("stable")
            else:
                categories.add("unstable")

        self.__name__ = self.__repr__()

    def __repr__(self) -> str:
        """
        Return a call string that would recreate this object.

        Examples
        --------
        >>> lead = Particle('lead')
        >>> repr(lead)
        'Particle("Pb")'
        """
        return f'Particle("{self.symbol}")'

    def __str__(self) -> str:
        """Return the particle's symbol."""
        return self.symbol

    def __eq__(self, other) -> bool:
        """
        Determine if two objects correspond to the same particle.

        This method will return `True` if ``other`` is an identical
        `~plasmapy.particles.Particle` instance or a `str` representing the
        same particle, and return `False` if ``other`` is a different
        `~plasmapy.particles.Particle` or a `str` representing a different
        particle.

        If ``other`` is not a `str` or `~plasmapy.particles.Particle`
        instance, then this method will raise a `TypeError`.  If
        ``other.symbol`` equals ``self.symbol`` but the attributes
        differ, then this method will raise a
        `~plasmapy.particles.exceptions.ParticleError`.

        Examples
        --------
        >>> electron = Particle('e-')
        >>> positron = Particle('e+')
        >>> electron == positron
        False
        >>> electron == 'e-'
        True
        """
        if isinstance(other, str):
            try:
                other_particle = Particle(other)
                return self.symbol == other_particle.symbol
            except InvalidParticleError as exc:
                raise InvalidParticleError(
                    f"{other} is not a particle and cannot be compared to {self}."
                ) from exc

        if not isinstance(other, self.__class__):
            raise TypeError(
                f"The equality of a Particle object with a {type(other)} is undefined."
            )

        no_symbol_attr = "symbol" not in dir(self) or "symbol" not in dir(other)
        no_attributes_attr = "_attributes" not in dir(self) or "_attributes" not in dir(
            other
        )

        if no_symbol_attr or no_attributes_attr:  # coverage: ignore
            raise TypeError(f"The equality of {self} with {other} is undefined.")

        same_particle = self.symbol == other.symbol

        # The following two loops are a hack to enable comparisons
        # between defaultdicts.  By accessing all of the defined keys in
        # each of the defaultdicts, this makes sure that
        # self._attributes and other._attributes have the same keys.

        # TODO: create function in utils to account for equality between
        # defaultdicts, and implement it here

        for attribute in self._attributes.keys():
            other._attributes[attribute]

        for attribute in other._attributes.keys():
            self._attributes[attribute]

        same_attributes = self._attributes == other._attributes

        if same_particle and not same_attributes:  # coverage: ignore
            raise ParticleError(
                f"{self} and {other} should be the same Particle, but "
                f"have differing attributes.\n\n"
                f"The attributes of {self} are:\n\n{self._attributes}\n\n"
                f"The attributes of {other} are:\n\n{other._attributes}\n"
            )

        return same_particle

    def __ne__(self, other) -> bool:
        """
        Test whether or not two objects are different particles.

        This method will return `False` if ``other`` is an identical
        `~plasmapy.particles.Particle` instance or a `str` representing the
        same particle, and return `True` if ``other`` is a different
        `~plasmapy.particles.Particle` or a `str` representing a different
        particle.

        If ``other`` is not a `str` or `~plasmapy.particles.Particle`
        instance, then this method will raise a `TypeError`.  If
        ``other.symbol`` equals ``self.symbol`` but the attributes
        differ, then this method will raise a
        `~plasmapy.particles.exceptions.ParticleError`.
        """
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """
        Allow use of `hash` so that a `~plasmapy.particles.Particle`
        instance may be used as a key in a `dict`.
        """
        return hash(self.__repr__())

    def __invert__(self) -> Particle:
        """
        Return the corresponding antiparticle, or raise an
        `~plasmapy.particles.exceptions.ParticleError` if the particle is not an
        elementary particle.
        """
        return self.antiparticle

    @property
    def json_dict(self) -> dict:
        """
        A JSON friendly dictionary representation of the particle.

        See `AbstractParticle.json_dict` for more details.

        Examples
        --------
        >>> lead = Particle('lead')
        >>> lead.json_dict
        {'plasmapy_particle': {'type': 'Particle',
            'module': 'plasmapy.particles.particle_class',
            'date_created': '...',
            '__init__': {'args': ('Pb',), 'kwargs': {}}}}
        >>> electron = Particle('e-')
        >>> electron.json_dict
        {'plasmapy_particle': {'type': 'Particle',
            'module': 'plasmapy.particles.particle_class',
            'date_created': '...',
            '__init__': {'args': ('e-',), 'kwargs': {}}}}
        """
        particle_dictionary = super().json_dict
        particle_dictionary["plasmapy_particle"]["__init__"]["args"] = (self.symbol,)
        return particle_dictionary

    @property
    def particle(self) -> str:
        """
        The symbol of the particle, atom, isotope, or ion.

        .. deprecated:: 0.6.0
            `Particle.particle` has been deprecated and will be removed in
            a subsequent release of PlasmaPy.  Use `Particle.symbol`
            instead.
        """
        warnings.warn(
            "Particle.particle has been deprecated and will be removed in "
            "a subsequent release. Use Particle.symbol instead.",
            FutureWarning,
        )
        return self.symbol

    @property
    def symbol(self) -> str:
        """
        The symbol of the particle, atom, isotope, or ion.

        This attribute will return the canonical symbol for special
        particles (e.g., ``"p+"``, ``"e-"``, or ``"n"``), the atomic
        symbol for elements (e.g., ``"Fe"``), the isotopic symbol for
        isotopes (e.g., ``"D"`` or ``"Fe-56"``), and the ionic symbol
        for ions (e.g., ``"N 1+"`` or ``"He-4 1+"``).

        Examples
        --------
        >>> electron = Particle('positron')
        >>> electron.symbol
        'e+'
        >>> deuteron = Particle('D 1+')
        >>> deuteron.symbol
        'D 1+'
        """
        return self._attributes["symbol"]

    @property
    def antiparticle(self) -> Particle:
        """
        The antiparticle corresponding to the particle.

        This attribute may be accessed by using the unary operator ``~``
        on a `~plasmapy.particles.Particle` instance.

        Raises
        ------
        `~plasmapy.particles.exceptions.ParticleError`
            If the particle is not an elementary particle and does not
            have a defined antiparticle.

        Examples
        --------
        >>> electron = Particle('e-')
        >>> electron.antiparticle
        Particle("e+")

        >>> antineutron = Particle('antineutron')
        >>> ~antineutron
        Particle("n")
        """
        if self.symbol in _antiparticles.keys():
            return Particle(_antiparticles[self.symbol])
        else:
            raise ParticleError(
                "The unary operator can only be used for elementary "
                "particles and antiparticles."
            )

    @property
    def element(self) -> Optional[str]:
        """
        The atomic symbol if the particle corresponds to an element, and
        `None` otherwise.

        Examples
        --------
        >>> alpha = Particle('alpha')
        >>> alpha.element
        'He'
        """
        return self._attributes["element"]

    @property
    def isotope(self) -> Optional[str]:
        """
        The isotope symbol if the particle corresponds to an isotope,
        and `None` otherwise.

        Examples
        --------
        >>> alpha = Particle('alpha')
        >>> alpha.isotope
        'He-4'
        """
        return self._attributes["isotope"]

    @property
    def ionic_symbol(self) -> Optional[str]:
        """
        The ionic symbol if the particle corresponds to an ion or
        neutral atom, and `None` otherwise.

        Examples
        --------
        >>> deuteron = Particle('deuteron')
        >>> deuteron.ionic_symbol
        'D 1+'
        >>> hydrogen_atom = Particle('H', Z=0)
        >>> hydrogen_atom.ionic_symbol
        'H 0+'
        """
        return self._attributes["ion"]

    @property
    def roman_symbol(self) -> Optional[str]:
        """
        The spectral name of the particle (i.e. the ionic symbol in
        Roman numeral notation).

        If the particle is not an ion or neutral atom, return `None`.
        The roman numeral represents one plus the integer charge. Raise
        `ChargeError` if no charge has been specified and
        `~plasmapy.utils.roman.roman.OutOfRangeError` if the charge is
        negative.

        Examples
        --------
        >>> proton = Particle('proton')
        >>> proton.roman_symbol
        'H-1 II'
        >>> hydrogen_atom = Particle('H', Z=0)
        >>> hydrogen_atom.roman_symbol
        'H I'
        """
        if not self._attributes["element"]:
            return None
        if self._attributes["integer charge"] is None:
            raise ChargeError(f"The charge of particle {self} has not been specified.")
        if self._attributes["integer charge"] < 0:
            raise roman.OutOfRangeError("Cannot convert negative charges to Roman.")

        symbol = self.isotope if self.isotope else self.element
        integer_charge = self._attributes["integer charge"]
        roman_charge = roman.to_roman(integer_charge + 1)
        return f"{symbol} {roman_charge}"

    @property
    def element_name(self) -> str:
        """
        The name of the element corresponding to this particle.

        Raises
        ------
        `~plasmapy.particles.exceptions.InvalidElementError`
            If the particle does not correspond to an element.

        Examples
        --------
        >>> tritium = Particle('T')
        >>> tritium.element_name
        'hydrogen'
        """
        if not self.element:
            raise InvalidElementError(_category_errmsg(self, "element"))
        return self._attributes["element name"]

    @property
    def isotope_name(self) -> Optional[str]:
        """
        The name of the element along with the isotope symbol if the
        particle corresponds to an isotope, or `None` if it does not.

        Raises
        ------
        `~plasmapy.particles.exceptions.InvalidElementError`
            If the particle is not a valid element.

        `~plasmapy.particles.exceptions.InvalidIsotopeError`
            If the particle is not a valid isotope.

        Examples
        --------
        >>> deuterium = Particle("D")
        >>> deuterium.isotope_name
        'deuterium'
        >>> iron_isotope = Particle("Fe-56", Z=16)
        >>> iron_isotope.isotope_name
        'iron-56'
        """
        if not self.element:
            raise InvalidElementError(_category_errmsg(self.symbol, "element"))
        elif not self.isotope:
            raise InvalidIsotopeError(_category_errmsg(self, "isotope"))

        if self.isotope == "D":
            isotope_name = "deuterium"
        elif self.isotope == "T":
            isotope_name = "tritium"
        else:
            isotope_name = f"{self.element_name}-{self.mass_number}"

        return isotope_name

    @property
    def integer_charge(self) -> Integral:
        """
        The particle's electrical charge in units of the elementary charge.

        Raises
        ------
        `~plasmapy.particles.exceptions.ChargeError`
            If the charge has not been specified.

        Examples
        --------
        >>> muon = Particle('mu-')
        >>> muon.integer_charge
        -1
        """
        if self._attributes["integer charge"] is None:
            raise ChargeError(f"The charge of particle {self} has not been specified.")
        return self._attributes["integer charge"]

    @property
    def charge(self) -> u.C:
        """
        The particle's electrical charge in coulombs.

        Raises
        ------
        `~plasmapy.particles.exceptions.ChargeError`
            If the charge has not been specified.

        Examples
        --------
        >>> electron = Particle('e-')
        >>> electron.charge
        <Quantity -1.60217662e-19 C>
        """
        if self._attributes["charge"] is None:
            raise ChargeError(f"The charge of particle {self} has not been specified.")
        if self._attributes["integer charge"] == 1:
            return const.e.si

        return self._attributes["charge"]

    @property
    def standard_atomic_weight(self) -> u.kg:
        """
        The element's standard atomic weight in kg.

        Raises
        ------
        `~plasmapy.particles.exceptions.InvalidElementError`
            If the particle is not an element or corresponds to an
            isotope or ion.

        `~plasmapy.particles.exceptions.MissingParticleDataError`
            If the element does not have a defined standard atomic
            weight.

        Examples
        --------
        >>> oxygen = Particle('O')
        >>> oxygen.standard_atomic_weight
        <Quantity 2.656696...e-26 kg>
        """
        if self.isotope or self.is_ion or not self.element:
            raise InvalidElementError(_category_errmsg(self, "element"))
        if self._attributes["standard atomic weight"] is None:  # coverage: ignore
            raise MissingParticleDataError(
                f"The standard atomic weight of {self} is unavailable."
            )
        return self._attributes["standard atomic weight"].to(u.kg)

    @property
    def mass(self) -> u.kg:
        """
        The mass of the particle in kilograms.

        If the particle is an element and not an isotope or ion, then
        this attribute will return the standard atomic weight, if
        available.

        If the particle is an isotope but not an ion, then this
        attribute will return the isotopic mass, including bound
        electrons.

        If the particle is an ion, then this attribute will return the
        mass of the element or isotope (as just described) minus the
        product of the integer charge and the electron mass.

        For special particles, this attribute will return the standard
        value for the particle's mass.

        Raises
        ------
        `~plasmapy.particles.exceptions.MissingParticleDataError`.
            If the mass is unavailable (e.g., for neutrinos or elements
            with no standard atomic weight.

        Examples
        --------
        >>> Particle('He').mass
        <Quantity 6.64647...e-27 kg>
        >>> Particle('He+').mass
        <Quantity 6.64556...e-27 kg>
        >>> Particle('He-4 +1').mass
        <Quantity 6.64556...e-27 kg>
        >>> Particle('alpha').mass
        <Quantity 6.64465...e-27 kg>
        """

        if self._attributes["mass"] is not None:
            return self._attributes["mass"].to(u.kg)

        if self.is_ion:

            if self.isotope:
                base_mass = self._attributes["isotope mass"]
            else:
                base_mass = self._attributes["standard atomic weight"]

            if base_mass is None:
                raise MissingParticleDataError(
                    f"The mass of ion '{self.ionic_symbol}' is not available."
                )

            mass = base_mass - self.integer_charge * const.m_e

            return mass.to(u.kg)

        if self.element:

            if self.isotope:
                mass = self._attributes["isotope mass"]
            else:
                mass = self._attributes["standard atomic weight"]

            if mass is not None:
                return mass.to(u.kg)

        raise MissingParticleDataError(f"The mass of {self} is not available.")

    @property
    def nuclide_mass(self) -> u.kg:
        """
        The mass of the bare nucleus of an isotope or a neutron.

        Raises
        ------
        `~plasmapy.particles.exceptions.InvalidIsotopeError`
            If the particle is not an isotope or neutron.

        `~plasmapy.particles.exceptions.MissingParticleDataError`
            If the isotope mass is not available.

        Examples
        --------
        >>> deuterium = Particle('D')
        >>> deuterium.nuclide_mass
        <Quantity 3.34358372e-27 kg>
        """

        if self.isotope == "H-1":
            return const.m_p
        elif self.isotope == "D":
            return _special_ion_masses["D 1+"]
        elif self.isotope == "T":
            return _special_ion_masses["T 1+"]
        elif self.symbol == "n":
            return const.m_n

        if not self.isotope:
            raise InvalidIsotopeError(_category_errmsg(self, "isotope"))

        base_mass = self._attributes["isotope mass"]

        if base_mass is None:  # coverage: ignore
            raise MissingParticleDataError(
                f"The mass of a {self.isotope} nuclide is not available."
            )

        _nuclide_mass = (
            self._attributes["isotope mass"] - self.atomic_number * const.m_e
        )

        return _nuclide_mass.to(u.kg)

    @property
    def mass_energy(self) -> u.J:
        """
        The mass energy of the particle in joules.

        If the particle is an isotope or nuclide, return the mass energy
        of the nucleus only.

        If the mass of the particle is not known, then raise a
        `~plasmapy.particles.exceptions.MissingParticleDataError`.

        Examples
        --------
        >>> proton = Particle('p+')
        >>> proton.mass_energy
        <Quantity 1.503277...e-10 J>

        >>> protium = Particle('H-1 0+')
        >>> protium.mass_energy
        <Quantity 1.503277...e-10 J>

        >>> electron = Particle('electron')
        >>> electron.mass_energy.to('MeV')
        <Quantity 0.510998... MeV>
        """
        try:
            mass = self.nuclide_mass if self.isotope else self.mass
            energy = mass * const.c ** 2
            return energy.to(u.J)
        except MissingParticleDataError:
            raise MissingParticleDataError(
                f"The mass energy of {self.symbol} is not available "
                f"because the mass is unknown."
            ) from None

    @property
    def binding_energy(self) -> u.J:
        """
        The particle's nuclear binding energy.

        Raises
        ------
        `~plasmapy.particles.exceptions.InvalidIsotopeError`
            If the particle is not a nucleon or isotope.

        Examples
        --------
        >>> alpha = Particle('alpha')
        >>> alpha.binding_energy
        <Quantity 4.53346...e-12 J>
        >>> Particle('T').binding_energy.to('MeV')
        <Quantity 8.481... MeV>

        The binding energy of a nucleon equals 0 joules.

        >>> neutron = Particle('n')
        >>> proton = Particle('p+')
        >>> neutron.binding_energy
        <Quantity 0. J>
        >>> proton.binding_energy
        <Quantity 0. J>
        """

        if self._attributes["baryon number"] == 1:
            return 0 * u.J

        if not self.isotope:
            raise InvalidIsotopeError(
                f"The nuclear binding energy may only be calculated for nucleons and isotopes."
            )

        number_of_protons = self.atomic_number
        number_of_neutrons = self.mass_number - self.atomic_number

        mass_of_protons = number_of_protons * const.m_p
        mass_of_neutrons = number_of_neutrons * const.m_n

        mass_of_nucleons = mass_of_protons + mass_of_neutrons

        mass_defect = mass_of_nucleons - self.nuclide_mass
        nuclear_binding_energy = mass_defect * const.c ** 2

        return nuclear_binding_energy.to(u.J)

    @property
    def atomic_number(self) -> Integral:
        """
        Return the number of protons in an element, isotope, or ion.

        Raises
        ------
        `~plasmapy.particles.exceptions.InvalidElementError`.
            If the particle does not correspond to an element.

        Examples
        --------
        >>> proton = Particle('p+')
        >>> proton.atomic_number
        1
        >>> curium = Particle('Cm')
        >>> curium.atomic_number
        96
        """
        if not self.element:
            raise InvalidElementError(_category_errmsg(self, "element"))
        return self._attributes["atomic number"]

    @property
    def mass_number(self) -> Integral:
        """
        The total number of protons and neutrons in an isotope or nuclide.

        Raises
        ------
        `~plasmapy.particles.exceptions.InvalidIsotopeError`.
            If the particle does not correspond to an isotope.

        Examples
        --------
        >>> alpha = Particle('helium-4 2+')
        >>> alpha.mass_number
        4
        """
        if not self.isotope:
            raise InvalidIsotopeError(_category_errmsg(self, "isotope"))
        return self._attributes["mass number"]

    @property
    def neutron_number(self) -> Integral:
        """
        Return the number of neutrons in an isotope or nucleon.

        This attribute will return the number of neutrons in an isotope,
        or ``1`` for a neutron.

        If this particle is not an isotope or neutron, then this
        attribute will raise an `~plasmapy.particles.exceptions.InvalidIsotopeError`.

        Examples
        --------
        >>> alpha = Particle('He-4++')
        >>> alpha.neutron_number
        2
        >>> Particle('n').neutron_number
        1
        """
        if self.symbol == "n":
            return 1
        elif self.isotope:
            return self.mass_number - self.atomic_number
        else:  # coverage: ignore
            raise InvalidIsotopeError(_category_errmsg(self, "isotope"))

    @property
    def electron_number(self) -> Integral:
        """
        The number of electrons in an ion.

        This attribute will return the number of bound electrons in an
        ion, or ``1`` for an electron.

        Raises
        ------
        `~plasmapy.particles.exceptions.InvalidIonError`
            If this particle is not an ion or electron.

        Examples
        --------
        >>> Particle('Li 0+').electron_number
        3
        >>> Particle('e-').electron_number
        1
        """
        if self.symbol == "e-":
            return 1
        elif self.ionic_symbol:
            return self.atomic_number - self.integer_charge
        else:  # coverage: ignore
            raise InvalidIonError(_category_errmsg(self, "ion"))

    @property
    def isotopic_abundance(self) -> u.Quantity:
        """
        The isotopic abundance of an isotope.

        Raises
        ------
        `~plasmapy.particles.exceptions.InvalidIsotopeError`
            If the particle does not correspond to an isotope.

        `~plasmapy.particles.exceptions.MissingParticleDataError`
            If the isotopic abundance is not available.

        Examples
        --------
        >>> D = Particle('deuterium')
        >>> D.isotopic_abundance
        0.000115
        """
        from .atomic import common_isotopes

        if not self.isotope or self.is_ion:  # coverage: ignore
            raise InvalidIsotopeError(_category_errmsg(self.symbol, "isotope"))

        abundance = self._attributes.get("isotopic abundance", 0.0)

        if not common_isotopes(self.element):
            warnings.warn(
                f"No isotopes of {self.element} have an isotopic abundance. "
                f"The isotopic abundance of {self.isotope} is being returned as 0.0",
                ParticleWarning,
            )

        return abundance

    @property
    def baryon_number(self) -> Integral:
        """
        The number of baryons in a particle.

        This attribute will return the number of protons and neutrons
        minus the number of antiprotons and antineutrons. The baryon
        number is equivalent to the mass number for isotopes.

        Raises
        ------
        `~plasmapy.particles.exceptions.MissingParticleDataError`
            If the baryon number is unavailable.

        Examples
        --------
        >>> alpha = Particle('alpha')
        >>> alpha.baryon_number
        4
        """
        if self._attributes["baryon number"] is None:  # coverage: ignore
            raise MissingParticleDataError(
                f"The baryon number for '{self.symbol}' is not available."
            )
        return self._attributes["baryon number"]

    @property
    def lepton_number(self) -> Integral:
        """
        Return ``1`` for leptons, ``-1`` for antileptons, and ``0``
        otherwise.

        This attribute returns the number of leptons minus the number of
        antileptons, excluding bound electrons in an atom or ion.

        Raises
        ------
        `~plasmapy.particles.exceptions.MissingParticleDataError`
            If the lepton number is unavailable.

        Examples
        --------
        >>> Particle('e-').lepton_number
        1
        >>> Particle('mu+').lepton_number
        -1
        >>> Particle('He-4 0+').lepton_number
        0
        """
        if self._attributes["lepton number"] is None:  # coverage: ignore
            raise MissingParticleDataError(
                f"The lepton number for {self.symbol} is not available."
            )
        return self._attributes["lepton number"]

    @property
    def half_life(self) -> Union[u.Quantity, str]:
        """
        The particle's half-life in seconds, or a `str` with half-life
        information.

        Particles that do not have sufficiently well-constrained
        half-lives will return a `str` containing the information
        that is available about the half-life and issue a
        `~plasmapy.particles.exceptions.MissingParticleDataWarning`.

        Examples
        --------
        >>> neutron = Particle('n')
        >>> neutron.half_life
        <Quantity 881.5 s>
        """
        if self.element and not self.isotope:
            raise InvalidIsotopeError(_category_errmsg(self.symbol, "isotope"))

        if isinstance(self._attributes["half-life"], str):
            warnings.warn(
                f"The half-life for {self.symbol} is not known precisely; "
                "returning string with estimated value.",
                MissingParticleDataWarning,
            )

        if self._attributes["half-life"] is None:
            raise MissingParticleDataError(
                f"The half-life of '{self.symbol}' is not available."
            )
        return self._attributes["half-life"]

    @property
    def spin(self) -> Real:
        """
        Return the spin of the particle.

        If the spin is unavailable, then a
        `~plasmapy.particles.exceptions.MissingParticleDataError` will be raised.

        Examples
        --------
        >>> positron = Particle('e+')
        >>> positron.spin
        0.5
        """
        if self._attributes["spin"] is None:
            raise MissingParticleDataError(
                f"The spin of particle '{self.symbol}' is unavailable."
            )

        return self._attributes["spin"]

    @property
    def periodic_table(self) -> namedtuple:
        """
        A `~collections.namedtuple` that provides access to category,
        period, group, and block information about an element.

        Raises
        ------
        `~plasmapy.particles.exceptions.InvalidElementError`
            If the particle is not an element, isotope, or ion.

        Examples
        --------
        >>> gold = Particle('Au')
        >>> gold.periodic_table.category
        'transition metal'
        >>> gold.periodic_table.period
        6
        >>> gold.periodic_table.group
        11
        >>> gold.periodic_table.block
        'd'
        """
        if self.element:
            return self._attributes["periodic table"]
        else:  # coverage: ignore
            raise InvalidElementError(_category_errmsg(self.symbol, "element"))

    @property
    def categories(self) -> Set[str]:
        """
        Return the particle's categories.

        Examples
        --------
        >>> gold = Particle('Au')
        >>> 'transition metal' in gold.categories
        True
        >>> 'antilepton' in gold.categories
        False

        """
        return self._categories

    def is_category(
        self,
        *category_tuple,
        require: Union[str, Iterable[str]] = None,
        any_of: Union[str, Iterable[str]] = None,
        exclude: Union[str, Iterable[str]] = None,
    ) -> bool:
        """
        Determine if the particle meets categorization criteria.

        Return `True` if the particle is consistent with the provided
        categories, and `False` otherwise.

        Parameters
        ----------
        *category_tuple
            Required categories in the form of one or more `str` objects
            or an iterable.

        require : `str` or iterable providing `str` objects, optional, keyword-only
            One or more categories.  This method will return `False` if
            the `Particle` does not belong to all of these categories.

        any_of : `str` or iterable providing `str` objects, optional, keyword-only
            One or more categories. This method will return `False` if
            the `Particle` does not belong to at least one of these
            categories.

        exclude : `str` or iterable providing `str` objects, optional, keyword-only
            One or more categories.  This method will return `False` if
            the `Particle` belongs to any of these categories.

        Notes
        -----
        A `set` containing all valid categories may be accessed by the
        ``valid_categories`` attribute of `~Particle.is_category`.

        Examples
        --------
        Required categories may be entered as positional arguments,
        including as a `list`, `set`, or `tuple` of required categories.

        >>> electron = Particle("e-")
        >>> electron.is_category("lepton")
        True
        >>> electron.is_category("lepton", "baryon")
        False
        >>> electron.is_category(["fermion", "matter"])
        True

        Required arguments may also be provided using the ``require``
        keyword argument.

        >>> electron.is_category(require="lepton")
        True
        >>> electron.is_category(require=["lepton", "baryon"])
        False

        This method will return `False` if the particle does not belong
        to at least one of the categories provided with the ``any_of``
        keyword argument.

        >>> electron.is_category(any_of=["lepton", "baryon"])
        True
        >>> electron.is_category(any_of=("noble gas", "lanthanide", "halogen"))
        False

        This method will return `False` if the particle belongs to any
        of the categories provided in the ``exclude`` keyword argument.

        >>> electron.is_category(exclude="baryon")
        True
        >>> electron.is_category(exclude={"lepton", "baryon"})
        False

        The ``require``, ``any_of``, and ``exclude`` keywords may be
        combined.  If the particle matches all of the provided criteria,
        then `~Particle.is_category` will return `True`.

        >>> electron.is_category(
        ...     require="fermion", any_of={'lepton', 'baryon'}, exclude='charged',
        ... )
        False
        """

        def become_set(arg: Union[str, Set, Tuple, List]) -> Set[str]:
            """Change the argument into a `set`."""
            if arg is None:
                return set()
            if isinstance(arg, set):
                return arg
            if isinstance(arg, str):
                return {arg}
            if isinstance(arg[0], (tuple, list, set)):
                return set(arg[0])
            else:
                return set(arg)

        if category_tuple and require:  # coverage: ignore
            raise ParticleError(
                "No positional arguments are allowed if the `require` keyword "
                "is set in is_category."
            )

        require = become_set(category_tuple) if category_tuple else become_set(require)
        exclude = become_set(exclude)
        any_of = become_set(any_of)

        invalid_categories = (require | exclude | any_of) - _valid_categories

        duplicate_categories = require & exclude | exclude & any_of | require & any_of

        categories_and_adjectives = [
            (invalid_categories, "invalid"),
            (duplicate_categories, "duplicated"),
        ]

        for problem_categories, adjective in categories_and_adjectives:
            if problem_categories:
                raise ParticleError(
                    f"The following categories in {self.__repr__()}"
                    f".is_category are {adjective}: {problem_categories}"
                )

        if exclude and exclude & self._categories:
            return False

        if any_of and not any_of & self._categories:
            return False

        return require <= self._categories

    @property
    def is_electron(self) -> bool:
        """
        Return `True` if the particle is an electron, and `False`
        otherwise.

        Examples
        --------
        >>> Particle('e-').is_electron
        True
        >>> Particle('e+').is_electron
        False

        """
        return self == "e-"

    @property
    def is_ion(self) -> bool:
        """
        Return `True` if the particle is an ion, and `False` otherwise.

        Examples
        --------
        >>> Particle('D+').is_ion
        True
        >>> Particle('H-1 0+').is_ion
        False
        >>> Particle('e+').is_ion
        False

        """
        return self.is_category("ion")

    def ionize(self, n: Integral = 1, inplace: bool = False):
        """
        Create a new `~plasmapy.particles.Particle` instance corresponding
        to the current `~plasmapy.particles.Particle` after being ionized
        ``n`` times.

        If ``inplace`` is `False` (default), then return the ionized
        `~plasmapy.particles.Particle`.

        If ``inplace`` is `True`, then replace the current
        `~plasmapy.particles.Particle` with the newly ionized
        `~plasmapy.particles.Particle`.

        Parameters
        ----------
        n : positive integer
            The number of bound electrons to remove from the
            `~plasmapy.particles.Particle` object.  Defaults to ``1``.

        inplace : bool, optional
            If `True`, then replace the current
            `~plasmapy.particles.Particle` instance with the newly ionized
            `~plasmapy.particles.Particle`.

        Returns
        -------
        particle : ~plasmapy.particles.Particle
            A new `~plasmapy.particles.Particle` object that has been
            ionized ``n`` times relative to the original
            `~plasmapy.particles.Particle`.  If ``inplace`` is `False`,
            instead return `None`.

        Raises
        ------
        `~plasmapy.particles.exceptions.InvalidElementError`
            If the `~plasmapy.particles.Particle` is not an element.

        `~plasmapy.particles.exceptions.ChargeError`
            If no charge information for the `~plasmapy.particles.Particle`
            object is specified.

        `~plasmapy.particles.exceptions.InvalidIonError`
            If there are less than ``n`` remaining bound electrons.

        ValueError
            If ``n`` is not positive.

        Examples
        --------
        >>> Particle("Fe 6+").ionize()
        Particle("Fe 7+")
        >>> helium_particle = Particle("He-4 0+")
        >>> helium_particle.ionize(n=2, inplace=True)
        >>> helium_particle
        Particle("He-4 2+")

        """
        if not self.element:
            raise InvalidElementError(
                f"Cannot ionize {self.symbol} because it is not a "
                f"neutral atom or ion."
            )
        if not self.is_category(any_of={"charged", "uncharged"}):
            raise ChargeError(
                f"Cannot ionize {self.symbol} because its charge " f"is not specified."
            )
        if self.integer_charge == self.atomic_number:
            raise InvalidIonError(
                f"The particle {self.symbol} is already fully "
                f"ionized and cannot be ionized further."
            )
        if not isinstance(n, Integral):
            raise TypeError("n must be a positive integer.")
        if n <= 0:
            raise ValueError("n must be a positive number.")

        base_particle = self.isotope if self.isotope else self.element
        new_integer_charge = self.integer_charge + n

        if inplace:
            self.__init__(base_particle, Z=new_integer_charge)
        else:
            return Particle(base_particle, Z=new_integer_charge)

    def recombine(self, n: Integral = 1, inplace=False):
        """
        Create a new `~plasmapy.particles.Particle` instance corresponding
        to the current `~plasmapy.particles.Particle` after undergoing
        recombination ``n`` times.

        If ``inplace`` is `False` (default), then return the
        `~plasmapy.particles.Particle` that just underwent recombination.

        If ``inplace`` is `True`, then replace the current
        `~plasmapy.particles.Particle` with the `~plasmapy.particles.Particle`
        that just underwent recombination.

        Parameters
        ----------
        n : positive integer
            The number of electrons to recombine into the
            `~plasmapy.particles.Particle` object.

        inplace : bool, optional
            If `True`, then replace the current
            `~plasmapy.particles.Particle` instance with the
            `~plasmapy.particles.Particle` that just underwent
            recombination.

        Returns
        -------
        particle : ~plasmapy.particles.Particle
            A new `~plasmapy.particles.Particle` object that has undergone
            recombination ``n`` times relative to the original
            `~plasmapy.particles.Particle`.  If ``inplace`` is `False`,
            instead return `None`.

        Raises
        ------
        ~plasmapy.particles.InvalidElementError
            If the `~plasmapy.particles.Particle` is not an element.

        ~plasmapy.particles.ChargeError
            If no charge information for the `~plasmapy.particles.Particle`
            object is specified.

        ValueError
            If ``n`` is not positive.

        Examples
        --------
        >>> Particle("Fe 6+").recombine()
        Particle("Fe 5+")
        >>> helium_particle = Particle("He-4 2+")
        >>> helium_particle.recombine(n=2, inplace=True)
        >>> helium_particle
        Particle("He-4 0+")

        """

        if not self.element:
            raise InvalidElementError(
                f"{self.symbol} cannot undergo recombination because "
                f"it is not a neutral atom or ion."
            )
        if not self.is_category(any_of={"charged", "uncharged"}):
            raise ChargeError(
                f"{self.symbol} cannot undergo recombination because "
                f"its charge is not specified."
            )
        if not isinstance(n, Integral):
            raise TypeError("n must be a positive integer.")
        if n <= 0:
            raise ValueError("n must be a positive number.")

        base_particle = self.isotope if self.isotope else self.element
        new_integer_charge = self.integer_charge - n

        if inplace:
            self.__init__(base_particle, Z=new_integer_charge)
        else:
            return Particle(base_particle, Z=new_integer_charge)


Particle.is_category.valid_categories = _valid_categories
"""All valid particle categories."""


class DimensionlessParticle(AbstractParticle):
    """
    A class to represent dimensionless custom particles.

    This class may be used, for example, to represent a particle in a
    dimensionless particle-in-cell simulation.

    Parameters
    ----------
    mass : positive real number, keyword-only, optional
        The mass of the dimensionless particle.  Defaults to `numpy.nan`.

    charge : real number, keyword-only, optional
        The electric charge of the dimensionless particle.  Defaults to
        `numpy.nan`.

    symbol : str, optional
        The symbol to be assigned to the dimensionless particle.

    See Also
    --------
    ~plasmapy.particles.Particle
    ~plasmapy.particles.CustomParticle

    Notes
    -----
    `DimensionlessParticle` instances are not considered `ParticleLike`
    because dimensionless particles cannot uniquely identify a physical
    particle without normalization information.

    Examples
    --------
    >>> from plasmapy.particles import DimensionlessParticle
    >>> dimensionless_particle = DimensionlessParticle(mass=1.0, charge=-1.0, symbol="ξ")
    >>> dimensionless_particle.mass
    1.0
    >>> dimensionless_particle.charge
    -1.0
    >>> dimensionless_particle.symbol
    'ξ'
    """

    def __init__(self, *, mass: Real = None, charge: Real = None, symbol: str = None):
        try:
            self.mass = mass
            self.charge = charge
            self.symbol = symbol
        except Exception as exc:
            raise InvalidParticleError(
                f"Unable to create a custom particle with a mass of "
                f"{mass} and a charge of {charge}."
            ) from exc

    def __repr__(self):
        """
        Return a string representation of a dimensionless particle.

        Examples
        --------
        >>> dimensionless_particle = DimensionlessParticle(mass=1.45, charge=1.23)
        >>> repr(dimensionless_particle)
        'DimensionlessParticle(mass=1.45, charge=1.23)'
        """
        return f"DimensionlessParticle(mass={self.mass}, charge={self.charge})"

    @staticmethod
    def _validate_parameter(obj, can_be_negative=True) -> np.float64:
        """Verify that the argument corresponds to a valid real number."""

        # TODO: Replace with validator? Use an equivalency between coulombs and reals.

        if obj is None or obj is np.nan:
            return np.nan
        elif np.isinf(obj):
            return obj
        elif isinstance(obj, bool):
            raise TypeError("Expecting a real number, not a bool.")
        elif isinstance(obj, u.Quantity) and not isinstance(obj.value, Real):
            raise ValueError("The value of a Quantity must be a real number.")

        try:
            new_obj = np.float64(obj)
        except Exception:
            raise TypeError(f"Cannot convert {obj} to numpy.float64.")

        if hasattr(new_obj, "__len__"):
            raise TypeError("Expecting a real number, not a collection.")

        if not can_be_negative and new_obj < 0:
            raise ValueError("Expecting a nonnegative number.")

        return new_obj

    @property
    def json_dict(self) -> dict:
        """
        A `json` friendly dictionary representation of the particle.

        See `AbstractParticle.json_dict` for more details.

        Examples
        --------
        >>> from plasmapy.particles import DimensionlessParticle
        >>> dimensionless_particle = DimensionlessParticle(mass=1.0, charge=-1.0)
        >>> dimensionless_particle.json_dict
        {'plasmapy_particle': {'type': 'DimensionlessParticle',
            'module': 'plasmapy.particles.particle_class',
            'date_created': '...',
            '__init__': {'args': (), 'kwargs': {'mass': 1.0, 'charge': -1.0,
            'symbol': 'DimensionlessParticle(mass=1.0, charge=-1.0)'}}}}
        >>> dimensionless_particle = DimensionlessParticle(mass=1.0)
        >>> dimensionless_particle.json_dict
        {'plasmapy_particle': {'type': 'DimensionlessParticle',
            'module': 'plasmapy.particles.particle_class',
            'date_created': '...',
            '__init__': {'args': (), 'kwargs': {'mass': 1.0, 'charge': nan,
            'symbol': 'DimensionlessParticle(mass=1.0, charge=nan)'}}}}
        """
        particle_dictionary = super().json_dict
        particle_dictionary["plasmapy_particle"]["__init__"]["kwargs"] = {
            "mass": self.mass,
            "charge": self.charge,
            "symbol": self.symbol,
        }
        return particle_dictionary

    @property
    def mass(self) -> np.float64:
        """The dimensionless mass of the particle."""
        return self._mass

    @property
    def charge(self) -> np.float64:
        """The dimensionless charge of the particle."""
        return self._charge

    @mass.setter
    def mass(self, m: Optional[Union[Real, u.Quantity]]):
        try:
            self._mass = self._validate_parameter(m, can_be_negative=False)
        except (TypeError, ValueError):
            raise InvalidParticleError(
                f"The mass of a dimensionless particle must be a real "
                f"number that is greater than or equal to zero, not: {m}"
            ) from None
        if self._mass is np.nan:
            warnings.warn(
                "DimensionlessParticle mass set to NaN", MissingParticleDataWarning
            )

    @charge.setter
    def charge(self, q: Optional[Union[Real, u.Quantity]]):
        try:
            self._charge = self._validate_parameter(q, can_be_negative=True)
        except (TypeError, ValueError):
            raise InvalidParticleError(
                f"The charge of a dimensionless particle must be a real "
                f"number, not: {q}"
            ) from None
        if self._charge is np.nan:
            warnings.warn(
                "DimensionlessParticle charge set to NaN", MissingParticleDataWarning
            )

    @property
    def symbol(self) -> str:
        """
        The symbol assigned to the dimensionless particle.

        If no symbol was defined, then return the value given by `repr`.
        """
        return self._symbol

    @symbol.setter
    def symbol(self, new_symbol: str):
        if new_symbol is None:
            self._symbol = repr(self)
        elif isinstance(new_symbol, str):
            self._symbol = new_symbol
        else:
            raise TypeError("symbol needs to be a string.")


class CustomParticle(AbstractPhysicalParticle):
    """
    A class to represent custom particles.

    Example use cases for this class include representing an average
    ion in a multi-component plasma, molecules, or dust grains.

    Parameters
    ----------
    mass : ~astropy.units.Quantity, optional
        The mass of the custom particle in units of mass.

    charge : ~astropy.units.Quantity or ~numbers.Real, optional
        The electric charge of the custom particle.  If provided as a
        `~astropy.units.Quantity`, then it must be in units of electric
        charge.  If provided as a real number, then it is treated as the
        ratio of the charge to the elementary charge.

    symbol : str, optional
        The symbol to be assigned to the custom particle.

    Raises
    ------
    InvalidParticleError
        If the charge or mass provided is invalid so that the custom
        particle cannot be created.

    See Also
    --------
    ~plasmapy.particles.Particle
    ~plasmapy.particles.DimensionlessParticle

    Notes
    -----
    If the charge or mass is not specified, then the corresponding value
    will be set to ``numpy.nan`` in the appropriate units.

    Examples
    --------
    >>> from astropy import units as u
    >>> from plasmapy.particles import CustomParticle
    >>> custom_particle = CustomParticle(mass=1.5e-26 * u.kg, charge=-1, symbol="Ξ")
    >>> custom_particle.mass
    <Quantity 1.5e-26 kg>
    >>> custom_particle.charge
    <Quantity -1.60217...e-19 C>
    >>> custom_particle.symbol
    'Ξ'
    """

    def __init__(self, mass: u.kg = None, charge: (u.C, Real) = None, symbol=None):
        try:
            self.mass = mass
            self.charge = charge
            self.symbol = symbol
        except Exception as exc:
            raise InvalidParticleError(
                f"Unable to create a custom particle with a mass of "
                f"{mass} and a charge of {charge}."
            ) from exc

    def __repr__(self):
        """
        Return a string representation of a custom particle.

        Examples
        --------
        >>> custom_particle = CustomParticle(mass=1.2e-26 * u.kg, charge=9.2e-19 * u.C)
        >>> repr(custom_particle)
        'CustomParticle(mass=1.2...e-26 kg, charge=9.2...e-19 C)'
        """
        return f"CustomParticle(mass={self.mass}, charge={self.charge})"

    @property
    def json_dict(self) -> dict:
        """
        A `json` friendly dictionary representation of the particle.

        See `AbstractParticle.json_dict` for more details.

        Examples
        --------
        >>> custom_particle = CustomParticle(mass=5.12 * u.kg, charge=6.2 * u.C, symbol="ξ")
        >>> custom_particle.json_dict
        {'plasmapy_particle': {'type': 'CustomParticle',
            'module': 'plasmapy.particles.particle_class',
            'date_created': '...',
            '__init__': {'args': (), 'kwargs': {'mass': '5.12 kg', 'charge': '6.2 C',
            'symbol': 'ξ'}}}}
        >>> custom_particle = CustomParticle(mass=1.5e-26 * u.kg)
        >>> custom_particle.json_dict
        {'plasmapy_particle': {'type': 'CustomParticle',
            'module': 'plasmapy.particles.particle_class',
            'date_created': '...',
            '__init__': {'args': (), 'kwargs': {'mass': '1.5e-26 kg', 'charge': 'nan C',
            'symbol': 'CustomParticle(mass=1.5e-26 kg, charge=nan C)'}}}}
        """
        particle_dictionary = super().json_dict
        particle_dictionary["plasmapy_particle"]["__init__"]["kwargs"] = {
            "mass": str(self.mass),
            "charge": str(self.charge),
            "symbol": self.symbol,
        }
        return particle_dictionary

    @property
    def charge(self) -> u.C:
        """Return the custom particle's electric charge in coulombs."""
        return self._charge

    @charge.setter
    def charge(self, q: Optional[Union[u.Quantity, Real]]):
        if q is None:
            q = np.nan * u.C
            warnings.warn(
                "CustomParticle charge set to NaN C", MissingParticleDataWarning
            )
        elif isinstance(q, str):
            q = u.Quantity(q)

        if np.isnan(q):
            self._charge = q
        elif isinstance(q, Real):
            self._charge = q * const.e.si
            warnings.warn(
                f"CustomParticle charge set to {q} times the elementary charge."
            )
        elif isinstance(q, u.Quantity):
            if not isinstance(q.value, Real):
                raise InvalidParticleError(
                    "The charge of a custom particle can only be a real "
                    "number or a quantity representing a real number with "
                    "units of charge."
                )
            try:
                self._charge = q.to(u.C)
            except u.UnitsError as exc:
                raise InvalidParticleError(
                    "The charge of a custom particle can only have units "
                    "that are compatible with coulombs."
                ) from exc
        else:
            raise TypeError(
                "The charge of a custom particle must be provided either "
                "as a Quantity with units compatible with coulombs or as "
                "a real number that represents the ratio of the charge to "
                "the elementary charge."
            )

    @property
    def mass(self) -> u.kg:
        """Return the custom particle's mass."""
        return self._mass

    @mass.setter
    def mass(self, m: u.kg):
        if m is None:
            m = np.nan * u.kg
            warnings.warn(
                "CustomParticle mass set to NaN kg", MissingParticleDataWarning
            )
        elif isinstance(m, str):
            m = u.Quantity(m)
        elif not isinstance(m, u.Quantity):
            raise TypeError(
                "The mass of a custom particle must be a nonnegative Quantity "
                "with units of mass."
            )
        if np.isnan(m):
            self._mass = m
        else:
            if not isinstance(m.value, Real):
                raise TypeError(
                    "The mass of a custom particle must be a real number "
                    "with units of mass."
                )
            try:
                self._mass = m.to(u.kg)
                if self.mass < 0 * u.kg:
                    raise ValueError("The mass of a particle must be nonnegative.")
            except u.UnitsError as exc:
                raise u.UnitsError(
                    "The mass of a custom particle must have units of mass."
                ) from exc

    @property
    def mass_energy(self) -> u.J:
        """
        The mass energy of the custom particle.

        Examples
        --------
        >>> import astropy.units as u
        >>> custom_particle = CustomParticle(mass = 2e-25 * u.kg, charge = 0 * u.C)
        >>> custom_particle.mass_energy.to('GeV')
        <Quantity 112.19177208 GeV>
        """
        return (self.mass * const.c ** 2).to(u.J)

    @property
    def symbol(self) -> str:
        """
        The symbol assigned to the custom particle.

        If no symbol was defined, then return the value given by `repr`.
        """
        return self._symbol

    @symbol.setter
    def symbol(self, new_symbol: str):
        if new_symbol is None:
            self._symbol = repr(self)
        elif isinstance(new_symbol, str):
            self._symbol = new_symbol
        else:
            raise TypeError("symbol needs to be a string.")


ParticleLike = Union[str, Integral, Particle, CustomParticle]

ParticleLike.__doc__ = """
An `object` is particle-like if it can be identified as an instance of
`Particle` or `CustomParticle`, or cast into one.

When used as a type hint annotation, `ParticleLike` indicates that an
argument should represent a physical particle. Particle-like objects
can include strings, integers, or instances of the `Particle` or
`CustomParticle` classes.

Notes
-----
Real world particles are typically represented as instances of the
`Particle` class in PlasmaPy.

>>> from plasmapy.particles import Particle
>>> Particle("proton")
Particle("p+")

All `Particle` instances, and objects that can be cast into `Particle`
instances, are particle-like.

* **Elements**

    An element may also be represented by a string that contains the atomic
    symbol (case-sensitive) or the name of the element, or an integer
    representing the atomic number. The element iron can be represented as
    ``"Fe"``, ``"iron"``, ``"Iron"``, ``26``, or ``Particle("Fe")``.

* **Isotopes**

    An isotope may be represented by a string that contains an atomic symbol
    or element name, followed by a hyphen and the mass number (with no spaces
    in between). The isotope :sup:`56`\ Fe can be represented as
    ``"Fe-56"``, ``"iron-56"``, or ``Particle("Fe-56")``. :sup:`1`\ H can be
    represented by ``"protium"``, :sup:`2`\ H can be represented by ``"D"``
    or ``"deuterium"``, and :sup:`3`\ H can be represented by ``"T"`` or
    ``"tritium"``.

* **Ions**

    An ion or ionic level may be represented by a string that contains a
    representation of an element or isotope, followed by charge information.
    For example, ``"He 1+"``, ``"He+"``, ``"helium 1+"``, and ``"He II"``
    all represent singly ionized helium.

    Charge information is typically separated from the element or isotope by
    a space, and given as an integer paired with a plus or minus sign. The
    sign can either precede or follow the integer (e.g., ``"Fe 0+"`` or
    ``"Fe +0"``). The charge information can also be given as a series of
    plus signs or of minus signs that immediately follow the element or
    isotope (e.g., ``"Fe++"`` for Fe\ :sup:`2+`\ ).

    Ions can also be represented using Roman numeral notation, where the Roman
    numeral indicates the integer charge plus one (e.g., ``"H I"`` represents
    H\ :sup:`0+` and ``"He-4 II"`` represents :sup:`4`\ He\ :sup:`1+`).

    D\ :sup:`1+` can also be represented by ``"deuteron"``, T\ :sup:`1+` can
    be represented by ``"triton"``, and :sup:`4`\ He\ :sup:`2+` can be
    represented by ``"alpha"``.

* **Special particles**

    A special particle may be represented by a string that contains
    the name of the particle (case-insensitive) or a standard symbol for it
    (case-sensitive). A neutron can be represented as ``"n"`` or
    ``"neutron"``; a proton can be represented as ``"p+"``, ``"p"``, or
    ``"Proton"``; and an electron can be represented by ``"e-"``, ``"e"``,
    or ``"ELECTRON"``.

* **Custom particles**

    `~plasmapy.particles.particle_class.CustomParticle` instances are
    particle-like because particle properties are provided in physical units.

.. note::

    `~plasmapy.particles.particle_class.DimensionlessParticle`
    instances are *not* particle-like because, without normalization
    information, they do not uniquely identify a physical particle.

See Also
--------
Particle
CustomParticle
~plasmapy.particles.decorators.particle_input

Examples
--------
Using `ParticleLike` as a type hint annotation indicates that an
argument or variable should represent a physical particle.

>>> from plasmapy.particles import ParticleLike, Particle
>>> def is_electron(particle: ParticleLike):
...     return particle == Particle("e-")
"""
