#!/usr/bin/env python3
"""Why the light-particle spectra differ at 20 MeV with correlated sampling, and the loss of residuals.

    investigate.py <investigation dir> <run_tests output dir> <TENDL Alpha/Inelastic dir> <output dir>

The flag-off sample without relabelling holds the tabulated draws, in the order they were made. The
closure test rebuilds the correlated light-particle spectra from those draws alone, using the channel
fractions of the flag-on run and the rejection of SampleCorrelated: if the flag-on spectra come out, the
steps of the toy are the cause of the shift, and each can be switched off to find its share.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analyze import tabulated

BEAM = 20.0
LIGHT = {"n": (0, 1), "p": (1, 1), "d": (1, 2), "t": (1, 3), "He3": (2, 3), "alpha": (2, 4)}
TOLERANCE = 1e-3
rng = np.random.default_rng(20)


def load_products(path):
    p = pd.read_csv(path)
    p["za"] = p.Z * 1000 + p.A
    p["sp"] = ""
    for name, (z, a) in LIGHT.items():
        p.loc[(p.Z == z) & (p.A == a) & (p.pdg != 22) & (p.pdg != 11), "sp"] = name
    return p


def order_stats(draws, out):
    """Energy of the k-th draw of a product in one interaction: the remaining-energy bookkeeping."""
    out.append("\n## Successive draws of one product in an interaction (flag off, tabulated draws)\n")
    out.append("| product | draw | entries | mean T (MeV) | max T (MeV) |\n|---|---|---|---|---|")
    for label, sel in (("Ca42", draws.za == 20042), ("n", draws.sp == "n"), ("p", draws.sp == "p"), ("alpha", draws.sp == "alpha")):
        d = draws[sel].copy()
        d["k"] = d.groupby("event").cumcount()
        for k, g in d.groupby("k"):
            if k < 4 and len(g) >= 20:
                out.append(f"| {label} | {k + 1} | {len(g)} | {g.kinetic.mean():.3f} | {g.kinetic.max():.3f} |")


def residual_loss(draws, tab, n_events, out):
    out.append("\n## Residual yields written out vs tabulated (flag off, no relabelling)\n")
    out.append("| residual | tabulated | written | written/tabulated | pull |\n|---|---|---|---|---|")
    for za in sorted((z for z, y in tab.items() if z > 2004 and y * n_events >= 100), key=lambda z: -tab[z]):
        k = (draws.za == za).sum()
        expected = tab[za] * n_events
        out.append(f"| {za} | {tab[za]:.5f} | {k / n_events:.5f} | {k / expected:.4f} | {(k - expected) / expected**0.5:.1f} |")


def pools(draws):
    """For each light species and multiplicity k, the first k draws of the interactions that had them."""
    result = {}
    for name in LIGHT:
        d = draws[draws.sp == name].copy()
        d["k"] = d.groupby("event").cumcount()
        result[name] = {}
        for k in range(1, 5):
            first = d[d.k < k]
            size = first.groupby("event").kinetic.transform("size")
            sel = first[size == k].sort_values(["event", "k"])
            if len(sel) >= k:
                result[name][k] = sel[["kinetic", "px", "py", "pz", "mass"]].values.reshape(-1, k, 5)
    return result


def first_draws(draws):
    """Draws without the memory of earlier draws: only the first of each interaction."""
    d = draws[draws.sp != ""].copy()
    d["k"] = d.groupby(["event", "sp"]).cumcount()
    return {name: g[["kinetic", "px", "py", "pz", "mass"]].values for name, g in d[d.k == 0].groupby("sp")}


def channels(on, n_events):
    """Fractions of the flag-on exit channels."""
    light = on[on.sp != ""]
    counts = light.groupby(["event", "sp"]).size().unstack(fill_value=0).reindex(columns=list(LIGHT), fill_value=0)
    heavy = on[(on.sp == "") & (on.A > 4)].set_index("event").za
    table = counts.join(heavy.rename("res"), how="right").fillna(0).astype(int)
    grouped = table.groupby(["res"] + list(LIGHT)).size().sort_values(ascending=False) / n_events
    return grouped


def toy(chans, pool, single, masses, n_total, reject=True, memory=True):
    """Spectra of the channel mixture. Returns {species: (T, cos)} and the acceptance per channel."""
    p_beam = np.sqrt((BEAM + masses["proj"]) ** 2 - masses["proj"] ** 2)
    initial = np.array([BEAM + masses["proj"] + masses["targ"], 0.0, 0.0, p_beam])
    spectra = {name: [] for name in LIGHT}
    acceptance = {}
    for key, fraction in chans.items():
        res, counts = key[0], dict(zip(LIGHT, key[1:]))
        want = max(int(fraction * n_total), 1)
        tries = want * 40
        vectors, parts = np.zeros((tries, 4)), {}
        possible = True
        for name, k in counts.items():
            if k == 0:
                continue
            if memory:
                source = pool[name].get(k)
                if source is None:
                    possible = False
                    break
                picked = source[rng.integers(len(source), size=tries)]
            else:
                source = single.get(name)
                if source is None:
                    possible = False
                    break
                picked = source[rng.integers(len(source), size=tries * k)].reshape(tries, k, 5)
            parts[name] = picked
            vectors[:, 0] += (picked[..., 0] + picked[..., 4]).sum(axis=1)
            vectors[:, 1:] += picked[..., 1:4].sum(axis=1)
        if not possible:
            continue
        left = initial - vectors
        m2 = left[:, 0] ** 2 - (left[:, 1:] ** 2).sum(axis=1)
        keep = (left[:, 0] > 0) & (m2 > 0) & (np.sqrt(np.maximum(m2, 0)) - masses[res] > -TOLERANCE)
        acceptance[key] = keep.mean()
        index = np.flatnonzero(keep) if reject else np.arange(tries)
        index = index[:want]
        for name, picked in parts.items():
            chosen = picked[index].reshape(-1, 5)
            spectra[name].append(chosen)
    return {k: np.concatenate(v) for k, v in spectra.items() if v}, acceptance


def cos_theta(x):
    return x[:, 3] / np.sqrt((x[:, 1:4] ** 2).sum(axis=1))


def scan(inv, out, figures):
    rows = []
    for e in sorted(int(f.stem.split("_")[2]) for f in inv.glob("scan_on_*_events.csv")):
        row = {"E": e}
        for mode in ("off", "on"):
            p = load_products(inv / f"scan_{mode}_{e}_products.csv")
            n = len(pd.read_csv(inv / f"scan_{mode}_{e}_events.csv"))
            for s in ("n", "p", "alpha"):
                row[f"T_{s}_{mode}"] = p[p.sp == s].kinetic.mean()
                row[f"err_{s}_{mode}"] = p[p.sp == s].kinetic.std() / max((p.sp == s).sum(), 1) ** 0.5
                row[f"y_{s}_{mode}"] = (p.sp == s).sum() / n
            if mode == "on":
                light = p[p.sp == "n"].groupby("event").size()
                row["f_2n"] = (light >= 2).sum() / n
        rows.append(row)
    t = pd.DataFrame(rows)
    out.append("\n## Energy scan: mean T with the flag on vs off\n")
    out.append("`on/off` for neutrons and protons, which relabelling cannot touch; the alphas of the flag-off runs include relabelled products.\n")
    out.append("| E (MeV) | mean T n off | on/off | mean T p off | on/off | alpha on (MeV) | events with >= 2 n (on) |\n|---|---|---|---|---|---|---|")
    ratio_err = lambda r, s: (r[f"T_{s}_on"] / r[f"T_{s}_off"]) * np.hypot(r[f"err_{s}_on"] / r[f"T_{s}_on"], r[f"err_{s}_off"] / r[f"T_{s}_off"])
    for _, r in t.iterrows():
        out.append(f"| {r.E:.0f} | {r.T_n_off:.3f} | {r.T_n_on / r.T_n_off:.3f} +- {ratio_err(r, 'n'):.3f} | {r.T_p_off:.3f} | {r.T_p_on / r.T_p_off:.3f} +- {ratio_err(r, 'p'):.3f} | {r.T_alpha_on:.3f} | {r.f_2n:.3f} |")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for s, c in (("n", "C0"), ("p", "C1")):
        ax.errorbar(t.E, t[f"T_{s}_on"] / t[f"T_{s}_off"], yerr=t[f"err_{s}_on"] / t[f"T_{s}_off"], marker="o", color=c, label=s)
    ax2 = ax.twinx()
    ax2.plot(t.E, t.f_2n, "k--", label=">= 2 n")
    ax2.set_ylabel("fraction of events with >= 2 neutrons (on)")
    ax.axhline(1, color="grey", lw=0.8)
    ax.set_xlabel("alpha energy (MeV)")
    ax.set_ylabel("mean T: correlated / independent")
    ax.legend(loc="lower left")
    ax2.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(figures / "scan_mean_T.pdf")
    plt.close(fig)


def budget(draws, on, n_events, tab, masses, out):
    """Mean energy per interaction, in the tabulated draws and with the flag on."""
    available = BEAM + masses["proj"] + masses["targ"]
    out.append("\n## Energy budget per interaction (MeV)\n")
    out.append("| carried by | tabulated draws: yield x mean T | correlated |\n|---|---|---|")
    groups = {"n": lambda p: p.sp == "n", "p": lambda p: p.sp == "p", "d,t,He3": lambda p: p.sp.isin(["d", "t", "He3"]),
              "alpha": lambda p: p.sp == "alpha", "photons": lambda p: p.pdg == 22, "residual": lambda p: (p.sp == "") & (p.A > 4)}
    totals = [0.0, 0.0]
    for name, f in groups.items():
        a, b = draws[f(draws)].kinetic.sum() / n_events, on[f(on)].kinetic.sum() / n_events
        totals[0] += a
        totals[1] += b
        out.append(f"| {name} | {a:.3f} | {b:.3f} |")
    out.append(f"| total kinetic | {totals[0]:.3f} | {totals[1]:.3f} |")
    # The correlated events balance, so they give the kinetic energy available on average. It cannot be
    # computed from the tabulated yields: their A sums to less than 44, and each missing nucleon counts
    # as about 930 MeV.
    rest_on = on[on.pdg != 22].mass.sum() / n_events
    out.append(f"\nAvailable kinetic energy (E_in - rest mass of the correlated events): {available - rest_on:.3f} MeV.")
    baryons = sum(y * (z % 1000) for z, y in tab.items() if z > 0)
    out.append(f"\nSum of tabulated yield x A: {baryons:.4f} (the reaction has A = 44).")


def main(inv, results, tendl, target):
    inv, results, target = Path(inv), Path(results), Path(target)
    target.mkdir(parents=True, exist_ok=True)
    out = ["# Investigation of the 20 MeV differences and the residual loss\n"]
    draws = load_products(inv / "draws_20_products.csv")
    n_draws = len(pd.read_csv(inv / "draws_20_events.csv"))
    on = load_products(results / "data/corr_on_20_products.csv")
    off = load_products(results / "data/corr_off_20_products.csv")
    n_on = len(pd.read_csv(results / "data/corr_on_20_events.csv"))
    events = pd.read_csv(results / "data/corr_on_20_events.csv", nrows=1).iloc[0]
    tab = tabulated(tendl, BEAM)

    order_stats(draws, out)
    residual_loss(draws, tab, n_draws, out)
    budget(draws, on, n_on, tab, {"proj": events.proj_mass, "targ": events.targ_mass}, out)

    chans = channels(on, n_on)
    masses = {"proj": events.proj_mass, "targ": events.targ_mass}
    masses.update(on[(on.sp == "") & (on.A > 4) & (on.excitation == 0)].groupby("za").mass.first().to_dict())
    chans = chans[[key[0] in masses for key in chans.index]]
    out.append(f"\n## Exit channels with the flag on ({chans.sum():.4f} of the events covered)\n")
    pool, single = pools(draws), first_draws(draws)
    n_total = 400000
    full, acceptance = toy(chans, pool, single, masses, n_total)
    no_reject, _ = toy(chans, pool, single, masses, n_total, reject=False)
    no_memory, _ = toy(chans, pool, single, masses, n_total, memory=False)

    out.append("| residual | light particles | fraction | acceptance of a draw |\n|---|---|---|---|")
    for key, fraction in chans.head(12).items():
        counts = ", ".join(f"{k} {name}" for name, k in zip(LIGHT, key[1:]) if k)
        out.append(f"| {key[0]} | {counts} | {fraction:.4f} | {acceptance.get(key, float('nan')):.3f} |")

    out.append("\n## Closure and steps, mean T (MeV)\n")
    out.append("Tabulated draws -> channel multiplicities without rejection -> with rejection (the toy) -> the flag-on run.\n")
    out.append("| species | tabulated draws | channels, no rejection | toy without draw memory | toy | flag on | toy/on |\n|---|---|---|---|---|---|---|")
    for s in ("n", "p", "alpha"):
        t = draws[draws.sp == s].kinetic.mean()
        a, b, m = no_reject[s][:, 0].mean(), full[s][:, 0].mean(), no_memory[s][:, 0].mean()
        o = on[on.sp == s].kinetic.mean()
        out.append(f"| {s} | {t:.4f} | {a:.4f} | {m:.4f} | {b:.4f} | {o:.4f} | {b / o:.4f} |")

    out.append("\n## Mean T per channel with the flag on (MeV)\n")
    out.append("| residual | species | entries | mean T on | mean T of the tabulated draws |\n|---|---|---|---|---|")
    res_of = on[(on.sp == "") & (on.A > 4)].set_index("event").za
    light = on[on.sp != ""].join(res_of.rename("res"), on="event")
    for (res, s), g in light.groupby(["res", "sp"]):
        if len(g) >= 2000 and s in ("n", "p", "alpha"):
            out.append(f"| {res} | {s} | {len(g)} | {g.kinetic.mean():.3f} | {draws[draws.sp == s].kinetic.mean():.3f} |")

    fig, axes = plt.subplots(2, 3, figsize=(13, 6.5), sharex="col", gridspec_kw={"height_ratios": [3, 1]})
    for j, s in enumerate(("n", "p", "alpha")):
        edges = np.linspace(0, BEAM + 2, 45)
        tabulated_t = draws[draws.sp == s].kinetic.values
        on_t = on[on.sp == s].kinetic.values
        h_on = np.histogram(on_t, edges)[0] / len(on_t)
        for values, label, style in ((tabulated_t, "tabulated draws", "C0"), (no_reject[s][:, 0], "channels, no rejection", "C2"), (full[s][:, 0], "toy with rejection", "C3")):
            h = np.histogram(values, edges)[0] / len(values)
            axes[0][j].stairs(h, edges, color=style, label=label)
            with np.errstate(divide="ignore", invalid="ignore"):
                axes[1][j].stairs(np.where(h_on > 0, h / h_on, np.nan), edges, color=style)
        axes[0][j].stairs(h_on, edges, color="k", label="flag on")
        axes[0][j].set_yscale("log")
        axes[0][j].set_ylabel(f"{s}: fraction per bin")
        axes[1][j].set_ylim(0, 3)
        axes[1][j].axhline(1, color="grey", lw=0.8)
        axes[1][j].set_ylabel("ratio to flag on")
        axes[1][j].set_xlabel(f"{s} T (MeV)")
    axes[0][0].legend()
    fig.suptitle("alpha + 40Ar, 20 MeV, Poisson: closure of the correlated spectra")
    fig.tight_layout()
    fig.savefig(target / "closure_20MeV.pdf")
    plt.close(fig)

    scan(inv, out, target)
    (target / "investigation.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main(*sys.argv[1:5])
