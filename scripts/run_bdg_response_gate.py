#!/usr/bin/env python3
"""Run the first minimal BdG response gate for MATBG stiffness components."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from matbg.bm_model import BMModel, BMParameters  # noqa: E402
from matbg.response_scan import build_response_cache, evaluate_eta_grid  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nk", type=int, default=3)
    parser.add_argument("--n-shell", type=int, default=3)
    parser.add_argument("--n-keep", type=int, default=2)
    parser.add_argument("--delta0", type=float, default=1.0)
    parser.add_argument("--mu", type=float, default=0.0)
    parser.add_argument("--dk", type=float, default=1.0e-6)
    parser.add_argument("--m0", default="tau0_sigma0")
    parser.add_argument("--m1", default="taux_sigmax")
    parser.add_argument(
        "--etas",
        type=float,
        nargs="+",
        default=[0.0, 0.25, 0.5, 0.75, 1.0],
    )
    parser.add_argument(
        "--normalization",
        default="fixed_frobenius_norm",
        choices=["fixed_frobenius_norm", "fixed_delta0"],
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "processed" / "bdg_response_gate.csv",
    )
    return parser.parse_args()

def main() -> int:
    args = parse_args()
    model = BMModel(BMParameters(n_shell=args.n_shell))
    cache = build_response_cache(
        model=model,
        nk=args.nk,
        n_keep=args.n_keep,
        dk=args.dk,
    )
    rows = evaluate_eta_grid(
        cache=cache,
        n_momenta=model.n_momenta,
        dimension=model.dimension,
        etas=args.etas,
        normalizations=[args.normalization],
        m0=args.m0,
        m1=args.m1,
        delta0=args.delta0,
        mu=args.mu,
        nk=args.nk,
        n_shell=args.n_shell,
        n_keep=args.n_keep,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"BM dimension: {model.dimension}")
    print(f"Wrote {args.output}")
    print(
        "eta W_pair Dxx_total Dxx_conv Dxx_geom Dxx_cross "
        "Dyy_total anis closure ph"
    )
    for row in rows:
        print(
            f"{float(row['eta']):4.2f} "
            f"{float(row['interband_pairing_weight_mean']):7.4f} "
            f"{float(row['Dxx_total_raw']):10.3f} "
            f"{float(row['Dxx_conv_raw']):10.3f} "
            f"{float(row['Dxx_geom_raw']):10.3f} "
            f"{float(row['Dxx_cross_raw']):10.3f} "
            f"{float(row['Dyy_total_raw']):10.3f} "
            f"{float(row['anisotropy_ratio']):7.3f} "
            f"{float(row['max_closure_error']):8.1e} "
            f"{float(row['max_ph_spectrum_error']):8.1e}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
