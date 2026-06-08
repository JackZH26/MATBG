#!/usr/bin/env python3
"""Run algebraic Gate 1 checks for projected interband pairing.

This script does not use the BM Hamiltonian yet.  It tests the linear-algebra
contract required by the production code:

1. define pairing in orbital basis;
2. project to band basis;
3. verify pairing symmetry between k and -k;
4. verify BdG Hermiticity and paired-spectrum particle-hole consistency;
5. verify gauge covariance under random band rephasing.
"""

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

from matbg.pairing import (  # noqa: E402
    GateCheckResult,
    apply_band_gauge,
    bdg_hamiltonian,
    gauge_transform_projected_pairing,
    hermiticity_error,
    interband_weight,
    orbital_pairing_matrix,
    paired_spectrum_error,
    pairing_symmetry_error,
    project_pairing,
    random_band_phases,
    relative_norm,
)


def random_orthonormal_columns(
    n_orbitals: int,
    n_bands: int,
    rng: np.random.Generator,
) -> np.ndarray:
    real = rng.normal(size=(n_orbitals, n_bands))
    imag = rng.normal(size=(n_orbitals, n_bands))
    q, _ = np.linalg.qr(real + 1j * imag)
    return q[:, :n_bands]


def run_one(
    eta: float,
    normalization: str,
    n_momenta: int,
    delta0: float,
    u_k: np.ndarray,
    u_minus_k: np.ndarray,
    gauge_k: np.ndarray,
    gauge_minus_k: np.ndarray,
) -> GateCheckResult:
    n_bands = u_k.shape[1]
    delta_orb = orbital_pairing_matrix(
        delta0=delta0,
        eta=eta,
        n_momenta=n_momenta,
        m0="tau0_sigma0",
        m1="taux_sigma0",
        normalization=normalization,
    )

    delta_k = project_pairing(u_k, delta_orb, u_minus_k)
    delta_minus_k = project_pairing(u_minus_k, delta_orb.T, u_k)

    eps_k = np.linspace(-2.0, 2.0, n_bands)
    eps_minus_k = np.linspace(-2.0, 2.0, n_bands)
    h_k = bdg_hamiltonian(eps_k, eps_minus_k, delta_k, mu=0.0)
    h_minus_k = bdg_hamiltonian(eps_minus_k, eps_k, delta_minus_k, mu=0.0)

    u_k_gauged = apply_band_gauge(u_k, gauge_k)
    u_minus_k_gauged = apply_band_gauge(u_minus_k, gauge_minus_k)
    delta_k_gauged = project_pairing(u_k_gauged, delta_orb, u_minus_k_gauged)
    delta_k_expected = gauge_transform_projected_pairing(
        delta_k,
        gauge_k,
        gauge_minus_k,
    )

    h_k_gauged = bdg_hamiltonian(eps_k, eps_minus_k, delta_k_gauged, mu=0.0)
    spectrum_error = relative_norm(
        np.sort(np.linalg.eigvalsh(h_k)),
        np.sort(np.linalg.eigvalsh(h_k_gauged)),
    )

    return GateCheckResult(
        eta=eta,
        normalization=normalization,
        interband_weight=interband_weight(delta_k),
        pairing_symmetry_error=pairing_symmetry_error(delta_k, delta_minus_k),
        hermiticity_error_k=hermiticity_error(h_k),
        hermiticity_error_minus_k=hermiticity_error(h_minus_k),
        particle_hole_error=paired_spectrum_error(h_k, h_minus_k),
        gauge_projection_error=relative_norm(delta_k_gauged, delta_k_expected),
        gauge_spectrum_error=spectrum_error,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--n-momenta", type=int, default=3)
    parser.add_argument("--n-bands", type=int, default=4)
    parser.add_argument("--delta0", type=float, default=1.0)
    parser.add_argument(
        "--independent-minus-k",
        action="store_true",
        help=(
            "Use an independent random U(-k). By default the script uses "
            "U(-k)=U(k)^*, so eta=0 is a clean band-diagonal toy baseline."
        ),
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
        default=ROOT / "data" / "processed" / "pairing_gate_results.csv",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rng = np.random.default_rng(args.seed)
    n_orbitals = 4 * args.n_momenta
    u_k = random_orthonormal_columns(n_orbitals, args.n_bands, rng)
    if args.independent_minus_k:
        u_minus_k = random_orthonormal_columns(n_orbitals, args.n_bands, rng)
    else:
        u_minus_k = u_k.conj()
    gauge_k = random_band_phases(args.n_bands, rng)
    gauge_minus_k = random_band_phases(args.n_bands, rng)

    results: list[GateCheckResult] = []
    for normalization in args.normalizations:
        for eta in args.etas:
            results.append(
                run_one(
                    eta=eta,
                    normalization=normalization,
                    n_momenta=args.n_momenta,
                    delta0=args.delta0,
                    u_k=u_k,
                    u_minus_k=u_minus_k,
                    gauge_k=gauge_k,
                    gauge_minus_k=gauge_minus_k,
                )
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[0].__dict__.keys()))
        writer.writeheader()
        for result in results:
            writer.writerow(result.__dict__)

    print(f"Wrote {args.output}")
    print(
        "normalization eta   W_inter    pair_sym    herm_k      herm_-k     "
        "ph_pair     gauge_proj gauge_spec  pass"
    )
    all_passed = True
    for result in results:
        passed = result.passed()
        all_passed = all_passed and passed
        print(
            f"{result.normalization:22s} "
            f"{result.eta:4.2f} "
            f"{result.interband_weight:10.6f} "
            f"{result.pairing_symmetry_error:10.2e} "
            f"{result.hermiticity_error_k:10.2e} "
            f"{result.hermiticity_error_minus_k:10.2e} "
            f"{result.particle_hole_error:10.2e} "
            f"{result.gauge_projection_error:10.2e} "
            f"{result.gauge_spectrum_error:10.2e} "
            f"{'yes' if passed else 'no'}"
        )

    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
