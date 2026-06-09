#!/usr/bin/env python3
"""Build a retained-proxy to central-flat-band filling crosswalk."""

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
from matbg.filling import (  # noqa: E402
    filling_proxy_from_energies,
    selected_band_filling_from_energies,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nk", type=int, default=7)
    parser.add_argument("--n-shell", type=int, default=3)
    parser.add_argument("--n-keep-proxy", type=int, default=6)
    parser.add_argument("--n-flat-bands", type=int, default=2)
    parser.add_argument("--degeneracy", type=float, default=4.0)
    parser.add_argument(
        "--mus",
        type=float,
        nargs="+",
        default=[-5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "processed" / "filling_crosswalk_nk7_nshell3.csv",
    )
    return parser.parse_args()


def average_occupied_count(energies_by_k: list[np.ndarray], mu: float) -> float:
    return float(np.mean([np.count_nonzero(energies < mu) for energies in energies_by_k]))


def average_occupation_fraction(energies_by_k: list[np.ndarray], mu: float) -> float:
    return float(np.mean([np.mean(energies < mu) for energies in energies_by_k]))


def main() -> int:
    args = parse_args()
    model = BMModel(BMParameters(n_shell=args.n_shell))
    mesh = model.centered_mesh(args.nk)

    retained_energies: list[np.ndarray] = []
    flat_energies: list[np.ndarray] = []
    for k_vec in mesh:
        eps_retained, _ = model.selected_bands(k_vec, n_keep=args.n_keep_proxy)
        eps_flat, _ = model.selected_bands(k_vec, n_keep=args.n_flat_bands)
        retained_energies.append(eps_retained)
        flat_energies.append(eps_flat)

    flat_min = min(float(np.min(energies)) for energies in flat_energies)
    flat_max = max(float(np.max(energies)) for energies in flat_energies)

    rows: list[dict[str, object]] = []
    for mu in args.mus:
        rows.append(
            {
                "mu_meV": mu,
                "nk": args.nk,
                "n_shell": args.n_shell,
                "n_keep_proxy": args.n_keep_proxy,
                "n_flat_bands": args.n_flat_bands,
                "spin_valley_degeneracy": args.degeneracy,
                "nu_proxy": filling_proxy_from_energies(
                    retained_energies,
                    mu,
                    spin_valley_degeneracy=args.degeneracy,
                ),
                "nu_flat": selected_band_filling_from_energies(
                    flat_energies,
                    mu,
                    spin_valley_degeneracy=args.degeneracy,
                ),
                "flat_occupied_bands_per_flavor": average_occupied_count(
                    flat_energies,
                    mu,
                ),
                "flat_occupation_fraction": average_occupation_fraction(
                    flat_energies,
                    mu,
                ),
                "flat_band_min_meV": flat_min,
                "flat_band_max_meV": flat_max,
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0].keys()),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"BM dimension: {model.dimension}")
    print(f"Cached k points: {len(mesh)}")
    print(f"Central flat-band window: [{flat_min:.6f}, {flat_max:.6f}] meV")
    print(f"Wrote {args.output}")
    print("mu nu_proxy nu_flat flat_occ_per_flavor")
    for row in rows:
        print(
            f"{float(row['mu_meV']):6.2f} "
            f"{float(row['nu_proxy']):9.4f} "
            f"{float(row['nu_flat']):8.4f} "
            f"{float(row['flat_occupied_bands_per_flavor']):10.4f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
