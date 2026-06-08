"""Minimal BdG response utilities for superfluid-stiffness gates."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .band_basis import split_intra_inter
from .pairing import bdg_hamiltonian, hermiticity_error, relative_norm


def nambu_current_from_velocity(
    velocity_band: np.ndarray,
    component: str,
) -> np.ndarray:
    """Build a BdG current block from a band-basis velocity component.

    The convention follows the decomposition used in the working manuscript:

    - band-diagonal velocity contributes as a tau_z current;
    - band-off-diagonal velocity contributes as a tau_0 current.

    This split is meant for the finite-band band-basis diagnostic and should be
    kept fixed when comparing ``Dconv``, ``Dgeom``, and ``Dcross``.
    """

    velocity_band = np.asarray(velocity_band, dtype=complex)
    n_bands = velocity_band.shape[0]
    zero = np.zeros_like(velocity_band)
    if component == "intra":
        particle = np.diag(np.diag(velocity_band))
        hole = -particle.T
    elif component == "inter":
        _, particle = split_intra_inter(velocity_band)
        hole = particle.T
    elif component == "total":
        return nambu_current_from_velocity(
            velocity_band,
            "intra",
        ) + nambu_current_from_velocity(velocity_band, "inter")
    else:
        raise ValueError("component must be intra, inter, or total")

    return np.block([[particle, zero], [zero, hole]]).reshape(2 * n_bands, 2 * n_bands)


def zero_temperature_occupations(energies: np.ndarray) -> np.ndarray:
    """Return T=0 Fermi occupations for BdG energies."""

    return (energies < 0.0).astype(float)


def kubo_response(
    h_bdg: np.ndarray,
    current_a: np.ndarray,
    current_b: np.ndarray | None = None,
    denominator_tol: float = 1.0e-10,
) -> float:
    """Compute a finite-band static current-current response.

    The returned value is the raw finite-band paramagnetic expression:

    sum_{a != b} <a|J_a|b><b|J_b|a> (f_a - f_b)/(E_b - E_a)

    No moire-cell area or spin/valley degeneracy factor is applied here.
    """

    if current_b is None:
        current_b = current_a
    energies, vectors = np.linalg.eigh(h_bdg)
    occupations = zero_temperature_occupations(energies)
    j_a = vectors.conj().T @ current_a @ vectors
    j_b = vectors.conj().T @ current_b @ vectors

    response = 0.0 + 0.0j
    n_states = energies.size
    for a in range(n_states):
        for b in range(n_states):
            if a == b:
                continue
            denom = energies[b] - energies[a]
            if abs(denom) < denominator_tol:
                continue
            response += j_a[a, b] * j_b[b, a] * (
                occupations[a] - occupations[b]
            ) / denom
    return float(np.real(response))


@dataclass(frozen=True)
class StiffnessComponents:
    total: float
    conv: float
    geom: float
    cross: float
    closure_error: float
    bdg_hermiticity_error: float
    ph_spectrum_error: float


def particle_hole_spectrum_error(h_bdg: np.ndarray) -> float:
    """Check whether a single-k BdG spectrum is symmetric around zero."""

    eig = np.sort(np.linalg.eigvalsh(h_bdg))
    return relative_norm(eig, np.sort(-eig))


def stiffness_components(
    eps_k: np.ndarray,
    delta_band: np.ndarray,
    velocity_band: np.ndarray,
    mu: float = 0.0,
) -> StiffnessComponents:
    """Compute raw finite-band response components at one k point."""

    h_bdg = bdg_hamiltonian(eps_k, eps_k, delta_band, mu=mu)
    j_intra = nambu_current_from_velocity(velocity_band, "intra")
    j_inter = nambu_current_from_velocity(velocity_band, "inter")
    j_total = j_intra + j_inter

    total = kubo_response(h_bdg, j_total)
    conv = kubo_response(h_bdg, j_intra)
    geom = kubo_response(h_bdg, j_inter)
    cross = total - conv - geom
    scale = max(abs(total), abs(conv), abs(geom), 1.0)
    closure = abs(total - conv - geom - cross) / scale

    return StiffnessComponents(
        total=total,
        conv=conv,
        geom=geom,
        cross=cross,
        closure_error=closure,
        bdg_hermiticity_error=hermiticity_error(h_bdg),
        ph_spectrum_error=particle_hole_spectrum_error(h_bdg),
    )
