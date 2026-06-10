#!/usr/bin/env python3
"""Run grid/truncation/shell robustness scans for the PRB major revision."""

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
    parser.add_argument("--nks", type=int, nargs="+", default=[9, 11, 13, 15])
    parser.add_argument("--n-keeps", type=int, nargs="+", default=[4, 6, 8])
    parser.add_argument("--n-shells", type=int, nargs="+", default=[2, 3, 4])
    parser.add_argument("--mus", type=float, nargs="+", default=[-4.0, -2.0, 0.0, 2.0, 4.0])
    parser.add_argument("--etas", type=float, nargs="+", default=[0.0, 0.5, 1.0])
    parser.add_argument(
        "--normalizations",
        nargs="+",
        default=["fixed_frobenius_norm", "fixed_delta0"],
    )
    parser.add_argument("--m0", default="tau0_sigma0")
    parser.add_argument("--m1", default="taux_sigmax")
    parser.add_argument("--delta0", type=float, default=1.0)
    parser.add_argument("--dk", type=float, default=1.0e-6)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "processed" / "prb_major_revision_robustness_matrix.csv",
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=ROOT / "data" / "processed" / "prb_major_revision_robustness_summary.csv",
    )
    return parser.parse_args()


def as_float(row: dict[str, object], key: str) -> float:
    return float(row[key])


def summarize_rows(
    rows: list[dict[str, object]],
    eta_baseline: float,
    eta_target: float,
) -> list[dict[str, object]]:
    baseline: dict[tuple[int, int, int, str, float], dict[str, object]] = {}
    target: dict[tuple[int, int, int, str, float], dict[str, object]] = {}
    for row in rows:
        key = (
            int(row["nk"]),
            int(row["n_keep"]),
            int(row["n_shell"]),
            str(row["normalization"]),
            as_float(row, "mu_meV"),
        )
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
        rel = target_d / base_d - 1.0 if base_d != 0.0 else float("nan")
        summary.append(
            {
                "nk": key[0],
                "n_keep": key[1],
                "n_shell": key[2],
                "m0": base["m0"],
                "m1": base["m1"],
                "normalization": key[3],
                "mu_meV": key[4],
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
    rows: list[dict[str, object]] = []
    total_configs = len(args.n_shells) * len(args.n_keeps) * len(args.nks)
    config_index = 0

    for n_shell in args.n_shells:
        model = BMModel(BMParameters(n_shell=n_shell))
        for n_keep in args.n_keeps:
            for nk in args.nks:
                config_index += 1
                print(
                    f"[{config_index}/{total_configs}] "
                    f"n_shell={n_shell} n_keep={n_keep} nk={nk}",
                    flush=True,
                )
                cache = build_response_cache(
                    model=model,
                    nk=nk,
                    n_keep=n_keep,
                    dk=args.dk,
                )
                for mu in args.mus:
                    rows.extend(
                        evaluate_eta_grid(
                            cache=cache,
                            n_momenta=model.n_momenta,
                            dimension=model.dimension,
                            etas=args.etas,
                            normalizations=args.normalizations,
                            m0=args.m0,
                            m1=args.m1,
                            delta0=args.delta0,
                            mu=mu,
                            nk=nk,
                            n_shell=n_shell,
                            n_keep=n_keep,
                        )
                    )

    summary = summarize_rows(rows, eta_baseline=args.etas[0], eta_target=args.etas[-1])
    write_csv(args.output, rows)
    write_csv(args.summary_output, summary)

    frob_rows = [row for row in summary if row["normalization"] == "fixed_frobenius_norm"]
    delta_rows = [row for row in summary if row["normalization"] == "fixed_delta0"]
    print(f"Wrote {args.output}")
    print(f"Wrote {args.summary_output}")
    print(f"Raw rows: {len(rows)}")
    print(f"Summary rows: {len(summary)}")
    print(
        "fixed_frobenius positive rows: "
        f"{sum(float(row['D_iso_rel_target_vs_baseline']) > 0.0 for row in frob_rows)}/{len(frob_rows)}"
    )
    print(
        "fixed_delta0 positive rows: "
        f"{sum(float(row['D_iso_rel_target_vs_baseline']) > 0.0 for row in delta_rows)}/{len(delta_rows)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
