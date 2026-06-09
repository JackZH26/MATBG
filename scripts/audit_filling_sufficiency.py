#!/usr/bin/env python3
"""Audit whether the filling crosswalk supports the mechanism-paper scope."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
FILLING_CROSSWALK = PROCESSED / "filling_crosswalk_nk7_nshell3.csv"
DENSE_SUMMARY = PROCESSED / "mu_eta_response_scan_nk7_nkeep6_eta1_summary.csv"
OUTPUT = PROCESSED / "filling_sufficiency_audit.csv"


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


def values(rows: list[dict[str, str]], key: str) -> list[float]:
    return [float(row[key]) for row in rows]


def fmt(value: float, digits: int = 3) -> str:
    return f"{value:.{digits}f}"


def status(ok: bool) -> str:
    return "pass" if ok else "fail"


def is_strictly_increasing(data: list[float]) -> bool:
    return all(right > left for left, right in zip(data, data[1:]))


def is_nondecreasing(data: list[float]) -> bool:
    return all(right >= left for left, right in zip(data, data[1:]))


def unique_sorted(data: list[float]) -> list[float]:
    return sorted({round(value, 12) for value in data})


def build_audit_rows() -> list[AuditRow]:
    crosswalk = load_csv(FILLING_CROSSWALK)
    dense = load_csv(DENSE_SUMMARY)

    mus = values(crosswalk, "mu_meV")
    dense_mus = unique_sorted(values(dense, "mu_meV"))
    nu_proxy = values(crosswalk, "nu_proxy")
    nu_flat = values(crosswalk, "nu_flat")
    flat_occ = values(crosswalk, "flat_occupied_bands_per_flavor")
    flat_fraction = values(crosswalk, "flat_occupation_fraction")
    flat_min = values(crosswalk, "flat_band_min_meV")
    flat_max = values(crosswalk, "flat_band_max_meV")

    mu_min = min(mus)
    mu_max = max(mus)
    flat_band_min = min(flat_min)
    flat_band_max = max(flat_max)
    min_abs_nu0 = min(abs(value) for value in nu_flat)
    min_abs_num2 = min(abs(value + 2.0) for value in nu_flat)
    min_abs_nup2 = min(abs(value - 2.0) for value in nu_flat)

    rows = [
        AuditRow(
            check_id="mu_grid_matches_dense_scan",
            status=status(unique_sorted(mus) == dense_mus),
            measured_value=f"{len(unique_sorted(mus))} crosswalk mus match dense summary",
            criterion="crosswalk mu grid equals the dense response summary mu grid",
            consequence="supports direct table-to-table reading of mu and filling labels",
        ),
        AuditRow(
            check_id="nu_proxy_monotone",
            status=status(is_strictly_increasing(nu_proxy)),
            measured_value=(
                f"nu_proxy range={fmt(min(nu_proxy))} to {fmt(max(nu_proxy))}"
            ),
            criterion="retained-band proxy is strictly increasing over the scan",
            consequence="supports using nu_proxy only as an ordering label",
        ),
        AuditRow(
            check_id="nu_flat_nondecreasing",
            status=status(is_nondecreasing(nu_flat)),
            measured_value=f"nu_flat range={fmt(min(nu_flat))} to {fmt(max(nu_flat))}",
            criterion="central-flat-band filling is nondecreasing over the scan",
            consequence="supports a consistent flat-band counting crosswalk",
        ),
        AuditRow(
            check_id="flat_band_window_inside_mu_scan",
            status=status(mu_min <= flat_band_min and mu_max >= flat_band_max),
            measured_value=(
                f"mu=[{fmt(mu_min)}, {fmt(mu_max)}] meV; "
                f"flat window=[{fmt(flat_band_min)}, {fmt(flat_band_max)}] meV"
            ),
            criterion="dense mu range brackets the central two-band energy window",
            consequence="supports empty-to-full central-flat-band coverage",
        ),
        AuditRow(
            check_id="nu_flat_full_range_spanned",
            status=status(min(nu_flat) <= -4.0 and max(nu_flat) >= 4.0),
            measured_value=f"nu_flat min/max={fmt(min(nu_flat))}, {fmt(max(nu_flat))}",
            criterion="central-flat-band count spans -4 to +4 with g=4",
            consequence="supports full flat-band counting coverage for the mechanism scan",
        ),
        AuditRow(
            check_id="flat_occupation_bounds",
            status=status(
                min(flat_occ) >= 0.0
                and max(flat_occ) <= 2.0
                and min(flat_fraction) >= 0.0
                and max(flat_fraction) <= 1.0
            ),
            measured_value=(
                f"occupied bands/flavor={fmt(min(flat_occ))} to {fmt(max(flat_occ))}"
            ),
            criterion="central pair occupancy stays within the two-band bounds",
            consequence="checks that the crosswalk remains a valid counting reference",
        ),
        AuditRow(
            check_id="central_filling_sampled",
            status=status(min_abs_nu0 <= 0.75),
            measured_value=f"closest |nu_flat|={fmt(min_abs_nu0)}",
            criterion="dense mu grid samples the central flat-band filling region",
            consequence="supports reading the response map across the central crossing",
        ),
        AuditRow(
            check_id="pm2_filling_neighborhoods_sampled",
            status=status(min_abs_num2 <= 0.5 and min_abs_nup2 <= 0.5),
            measured_value=(
                f"closest to -2: {fmt(min_abs_num2)}; "
                f"closest to +2: {fmt(min_abs_nup2)}"
            ),
            criterion="dense mu grid includes counting-reference points near nu_flat=+-2",
            consequence="allows qualitative orientation relative to common MATBG fillings",
        ),
    ]

    all_numeric_pass = all(row.status == "pass" for row in rows)
    rows.append(
        AuditRow(
            check_id="overall_filling_reference_sufficiency",
            status=status(all_numeric_pass),
            measured_value=f"{sum(row.status == 'pass' for row in rows)}/{len(rows)} numeric gates pass",
            criterion="all filling crosswalk mechanism-scope gates pass",
            consequence=(
                "sufficient as a BM central-flat-band counting reference; "
                "not sufficient as a device-level carrier-density calibration"
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
            writer.writerow(row.__dict__)


def main() -> int:
    rows = build_audit_rows()
    write_rows(OUTPUT, rows)
    print(f"Wrote {OUTPUT}")
    pass_count = sum(row.status == "pass" for row in rows)
    print(f"Filling sufficiency checks passed: {pass_count}/{len(rows)}")
    for row in rows:
        print(f"{row.check_id}: {row.status} ({row.measured_value})")
    return 0 if pass_count == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
