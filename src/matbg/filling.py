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
    It remains a diagnostic proxy, not an experimental calibration.
    """

    if not energies_by_k:
        raise ValueError("energies_by_k must be non-empty")
    occupations = []
    for energies in energies_by_k:
        energies = np.asarray(energies, dtype=float)
        occupations.append(float(np.mean(energies < mu)))
    average_occupation = float(np.mean(occupations))
    return spin_valley_degeneracy * (average_occupation - 0.5)


def selected_band_filling_from_energies(
    energies_by_k: list[np.ndarray],
    mu: float,
    spin_valley_degeneracy: float = 4.0,
) -> float:
    """Return filling relative to half filling for a chosen band set.

    Unlike :func:`filling_proxy_from_energies`, this counts the number of
    occupied selected bands per momentum before applying the spin-valley
    degeneracy.  For a central two-band MATBG flat-band subspace and
    degeneracy 4, the resulting range is ``[-4, 4]``.
    """

    if not energies_by_k:
        raise ValueError("energies_by_k must be non-empty")

    band_counts = {np.asarray(energies).size for energies in energies_by_k}
    if len(band_counts) != 1:
        raise ValueError("all k points must have the same number of energies")
    n_bands = band_counts.pop()
    if n_bands < 1:
        raise ValueError("each k point must contain at least one energy")

    occupied_counts = []
    for energies in energies_by_k:
        energies = np.asarray(energies, dtype=float)
        occupied_counts.append(float(np.count_nonzero(energies < mu)))
    average_occupied = float(np.mean(occupied_counts))
    return spin_valley_degeneracy * (average_occupied - 0.5 * n_bands)
