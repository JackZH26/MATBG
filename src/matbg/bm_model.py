"""Minimal Bistritzer-MacDonald continuum model utilities.

This module is intentionally scoped to the normal-state problem needed for the
next research gate: generate BM eigenvectors in the same orbital ordering used
by the projected-pairing utilities.

Basis ordering:
    for each moire reciprocal vector G:
        top_A, top_B, bottom_A, bottom_B

Units:
    momenta in 1/Angstrom, energies in meV.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


GRAPHENE_A_ANGSTROM = 2.46


def rotation(angle_rad: float) -> np.ndarray:
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    return np.array([[c, -s], [s, c]], dtype=float)


def central_square_indices(n_shell: int) -> list[tuple[int, int]]:
    """Return (m,n) indices with -n_shell <= m,n <= n_shell."""

    return [
        (m, n)
        for m in range(-n_shell, n_shell + 1)
        for n in range(-n_shell, n_shell + 1)
    ]


@dataclass(frozen=True)
class BMParameters:
    theta_deg: float = 1.05
    vF_eV_A: float = 2.135
    w0_meV: float = 87.2
    w1_meV: float = 109.0
    n_shell: int = 3
    valley: int = 1


class BMModel:
    """Single-valley BM continuum model with a square G cutoff."""

    def __init__(self, params: BMParameters | None = None) -> None:
        self.params = params or BMParameters()
        if self.params.valley not in (-1, 1):
            raise ValueError("valley must be +1 or -1")

        self.theta = np.deg2rad(self.params.theta_deg)
        graphene_k = 4.0 * np.pi / (3.0 * GRAPHENE_A_ANGSTROM)
        self.k_theta = 2.0 * graphene_k * np.sin(self.theta / 2.0)

        # First-star momentum transfers for valley +. Valley - is represented
        # by complex conjugating tunneling matrices and reversing chirality in
        # the Dirac blocks.
        self.q1 = self.k_theta * np.array([0.0, -1.0])
        self.q2 = self.k_theta * np.array([np.sqrt(3.0) / 2.0, 0.5])
        self.q3 = self.k_theta * np.array([-np.sqrt(3.0) / 2.0, 0.5])
        self.b1 = self.q2 - self.q1
        self.b2 = self.q3 - self.q1

        self.g_indices = central_square_indices(self.params.n_shell)
        self.g_index_lookup = {idx: i for i, idx in enumerate(self.g_indices)}
        self.g_vectors = np.array(
            [m * self.b1 + n * self.b2 for (m, n) in self.g_indices],
            dtype=float,
        )

    @property
    def n_momenta(self) -> int:
        return len(self.g_indices)

    @property
    def dimension(self) -> int:
        return 4 * self.n_momenta

    def tunneling_matrices(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        w0 = self.params.w0_meV
        w1 = self.params.w1_meV
        omega = np.exp(2j * np.pi / 3.0)
        t1 = np.array([[w0, w1], [w1, w0]], dtype=complex)
        t2 = np.array([[w0, w1 * omega.conjugate()], [w1 * omega, w0]], dtype=complex)
        t3 = np.array([[w0, w1 * omega], [w1 * omega.conjugate(), w0]], dtype=complex)
        if self.params.valley == -1:
            return t1.conj(), t2.conj(), t3.conj()
        return t1, t2, t3

    def dirac_block(self, momentum: np.ndarray, layer: str) -> np.ndarray:
        """Return a rotated monolayer Dirac Hamiltonian."""

        angle = self.theta / 2.0 if layer == "top" else -self.theta / 2.0
        rotated = rotation(-angle) @ momentum
        xi = self.params.valley
        px, py = rotated
        prefactor = -1000.0 * self.params.vF_eV_A
        return prefactor * np.array(
            [[0.0, xi * px - 1j * py], [xi * px + 1j * py, 0.0]],
            dtype=complex,
        )

    def hamiltonian(self, k_vec: np.ndarray) -> np.ndarray:
        """Build the BM Hamiltonian at moire momentum k_vec."""

        k_vec = np.asarray(k_vec, dtype=float)
        h = np.zeros((self.dimension, self.dimension), dtype=complex)
        t1, t2, t3 = self.tunneling_matrices()

        for i, (mn, g_vec) in enumerate(zip(self.g_indices, self.g_vectors)):
            base = 4 * i
            top_slice = slice(base, base + 2)
            bottom_slice = slice(base + 2, base + 4)

            # The bottom layer is shifted by q1 in the standard BM gauge.
            h[top_slice, top_slice] = self.dirac_block(k_vec + g_vec, "top")
            h[bottom_slice, bottom_slice] = self.dirac_block(
                k_vec + g_vec + self.q1,
                "bottom",
            )

            # Couplings top(G) -> bottom(G), bottom(G+b1), bottom(G+b2).
            self._add_tunneling(h, i, mn, (0, 0), t1)
            self._add_tunneling(h, i, mn, (1, 0), t2)
            self._add_tunneling(h, i, mn, (0, 1), t3)

        return h

    def _add_tunneling(
        self,
        h: np.ndarray,
        top_i: int,
        top_mn: tuple[int, int],
        bottom_shift: tuple[int, int],
        matrix: np.ndarray,
    ) -> None:
        bottom_mn = (top_mn[0] + bottom_shift[0], top_mn[1] + bottom_shift[1])
        bottom_i = self.g_index_lookup.get(bottom_mn)
        if bottom_i is None:
            return

        top_slice = slice(4 * top_i, 4 * top_i + 2)
        bottom_slice = slice(4 * bottom_i + 2, 4 * bottom_i + 4)
        h[top_slice, bottom_slice] += matrix
        h[bottom_slice, top_slice] += matrix.conj().T

    def eigensystem(self, k_vec: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Return sorted eigenvalues and eigenvectors."""

        energies, vectors = np.linalg.eigh(self.hamiltonian(k_vec))
        order = np.argsort(energies)
        return energies[order], vectors[:, order]

    def velocity_operator(
        self,
        k_vec: np.ndarray,
        direction: str,
        dk: float = 1.0e-6,
    ) -> np.ndarray:
        """Return finite-difference dH/dk_direction in meV Angstrom."""

        if direction == "x":
            step = np.array([dk, 0.0])
        elif direction == "y":
            step = np.array([0.0, dk])
        else:
            raise ValueError("direction must be 'x' or 'y'")
        return (self.hamiltonian(k_vec + step) - self.hamiltonian(k_vec - step)) / (
            2.0 * dk
        )

    def selected_velocity(
        self,
        k_vec: np.ndarray,
        vectors: np.ndarray,
        direction: str,
        dk: float = 1.0e-6,
    ) -> np.ndarray:
        """Project dH/dk into a selected band subspace."""

        velocity = self.velocity_operator(k_vec, direction=direction, dk=dk)
        return vectors.conj().T @ velocity @ vectors

    def selected_bands(
        self,
        k_vec: np.ndarray,
        n_keep: int = 2,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Return central bands around charge neutrality, sorted by energy."""

        energies, vectors = self.eigensystem(k_vec)
        if n_keep < 1 or n_keep > energies.size:
            raise ValueError("n_keep must be between 1 and the model dimension")
        center = energies.size // 2
        start = center - n_keep // 2
        stop = start + n_keep
        selected = np.arange(start, stop)
        return energies[selected], vectors[:, selected]

    def fractional_k(self, x: float, y: float) -> np.ndarray:
        """Return k = x*b1 + y*b2."""

        return x * self.b1 + y * self.b2

    def centered_mesh(self, nk: int) -> np.ndarray:
        """Return a centered parallelogram mesh in fractional b1,b2 coords."""

        if nk < 1:
            raise ValueError("nk must be positive")
        values = (np.arange(nk) - (nk - 1) / 2.0) / nk
        return np.array(
            [self.fractional_k(x, y) for x in values for y in values],
            dtype=float,
        )

    def central_bandwidth(self, nk: int = 5, n_keep: int = 2) -> float:
        """Estimate bandwidth of the n_keep central bands on a coarse mesh."""

        all_energies = []
        for k_vec in self.centered_mesh(nk):
            energies, _ = self.selected_bands(k_vec, n_keep=n_keep)
            all_energies.extend(energies.tolist())
        return float(max(all_energies) - min(all_energies))
