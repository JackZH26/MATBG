"""Pairing-matrix utilities for MATBG interband-pairing tests.

The functions here are intentionally small and model-agnostic.  They define
orbital-basis pairing matrices, project them to a normal-state band basis, and
run the algebraic checks needed before production stiffness scans.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


INTERNAL_BASIS = ("top_A", "top_B", "bottom_A", "bottom_B")


def _pauli() -> dict[str, np.ndarray]:
    return {
        "0": np.eye(2, dtype=complex),
        "x": np.array([[0, 1], [1, 0]], dtype=complex),
        "y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "z": np.array([[1, 0], [0, -1]], dtype=complex),
    }


def internal_pairing_matrix(name: str) -> np.ndarray:
    """Return a 4x4 layer-sublattice pairing matrix.

    The internal basis is (top_A, top_B, bottom_A, bottom_B).  Matrix names use
    ``tau{layer}_sigma{sublattice}``, for example ``taux_sigma0``.
    """

    aliases = {
        "identity_s": "tau0_sigma0",
        "interlayer_same_sublattice_s": "taux_sigma0",
        "sublattice_imbalanced_s": "tau0_sigmaz",
        "interlayer_sublattice_mixed_s": "taux_sigmax",
        "layer_sublattice_imbalanced_s": "tauz_sigmaz",
    }
    name = aliases.get(name, name)

    if "_sigma" not in name or not name.startswith("tau"):
        raise ValueError(f"Unsupported pairing matrix name: {name}")

    tau_name, sigma_name = name.split("_sigma", 1)
    tau_key = tau_name.replace("tau", "")
    sigma_key = sigma_name
    matrices = _pauli()
    if tau_key not in matrices or sigma_key not in matrices:
        raise ValueError(f"Unsupported Pauli key in pairing matrix: {name}")

    return np.kron(matrices[tau_key], matrices[sigma_key])


def expand_internal_matrix(matrix: np.ndarray, n_momenta: int) -> np.ndarray:
    """Expand a 4x4 internal matrix over momentum-shell blocks."""

    matrix = np.asarray(matrix, dtype=complex)
    if matrix.shape != (4, 4):
        raise ValueError(f"Expected a 4x4 internal matrix, got {matrix.shape}")
    if n_momenta < 1:
        raise ValueError("n_momenta must be positive")
    return np.kron(np.eye(n_momenta, dtype=complex), matrix)


def frobenius_normalize(matrix: np.ndarray, target_norm: float) -> np.ndarray:
    """Scale ``matrix`` to the requested Frobenius norm."""

    norm = np.linalg.norm(matrix)
    if norm == 0:
        raise ValueError("Cannot normalize a zero matrix")
    return matrix * (target_norm / norm)


def orbital_pairing_matrix(
    delta0: float,
    eta: float,
    n_momenta: int,
    m0: str = "tau0_sigma0",
    m1: str = "taux_sigma0",
    normalization: str = "fixed_frobenius_norm",
) -> np.ndarray:
    """Build ``Delta_orb = delta0 * normalize[M0 + eta M1]``.

    ``normalization`` can be:
    - ``fixed_frobenius_norm``: keep ``||M0 + eta M1||_F = ||M0||_F``.
    - ``fixed_delta0``: do not rescale the matrix combination.
    """

    m0_orb = expand_internal_matrix(internal_pairing_matrix(m0), n_momenta)
    m1_orb = expand_internal_matrix(internal_pairing_matrix(m1), n_momenta)
    raw = m0_orb + eta * m1_orb

    if normalization == "fixed_frobenius_norm":
        raw = frobenius_normalize(raw, np.linalg.norm(m0_orb))
    elif normalization == "fixed_delta0":
        pass
    else:
        raise ValueError(f"Unsupported normalization mode: {normalization}")

    return delta0 * raw


def project_pairing(
    u_k: np.ndarray,
    delta_orb: np.ndarray,
    u_minus_k: np.ndarray,
) -> np.ndarray:
    """Project an orbital-basis pairing matrix into the band basis.

    Formula:
        Delta_band(k) = U^\dagger(k) Delta_orb(k) U^*(-k)
    """

    return u_k.conj().T @ delta_orb @ u_minus_k.conj()


def interband_weight(delta_band: np.ndarray) -> float:
    """Return sum_{n != m}|Delta_nm|^2 / sum_{n,m}|Delta_nm|^2."""

    weights = np.abs(delta_band) ** 2
    total = float(np.sum(weights))
    if total == 0:
        return 0.0
    diagonal = float(np.sum(np.abs(np.diag(delta_band)) ** 2))
    return (total - diagonal) / total


def bdg_hamiltonian(
    eps_k: Iterable[float],
    eps_minus_k: Iterable[float],
    delta_band: np.ndarray,
    mu: float = 0.0,
) -> np.ndarray:
    """Build a finite-band BdG Hamiltonian at paired momenta k and -k."""

    eps_k = np.asarray(list(eps_k), dtype=float)
    eps_minus_k = np.asarray(list(eps_minus_k), dtype=float)
    delta_band = np.asarray(delta_band, dtype=complex)

    n_bands = eps_k.size
    if eps_minus_k.size != n_bands:
        raise ValueError("eps_k and eps_minus_k must have the same length")
    if delta_band.shape != (n_bands, n_bands):
        raise ValueError(
            f"delta_band shape {delta_band.shape} incompatible with {n_bands} bands"
        )

    upper_left = np.diag(eps_k - mu)
    lower_right = -np.diag(eps_minus_k - mu)
    upper = np.hstack([upper_left, delta_band])
    lower = np.hstack([delta_band.conj().T, lower_right])
    return np.vstack([upper, lower])


def random_band_phases(n_bands: int, rng: np.random.Generator) -> np.ndarray:
    """Return a diagonal matrix of random U(1) band phases."""

    phases = rng.uniform(0.0, 2.0 * np.pi, size=n_bands)
    return np.diag(np.exp(1j * phases))


def apply_band_gauge(u: np.ndarray, gauge: np.ndarray) -> np.ndarray:
    """Apply a band-basis phase convention change U -> U G."""

    return u @ gauge


def gauge_transform_projected_pairing(
    delta_band: np.ndarray,
    gauge_k: np.ndarray,
    gauge_minus_k: np.ndarray,
) -> np.ndarray:
    """Expected projected-pairing transformation under U(k)->U(k)G(k)."""

    return gauge_k.conj().T @ delta_band @ gauge_minus_k.conj()


def relative_norm(a: np.ndarray, b: np.ndarray | None = None) -> float:
    """Return ||a-b||/max(||a||, ||b||, 1) or ||a|| if b is None."""

    if b is None:
        return float(np.linalg.norm(a))
    denom = max(float(np.linalg.norm(a)), float(np.linalg.norm(b)), 1.0)
    return float(np.linalg.norm(a - b) / denom)


def hermiticity_error(matrix: np.ndarray) -> float:
    """Relative Hermiticity error."""

    return relative_norm(matrix, matrix.conj().T)


def paired_spectrum_error(h_k: np.ndarray, h_minus_k: np.ndarray) -> float:
    """Relative error for the paired-spectrum PH check E(k) = -E(-k)."""

    eig_k = np.sort(np.linalg.eigvalsh(h_k))
    eig_minus = np.sort(-np.linalg.eigvalsh(h_minus_k))
    return relative_norm(eig_k, eig_minus)


def pairing_symmetry_error(delta_k: np.ndarray, delta_minus_k: np.ndarray) -> float:
    """Relative error for Delta(k) = Delta^T(-k)."""

    return relative_norm(delta_k, delta_minus_k.T)


@dataclass(frozen=True)
class GateCheckResult:
    eta: float
    normalization: str
    interband_weight: float
    pairing_symmetry_error: float
    hermiticity_error_k: float
    hermiticity_error_minus_k: float
    particle_hole_error: float
    gauge_projection_error: float
    gauge_spectrum_error: float

    def passed(
        self,
        pairing_tol: float = 1.0e-10,
        hermiticity_tol: float = 1.0e-12,
        particle_hole_tol: float = 1.0e-8,
        gauge_projection_tol: float = 1.0e-10,
        gauge_spectrum_tol: float = 1.0e-8,
    ) -> bool:
        return (
            self.pairing_symmetry_error < pairing_tol
            and self.hermiticity_error_k < hermiticity_tol
            and self.hermiticity_error_minus_k < hermiticity_tol
            and self.particle_hole_error < particle_hole_tol
            and self.gauge_projection_error < gauge_projection_tol
            and self.gauge_spectrum_error < gauge_spectrum_tol
        )
