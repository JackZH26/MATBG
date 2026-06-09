"""Unit-conversion helpers for BM response diagnostics."""

from __future__ import annotations

import numpy as np

from .bm_model import GRAPHENE_A_ANGSTROM

MEV_PER_EV = 1000.0
KELVIN_PER_EV = 11604.51812
DEFAULT_SPIN_VALLEY_DEGENERACY = 4.0


def moire_length_angstrom(
    theta_deg: float,
    graphene_a_angstrom: float = GRAPHENE_A_ANGSTROM,
) -> float:
    """Return the moire lattice constant in Angstrom."""

    theta = np.deg2rad(theta_deg)
    return graphene_a_angstrom / (2.0 * np.sin(theta / 2.0))


def moire_cell_area_angstrom2(theta_deg: float) -> float:
    """Return the triangular moire unit-cell area in square Angstrom."""

    length = moire_length_angstrom(theta_deg)
    return float(np.sqrt(3.0) * length * length / 2.0)


def moire_reciprocal_scale_angstrom_inv(theta_deg: float) -> float:
    """Return the magnitude of a primitive moire reciprocal vector."""

    theta = np.deg2rad(theta_deg)
    graphene_k = 4.0 * np.pi / (3.0 * GRAPHENE_A_ANGSTROM)
    k_theta = 2.0 * graphene_k * np.sin(theta / 2.0)
    return float(np.sqrt(3.0) * k_theta)


def raw_mev_a2_to_ev_a2(
    raw_value: float,
    degeneracy: float = 1.0,
) -> float:
    """Convert raw response values from meV A^2 to eV A^2."""

    return degeneracy * raw_value / MEV_PER_EV


def ev_a2_to_cell_energy_ev(
    value_ev_a2: float,
    theta_deg: float,
) -> float:
    """Convert eV A^2 to an energy scale per moire unit-cell area."""

    return value_ev_a2 / moire_cell_area_angstrom2(theta_deg)


def ev_a2_to_cell_kelvin(
    value_ev_a2: float,
    theta_deg: float,
) -> float:
    """Convert eV A^2 to Kelvin after dividing by the moire cell area."""

    return KELVIN_PER_EV * ev_a2_to_cell_energy_ev(value_ev_a2, theta_deg)
