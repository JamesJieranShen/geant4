#!/usr/bin/env python3
"""Compare the output of run_tests.sh: identity of the event records, and correlated vs independent.

    analyze.py <output dir> <TENDL Alpha/Inelastic dir>  ->  <output dir>/report.md, spectra_<E>.pdf
"""
import filecmp
import re
import sys
import zlib
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ENERGIES = [5, 10, 20]
METHODS = ["Poisson", "default"]
LIGHT = {"n": (0, 1), "p": (1, 1), "d": (1, 2), "t": (1, 3), "He3": (2, 3), "alpha": (2, 4)}
TARGET_ZA = (18, 40)
PROJECTILE_ZA = (2, 4)
E_TOLERANCE = 1e-3  # MeV: 1 keV, the excitation below which SampleCorrelated takes the ground state


def same(data, a, b):
    return all(filecmp.cmp(data / f"{a}_{s}.csv", data / f"{b}_{s}.csv", shallow=False) for s in ("events", "products"))


def tabulated(tendl_dir, energy, target="18_40_Argon"):
    """Yields of the MT5 (F02) products at this energy, as {ZA: yield}, straight from the data file."""
    lines = zlib.decompress(Path(tendl_dir, "F02", f"{target}.z").read_bytes()).decode().splitlines()
    head = re.compile(r"^\s*\d\.\d{6}e[+-]\d\d\s+\d\.\d+e[+-]\d\d\s+0\s+\d+\s*$")
    out = {}
    for i, line in enumerate(lines):
        if not head.match(line):
            continue
        j = i + 2
        n = int(lines[j].split()[0])
        j += 2 + int(lines[j + 1].split()[0])
        v = []
        while len(v) < 2 * n:
            v += [float(x) for x in lines[j].split()]
            j += 1
        out[round(float(line.split()[0]))] = float(np.interp(energy * 1e6, v[0::2], v[1::2]))
    return out


def load(data, name):
    return pd.read_csv(data / f"{name}_events.csv"), pd.read_csv(data / f"{name}_products.csv")


def conservation(events, products):
    """Per interaction, imbalances of Z, A and energy (MeV). Bound-electron mass is not tracked: e- count as kinetic."""
    interactions = events[events.process == "alphaInelastic"].set_index("event")
    p = products[products.event.isin(interactions.index)]
    electron = p.pdg == 11
    out = pd.DataFrame(index=interactions.index)
    nuclear = p[~electron]
    out["dZ"] = nuclear.groupby("event").Z.sum().reindex(out.index, fill_value=0) - (TARGET_ZA[0] + PROJECTILE_ZA[0])
    out["dA"] = nuclear.groupby("event").A.sum().reindex(out.index, fill_value=0) - (TARGET_ZA[1] + PROJECTILE_ZA[1])
    energy = (p.kinetic + np.where(electron, 0.0, p.mass)).groupby(p.event).sum().reindex(out.index, fill_value=0.0)
    out["dE"] = energy - (interactions.kinetic + interactions.proj_mass + interactions.targ_mass)
    return out


def species(products):
    """A label for each product: light particle name, gamma, e-, or ZA for the residuals."""
    labels = np.full(len(products), "", dtype=object)
    z, a, pdg = products.Z.values, products.A.values, products.pdg.values
    labels[pdg == 22] = "gamma"
    labels[pdg == 11] = "e-"
    for name, (lz, la) in LIGHT.items():
        labels[(z == lz) & (a == la) & (pdg != 22) & (pdg != 11)] = name
    rest = labels == ""
    labels[rest] = (z[rest] * 1000 + a[rest]).astype(str)
    return labels


def spectra_stats(a, b):
    """Means and the chi2/ndf of two equal-binning normalised histograms."""
    lo, hi = min(a.min(), b.min()), max(a.max(), b.max())
    edges = np.linspace(lo, hi + 1e-9, 41)
    ha, hb = np.histogram(a, edges)[0], np.histogram(b, edges)[0]
    keep = (ha + hb) > 0
    fa, fb = ha / len(a), hb / len(b)
    var = ha / len(a) ** 2 + hb / len(b) ** 2
    chi2 = (((fa - fb)[keep]) ** 2 / var[keep]).sum()
    return chi2 / max(keep.sum() - 1, 1)


def main(out, tendl_dir):
    out = Path(out)
    data = out / "data"
    r = ["# ParticleHP MT5 validation: alpha + 40Ar\n"]

    # log of the method really used
    r.append("## Multiplicity method actually used\n")
    r.append("| run | method reported by G4ParticleHPManager |\n|---|---|")
    for name in ["id_base_Poisson_10", "id_off_Poisson_10", "id_base_default_10", "id_off_default_10", "corr_off_10", "corr_on_10"]:
        m = re.search(r"VALIDATION multiplicity method: (\w+)", (out / "logs" / f"{name}.log").read_text())
        r.append(f"| {name} | {m.group(1) if m else 'NOT FOUND'} |")

    # identity
    r.append("\n## Test 1: identity\n")
    r.append("Byte comparison of the event records, 100k primaries each. `off` is the flag explicitly off, `unset` is the"
             " default of the flag.\n")
    r.append("| E (MeV) | method | base = base (repeat) | base = PR off | base = PR unset | control: other seed differs | control: PR on differs |\n|---|---|---|---|---|---|---|")
    passed = True
    for e in ENERGIES:
        for m in METHODS:
            base = f"id_base_{m}_{e}"
            rep, off, unset = (same(data, base, f"id_{k}_{m}_{e}") for k in ("base2", "off", "unset"))
            seed, on = (not same(data, base, f"id_{k}_{m}_{e}") for k in ("otherseed", "on"))
            passed &= rep and off and unset and seed and on
            r.append(f"| {e} | {m} | {rep} | {off} | {unset} | {seed} | {on} |")
    r.append(f"\nAll passed: **{passed}**")

    r.append("\n## Test 2: correlated (flag on) vs independent (flag off), Poisson\n")
    for e in ENERGIES:
        ev_off, pr_off = load(data, f"corr_off_{e}")
        ev_on, pr_on = load(data, f"corr_on_{e}")
        n_off = (ev_off.process == "alphaInelastic").sum()
        n_on = (ev_on.process == "alphaInelastic").sum()
        pr_off["sp"], pr_on["sp"] = species(pr_off), species(pr_on)
        tab = tabulated(tendl_dir, e)
        r.append(f"\n### E = {e} MeV\n")
        r.append(f"Inelastic interactions: off {n_off} of {len(ev_off)} primaries, on {n_on} of {len(ev_on)}.\n")

        r.append("| conservation per interaction | off | on |\n|---|---|---|")
        c_off, c_on = conservation(ev_off, pr_off), conservation(ev_on, pr_on)
        for label, f in (
            ("Z conserved", lambda c: c.dZ == 0),
            ("A conserved", lambda c: c.dA == 0),
            ("E conserved within 1 keV", lambda c: c.dE.abs() < E_TOLERANCE),
            ("all three", lambda c: (c.dZ == 0) & (c.dA == 0) & (c.dE.abs() < E_TOLERANCE)),
        ):
            r.append(f"| {label} | {f(c_off).mean():.5f} | {f(c_on).mean():.5f} |")
        r.append(f"| RMS of E imbalance (MeV) | {c_off.dE.std():.4g} | {c_on.dE.std():.4g} |")

        r.append("\n| product | tabulated yield | off | on | (on-off)/sigma | on/tabulated |\n|---|---|---|---|---|---|")
        counts_off, counts_on = pr_off.sp.value_counts(), pr_on.sp.value_counts()
        names = list(LIGHT) + ["gamma", "e-"]
        residuals = sorted(
            set(s for s in set(counts_off.index) | set(counts_on.index) if s.isdigit()),
            key=lambda s: -max(counts_off.get(s, 0), counts_on.get(s, 0)),
        )
        za_light = {"n": 1, "p": 1001, "d": 1002, "t": 1003, "He3": 2003, "alpha": 2004, "gamma": 0}
        for s in names + residuals[:12]:
            ko, kn = counts_off.get(s, 0), counts_on.get(s, 0)
            yo, yn = ko / n_off, kn / n_on
            err = np.sqrt(ko / n_off**2 + kn / n_on**2)
            t = tab.get(za_light[s] if s in za_light else int(s) if s.isdigit() else -1, float("nan"))
            pull = (yn - yo) / err if err > 0 else float("nan")
            ratio = yn / t if t and t > 0 else float("nan")
            r.append(f"| {s} | {t:.5g} | {yo:.5g} | {yn:.5g} | {pull:.1f} | {ratio:.4f} |")

        r.append("\n| spectrum | mean T off (MeV) | mean T on (MeV) | T chi2/ndf | mean cos off | mean cos on | cos chi2/ndf |\n|---|---|---|---|---|---|---|")
        fig, axes = plt.subplots(2, 4, figsize=(16, 7))
        for ax_t, ax_c, s in zip(axes[0], axes[1], ["n", "p", "alpha", "gamma"]):
            so, sn = pr_off[pr_off.sp == s], pr_on[pr_on.sp == s]
            if len(so) == 0 or len(sn) == 0:
                r.append(f"| {s} | no entries: off {len(so)}, on {len(sn)} | | | | | |")
                continue
            co = so.pz / np.sqrt(so.px**2 + so.py**2 + so.pz**2)
            cn = sn.pz / np.sqrt(sn.px**2 + sn.py**2 + sn.pz**2)
            r.append(f"| {s} | {so.kinetic.mean():.4f} | {sn.kinetic.mean():.4f} | {spectra_stats(so.kinetic, sn.kinetic):.1f}"
                     f" | {co.mean():.4f} | {cn.mean():.4f} | {spectra_stats(co, cn):.1f} |")
            for ax, a, b, x in ((ax_t, so.kinetic, sn.kinetic, "T (MeV)"), (ax_c, co, cn, r"cos$\theta$")):
                edges = np.linspace(min(a.min(), b.min()), max(a.max(), b.max()), 41)
                ax.hist(a, edges, weights=np.full(len(a), 1 / n_off), histtype="step", label="independent (off)")
                ax.hist(b, edges, weights=np.full(len(b), 1 / n_on), histtype="step", label="correlated (on)")
                ax.set_xlabel(f"{s} {x}")
                ax.set_ylabel("per interaction")
            ax_t.set_yscale("log")
        axes[0][0].legend()
        fig.suptitle(f"alpha + 40Ar, {e} MeV, Poisson")
        fig.tight_layout()
        fig.savefig(out / f"spectra_{e}.pdf")
        plt.close(fig)

    (out / "report.md").write_text("\n".join(r) + "\n")
    print("\n".join(r))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
