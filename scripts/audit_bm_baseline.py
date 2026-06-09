#!/usr/bin/env python3
"""Audit BM bandwidth and optional band-diagonal response baselines."""

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
from matbg.response_scan import build_response_cache  # noqa: E402
from matbg.stiffness import stiffness_components  # noqa: E402
from matbg.units import raw_mev_a2_to_ev_a2  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--theta-values", type=float, nargs="+", default=[1.05])
    parser.add_argument("--n-shell-values", type=int, nargs="+", default=[3])
    parser.add_argument("--nk-bandwidth", type=int, default=21)
    parser.add_argument("--nk-response", type=int, default=0)
    parser.add_argument("--n-keep-response", type=int, default=2)
    parser.add_argument("--delta0", type=float, default=1.0)
    parser.add_argument("--mu", type=float, default=0.0)
    parser.add_argument("--dk", type=float, default=1.0e-6)
    parser.add_argument("--vF-eV-A", type=float, default=2.135)
    parser.add_argument("--w0-meV", type=float, default=87.2)
    parser.add_argument("--w1-meV", type=float, default=109.0)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "processed" / "bm_baseline_audit.csv",
    )
    return parser.parse_args()


def average(values: list[float]) -> float:
    return float(np.mean(np.asarray(values, dtype=float)))


def band_diagonal_response(
    model: BMModel,
    nk: int,
    n_keep: int,
    delta0: float,
    mu: float,
    dk: float,
) -> dict[str, float]:
    cache = build_response_cache(model=model, nk=nk, n_keep=n_keep, dk=dk)
    delta_band = delta0 * np.eye(n_keep, dtype=complex)
    values: dict[str, list[float]] = {
        "Dxx_total": [],
        "Dxx_conv": [],
        "Dxx_geom": [],
        "Dyy_total": [],
        "Dyy_conv": [],
        "Dyy_geom": [],
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

    d_iso = 0.5 * (average(values["Dxx_total"]) + average(values["Dyy_total"]))
    dconv_iso = 0.5 * (average(values["Dxx_conv"]) + average(values["Dyy_conv"]))
    dgeom_iso = 0.5 * (average(values["Dxx_geom"]) + average(values["Dyy_geom"]))
    return {
        "D_iso_eV_A2": raw_mev_a2_to_ev_a2(d_iso),
        "Dconv_iso_eV_A2": raw_mev_a2_to_ev_a2(dconv_iso),
        "Dgeom_iso_eV_A2": raw_mev_a2_to_ev_a2(dgeom_iso),
        "geom_fraction": dgeom_iso / d_iso if d_iso != 0 else np.nan,
    }


def main() -> int:
    args = parse_args()
    rows: list[dict[str, object]] = []
    for n_shell in args.n_shell_values:
        for theta in args.theta_values:
            model = BMModel(
                BMParameters(
                    theta_deg=theta,
                    vF_eV_A=args.vF_eV_A,
                    w0_meV=args.w0_meV,
                    w1_meV=args.w1_meV,
                    n_shell=n_shell,
                )
            )
            row: dict[str, object] = {
                "theta_deg": theta,
                "n_shell": n_shell,
                "dimension": model.dimension,
                "nk_bandwidth": args.nk_bandwidth,
                "bandwidth_nkeep2_meV": model.central_bandwidth(
                    nk=args.nk_bandwidth,
                    n_keep=2,
                ),
                "bandwidth_nkeep6_meV": model.central_bandwidth(
                    nk=args.nk_bandwidth,
                    n_keep=6,
                ),
            }
            if args.nk_response > 0:
                response = band_diagonal_response(
                    model=model,
                    nk=args.nk_response,
                    n_keep=args.n_keep_response,
                    delta0=args.delta0,
                    mu=args.mu,
                    dk=args.dk,
                )
                row.update(
                    {
                        "nk_response": args.nk_response,
                        "n_keep_response": args.n_keep_response,
                        **response,
                    }
                )
            rows.append(row)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {args.output}")
    for row in rows:
        msg = (
            f"theta={float(row['theta_deg']):.4f} "
            f"n_shell={row['n_shell']} "
            f"W2={float(row['bandwidth_nkeep2_meV']):.3f} meV"
        )
        if "D_iso_eV_A2" in row:
            msg += f" D_iso={float(row['D_iso_eV_A2']):.2f} eV A^2"
        print(msg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
