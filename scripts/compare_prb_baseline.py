#!/usr/bin/env python3
"""Compare current response baselines against PRB manuscript benchmarks."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from matbg.units import raw_mev_a2_to_ev_a2  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("response", type=Path)
    parser.add_argument(
        "--benchmark",
        type=Path,
        default=ROOT / "data" / "processed" / "baseline_benchmarks.csv",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--normalization", default="fixed_frobenius_norm")
    parser.add_argument("--eta", type=float, default=0.0)
    parser.add_argument("--mu", type=float, default=0.0)
    parser.add_argument("--delta0", type=float, default=1.0)
    parser.add_argument("--benchmark-pairing", default="uniform_s")
    return parser.parse_args()


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(row: dict[str, str], key: str) -> float:
    return float(row[key])


def close(value: float, target: float) -> bool:
    return abs(value - target) < 1.0e-12


def d_iso(row: dict[str, str]) -> float:
    if "D_iso_raw" in row and row["D_iso_raw"]:
        return as_float(row, "D_iso_raw")
    return 0.5 * (as_float(row, "Dxx_total_raw") + as_float(row, "Dyy_total_raw"))


def component_iso(row: dict[str, str], component: str) -> float:
    return 0.5 * (
        as_float(row, f"Dxx_{component}_raw") + as_float(row, f"Dyy_{component}_raw")
    )


def select_response_rows(
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> list[dict[str, str]]:
    selected = []
    for row in rows:
        if row["normalization"] != args.normalization:
            continue
        if not close(as_float(row, "eta"), args.eta):
            continue
        if not close(as_float(row, "mu_meV"), args.mu):
            continue
        if not close(as_float(row, "delta0_meV"), args.delta0):
            continue
        selected.append(row)
    return selected


def benchmark_by_nkeep(
    rows: list[dict[str, str]],
    args: argparse.Namespace,
) -> dict[int, dict[str, str]]:
    benchmarks = {}
    for row in rows:
        if row["pairing"] != args.benchmark_pairing:
            continue
        if not close(as_float(row, "mu_meV"), args.mu):
            continue
        if not close(as_float(row, "delta0_meV"), args.delta0):
            continue
        benchmarks[int(float(row["n_keep"]))] = row
    return benchmarks


def relative_delta(current: float, reference: float) -> float:
    return current / reference - 1.0


def interpretation_note(response: dict[str, str]) -> str:
    if response.get("partner") == "band_diagonal_uniform_s":
        return (
            "Current row uses an explicit band-diagonal uniform-s gap in the "
            "retained band subspace."
        )
    return (
        "Current eta=0 is the orbital-projected tr_sewn baseline, not necessarily "
        "the PRB band-diagonal uniform-s ansatz."
    )


def comparison_row(
    response: dict[str, str],
    benchmark: dict[str, str],
    args: argparse.Namespace,
) -> dict[str, object]:
    current_total = raw_mev_a2_to_ev_a2(d_iso(response))
    current_conv = raw_mev_a2_to_ev_a2(component_iso(response, "conv"))
    current_geom = raw_mev_a2_to_ev_a2(component_iso(response, "geom"))
    current_cross = raw_mev_a2_to_ev_a2(component_iso(response, "cross"))
    reference_total = as_float(benchmark, "D_total_eV_A2")
    reference_conv = as_float(benchmark, "D_conv_eV_A2")
    reference_geom = as_float(benchmark, "D_geom_eV_A2")
    return {
        "response_file": str(args.response),
        "benchmark_source": benchmark["source"],
        "current_pairing": f"{response['m0']}+eta*{response['m1']}",
        "benchmark_pairing": benchmark["pairing"],
        "normalization": response["normalization"],
        "eta": response["eta"],
        "mu_meV": response["mu_meV"],
        "delta0_meV": response["delta0_meV"],
        "n_keep": response["n_keep"],
        "current_nk": response["nk"],
        "benchmark_nk": benchmark["nk"],
        "D_total_current_eV_A2": current_total,
        "D_total_benchmark_eV_A2": reference_total,
        "D_total_relative_delta": relative_delta(current_total, reference_total),
        "D_conv_current_eV_A2": current_conv,
        "D_conv_benchmark_eV_A2": reference_conv,
        "D_conv_relative_delta": relative_delta(current_conv, reference_conv),
        "D_geom_current_eV_A2": current_geom,
        "D_geom_benchmark_eV_A2": reference_geom,
        "D_geom_relative_delta": relative_delta(current_geom, reference_geom),
        "D_cross_current_eV_A2": current_cross,
        "geom_fraction_current": current_geom / current_total,
        "geom_fraction_benchmark": as_float(benchmark, "geom_fraction_percent") / 100.0,
        "units_note": "current raw/1000 gives eV A^2 per flavor; benchmark is per valley per spin",
        "interpretation_note": interpretation_note(response),
    }


def main() -> int:
    args = parse_args()
    responses = select_response_rows(load_rows(args.response), args)
    benchmarks = benchmark_by_nkeep(load_rows(args.benchmark), args)

    fieldnames = [
        "response_file",
        "benchmark_source",
        "current_pairing",
        "benchmark_pairing",
        "normalization",
        "eta",
        "mu_meV",
        "delta0_meV",
        "n_keep",
        "current_nk",
        "benchmark_nk",
        "D_total_current_eV_A2",
        "D_total_benchmark_eV_A2",
        "D_total_relative_delta",
        "D_conv_current_eV_A2",
        "D_conv_benchmark_eV_A2",
        "D_conv_relative_delta",
        "D_geom_current_eV_A2",
        "D_geom_benchmark_eV_A2",
        "D_geom_relative_delta",
        "D_cross_current_eV_A2",
        "geom_fraction_current",
        "geom_fraction_benchmark",
        "units_note",
        "interpretation_note",
    ]
    output_rows = [
        comparison_row(row, benchmarks[int(float(row["n_keep"]))], args)
        for row in responses
        if int(float(row["n_keep"])) in benchmarks
    ]
    if not output_rows:
        raise SystemExit("No matching response/benchmark rows found")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Wrote {args.output}")
    for row in output_rows:
        print(
            f"n_keep={row['n_keep']} total delta="
            f"{100.0 * float(row['D_total_relative_delta']):+.2f}% "
            f"geom fraction current={100.0 * float(row['geom_fraction_current']):.1f}% "
            f"benchmark={100.0 * float(row['geom_fraction_benchmark']):.1f}%"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
