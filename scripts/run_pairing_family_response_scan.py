#!/usr/bin/env python3
"""Scan normalized response signatures across an orbital pairing family."""

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
from matbg.pairing import internal_pairing_matrix  # noqa: E402
from matbg.response_scan import build_response_cache, evaluate_eta_grid  # noqa: E402


DEFAULT_M1S = [
    "taux_sigmax",
    "taux_sigma0",
    "tau0_sigmaz",
    "tauz_sigmaz",
    "tau0_sigmax",
    "taux_sigmaz",
    "tauz_sigma0",
    "tauz_sigmax",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nk", type=int, default=7)
    parser.add_argument("--n-shell", type=int, default=3)
    parser.add_argument("--n-keep", type=int, default=6)
    parser.add_argument("--delta0", type=float, default=1.0)
    parser.add_argument("--dk", type=float, default=1.0e-6)
    parser.add_argument("--m0", default="tau0_sigma0")
    parser.add_argument("--m1s", nargs="+", default=DEFAULT_M1S)
    parser.add_argument("--mus", type=float, nargs="+", default=[-4.0, 0.0, 2.0, 4.0])
    parser.add_argument("--etas", type=float, nargs="+", default=[0.0, 1.0])
    parser.add_argument(
        "--normalizations",
        nargs="+",
        default=["fixed_frobenius_norm", "fixed_delta0"],
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "processed" / "pairing_family_response_scan.csv",
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=ROOT / "data" / "processed" / "pairing_family_response_summary.csv",
    )
    return parser.parse_args()


def matrix_flags(name: str) -> dict[str, object]:
    matrix = internal_pairing_matrix(name)
    return {
        "matrix_hermitian": bool(np.allclose(matrix, matrix.conj().T)),
        "matrix_symmetric": bool(np.allclose(matrix, matrix.T)),
        "matrix_real": bool(np.allclose(matrix.imag, 0.0)),
        "matrix_trace_real": float(np.trace(matrix).real),
        "matrix_frobenius_norm": float(np.linalg.norm(matrix)),
    }


def as_float(row: dict[str, object], key: str) -> float:
    return float(row[key])


def summarize_rows(
    rows: list[dict[str, object]],
    eta_baseline: float,
    eta_target: float,
) -> list[dict[str, object]]:
    baseline: dict[tuple[str, str, float], dict[str, object]] = {}
    target: dict[tuple[str, str, float], dict[str, object]] = {}
    for row in rows:
        key = (str(row["m1"]), str(row["normalization"]), as_float(row, "mu_meV"))
        eta = as_float(row, "eta")
        if abs(eta - eta_baseline) < 1.0e-12:
            baseline[key] = row
        if abs(eta - eta_target) < 1.0e-12:
            target[key] = row

    summary: list[dict[str, object]] = []
    for key in sorted(set(baseline).intersection(target)):
        base = baseline[key]
        targ = target[key]
        base_d = as_float(base, "D_iso_raw")
        target_d = as_float(targ, "D_iso_raw")
        rel = target_d / base_d - 1.0 if base_d != 0 else float("nan")
        summary.append(
            {
                "m1": key[0],
                "normalization": key[1],
                "mu_meV": key[2],
                "eta_baseline": eta_baseline,
                "eta_target": eta_target,
                "D_iso_baseline": base_d,
                "D_iso_target": target_d,
                "D_iso_rel_target_vs_baseline": rel,
                "D_iso_rel_percent": 100.0 * rel,
                "W_inter_baseline": as_float(base, "interband_pairing_weight_mean"),
                "W_inter_target": as_float(targ, "interband_pairing_weight_mean"),
                "geom_fraction_baseline": as_float(base, "geom_fraction_total"),
                "geom_fraction_target": as_float(targ, "geom_fraction_total"),
                "anisotropy_norm_baseline": as_float(base, "anisotropy_norm"),
                "anisotropy_norm_target": as_float(targ, "anisotropy_norm"),
                "max_closure_error": max(
                    as_float(base, "max_closure_error"),
                    as_float(targ, "max_closure_error"),
                ),
                "max_bdg_hermiticity_error": max(
                    as_float(base, "max_bdg_hermiticity_error"),
                    as_float(targ, "max_bdg_hermiticity_error"),
                ),
                "max_ph_spectrum_error": max(
                    as_float(base, "max_ph_spectrum_error"),
                    as_float(targ, "max_ph_spectrum_error"),
                ),
            }
        )
    return summary


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0].keys()),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    model = BMModel(BMParameters(n_shell=args.n_shell))
    cache = build_response_cache(
        model=model,
        nk=args.nk,
        n_keep=args.n_keep,
        dk=args.dk,
    )

    flags_by_m1 = {m1: matrix_flags(m1) for m1 in args.m1s}
    rows: list[dict[str, object]] = []
    for m1 in args.m1s:
        for mu in args.mus:
            for row in evaluate_eta_grid(
                cache=cache,
                n_momenta=model.n_momenta,
                dimension=model.dimension,
                etas=args.etas,
                normalizations=args.normalizations,
                m0=args.m0,
                m1=m1,
                delta0=args.delta0,
                mu=mu,
                nk=args.nk,
                n_shell=args.n_shell,
                n_keep=args.n_keep,
            ):
                row.update(flags_by_m1[m1])
                rows.append(row)

    summary = summarize_rows(rows, eta_baseline=args.etas[0], eta_target=args.etas[-1])
    write_csv(args.output, rows)
    write_csv(args.summary_output, summary)

    frob_rows = [
        row
        for row in summary
        if row["normalization"] == "fixed_frobenius_norm"
    ]
    fixed_delta0_rows = [
        row
        for row in summary
        if row["normalization"] == "fixed_delta0"
    ]
    positive_frob = {
        str(row["m1"])
        for row in frob_rows
        if float(row["D_iso_rel_target_vs_baseline"]) > 0.0
    }
    print(f"BM dimension: {model.dimension}")
    print(f"Cached k points: {len(cache)}")
    print(f"Scanned pairing directions: {len(args.m1s)}")
    print(f"Wrote {args.output}")
    print(f"Wrote {args.summary_output}")
    print(
        "fixed_frobenius positive rows: "
        f"{sum(float(row['D_iso_rel_target_vs_baseline']) > 0.0 for row in frob_rows)}/{len(frob_rows)}"
    )
    print(
        "fixed_delta0 positive rows: "
        f"{sum(float(row['D_iso_rel_target_vs_baseline']) > 0.0 for row in fixed_delta0_rows)}/{len(fixed_delta0_rows)}"
    )
    print("directions with at least one positive fixed_frobenius row:")
    print(", ".join(sorted(positive_frob)) if positive_frob else "none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
