"""Reusable response-scan helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from .bm_model import BMModel
from .filling import filling_proxy_from_energies
from .pairing import interband_weight, orbital_pairing_matrix, project_pairing
from .stiffness import stiffness_components


@dataclass(frozen=True)
class KPointResponseData:
    k_vec: np.ndarray
    eps: np.ndarray
    vectors: np.ndarray
    velocity_x: np.ndarray
    velocity_y: np.ndarray


def build_response_cache(
    model: BMModel,
    nk: int,
    n_keep: int,
    dk: float = 1.0e-6,
) -> list[KPointResponseData]:
    """Precompute normal-state data reused across eta/mu scans."""

    cache: list[KPointResponseData] = []
    for k_vec in model.centered_mesh(nk):
        eps, vectors = model.selected_bands(k_vec, n_keep=n_keep)
        cache.append(
            KPointResponseData(
                k_vec=k_vec,
                eps=eps,
                vectors=vectors,
                velocity_x=model.selected_velocity(k_vec, vectors, "x", dk=dk),
                velocity_y=model.selected_velocity(k_vec, vectors, "y", dk=dk),
            )
        )
    return cache


def _average(values: list[float]) -> float:
    return float(np.mean(np.asarray(values, dtype=float)))


def evaluate_response_row(
    cache: list[KPointResponseData],
    n_momenta: int,
    dimension: int,
    eta: float,
    normalization: str,
    m0: str,
    m1: str,
    delta0: float,
    mu: float,
    nk: int,
    n_shell: int,
    n_keep: int,
) -> dict[str, object]:
    """Evaluate one eta/normalization response row using cached BM data."""

    delta_orb = orbital_pairing_matrix(
        delta0=delta0,
        eta=eta,
        n_momenta=n_momenta,
        m0=m0,
        m1=m1,
        normalization=normalization,
    )

    weights: list[float] = []
    values: dict[str, list[float]] = {
        "Dxx_total": [],
        "Dxx_conv": [],
        "Dxx_geom": [],
        "Dxx_cross": [],
        "Dyy_total": [],
        "Dyy_conv": [],
        "Dyy_geom": [],
        "Dyy_cross": [],
        "closure_error": [],
        "bdg_hermiticity_error": [],
        "ph_spectrum_error": [],
    }

    for item in cache:
        # tr_sewn convention: U_-(-k) := U_+(k)^*
        delta_band = project_pairing(item.vectors, delta_orb, item.vectors.conj())
        weights.append(interband_weight(delta_band))

        for prefix, velocity in (("Dxx", item.velocity_x), ("Dyy", item.velocity_y)):
            components = stiffness_components(
                eps_k=item.eps,
                delta_band=delta_band,
                velocity_band=velocity,
                mu=mu,
            )
            values[f"{prefix}_total"].append(components.total)
            values[f"{prefix}_conv"].append(components.conv)
            values[f"{prefix}_geom"].append(components.geom)
            values[f"{prefix}_cross"].append(components.cross)
            values["closure_error"].append(components.closure_error)
            values["bdg_hermiticity_error"].append(components.bdg_hermiticity_error)
            values["ph_spectrum_error"].append(components.ph_spectrum_error)

    dxx_total = _average(values["Dxx_total"])
    dyy_total = _average(values["Dyy_total"])
    dxx_geom = _average(values["Dxx_geom"])
    dyy_geom = _average(values["Dyy_geom"])
    d_iso = 0.5 * (dxx_total + dyy_total)
    geom_fraction = (
        (dxx_geom + dyy_geom) / (dxx_total + dyy_total)
        if (dxx_total + dyy_total) != 0
        else np.nan
    )
    anisotropy_ratio = dxx_total / dyy_total if dyy_total != 0 else np.nan
    anisotropy_norm = (
        (dxx_total - dyy_total) / (dxx_total + dyy_total)
        if (dxx_total + dyy_total) != 0
        else np.nan
    )

    row: dict[str, object] = {
        "eta": eta,
        "normalization": normalization,
        "m0": m0,
        "m1": m1,
        "partner": "tr_sewn",
        "nk": nk,
        "n_shell": n_shell,
        "n_keep": n_keep,
        "dimension": dimension,
        "delta0_meV": delta0,
        "mu_meV": mu,
        "nu_proxy": filling_proxy_from_energies([item.eps for item in cache], mu),
        "interband_pairing_weight_mean": _average(weights),
        "D_iso_raw": d_iso,
        "geom_fraction_total": geom_fraction,
        "anisotropy_ratio": anisotropy_ratio,
        "anisotropy_norm": anisotropy_norm,
        "max_closure_error": float(np.max(values["closure_error"])),
        "max_bdg_hermiticity_error": float(np.max(values["bdg_hermiticity_error"])),
        "max_ph_spectrum_error": float(np.max(values["ph_spectrum_error"])),
    }
    for key in (
        "Dxx_total",
        "Dxx_conv",
        "Dxx_geom",
        "Dxx_cross",
        "Dyy_total",
        "Dyy_conv",
        "Dyy_geom",
        "Dyy_cross",
    ):
        row[f"{key}_raw"] = _average(values[key])
    return row


def evaluate_eta_grid(
    cache: list[KPointResponseData],
    n_momenta: int,
    dimension: int,
    etas: Iterable[float],
    normalizations: Iterable[str],
    m0: str,
    m1: str,
    delta0: float,
    mu: float,
    nk: int,
    n_shell: int,
    n_keep: int,
) -> list[dict[str, object]]:
    """Evaluate a full eta x normalization grid."""

    rows: list[dict[str, object]] = []
    for normalization in normalizations:
        for eta in etas:
            rows.append(
                evaluate_response_row(
                    cache=cache,
                    n_momenta=n_momenta,
                    dimension=dimension,
                    eta=eta,
                    normalization=normalization,
                    m0=m0,
                    m1=m1,
                    delta0=delta0,
                    mu=mu,
                    nk=nk,
                    n_shell=n_shell,
                    n_keep=n_keep,
                )
            )
    return rows
