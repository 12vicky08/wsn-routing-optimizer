#!/usr/bin/env python3
"""
Generate all required result figures from data/wsn_raw_results.csv.
Vector PDF output into figures/, using scripts/style.py's shared styling.
"""
import os
import sys
import numpy as np
import pandas as pd
from scipy import stats as spstats

sys.path.insert(0, os.path.dirname(__file__))
from style import SCHEMES, new_figure, plot_scheme_series, finalize_and_save

HERE = os.path.dirname(__file__)
DATA_CSV = os.path.join(HERE, "..", "data", "wsn_raw_results.csv")
FIG_DIR = os.path.join(HERE, "..", "figures")


def mean_ci95(series):
    n = len(series)
    if n < 2:
        return series.mean(), 0.0
    m = series.mean()
    sem = series.std(ddof=1) / np.sqrt(n)
    h = sem * spstats.t.ppf(0.975, n - 1)
    return m, h


def agg(df, group_cols, value_col):
    """Return DataFrame indexed by group_cols with mean and ci95 columns."""
    rows = []
    for keys, sub in df.groupby(group_cols):
        m, h = mean_ci95(sub[value_col])
        if not isinstance(keys, tuple):
            keys = (keys,)
        rows.append(list(keys) + [m, h])
    cols = (group_cols if isinstance(group_cols, list) else [group_cols]) + ["mean", "ci95"]
    return pd.DataFrame(rows, columns=cols)


def plot_metric_vs_x(df, x_col, y_col, xlabel, ylabel, out_name, x_is_density=True):
    fig, ax = new_figure()
    a = agg(df, ["scheme", x_col], y_col)
    for scheme in SCHEMES:
        sub = a[a.scheme == scheme].sort_values(x_col)
        if sub.empty:
            continue
        plot_scheme_series(ax, sub[x_col], sub["mean"], scheme, yerr=sub["ci95"])
    finalize_and_save(fig, ax, xlabel, ylabel, os.path.join(FIG_DIR, out_name))
    print(f"wrote {out_name}")


def plot_lifetime_bars(df):
    fig, ax = new_figure()
    metrics = ["fndTimeSec", "hndTimeSec", "lndTimeSec"]
    labels = ["FND", "HND", "LND"]
    x = np.arange(len(SCHEMES))
    width = 0.25
    means = {m: [] for m in metrics}
    errs = {m: [] for m in metrics}
    density = df[(df.dataRateKbps == 250)]
    for scheme in SCHEMES:
        sub = density[density.scheme == scheme]
        for m in metrics:
            vals = sub[sub[m] >= 0][m]  # exclude -1 (not reached)
            mm, hh = mean_ci95(vals) if len(vals) else (0, 0)
            means[m].append(mm)
            errs[m].append(hh)
    from style import _COLORS
    for i, (m, lbl) in enumerate(zip(metrics, labels)):
        ax.bar(x + (i - 1) * width, means[m], width, yerr=errs[m], capsize=2,
               label=lbl, color=["#0072B2", "#E69F00", "#009E73"][i])
    ax.set_xticks(x)
    ax.set_xticklabels(SCHEMES, rotation=30, ha="right", fontsize=7)
    ax.set_ylabel("Time (s)")
    ax.legend(frameon=False)
    ax.grid(True, axis="y", linewidth=0.4, alpha=0.4)
    fig.savefig(os.path.join(FIG_DIR, "fig3_lifetime_fnd_hnd_lnd.pdf"), format="pdf", bbox_inches="tight")
    print("wrote fig3_lifetime_fnd_hnd_lnd.pdf")


def plot_energy_efficiency(df):
    fig, ax = new_figure()
    density = df[(df.dataRateKbps == 250)]
    rows = []
    for scheme in SCHEMES:
        sub = density[density.scheme == scheme]
        eff = sub["packetsReceived"] / sub["totalEnergyConsumedJ"].replace(0, np.nan)
        m, h = mean_ci95(eff.dropna())
        rows.append((scheme, m, h))
    schemes_, means_, errs_ = zip(*rows)
    from style import _COLORS
    colors = [_COLORS[s] for s in schemes_]
    ax.bar(range(len(schemes_)), means_, yerr=errs_, capsize=3, color=colors)
    ax.set_xticks(range(len(schemes_)))
    ax.set_xticklabels(schemes_, rotation=30, ha="right", fontsize=7)
    ax.set_ylabel("Packets delivered per Joule")
    ax.grid(True, axis="y", linewidth=0.4, alpha=0.4)
    fig.savefig(os.path.join(FIG_DIR, "fig7_energy_efficiency.pdf"), format="pdf", bbox_inches="tight")
    print("wrote fig7_energy_efficiency.pdf")


def main():
    df = pd.read_csv(DATA_CSV)
    density = df[df.dataRateKbps == 250]
    traffic = df[df.numNodes == 200]

    plot_metric_vs_x(density, "numNodes", "throughputKbps",
                      "Node density", "Throughput (kbps)", "fig1a_throughput_vs_density.pdf")
    plot_metric_vs_x(traffic, "dataRateKbps", "throughputKbps",
                      "Offered load (kbps)", "Throughput (kbps)", "fig1b_throughput_vs_load.pdf")

    plot_metric_vs_x(density, "numNodes", "pdrPercent",
                      "Node density", "Packet Delivery Ratio (%)", "fig2a_pdr_vs_density.pdf")
    plot_metric_vs_x(traffic, "dataRateKbps", "pdrPercent",
                      "Offered load (kbps)", "Packet Delivery Ratio (%)", "fig2b_pdr_vs_load.pdf")

    plot_lifetime_bars(df)

    plot_metric_vs_x(density, "numNodes", "avgDelaySec",
                      "Node density", "End-to-end delay (s)", "fig4a_delay_vs_density.pdf")
    plot_metric_vs_x(traffic, "dataRateKbps", "avgDelaySec",
                      "Offered load (kbps)", "End-to-end delay (s)", "fig4b_delay_vs_load.pdf")

    plot_metric_vs_x(density, "numNodes", "totalEnergyConsumedJ",
                      "Node density", "Cumulative energy consumed (J)", "fig5_energy_vs_density.pdf")

    plot_metric_vs_x(traffic, "dataRateKbps", "pdrPercent",
                      "Offered load (kbps)", "PDR (%) -- traffic sensitivity", "fig6_traffic_sensitivity.pdf")

    plot_energy_efficiency(df)

    # Turning angle bar (smoothness claim check)
    fig, ax = new_figure()
    ta = df.groupby("scheme")["avgTurningAngleDeg"].agg(list)
    rows = []
    for scheme in SCHEMES:
        vals = pd.Series(ta[scheme])
        m, h = mean_ci95(vals)
        rows.append((scheme, m, h))
    schemes_, means_, errs_ = zip(*rows)
    from style import _COLORS
    colors = [_COLORS[s] for s in schemes_]
    ax.bar(range(len(schemes_)), means_, yerr=errs_, capsize=3, color=colors)
    ax.set_xticks(range(len(schemes_)))
    ax.set_xticklabels(schemes_, rotation=30, ha="right", fontsize=7)
    ax.set_ylabel("Average turning angle (deg)")
    ax.grid(True, axis="y", linewidth=0.4, alpha=0.4)
    fig.savefig(os.path.join(FIG_DIR, "fig8_turning_angle.pdf"), format="pdf", bbox_inches="tight")
    print("wrote fig8_turning_angle.pdf")

    print("\nAll figures written to", FIG_DIR)


if __name__ == "__main__":
    main()
