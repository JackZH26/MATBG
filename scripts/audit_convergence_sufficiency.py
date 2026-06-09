#!/usr/bin/env python3
"""Audit whether finite-grid data support the current mechanism claim."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
NK_TREND = PROCESSED / "nk_trend_audit_nkeep6.csv"
NK15_SUMMARY = PROCESSED / "mu_response_scan_nk15_nkeep6_spotcheck_summary.csv"
OUTPUT = PROCESSED / "convergence_sufficiency_audit.csv"


@dataclass(frozen=True)
class AuditRow:
    check_id: str
    status: str
    measured_value: str
    criterion: str
    consequence: str


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def keypoint_summary_path(nk: int) -> Path:
    return PROCESSED / f"mu_response_scan_nk{nk}_nkeep6_keypoints_summary.csv"


def pct(value: str | float) -> float:
    return 100.0 * float(value)


def fmt(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}"


def status(ok: bool) -> str:
    return "pass" if ok else "fail"


def load_keypoint_values() -> dict[tuple[str, float], dict[int, float]]:
    values: dict[tuple[str, float], dict[int, float]] = {}
    for nk in (9, 11, 13):
        for row in load_csv(keypoint_summary_path(nk)):
            key = (row["normalization"], float(row["mu_meV"]))
            values.setdefault(key, {})[nk] = pct(row["D_iso_rel_target_vs_baseline"])
    return values


def load_nk15_values() -> dict[tuple[str, float], float]:
    return {
        (row["normalization"], float(row["mu_meV"])): pct(
            row["D_iso_rel_target_vs_baseline"]
        )
        for row in load_csv(NK15_SUMMARY)
    }


def load_nk15_winter() -> list[float]:
    return [float(row["W_inter_target"]) for row in load_csv(NK15_SUMMARY)]


def build_audit_rows() -> list[AuditRow]:
    keypoints = load_keypoint_values()
    trend_rows = load_csv(NK_TREND)
    nk15 = load_nk15_values()

    frob_key_values = [
        value
        for (normalization, _mu), by_nk in keypoints.items()
        if normalization == "fixed_frobenius_norm"
        for value in by_nk.values()
    ]
    frob_ranges = []
    for mu in (-4.0, 0.0, 2.0, 4.0):
        values = list(keypoints[("fixed_frobenius_norm", mu)].values())
        frob_ranges.append(max(values) - min(values))

    frob_trend_h2 = [
        float(row["intercept_percent_h2"])
        for row in trend_rows
        if row["normalization"] == "fixed_frobenius_norm"
    ]
    frob_trend_h1 = [
        float(row["intercept_percent_h1"])
        for row in trend_rows
        if row["normalization"] == "fixed_frobenius_norm"
    ]
    frob_nk15 = [
        nk15[("fixed_frobenius_norm", 0.0)],
        nk15[("fixed_frobenius_norm", 2.0)],
    ]
    frob_nk15_deltas = [
        nk15[("fixed_frobenius_norm", mu)]
        - keypoints[("fixed_frobenius_norm", mu)][13]
        for mu in (0.0, 2.0)
    ]

    delta0_key_values = [
        value
        for (normalization, _mu), by_nk in keypoints.items()
        if normalization == "fixed_delta0"
        for value in by_nk.values()
    ]
    delta0_nk15 = [
        nk15[("fixed_delta0", 0.0)],
        nk15[("fixed_delta0", 2.0)],
    ]
    delta0_trend_status = [
        row["measured_sign_status"]
        for row in trend_rows
        if row["normalization"] == "fixed_delta0"
    ]

    winter_values = []
    for (normalization, _mu), by_nk in keypoints.items():
        if normalization != "fixed_frobenius_norm":
            continue
        for nk in by_nk:
            summary = load_csv(keypoint_summary_path(nk))
            for row in summary:
                if (
                    row["normalization"] == "fixed_frobenius_norm"
                    and float(row["mu_meV"]) == _mu
                ):
                    winter_values.append(float(row["W_inter_target"]))
                    break
    winter_values.extend(load_nk15_winter())
    winter_spread = max(winter_values) - min(winter_values)

    rows = [
        AuditRow(
            check_id="frob_keypoint_positive",
            status=status(min(frob_key_values) > 0.0),
            measured_value=(
                f"min={fmt(min(frob_key_values))}%, "
                f"max={fmt(max(frob_key_values))}%"
            ),
            criterion="all fixed-Frobenius nk=9/11/13 key-point responses > 0",
            consequence="supports sign stability of the normalized mechanism signal",
        ),
        AuditRow(
            check_id="frob_keypoint_range",
            status=status(max(frob_ranges) <= 3.0),
            measured_value=f"largest per-mu range={fmt(max(frob_ranges))} percentage points",
            criterion="largest nk=9/11/13 per-mu spread <= 3 percentage points",
            consequence="supports order-of-magnitude stability rather than precision extrapolation",
        ),
        AuditRow(
            check_id="frob_trend_intercepts_positive",
            status=status(min(frob_trend_h1 + frob_trend_h2) > 0.0),
            measured_value=(
                f"h2 min={fmt(min(frob_trend_h2))}%, "
                f"h1 min={fmt(min(frob_trend_h1))}%"
            ),
            criterion="both 1/nk and 1/nk^2 fixed-Frobenius intercept audits > 0",
            consequence="supports positive trend-sign robustness without claiming a continuum value",
        ),
        AuditRow(
            check_id="frob_nk15_positive",
            status=status(min(frob_nk15) > 0.0),
            measured_value=f"nk15 mu=0,2 values={fmt(frob_nk15[0])}%, {fmt(frob_nk15[1])}%",
            criterion="targeted nk=15 fixed-Frobenius spot checks > 0",
            consequence="tests the central representative points on a denser mesh",
        ),
        AuditRow(
            check_id="frob_nk15_close_to_nk13",
            status=status(max(abs(value) for value in frob_nk15_deltas) <= 1.5),
            measured_value=(
                "max |nk15-nk13|="
                f"{fmt(max(abs(value) for value in frob_nk15_deltas))} percentage points"
            ),
            criterion="targeted nk15 shifts from nk13 are <= 1.5 percentage points",
            consequence="supports scale stability at the two central representative points",
        ),
        AuditRow(
            check_id="delta0_control_weak",
            status=status(max(abs(value) for value in delta0_key_values + delta0_nk15) <= 2.0),
            measured_value=(
                "max measured |fixed-Delta0 response|="
                f"{fmt(max(abs(value) for value in delta0_key_values + delta0_nk15))}%"
            ),
            criterion="fixed-Delta0 measured-grid control remains within 2 percent",
            consequence="supports the normalization-conditioned interpretation",
        ),
        AuditRow(
            check_id="delta0_control_sign_sensitive",
            status=status(delta0_trend_status.count("mixed") >= 3),
            measured_value=(
                f"sign statuses={','.join(delta0_trend_status)}"
            ),
            criterion="at least three fixed-Delta0 trend rows have mixed measured signs",
            consequence="blocks a universal stiffness-enhancement interpretation",
        ),
        AuditRow(
            check_id="winter_grid_stability",
            status=status(winter_spread <= 0.004),
            measured_value=(
                f"W_inter range={fmt(min(winter_values), 4)}-{fmt(max(winter_values), 4)}"
            ),
            criterion="W_inter target spread across checked grids <= 0.004",
            consequence="supports stable projected-pairing scale across finite grids",
        ),
    ]

    all_pass = all(row.status == "pass" for row in rows)
    rows.append(
        AuditRow(
            check_id="overall_selected_grid_sufficiency",
            status=status(all_pass),
            measured_value=f"{sum(row.status == 'pass' for row in rows)}/{len(rows)} numeric gates pass",
            criterion="all finite-grid mechanism gates pass",
            consequence=(
                "sufficient for the selected-grid normalized mechanism claim; "
                "not sufficient for a final continuum-limit numerical estimate"
            ),
        )
    )
    return rows


def write_rows(path: Path, rows: list[AuditRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "check_id",
                "status",
                "measured_value",
                "criterion",
                "consequence",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "check_id": row.check_id,
                    "status": row.status,
                    "measured_value": row.measured_value,
                    "criterion": row.criterion,
                    "consequence": row.consequence,
                }
            )


def main() -> int:
    rows = build_audit_rows()
    write_rows(OUTPUT, rows)
    print(f"Wrote {OUTPUT}")
    pass_count = sum(row.status == "pass" for row in rows)
    print(f"Convergence sufficiency checks passed: {pass_count}/{len(rows)}")
    for row in rows:
        print(f"{row.check_id}: {row.status} ({row.measured_value})")
    return 0 if pass_count == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
