#!/usr/bin/env python3
"""Scan response sensitivity to valley-partner and sewing conventions."""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from matbg.bm_model import BMModel, BMParameters  # noqa: E402
from matbg.filling import filling_proxy_from_energies  # noqa: E402
from matbg.pairing import (  # noqa: E402
    interband_weight,
    orbital_pairing_matrix,
    project_pairing,
    relative_norm,
)
from matbg.response_scan import KPointResponseData, build_response_cache  # noqa: E402
from matbg.sewing import identity_time_reversal_target, procrustes_sew_subspace  # noqa: E402
from matbg.stiffness import stiffness_components  # noqa: E402


DEFAULT_PARTNERS = [
    "tr_sewn",
    "same_valley",
    "time_reversed_valley",
    "sewn_time_reversed_valley",
]


@dataclass(frozen=True)
class PartnerKPointData:
    vectors: np.ndarray
    raw_alignment_error: float
    best_alignment_error: float
    min_singular_value: float
    mean_singular_value: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nks", type=int, nargs="+", default=[9, 13, 15])
    parser.add_argument("--n-shells", type=int, nargs="+", default=[3, 4])
    parser.add_argument("--n-keep", type=int, default=6)
    parser.add_argument("--mus", type=float, nargs="+", default=[-4.0, 0.0, 2.0, 4.0])
    parser.add_argument("--etas", type=float, nargs="+", default=[0.0, 1.0])
    parser.add_argument(
        "--normalizations",
        nargs="+",
        default=["fixed_frobenius_norm", "fixed_delta0"],
    )
    parser.add_argument("--partners", nargs="+", default=DEFAULT_PARTNERS)
    parser.add_argument("--m0", default="tau0_sigma0")
    parser.add_argument("--m1", default="taux_sigmax")
    parser.add_argument("--delta0", type=float, default=1.0)
    parser.add_argument("--dk", type=float, default=1.0e-6)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "processed" / "valley_sewing_response_sensitivity.csv",
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=ROOT / "data" / "processed" / "valley_sewing_response_sensitivity_summary.csv",
    )
    return parser.parse_args()


def average(values: list[float]) -> float:
    return float(np.mean(np.asarray(values, dtype=float)))


def partner_vectors_for_k(
    partner: str,
    model: BMModel,
    minus_model: BMModel,
    k_vec: np.ndarray,
    u_k: np.ndarray,
    n_keep: int,
) -> PartnerKPointData:
    target = identity_time_reversal_target(u_k)
    if partner in ("tr_sewn", "conjugate_k"):
        return PartnerKPointData(
            vectors=target,
            raw_alignment_error=0.0,
            best_alignment_error=0.0,
            min_singular_value=1.0,
            mean_singular_value=1.0,
        )
    if partner == "same_valley":
        _, raw = model.selected_bands(-k_vec, n_keep=n_keep)
    elif partner in ("time_reversed_valley", "sewn_time_reversed_valley"):
        _, raw = minus_model.selected_bands(-k_vec, n_keep=n_keep)
    else:
        raise ValueError(f"Unsupported partner convention: {partner}")

    raw_alignment_error = relative_norm(raw, target)
    sewing = procrustes_sew_subspace(raw, target)
    if partner == "sewn_time_reversed_valley":
        vectors = sewing.aligned_vectors
        best_alignment_error = sewing.alignment_error
    else:
        vectors = raw
        best_alignment_error = sewing.alignment_error

    return PartnerKPointData(
        vectors=vectors,
        raw_alignment_error=raw_alignment_error,
        best_alignment_error=best_alignment_error,
        min_singular_value=sewing.min_singular_value,
        mean_singular_value=sewing.mean_singular_value,
    )


def build_partner_cache(
    model: BMModel,
    minus_model: BMModel,
    cache: list[KPointResponseData],
    partners: list[str],
    n_keep: int,
) -> dict[str, list[PartnerKPointData]]:
    return {
        partner: [
            partner_vectors_for_k(
                partner=partner,
                model=model,
                minus_model=minus_model,
                k_vec=item.k_vec,
                u_k=item.vectors,
                n_keep=n_keep,
            )
            for item in cache
        ]
        for partner in partners
    }


def evaluate_partner_row(
    cache: list[KPointResponseData],
    partner_data: list[PartnerKPointData],
    n_momenta: int,
    dimension: int,
    eta: float,
    normalization: str,
    m0: str,
    m1: str,
    delta0: float,
    mu: float,
    nk: int,
    n_shell: int,
    n_keep: int,
    partner: str,
) -> dict[str, object]:
    delta_orb = orbital_pairing_matrix(
        delta0=delta0,
        eta=eta,
        n_momenta=n_momenta,
        m0=m0,
        m1=m1,
        normalization=normalization,
    )
    weights: list[float] = []
    raw_alignment_errors: list[float] = []
    best_alignment_errors: list[float] = []
    min_singular_values: list[float] = []
    mean_singular_values: list[float] = []
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

    for item, partner_item in zip(cache, partner_data):
        delta_band = project_pairing(item.vectors, delta_orb, partner_item.vectors)
        weights.append(interband_weight(delta_band))
        raw_alignment_errors.append(partner_item.raw_alignment_error)
        best_alignment_errors.append(partner_item.best_alignment_error)
        min_singular_values.append(partner_item.min_singular_value)
        mean_singular_values.append(partner_item.mean_singular_value)

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
        if (dxx_total + dyy_total) != 0.0
        else float("nan")
    )
    anisotropy_norm = (
        (dxx_total - dyy_total) / (dxx_total + dyy_total)
        if (dxx_total + dyy_total) != 0.0
        else float("nan")
    )

    row: dict[str, object] = {
        "eta": eta,
        "normalization": normalization,
        "m0": m0,
        "m1": m1,
        "partner": partner,
        "nk": nk,
        "n_shell": n_shell,
        "n_keep": n_keep,
        "dimension": dimension,
        "delta0_meV": delta0,
        "mu_meV": mu,
        "nu_proxy": filling_proxy_from_energies([item.eps for item in cache], mu),
        "interband_pairing_weight_mean": average(weights),
        "D_iso_raw": d_iso,
        "geom_fraction_total": geom_fraction,
        "anisotropy_norm": anisotropy_norm,
        "raw_partner_alignment_error_mean": average(raw_alignment_errors),
        "raw_partner_alignment_error_max": float(np.max(raw_alignment_errors)),
        "best_partner_alignment_error_mean": average(best_alignment_errors),
        "best_partner_alignment_error_max": float(np.max(best_alignment_errors)),
        "partner_min_singular_value_mean": average(min_singular_values),
        "partner_min_singular_value_min": float(np.min(min_singular_values)),
        "partner_mean_singular_value_mean": average(mean_singular_values),
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


def summarize_rows(
    rows: list[dict[str, object]],
    eta_baseline: float,
    eta_target: float,
) -> list[dict[str, object]]:
    baseline: dict[tuple[int, int, int, str, str, float], dict[str, object]] = {}
    target: dict[tuple[int, int, int, str, str, float], dict[str, object]] = {}
    for row in rows:
        key = (
            int(row["nk"]),
            int(row["n_keep"]),
            int(row["n_shell"]),
            str(row["partner"]),
            str(row["normalization"]),
            float(row["mu_meV"]),
        )
        eta = float(row["eta"])
        if abs(eta - eta_baseline) < 1.0e-12:
            baseline[key] = row
        if abs(eta - eta_target) < 1.0e-12:
            target[key] = row

    summary: list[dict[str, object]] = []
    for key in sorted(set(baseline).intersection(target)):
        base = baseline[key]
        targ = target[key]
        base_d = float(base["D_iso_raw"])
        target_d = float(targ["D_iso_raw"])
        rel = target_d / base_d - 1.0 if base_d != 0.0 else float("nan")
        summary.append(
            {
                "nk": key[0],
                "n_keep": key[1],
                "n_shell": key[2],
                "partner": key[3],
                "normalization": key[4],
                "mu_meV": key[5],
                "eta_baseline": eta_baseline,
                "eta_target": eta_target,
                "D_iso_baseline": base_d,
                "D_iso_target": target_d,
                "D_iso_rel_target_vs_baseline": rel,
                "D_iso_rel_percent": 100.0 * rel,
                "W_inter_baseline": float(base["interband_pairing_weight_mean"]),
                "W_inter_target": float(targ["interband_pairing_weight_mean"]),
                "raw_partner_alignment_error_mean": float(
                    targ["raw_partner_alignment_error_mean"]
                ),
                "best_partner_alignment_error_mean": float(
                    targ["best_partner_alignment_error_mean"]
                ),
                "partner_min_singular_value_min": float(
                    targ["partner_min_singular_value_min"]
                ),
                "max_closure_error": max(
                    float(base["max_closure_error"]),
                    float(targ["max_closure_error"]),
                ),
                "max_bdg_hermiticity_error": max(
                    float(base["max_bdg_hermiticity_error"]),
                    float(targ["max_bdg_hermiticity_error"]),
                ),
                "max_ph_spectrum_error": max(
                    float(base["max_ph_spectrum_error"]),
                    float(targ["max_ph_spectrum_error"]),
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
    total_configs = len(args.n_shells) * len(args.nks)
    config_index = 0

    for n_shell in args.n_shells:
        model = BMModel(BMParameters(n_shell=n_shell, valley=1))
        minus_model = BMModel(BMParameters(n_shell=n_shell, valley=-1))
        for nk in args.nks:
            config_index += 1
            print(
                f"[{config_index}/{total_configs}] "
                f"n_shell={n_shell} n_keep={args.n_keep} nk={nk}",
                flush=True,
            )
            cache = build_response_cache(
                model=model,
                nk=nk,
                n_keep=args.n_keep,
                dk=args.dk,
            )
            partner_cache = build_partner_cache(
                model=model,
                minus_model=minus_model,
                cache=cache,
                partners=args.partners,
                n_keep=args.n_keep,
            )
            for partner in args.partners:
                for normalization in args.normalizations:
                    for eta in args.etas:
                        for mu in args.mus:
                            rows.append(
                                evaluate_partner_row(
                                    cache=cache,
                                    partner_data=partner_cache[partner],
                                    n_momenta=model.n_momenta,
                                    dimension=model.dimension,
                                    eta=eta,
                                    normalization=normalization,
                                    m0=args.m0,
                                    m1=args.m1,
                                    delta0=args.delta0,
                                    mu=mu,
                                    nk=nk,
                                    n_shell=n_shell,
                                    n_keep=args.n_keep,
                                    partner=partner,
                                )
                            )

    summary = summarize_rows(rows, eta_baseline=args.etas[0], eta_target=args.etas[-1])
    write_csv(args.output, rows)
    write_csv(args.summary_output, summary)

    print(f"Wrote {args.output}")
    print(f"Wrote {args.summary_output}")
    print(f"Raw rows: {len(rows)}")
    print(f"Summary rows: {len(summary)}")
    for partner in args.partners:
        partner_rows = [
            row
            for row in summary
            if row["partner"] == partner and row["normalization"] == "fixed_frobenius_norm"
        ]
        positives = sum(float(row["D_iso_rel_target_vs_baseline"]) > 0.0 for row in partner_rows)
        print(f"{partner}: fixed_frobenius positive {positives}/{len(partner_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
