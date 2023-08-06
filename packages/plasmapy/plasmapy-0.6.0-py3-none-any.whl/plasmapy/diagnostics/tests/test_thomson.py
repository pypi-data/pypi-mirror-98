"""
Tests for Thomson scattering analysis functions
"""

import astropy.units as u
import numpy as np
import pytest

from plasmapy.diagnostics import thomson
from plasmapy.particles import Particle


def width_at_value(x, y, val):
    """
    Calculates the width of a curve at a given value.
    """
    above = np.where(y > val, x, np.nan)
    return np.abs(np.nanmax(above) - np.nanmin(above))


def gen_collective_spectrum():
    """
    Generates an example Thomson scattering spectrum in the collective regime
    """
    wavelengths = np.arange(520, 545, 0.01) * u.nm
    probe_wavelength = 532 * u.nm
    n = 5e17 * u.cm ** -3
    probe_vec = np.array([1, 0, 0])
    scatter_vec = np.array([0, 1, 0])
    Te = 10 * u.eV
    Ti = np.array([10]) * u.eV
    ion_species = ["C-12 5+"]

    alpha, Skw = thomson.spectral_density(
        wavelengths,
        probe_wavelength,
        n,
        Te,
        Ti,
        ion_species=ion_species,
        probe_vec=probe_vec,
        scatter_vec=scatter_vec,
    )

    return alpha, wavelengths, Skw


def gen_multiple_ion_species_spectrum():
    """
    Generates an example Thomson scattering spectrum for multiple ion species
    that also have drift velocities. Parameters are set to be in the
    collective regime where ion species are important.
    """
    wavelengths = np.arange(520, 545, 0.01) * u.nm
    probe_wavelength = 532 * u.nm
    n = 5e17 * u.cm ** -3
    probe_vec = np.array([1, 0, 0])
    scatter_vec = np.array([0, 1, 0])
    ifract = np.array([0.7, 0.3])
    Te = 10 * u.eV
    Ti = np.array([5, 5]) * u.eV
    electron_vel = np.array([[300, 0, 0]]) * u.km / u.s
    ion_vel = np.array([[-500, 0, 0], [0, 500, 0]]) * u.km / u.s

    # Use this to also test passing in ion species as Particle objects
    ion_species = [Particle("p+"), Particle("C-12 5+")]

    alpha, Skw = thomson.spectral_density(
        wavelengths,
        probe_wavelength,
        n,
        Te,
        Ti,
        ifract=ifract,
        ion_species=ion_species,
        probe_vec=probe_vec,
        scatter_vec=scatter_vec,
        electron_vel=electron_vel,
        ion_vel=ion_vel,
    )

    return alpha, wavelengths, Skw


def gen_non_collective_spectrum():
    """
    Generates an example Thomson scattering spectrum in the non-collective
    regime
    """
    wavelengths = np.arange(500, 570, 0.01) * u.nm
    probe_wavelength = 532 * u.nm
    n = 5e15 * u.cm ** -3
    probe_vec = np.array([1, 0, 0])
    scatter_vec = np.array([0, 1, 0])
    Te = 100 * u.eV
    Ti = np.array([10]) * u.eV
    ion_species = ["H+"]

    alpha, Skw = thomson.spectral_density(
        wavelengths,
        probe_wavelength,
        n,
        Te,
        Ti,
        ion_species=ion_species,
        probe_vec=probe_vec,
        scatter_vec=scatter_vec,
    )

    return alpha, wavelengths, Skw


def test_different_input_types():

    # Define some constants
    wavelengths = np.arange(520, 545, 0.01) * u.nm
    probe_wavelength = 532 * u.nm
    n = 5e17 * u.cm ** -3
    probe_vec = np.array([1, 0, 0])
    scatter_vec = np.array([0, 1, 0])
    ifract = np.array([1.0])
    Te = np.array([10]) * u.eV
    Ti = np.array([10]) * u.eV
    ion_species = "C-12 5+"

    # Raise a ValueError with inconsistent ion array lengths
    with pytest.raises(ValueError):
        alpha, Skw = thomson.spectral_density(
            wavelengths,
            probe_wavelength,
            n,
            Te,
            Ti,
            ifract=np.array([0.5, 0.5]),
            ion_species=ion_species,
            probe_vec=probe_vec,
            scatter_vec=scatter_vec,
        )

    # Raise a ValueError with inconsistent ion temperature array
    with pytest.raises(ValueError):
        alpha, Skw = thomson.spectral_density(
            wavelengths,
            probe_wavelength,
            n,
            Te,
            np.array([5, 5]) * u.eV,
            ifract=ifract,
            ion_species=ion_species,
            probe_vec=probe_vec,
            scatter_vec=scatter_vec,
        )

    # Raise a ValueError with empty ion_species
    with pytest.raises(ValueError):
        alpha, Skw = thomson.spectral_density(
            wavelengths,
            probe_wavelength,
            n,
            Te,
            Ti,
            ifract=ifract,
            ion_species=[],
            probe_vec=probe_vec,
            scatter_vec=scatter_vec,
        )

    # Raise a Value Error with inconsistent electron array lengths
    # Te.size != efract.size
    with pytest.raises(ValueError):
        alpha, Skw = thomson.spectral_density(
            wavelengths,
            probe_wavelength,
            n,
            np.array([1, 10]) * u.eV,
            Ti,
            efract=np.array([0.5, 0.2, 0.3]),
            probe_vec=probe_vec,
            scatter_vec=scatter_vec,
        )

    # Electron vel shape not compatible with efract.size
    with pytest.raises(ValueError):
        alpha, Skw = thomson.spectral_density(
            wavelengths,
            probe_wavelength,
            n,
            Te,
            Ti,
            efract=np.array([0.5, 0.5]),
            electron_vel=np.array([[100, 0, 0]]) * u.km / u.s,
            probe_vec=probe_vec,
            scatter_vec=scatter_vec,
        )


def test_collective_spectrum():
    """
    Compares the generated spectrum to previously determined values
    """
    alpha, wavelength, Skw = gen_collective_spectrum()

    # Check that alpha is correct
    assert np.isclose(
        alpha.value, 1.801, atol=0.01
    ), "Collective case alpha returns {alpha} instead of expected 1.801"

    i_width = width_at_value(wavelength.value, Skw.value, 2e-13)
    e_width = width_at_value(wavelength.value, Skw.value, 0.2e-13)

    # Check that the widths of the ion and electron features match expectations
    assert np.isclose(i_width, 0.1599, 1e-3), (
        "Collective case ion feature "
        f"width is {i_width}"
        "instead of expected 0.1599"
    )

    assert np.isclose(e_width, 17.7899, 1e-3), (
        "Collective case electron "
        f"feature width is {e_width} "
        "instead of expected 17.7899"
    )


def test_non_collective_spectrum():
    """
    Compares the generated spectrum to previously determined values
    """
    alpha, wavelength, Skw = gen_non_collective_spectrum()

    # Check that alpha is correct
    assert np.isclose(
        alpha.value, 0.05707, atol=0.01
    ), "Non-collective case alpha returns {alpha} instead of expected 0.05707"

    e_width = width_at_value(wavelength.value, Skw.value, 0.2e-13)

    # Check that the widts of the electron feature matchs expectations
    assert np.isclose(e_width, 22.6699, 1e-3), (
        "Non-collective case electron "
        f"feature width is {e_width} "
        "instead of expected 22.6699"
    )


def test_multiple_ion_species_spectrum():
    """
    Compares the generated spectrum to previously determined values
    """

    alpha, wavelength, Skw = gen_multiple_ion_species_spectrum()

    # Compute the width and max of the spectrum, and the wavelength
    # of the max (sensitive to ion vel)
    width = width_at_value(wavelength.value, Skw.value, 0.2e-11)
    max_skw = np.max(Skw.value)
    max_wavelength = wavelength.value[np.argmax(Skw.value)]

    # Check width
    assert np.isclose(width, 0.049999, 1e-2), (
        f"Multiple ion species case spectrum width is {width} instead of "
        "expected 0.04999"
    )

    # Check max value
    assert np.isclose(max_skw, 2.4e-11, 1e-11), (
        f"Multiple ion species case spectrum max is {max_skw} instead of "
        "expected 2.4e-11"
    )

    # Check max peak location
    assert np.isclose(max_wavelength, 530.799, 1e-2), (
        "Multiple ion species case spectrum peak wavelength is "
        f"{max_wavelength} instead of expected 530.79"
    )


def test_split_populations():
    """
    This test makes sure that splitting a single population of ions or electrons
    into two identical halves returns the same result.
    """

    wavelengths = np.arange(520, 545, 0.01) * u.nm
    probe_wavelength = 532 * u.nm
    n = 5e17 * u.cm ** -3
    probe_vec = np.array([1, 0, 0])
    scatter_vec = np.array([0, 1, 0])

    # Combined
    Te = np.array([10]) * u.eV
    Ti = np.array([10]) * u.eV
    ion_species = ["H+"]
    ifract = np.array([1.0])
    efract = np.array([1.0])

    alpha, Skw0 = thomson.spectral_density(
        wavelengths,
        probe_wavelength,
        n,
        Te,
        Ti,
        ifract=ifract,
        efract=efract,
        ion_species=ion_species,
        probe_vec=probe_vec,
        scatter_vec=scatter_vec,
    )

    # Split e and i populations into two parts
    # this should not change the results since the parts are identical
    Te = np.array([10, 10]) * u.eV
    Ti = np.array([10, 10]) * u.eV
    ion_species = ["H+", "H+"]
    ifract = np.array([0.2, 0.8])
    efract = np.array([0.8, 0.2])

    alpha, Skw1 = thomson.spectral_density(
        wavelengths,
        probe_wavelength,
        n,
        Te,
        Ti,
        ifract=ifract,
        efract=efract,
        ion_species=ion_species,
        probe_vec=probe_vec,
        scatter_vec=scatter_vec,
    )

    # Calculate the deviation between the two spectra
    # (any differences should be in the noise)
    deviation = (Skw0 - Skw1) / Skw0 * 100

    assert np.all(deviation < 1e-6), "Failed split populations test"
