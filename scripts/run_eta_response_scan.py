#!/usr/bin/env python3
"""Run a cached dense eta scan for the finite-band BdG response."""

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
    parser.add_argument("--nk", type=int, default=7)
    parser.add_argument("--n-shell", type=int, default=3)
    parser.add_argument("--n-keep", type=int, default=6)
    parser.add_argument("--delta0", type=float, default=1.0)
    parser.add_argument("--mu", type=float, default=0.0)
    parser.add_argument("--dk", type=float, default=1.0e-6)
    parser.add_argument("--m0", default="tau0_sigma0")
    parser.add_argument("--m1", default="taux_sigmax")
    parser.add_argument(
        "--etas",
        type=float,
        nargs="+",
        default=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    )
    parser.add_argument(
        "--normalizations",
        nargs="+",
        default=["fixed_frobenius_norm", "fixed_delta0"],
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "processed" / "eta_response_scan.csv",
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
        normalizations=args.normalizations,
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
    print(f"Cached k points: {len(cache)}")
    print(f"Wrote {args.output}")
    print("norm eta W_pair Dxx_total Dyy_total anis Dxx_geom Dyy_geom ph")
    for row in rows:
        print(
            f"{str(row['normalization']):22s} "
            f"{float(row['eta']):4.2f} "
            f"{float(row['interband_pairing_weight_mean']):7.4f} "
            f"{float(row['Dxx_total_raw']):10.3f} "
            f"{float(row['Dyy_total_raw']):10.3f} "
            f"{float(row['anisotropy_ratio']):7.3f} "
            f"{float(row['Dxx_geom_raw']):10.3f} "
            f"{float(row['Dyy_geom_raw']):10.3f} "
            f"{float(row['max_ph_spectrum_error']):8.1e}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
