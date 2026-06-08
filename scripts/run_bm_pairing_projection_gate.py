#!/usr/bin/env python3
"""Project the first interband-pairing family using BM eigenvectors."""

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
from matbg.pairing import (  # noqa: E402
    apply_band_gauge,
    gauge_transform_projected_pairing,
    interband_weight,
    orbital_pairing_matrix,
    project_pairing,
    random_band_phases,
    relative_norm,
)
from matbg.sewing import identity_time_reversal_target, procrustes_sew_subspace  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nk", type=int, default=3)
    parser.add_argument("--n-shell", type=int, default=2)
    parser.add_argument("--n-keep", type=int, default=2)
    parser.add_argument("--delta0", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=11)
    parser.add_argument("--m0", default="tau0_sigma0")
    parser.add_argument("--m1", default="taux_sigma0")
    parser.add_argument(
        "--partner",
        choices=[
            "same_valley",
            "time_reversed_valley",
            "tr_sewn",
            "conjugate_k",
            "sewn_time_reversed_valley",
        ],
        default="tr_sewn",
        help="Which normal-state eigenvectors to use for the paired -k sector.",
    )
    parser.add_argument(
        "--etas",
        type=float,
        nargs="+",
        default=[0.0, 0.1, 0.25, 0.5, 0.75, 1.0],
    )
    parser.add_argument(
        "--normalizations",
        nargs="+",
        default=["fixed_frobenius_norm", "fixed_delta0"],
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "processed" / "bm_pairing_projection_gate.csv",
    )
    return parser.parse_args()


def gauge_projection_error(
    delta_band: np.ndarray,
    delta_orb: np.ndarray,
    u_k: np.ndarray,
    u_minus_k: np.ndarray,
    rng: np.random.Generator,
) -> float:
    n_bands = u_k.shape[1]
    gauge_k = random_band_phases(n_bands, rng)
    gauge_minus_k = random_band_phases(n_bands, rng)
    projected = project_pairing(
        apply_band_gauge(u_k, gauge_k),
        delta_orb,
        apply_band_gauge(u_minus_k, gauge_minus_k),
    )
    expected = gauge_transform_projected_pairing(delta_band, gauge_k, gauge_minus_k)
    return relative_norm(projected, expected)


def summarize(values: list[float]) -> tuple[float, float, float, float]:
    array = np.asarray(values, dtype=float)
    return (
        float(np.mean(array)),
        float(np.std(array)),
        float(np.min(array)),
        float(np.max(array)),
    )


def main() -> int:
    args = parse_args()
    rng = np.random.default_rng(args.seed)
    model = BMModel(BMParameters(n_shell=args.n_shell))
    partner_model = None
    if args.partner in ("time_reversed_valley", "sewn_time_reversed_valley"):
        partner_model = BMModel(BMParameters(n_shell=args.n_shell, valley=-1))
    elif args.partner == "same_valley":
        partner_model = model
    k_mesh = model.centered_mesh(args.nk)
    bandwidth = model.central_bandwidth(nk=args.nk, n_keep=args.n_keep)

    rows: list[dict[str, object]] = []
    for normalization in args.normalizations:
        for eta in args.etas:
            weights: list[float] = []
            diagonal_norms: list[float] = []
            total_norms: list[float] = []
            gauge_errors: list[float] = []
            sewing_errors: list[float] = []
            sewing_min_singulars: list[float] = []
            sewing_mean_singulars: list[float] = []

            delta_orb = orbital_pairing_matrix(
                delta0=args.delta0,
                eta=eta,
                n_momenta=model.n_momenta,
                m0=args.m0,
                m1=args.m1,
                normalization=normalization,
            )

            for k_vec in k_mesh:
                _, u_k = model.selected_bands(k_vec, n_keep=args.n_keep)
                if args.partner in ("tr_sewn", "conjugate_k"):
                    u_minus_k = u_k.conj()
                else:
                    _, u_minus_raw = partner_model.selected_bands(
                        -k_vec,
                        n_keep=args.n_keep,
                    )
                    if args.partner == "sewn_time_reversed_valley":
                        sewing = procrustes_sew_subspace(
                            u_minus_raw,
                            identity_time_reversal_target(u_k),
                        )
                        u_minus_k = sewing.aligned_vectors
                        sewing_errors.append(sewing.alignment_error)
                        sewing_min_singulars.append(sewing.min_singular_value)
                        sewing_mean_singulars.append(sewing.mean_singular_value)
                    else:
                        u_minus_k = u_minus_raw
                delta_band = project_pairing(u_k, delta_orb, u_minus_k)
                weights.append(interband_weight(delta_band))
                diagonal_norms.append(float(np.linalg.norm(np.diag(delta_band))))
                total_norms.append(float(np.linalg.norm(delta_band)))
                gauge_errors.append(
                    gauge_projection_error(delta_band, delta_orb, u_k, u_minus_k, rng)
                )

            weight_mean, weight_std, weight_min, weight_max = summarize(weights)
            diag_mean, _, _, _ = summarize(diagonal_norms)
            total_mean, _, _, _ = summarize(total_norms)
            gauge_mean, gauge_std, gauge_min, gauge_max = summarize(gauge_errors)
            if sewing_errors:
                sewing_error_mean, _, sewing_error_min, sewing_error_max = summarize(
                    sewing_errors
                )
                sewing_min_sv_mean, _, sewing_min_sv_min, _ = summarize(
                    sewing_min_singulars
                )
                sewing_mean_sv_mean, _, _, _ = summarize(sewing_mean_singulars)
            else:
                sewing_error_mean = sewing_error_min = sewing_error_max = 0.0
                sewing_min_sv_mean = sewing_min_sv_min = 1.0
                sewing_mean_sv_mean = 1.0
            rows.append(
                {
                    "normalization": normalization,
                    "m0": args.m0,
                    "m1": args.m1,
                    "eta": eta,
                    "nk": args.nk,
                    "n_shell": args.n_shell,
                    "n_keep": args.n_keep,
                    "partner": args.partner,
                    "dimension": model.dimension,
                    "central_bandwidth_meV": bandwidth,
                    "interband_weight_mean": weight_mean,
                    "interband_weight_std": weight_std,
                    "interband_weight_min": weight_min,
                    "interband_weight_max": weight_max,
                    "diag_gap_norm_mean": diag_mean,
                    "total_gap_norm_mean": total_mean,
                    "gauge_projection_error_mean": gauge_mean,
                    "gauge_projection_error_std": gauge_std,
                    "gauge_projection_error_min": gauge_min,
                    "gauge_projection_error_max": gauge_max,
                    "sewing_error_mean": sewing_error_mean,
                    "sewing_error_min": sewing_error_min,
                    "sewing_error_max": sewing_error_max,
                    "sewing_min_singular_mean": sewing_min_sv_mean,
                    "sewing_min_singular_min": sewing_min_sv_min,
                    "sewing_mean_singular_mean": sewing_mean_sv_mean,
                }
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"BM dimension: {model.dimension}")
    print(f"Estimated central-band bandwidth: {bandwidth:.6f} meV")
    print(f"Pairing family: M0={args.m0}, M1={args.m1}")
    print(f"Wrote {args.output}")
    print(
        "normalization eta   W_mean    W_std     W_min     W_max     "
        "gap_norm  gauge_max sew_err  sew_sv_min"
    )
    for row in rows:
        print(
            f"{str(row['normalization']):22s} "
            f"{float(row['eta']):4.2f} "
            f"{float(row['interband_weight_mean']):9.6f} "
            f"{float(row['interband_weight_std']):9.6f} "
            f"{float(row['interband_weight_min']):9.6f} "
            f"{float(row['interband_weight_max']):9.6f} "
            f"{float(row['total_gap_norm_mean']):9.6f} "
            f"{float(row['gauge_projection_error_max']):9.2e} "
            f"{float(row['sewing_error_max']):8.2e} "
            f"{float(row['sewing_min_singular_min']):8.4f}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
