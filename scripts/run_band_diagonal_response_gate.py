#!/usr/bin/env python3
"""Run a band-diagonal uniform-s response baseline."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from matbg.bm_model import BMModel, BMParameters  # noqa: E402
from matbg.filling import filling_proxy_from_energies  # noqa: E402
from matbg.pairing import interband_weight  # noqa: E402
from matbg.response_scan import build_response_cache  # noqa: E402
from matbg.stiffness import stiffness_components  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nk", type=int, default=14)
    parser.add_argument("--n-shell", type=int, default=3)
    parser.add_argument("--n-keep-values", type=int, nargs="+", default=[2, 4, 6])
    parser.add_argument("--delta0", type=float, default=1.0)
    parser.add_argument("--mu", type=float, default=0.0)
    parser.add_argument("--dk", type=float, default=1.0e-6)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "processed" / "band_diagonal_response_baseline.csv",
    )
    return parser.parse_args()


def average(values: list[float]) -> float:
    return float(np.mean(np.asarray(values, dtype=float)))


def evaluate_nkeep(
    model: BMModel,
    nk: int,
    n_keep: int,
    delta0: float,
    mu: float,
    dk: float,
) -> dict[str, object]:
    cache = build_response_cache(model=model, nk=nk, n_keep=n_keep, dk=dk)
    delta_band = delta0 * np.eye(n_keep, dtype=complex)
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

    dxx_total = average(values["Dxx_total"])
    dyy_total = average(values["Dyy_total"])
    dxx_geom = average(values["Dxx_geom"])
    dyy_geom = average(values["Dyy_geom"])
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
        "eta": 0.0,
        "normalization": "band_delta0",
        "m0": "band_identity",
        "m1": "none",
        "partner": "band_diagonal_uniform_s",
        "nk": nk,
        "n_shell": model.params.n_shell,
        "n_keep": n_keep,
        "dimension": model.dimension,
        "delta0_meV": delta0,
        "mu_meV": mu,
        "nu_proxy": filling_proxy_from_energies([item.eps for item in cache], mu),
        "interband_pairing_weight_mean": interband_weight(delta_band),
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
        row[f"{key}_raw"] = average(values[key])
    return row


def main() -> int:
    args = parse_args()
    model = BMModel(BMParameters(n_shell=args.n_shell))
    rows = [
        evaluate_nkeep(
            model=model,
            nk=args.nk,
            n_keep=n_keep,
            delta0=args.delta0,
            mu=args.mu,
            dk=args.dk,
        )
        for n_keep in args.n_keep_values
    ]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"BM dimension: {model.dimension}")
    print(f"Wrote {args.output}")
    print("n_keep D_iso Dconv_iso Dgeom_iso geom_fraction anis closure ph")
    for row in rows:
        dconv = 0.5 * (float(row["Dxx_conv_raw"]) + float(row["Dyy_conv_raw"]))
        dgeom = 0.5 * (float(row["Dxx_geom_raw"]) + float(row["Dyy_geom_raw"]))
        print(
            f"{int(row['n_keep']):6d} "
            f"{float(row['D_iso_raw']):10.3f} "
            f"{dconv:10.3f} "
            f"{dgeom:10.3f} "
            f"{float(row['geom_fraction_total']):8.3f} "
            f"{float(row['anisotropy_ratio']):7.3f} "
            f"{float(row['max_closure_error']):8.1e} "
            f"{float(row['max_ph_spectrum_error']):8.1e}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
