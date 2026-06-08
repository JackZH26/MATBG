"""Band-basis helper functions."""

from __future__ import annotations

import numpy as np

from .pairing import relative_norm


def split_intra_inter(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Split a band-basis matrix into diagonal and off-diagonal parts."""

    matrix = np.asarray(matrix, dtype=complex)
    intra = np.diag(np.diag(matrix))
    inter = matrix - intra
    return intra, inter


def offdiag_weight(matrix: np.ndarray) -> float:
    """Return ||offdiag(M)||_F^2 / ||M||_F^2."""

    matrix = np.asarray(matrix, dtype=complex)
    total = float(np.linalg.norm(matrix) ** 2)
    if total == 0:
        return 0.0
    _, inter = split_intra_inter(matrix)
    return float(np.linalg.norm(inter) ** 2 / total)


def decomposition_error(matrix: np.ndarray) -> float:
    """Return relative error of M = M_intra + M_inter."""

    intra, inter = split_intra_inter(matrix)
    return relative_norm(matrix, intra + inter)


def hermitian_projection_error(matrix: np.ndarray) -> float:
    """Return relative Hermiticity error."""

    return relative_norm(matrix, matrix.conj().T)
