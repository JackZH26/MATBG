# Flat-Band Endpoint Audit

日期：2026-06-09

## Question

Why does the PRB reconstruction route reproduce the extended-band endpoint
(`n_keep=6`) but not the flat-band endpoint (`n_keep=2`)?

## Commands

```text
python3 scripts/audit_flatband_endpoint.py --theta-values 1.05 --n-shell-values 3 --mesh-variants half_shift_centered gamma_centered positive_half_shift --band-selectors central_pair closest_abs valence_conduction --output data/processed/flatband_endpoint_audit_nk14.csv

python3 scripts/audit_flatband_endpoint.py --theta-values 1.00 1.05 1.10 1.15 1.20 --n-shell-values 3 --mesh-variants gamma_centered --band-selectors central_pair --output data/processed/flatband_endpoint_theta_scan_gamma_centered.csv

python3 scripts/audit_flatband_endpoint.py --theta-values 1.05 --n-shell-values 2 3 --mesh-variants gamma_centered --band-selectors central_pair --output data/processed/flatband_endpoint_nshell_scan_gamma_centered.csv
```

## Main Finding

The closest `n_keep=2` reconstruction is:

```text
mesh_variant = gamma_centered
band_selector = central_pair
candidate = double_conv_full_curv_all_tauz
theta = 1.05 deg
n_shell = 3
```

It gives:

```text
D_total = 66.18 vs PRB 67.50 eV A^2  (-1.95%)
D_conv  = 53.83 vs PRB 53.00 eV A^2  (+1.56%)
D_geom  = 12.36 vs PRB 14.50 eV A^2  (-14.79%)
geom fraction = 0.187 vs PRB 0.215
```

So the old flat-band total and conventional numbers can be nearly reproduced
by combining:

1. a Gamma-centered mesh convention;
2. the central valence/conduction pair;
3. an `all_tauz` current convention;
4. a factor of two on the intraband conventional term;
5. a full curvature-like correction in the conventional channel.

The geometric component remains low.

## Theta Scan

Keeping `gamma_centered + central_pair`:

```text
theta = 1.05:
D_total = 66.18, D_conv = 53.83, D_geom = 12.36

theta = 1.20:
D_total = 68.24, D_conv = 51.27, D_geom = 16.97
```

The `theta=1.20` point matches the old bandwidth scale better, but it overshoots
the old geometric component and is not a cleaner reconstruction overall.

## Cutoff Scan

With `gamma_centered + central_pair` at `theta=1.05`:

```text
n_shell = 3:
W = 6.21 meV, D_total = 66.18, D_conv = 53.83, D_geom = 12.36

n_shell = 2:
W = 11.91 meV, D_total = 45.25, D_conv = 34.48, D_geom = 10.77
```

Again, matching the old bandwidth scale does not imply matching the old
stiffness table.

## Interpretation

The old `n_keep=2` endpoint is sensitive to k-mesh convention and conventional
channel bookkeeping. A plausible reconstruction of the old total and
conventional entries exists, but it relies on a full curvature correction that
does not work as a universal correction at `n_keep=6`.

This strongly suggests the old PRB table mixed conventions or came from a
different implementation path than the current production response engine.

## Decision

Keep the PRB reconstruction route as a historical benchmark only. Do not use it
to set the production convention for the interband-pairing mechanism scans.

For manuscript development, either:

1. regenerate all absolute PRB-style tables from one explicitly declared modern
   convention; or
2. use normalized mechanism figures and defer absolute stiffness tables.
