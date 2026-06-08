"""Utilities for aligning paired valley subspaces.

The BM eigenvectors from two valleys are only defined up to unitary rotations
inside any retained finite-band subspace.  Before interpreting projected
pairing matrix elements as band-diagonal or band-off-diagonal, we need a
documented sewing convention.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .pairing import relative_norm


@dataclass(frozen=True)
class SewingResult:
    aligned_vectors: np.ndarray
    unitary: np.ndarray
    singular_values: np.ndarray
    alignment_error: float
    min_singular_value: float
    mean_singular_value: float


def procrustes_sew_subspace(
    raw_partner_vectors: np.ndarray,
    target_vectors: np.ndarray,
) -> SewingResult:
    """Align raw partner eigenvectors to target vectors by a unitary rotation.

    Given orthonormal column matrices A and B, find the unitary R that minimizes
    ||A R - B||_F.  The solution follows from the SVD of A^\dagger B.
    """

    if raw_partner_vectors.shape != target_vectors.shape:
        raise ValueError(
            "raw_partner_vectors and target_vectors must have the same shape"
        )

    overlap = raw_partner_vectors.conj().T @ target_vectors
    left, singular_values, right_h = np.linalg.svd(overlap)
    unitary = left @ right_h
    aligned = raw_partner_vectors @ unitary
    return SewingResult(
        aligned_vectors=aligned,
        unitary=unitary,
        singular_values=singular_values,
        alignment_error=relative_norm(aligned, target_vectors),
        min_singular_value=float(np.min(singular_values)),
        mean_singular_value=float(np.mean(singular_values)),
    )


def identity_time_reversal_target(u_k: np.ndarray) -> np.ndarray:
    """Return the identity-orbital time-reversal target U(k)^*."""

    return u_k.conj()
