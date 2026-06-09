"""Filling diagnostics for finite-band BM scans."""

from __future__ import annotations

import numpy as np


def filling_proxy_from_energies(
    energies_by_k: list[np.ndarray],
    mu: float,
    spin_valley_degeneracy: float = 4.0,
) -> float:
    """Return a simple normal-state filling proxy relative to half filling.

    The proxy counts occupied retained-band states at T=0 and maps the average
    occupation relative to half filling onto ``[-degeneracy/2, degeneracy/2]``.
    For the common two-flat-band case with spin/valley degeneracy 4, this gives
    a range close to ``[-4, 4]``.  For larger retained subspaces it remains a
    diagnostic proxy, not an experimental calibration.
    """

    if not energies_by_k:
        raise ValueError("energies_by_k must be non-empty")
    occupations = []
    for energies in energies_by_k:
        energies = np.asarray(energies, dtype=float)
        occupations.append(float(np.mean(energies < mu)))
    average_occupation = float(np.mean(occupations))
    return spin_valley_degeneracy * (average_occupation - 0.5)
