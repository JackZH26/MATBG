#!/usr/bin/env python3
"""Verify manuscript table values against processed CSV data."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEX_PATH = (
    ROOT
    / "Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_2026.tex"
)
SUPP_PATH = (
    ROOT
    / "Zhou_Interband_Pairing_Signatures_In_The_Superfluid_Response_Of_Magic_Angle_Twisted_Bilayer_Graphene_Supplemental_Material_2026.tex"
)
DENSE_SUMMARY = ROOT / "data" / "processed" / "mu_eta_response_scan_nk7_nkeep6_eta1_summary.csv"
NK9_SUMMARY = ROOT / "data" / "processed" / "mu_response_scan_nk9_nkeep6_keypoints_summary.csv"
NK11_SUMMARY = ROOT / "data" / "processed" / "mu_response_scan_nk11_nkeep6_keypoints_summary.csv"
NK13_SUMMARY = ROOT / "data" / "processed" / "mu_response_scan_nk13_nkeep6_keypoints_summary.csv"
NK15_SUMMARY = ROOT / "data" / "processed" / "mu_response_scan_nk15_nkeep6_spotcheck_summary.csv"
VALLEY_SEWING = ROOT / "data" / "processed" / "valley_sewing_diagnostic.csv"
PRB_RECON = ROOT / "data" / "processed" / "prb_table_reconstruction_nk14.csv"
FLAT_AUDIT = ROOT / "data" / "processed" / "flatband_endpoint_audit_nk14.csv"
FILLING_CROSSWALK = ROOT / "data" / "processed" / "filling_crosswalk_nk7_nshell3.csv"
NK_TREND = ROOT / "data" / "processed" / "nk_trend_audit_nkeep6.csv"
CONVERGENCE_SUFFICIENCY = (
    ROOT / "data" / "processed" / "convergence_sufficiency_audit.csv"
)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def table_block(tex: str, label: str) -> str:
    label_token = f"\\label{{{label}}}"
    label_pos = tex.index(label_token)
    start = tex.find("\\begin{tabular}", label_pos)
    end = tex.find("\\end{tabular}", start)
    if start < 0 or end < 0:
        raise ValueError(f"Could not locate tabular block for {label}")
    return tex[start:end]


def strip_latex_comment(line: str) -> str:
    for index, char in enumerate(line):
        if char == "%" and (index == 0 or line[index - 1] != "\\"):
            return line[:index]
    return line


def split_rows(block: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in block.splitlines():
        line = strip_latex_comment(line).strip()
        if "&" not in line or "\\\\" not in line:
            continue
        line = line.replace("\\\\", "").strip()
        cells = [cell.strip() for cell in line.split("&")]
        rows.append(cells)
    return rows


def number(cell: str) -> float:
    match = re.search(r"[-+]?\d+(?:\.\d+)?", cell)
    if match is None:
        raise ValueError(f"No numeric value found in cell: {cell!r}")
    return float(match.group(0))


def numbers(cell: str) -> list[float]:
    return [float(match) for match in re.findall(r"[-+]?\d+(?:\.\d+)?", cell)]


def assert_close(name: str, actual: float, expected: float, decimals: int) -> None:
    tolerance = 0.5 * 10.0 ** (-decimals) + 1.0e-12
    if abs(actual - expected) > tolerance:
        raise AssertionError(
            f"{name}: actual {actual} does not match expected {expected} "
            f"to {decimals} decimals"
        )


def rounded(value: str | float, decimals: int) -> float:
    return float(f"{float(value):.{decimals}f}")


def one_row(rows: list[dict[str, str]], **criteria: object) -> dict[str, str]:
    matches = []
    for row in rows:
        ok = True
        for key, expected in criteria.items():
            value = row[key]
            if isinstance(expected, float):
                ok = ok and abs(float(value) - expected) < 1.0e-12
            else:
                ok = ok and value == str(expected)
        if ok:
            matches.append(row)
    if len(matches) != 1:
        raise AssertionError(f"Expected one row for {criteria}, found {len(matches)}")
    return matches[0]


def verify_dense_eta(tex: str) -> None:
    rows = split_rows(table_block(tex, "tab:dense_eta"))
    data = load_csv(DENSE_SUMMARY)
    data_by_key = {
        (row["normalization"], int(float(row["mu_meV"]))): row
        for row in data
    }

    checked = 0
    for cells in rows:
        if len(cells) != 4:
            continue
        try:
            mu = int(number(cells[0]))
        except ValueError:
            continue
        frob = data_by_key[("fixed_frobenius_norm", mu)]
        delta0 = data_by_key[("fixed_delta0", mu)]
        assert_close(f"dense mu={mu} nu", number(cells[1]), rounded(frob["nu_proxy"], 3), 3)
        assert_close(
            f"dense mu={mu} fixed_frobenius",
            number(cells[2]),
            rounded(frob["D_iso_rel_target_vs_baseline"], 4),
            4,
        )
        assert_close(
            f"dense mu={mu} fixed_delta0",
            number(cells[3]),
            rounded(delta0["D_iso_rel_target_vs_baseline"], 4),
            4,
        )
        checked += 1
    if checked != 11:
        raise AssertionError(f"Expected 11 dense table rows, checked {checked}")


def verify_nk9(tex: str) -> None:
    rows = split_rows(table_block(tex, "tab:nk9"))
    data = load_csv(NK9_SUMMARY)
    data_by_key = {
        (row["normalization"], int(float(row["mu_meV"]))): row
        for row in data
    }

    checked = 0
    for cells in rows:
        if len(cells) != 3:
            continue
        try:
            mu = int(number(cells[0]))
        except ValueError:
            continue
        frob = data_by_key[("fixed_frobenius_norm", mu)]
        delta0 = data_by_key[("fixed_delta0", mu)]
        assert_close(
            f"nk9 mu={mu} fixed_frobenius",
            number(cells[1]),
            rounded(frob["D_iso_rel_target_vs_baseline"], 4),
            4,
        )
        assert_close(
            f"nk9 mu={mu} fixed_delta0",
            number(cells[2]),
            rounded(delta0["D_iso_rel_target_vs_baseline"], 4),
            4,
        )
        checked += 1
    if checked != 4:
        raise AssertionError(f"Expected 4 nk9 table rows, checked {checked}")


def expected_prb_rows() -> list[tuple[str, int, dict[str, str]]]:
    recon = load_csv(PRB_RECON)
    flat = load_csv(FLAT_AUDIT)
    return [
        (
            "current",
            2,
            one_row(recon, mode="current_tauz_tau0", n_keep=2.0),
        ),
        (
            "double",
            2,
            one_row(recon, mode="double_conv_all_tauz", n_keep=2.0),
        ),
        (
            "flat",
            2,
            one_row(
                flat,
                candidate="double_conv_full_curv_all_tauz",
                theta_deg=1.05,
                n_shell=3.0,
                mesh_variant="gamma_centered",
                band_selector="central_pair",
            ),
        ),
        (
            "double",
            6,
            one_row(recon, mode="double_conv_all_tauz", n_keep=6.0),
        ),
    ]


def verify_prb_audit(tex: str) -> None:
    rows = split_rows(table_block(tex, "tab:prb_audit"))
    numeric_rows = [row for row in rows if len(row) == 7 and row[1].strip().isdigit()]
    expected_rows = expected_prb_rows()
    if len(numeric_rows) != len(expected_rows):
        raise AssertionError(
            f"Expected {len(expected_rows)} PRB audit rows, found {len(numeric_rows)}"
        )

    for cells, (name, n_keep, data) in zip(numeric_rows, expected_rows):
        if n_keep != int(number(cells[1])):
            raise AssertionError(f"PRB row {name}: n_keep mismatch")
        assert_close(
            f"prb {name} n_keep={n_keep} total",
            number(cells[2]),
            rounded(data["D_total_eV_A2"], 2),
            2,
        )
        assert_close(
            f"prb {name} n_keep={n_keep} total target",
            number(cells[3]),
            rounded(data["target_D_total_eV_A2"], 2),
            2,
        )
        assert_close(
            f"prb {name} n_keep={n_keep} conv",
            number(cells[4]),
            rounded(data["D_conv_eV_A2"], 2),
            2,
        )
        assert_close(
            f"prb {name} n_keep={n_keep} conv target",
            number(cells[5]),
            rounded(data["target_D_conv_eV_A2"], 2),
            2,
        )
        assert_close(
            f"prb {name} n_keep={n_keep} geom",
            number(cells[6]),
            rounded(data["D_geom_eV_A2"], 2),
            2,
        )


def verify_supplemental_nk_convergence(tex: str) -> None:
    rows = split_rows(table_block(tex, "tab:sm_nk_convergence"))
    nk9 = load_csv(NK9_SUMMARY)
    nk11 = load_csv(NK11_SUMMARY)
    nk13 = load_csv(NK13_SUMMARY)
    nk9_by_key = {
        (row["normalization"], int(float(row["mu_meV"]))): row
        for row in nk9
    }
    nk11_by_key = {
        (row["normalization"], int(float(row["mu_meV"]))): row
        for row in nk11
    }
    nk13_by_key = {
        (row["normalization"], int(float(row["mu_meV"]))): row
        for row in nk13
    }

    checked = 0
    for cells in rows:
        if len(cells) != 5:
            continue
        if "Frobenius" not in cells[0] and "Delta" not in cells[0]:
            continue
        normalization = (
            "fixed_delta0" if "Delta" in cells[0] else "fixed_frobenius_norm"
        )
        mu_values = numbers(cells[0])
        if not mu_values:
            raise ValueError(f"No mu value found in cell: {cells[0]!r}")
        mu = int(mu_values[-1])
        value9 = float(nk9_by_key[(normalization, mu)]["D_iso_rel_target_vs_baseline"])
        value11 = float(nk11_by_key[(normalization, mu)]["D_iso_rel_target_vs_baseline"])
        value13 = float(nk13_by_key[(normalization, mu)]["D_iso_rel_target_vs_baseline"])
        assert_close(
            f"supp nk9 {normalization} mu={mu}",
            number(cells[1]),
            rounded(value9, 4),
            4,
        )
        assert_close(
            f"supp nk11 {normalization} mu={mu}",
            number(cells[2]),
            rounded(value11, 4),
            4,
        )
        assert_close(
            f"supp nk13 {normalization} mu={mu}",
            number(cells[3]),
            rounded(value13, 4),
            4,
        )
        assert_close(
            f"supp nk diff {normalization} mu={mu}",
            number(cells[4]),
            rounded(value13 - value9, 4),
            4,
        )
        checked += 1
    if checked != 8:
        raise AssertionError(f"Expected 8 supplemental convergence rows, checked {checked}")


def verify_supplemental_valley_sewing(tex: str) -> None:
    rows = split_rows(table_block(tex, "tab:sm_valley_sewing"))
    data = {
        int(float(row["n_keep"])): row
        for row in load_csv(VALLEY_SEWING)
    }

    checked = 0
    for cells in rows:
        if len(cells) != 4 or not cells[0].strip().isdigit():
            continue
        n_keep = int(number(cells[0]))
        row = data[n_keep]
        assert_close(
            f"supp valley n_keep={n_keep} alignment",
            number(cells[1]),
            rounded(row["alignment_error_mean"], 4),
            4,
        )
        assert_close(
            f"supp valley n_keep={n_keep} min singular mean",
            number(cells[2]),
            rounded(row["min_singular_mean"], 4),
            4,
        )
        assert_close(
            f"supp valley n_keep={n_keep} min singular min",
            number(cells[3]),
            rounded(row["min_singular_min"], 4),
            4,
        )
        checked += 1
    if checked != 3:
        raise AssertionError(f"Expected 3 supplemental valley rows, checked {checked}")


def verify_supplemental_filling_crosswalk(tex: str) -> None:
    rows = split_rows(table_block(tex, "tab:sm_filling_crosswalk"))
    data = {
        int(float(row["mu_meV"])): row
        for row in load_csv(FILLING_CROSSWALK)
    }

    checked = 0
    for cells in rows:
        if len(cells) != 4:
            continue
        try:
            mu = int(number(cells[0]))
        except ValueError:
            continue
        row = data[mu]
        assert_close(
            f"supp filling mu={mu} nu_proxy",
            number(cells[1]),
            rounded(row["nu_proxy"], 3),
            3,
        )
        assert_close(
            f"supp filling mu={mu} nu_flat",
            number(cells[2]),
            rounded(row["nu_flat"], 3),
            3,
        )
        assert_close(
            f"supp filling mu={mu} occupied flat bands",
            number(cells[3]),
            rounded(row["flat_occupied_bands_per_flavor"], 3),
            3,
        )
        checked += 1
    if checked != 11:
        raise AssertionError(
            f"Expected 11 supplemental filling crosswalk rows, checked {checked}"
        )


def verify_supplemental_nk_trend(tex: str) -> None:
    rows = split_rows(table_block(tex, "tab:sm_nk_trend"))
    data = {
        (row["normalization"], int(float(row["mu_meV"]))): row
        for row in load_csv(NK_TREND)
    }

    checked = 0
    for cells in rows:
        if len(cells) != 6:
            continue
        if "Frobenius" not in cells[0] and "Delta" not in cells[0]:
            continue
        normalization = (
            "fixed_delta0" if "Delta" in cells[0] else "fixed_frobenius_norm"
        )
        mu_values = numbers(cells[0])
        if not mu_values:
            raise ValueError(f"No mu value found in cell: {cells[0]!r}")
        mu = int(mu_values[-1])
        row = data[(normalization, mu)]
        assert_close(
            f"supp nk trend min {normalization} mu={mu}",
            number(cells[1]),
            rounded(row["min_percent"], 2),
            2,
        )
        assert_close(
            f"supp nk trend max {normalization} mu={mu}",
            number(cells[2]),
            rounded(row["max_percent"], 2),
            2,
        )
        assert_close(
            f"supp nk trend h2 {normalization} mu={mu}",
            number(cells[3]),
            rounded(row["intercept_percent_h2"], 2),
            2,
        )
        assert_close(
            f"supp nk trend h1 {normalization} mu={mu}",
            number(cells[4]),
            rounded(row["intercept_percent_h1"], 2),
            2,
        )
        if row["measured_sign_status"] not in cells[5]:
            raise AssertionError(
                f"supp nk trend sign {normalization} mu={mu}: "
                f"{cells[5]!r} does not contain {row['measured_sign_status']!r}"
            )
        checked += 1
    if checked != 8:
        raise AssertionError(f"Expected 8 supplemental nk trend rows, checked {checked}")


def verify_supplemental_nk15(tex: str) -> None:
    rows = split_rows(table_block(tex, "tab:sm_nk15"))
    nk13 = {
        (row["normalization"], int(float(row["mu_meV"]))): row
        for row in load_csv(NK13_SUMMARY)
    }
    nk15 = {
        (row["normalization"], int(float(row["mu_meV"]))): row
        for row in load_csv(NK15_SUMMARY)
    }

    checked = 0
    for cells in rows:
        if len(cells) != 5:
            continue
        if "Frobenius" not in cells[0] and "Delta" not in cells[0]:
            continue
        normalization = (
            "fixed_delta0" if "Delta" in cells[0] else "fixed_frobenius_norm"
        )
        mu_values = numbers(cells[0])
        if not mu_values:
            raise ValueError(f"No mu value found in cell: {cells[0]!r}")
        mu = int(mu_values[-1])
        value13 = float(nk13[(normalization, mu)]["D_iso_rel_target_vs_baseline"])
        row15 = nk15[(normalization, mu)]
        value15 = float(row15["D_iso_rel_target_vs_baseline"])
        assert_close(
            f"supp nk15 nk13 {normalization} mu={mu}",
            number(cells[1]),
            rounded(value13, 4),
            4,
        )
        assert_close(
            f"supp nk15 value {normalization} mu={mu}",
            number(cells[2]),
            rounded(value15, 4),
            4,
        )
        assert_close(
            f"supp nk15 diff {normalization} mu={mu}",
            number(cells[3]),
            rounded(value15 - value13, 4),
            4,
        )
        assert_close(
            f"supp nk15 winter {normalization} mu={mu}",
            number(cells[4]),
            rounded(row15["W_inter_target"], 4),
            4,
        )
        checked += 1
    if checked != 4:
        raise AssertionError(f"Expected 4 supplemental nk15 rows, checked {checked}")


def verify_supplemental_convergence_sufficiency(tex: str) -> None:
    rows = split_rows(table_block(tex, "tab:sm_convergence_sufficiency"))
    data = {row["check_id"]: row for row in load_csv(CONVERGENCE_SUFFICIENCY)}

    checked = 0
    for cells in rows:
        if len(cells) != 3:
            continue
        label = cells[0]
        actual = numbers(cells[1])
        if "Frob. sign" in label:
            expected = numbers(data["frob_keypoint_positive"]["measured_value"])
            assert_close("supp convergence frob min", actual[0], expected[0], 2)
            assert_close("supp convergence frob max", actual[1], expected[1], 2)
            checked += 1
        elif "Frob. spread" in label:
            expected = numbers(data["frob_keypoint_range"]["measured_value"])
            assert_close("supp convergence frob spread", actual[0], expected[0], 2)
            checked += 1
        elif "Trend intercepts" in label:
            expected = numbers(
                data["frob_trend_intercepts_positive"]["measured_value"]
            )
            assert_close("supp convergence trend h2", actual[0], expected[1], 2)
            assert_close("supp convergence trend h1", actual[1], expected[3], 2)
            checked += 1
        elif "nk=15" in label:
            expected_values = numbers(data["frob_nk15_positive"]["measured_value"])
            expected_shift = numbers(data["frob_nk15_close_to_nk13"]["measured_value"])
            assert_close("supp convergence nk15 mu0", actual[0], expected_values[-2], 2)
            assert_close("supp convergence nk15 mu2", actual[1], expected_values[-1], 2)
            assert_close("supp convergence nk15 shift", actual[2], expected_shift[-1], 2)
            checked += 1
        elif "Delta" in label:
            expected = numbers(data["delta0_control_weak"]["measured_value"])
            assert_close("supp convergence delta0 max", actual[0], expected[-1], 2)
            if "mixed" not in cells[1]:
                raise AssertionError("supp convergence delta0 row should report mixed signs")
            checked += 1
        elif "Overall scope" in label:
            expected = numbers(data["overall_selected_grid_sufficiency"]["measured_value"])
            assert_close("supp convergence numeric gate numerator", actual[0], expected[0], 0)
            assert_close("supp convergence numeric gate denominator", actual[1], expected[1], 0)
            checked += 1

    if checked != 6:
        raise AssertionError(
            f"Expected 6 supplemental convergence-sufficiency rows, checked {checked}"
        )


def main() -> int:
    tex = TEX_PATH.read_text()
    verify_dense_eta(tex)
    verify_nk9(tex)
    verify_prb_audit(tex)
    if SUPP_PATH.exists():
        supp = SUPP_PATH.read_text()
        verify_supplemental_nk_convergence(supp)
        verify_supplemental_valley_sewing(supp)
        verify_supplemental_filling_crosswalk(supp)
        verify_supplemental_nk_trend(supp)
        verify_supplemental_nk15(supp)
        verify_supplemental_convergence_sufficiency(supp)
    print("All manuscript and supplemental table values match processed CSV data.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
