#!/usr/bin/env python3
"""
Generate the four Section-6 result figures directly from
data/final_sweep/base_dutyOn.csv (and its [LOSSBREAKDOWN] lines in
run.log for the loss-outcome breakdown). No numbers are hardcoded or
copied from main.tex -- every value here is computed from the raw sweep.

Produces (into figures/):
  fig_turning_angle.pdf     -- 6.1, Table 2 (turning angle by scheme)
  fig_energy_efficiency.pdf -- 6.2, Table 3 (packets/J by scheme)
  fig_pdr_thr_delay.pdf     -- 6.3, new table (PDR / throughput / delay)
  fig_loss_breakdown.pdf    -- 6.5, Table 4 (loss breakdown by outcome)
"""
import os
import sys
import numpy as np
import pandas as pd
from scipy import stats as spstats

sys.path.insert(0, os.path.dirname(__file__))
from style import SCHEMES, setup_rcparams, bar_by_scheme, FIG_WIDTH_IN

HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, "..", "data", "final_sweep")
FIG_DIR = os.path.join(HERE, "..", "figures")


def mean_ci95(series):
    n = len(series)
    m = series.mean()
    if n < 2:
        return m, 0.0
    sem = series.std(ddof=1) / np.sqrt(n)
    return m, sem * spstats.t.ppf(0.975, n - 1)


def per_scheme(df, values_fn):
    means, errs = [], []
    for s in SCHEMES:
        sub = df[df.scheme == s]
        m, h = mean_ci95(values_fn(sub))
        means.append(m)
        errs.append(h)
    return means, errs


def fig_turning_angle(df):
    setup_rcparams()
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(FIG_WIDTH_IN, 3.0))
    means, errs = per_scheme(df, lambda s: s["avgTurningAngleDeg"])
    bar_by_scheme(ax, SCHEMES, means, errs)
    ax.set_ylabel("Turning angle (deg)")
    ax.grid(True, axis="y", linewidth=0.4, alpha=0.4)
    fig.savefig(os.path.join(FIG_DIR, "fig_turning_angle.pdf"), format="pdf", bbox_inches="tight")
    plt.close(fig)
    print("wrote fig_turning_angle.pdf", list(zip(SCHEMES, means, errs)))


def fig_energy_efficiency(df):
    setup_rcparams()
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(FIG_WIDTH_IN, 3.0))
    means, errs = per_scheme(df, lambda s: s["packetsReceived"] / s["totalEnergyConsumedJ"])
    bar_by_scheme(ax, SCHEMES, means, errs)
    ax.set_ylabel("Packets delivered / Joule")
    ax.grid(True, axis="y", linewidth=0.4, alpha=0.4)
    fig.savefig(os.path.join(FIG_DIR, "fig_energy_efficiency.pdf"), format="pdf", bbox_inches="tight")
    plt.close(fig)
    print("wrote fig_energy_efficiency.pdf", list(zip(SCHEMES, means, errs)))


def fig_pdr_thr_delay(df):
    setup_rcparams()
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(3, 1, figsize=(FIG_WIDTH_IN, 6.6), sharex=True)
    specs = [
        ("pdrPercent", "PDR (%)"),
        ("throughputKbps", "Throughput (kbps)"),
        ("avgDelaySec", "Delay (s)"),
    ]
    results = {}
    for ax, (col, ylabel) in zip(axes, specs):
        means, errs = per_scheme(df, lambda s, c=col: s[c])
        bar_by_scheme(ax, SCHEMES, means, errs)
        ax.set_ylabel(ylabel)
        ax.grid(True, axis="y", linewidth=0.4, alpha=0.4)
        results[col] = list(zip(SCHEMES, means, errs))
    axes[0].tick_params(labelbottom=False)
    axes[1].tick_params(labelbottom=False)
    axes[2].set_xticklabels(SCHEMES, rotation=30, ha="right", fontsize=8)
    fig.savefig(os.path.join(FIG_DIR, "fig_pdr_thr_delay.pdf"), format="pdf", bbox_inches="tight")
    plt.close(fig)
    for col, rows in results.items():
        print("wrote fig_pdr_thr_delay.pdf --", col, rows)


def parse_loss_breakdown(run_log_path):
    """Sum [LOSSBREAKDOWN] fields over the 60 'ON' (duty-cycle-enabled,
    base-condition) runs that base_dutyOn.csv itself corresponds to."""
    totals = {
        "packetsReceived": 0,
        "relayGreedyDeadEndDrops": 0,
        "leafBufferOverflowDrops": 0,
        "strandedAtNeverVisitedCH": 0,
        "strandedAtVisitedCH(notYetFlushed)": 0,
    }
    mode = None
    with open(run_log_path) as f:
        for line in f:
            if line.startswith("==="):
                mode = "ON" if " ON " in line else ("OFF" if " OFF " in line else None)
                continue
            if line.startswith("[LOSSBREAKDOWN]") and mode == "ON":
                fields = dict(kv.split("=", 1) for kv in line.strip().split(" ")[1:] if "=" in kv)
                for k in totals:
                    totals[k] += int(fields[k])
    return totals


def fig_loss_breakdown(run_log_path):
    setup_rcparams()
    import matplotlib.pyplot as plt
    totals = parse_loss_breakdown(run_log_path)
    labels = [
        "Received\nat sink",
        "Greedy-fwd\ndead end",
        "Leaf buffer\noverflow",
        "Stranded,\nCH never visited",
        "Stranded,\nCH visited,\nnot flushed",
    ]
    values = [
        totals["packetsReceived"],
        totals["relayGreedyDeadEndDrops"],
        totals["leafBufferOverflowDrops"],
        totals["strandedAtNeverVisitedCH"],
        totals["strandedAtVisitedCH(notYetFlushed)"],
    ]
    fig, ax = plt.subplots(figsize=(FIG_WIDTH_IN, 3.0))
    x = range(len(labels))
    ax.bar(x, values, color="#999999",
           hatch=["//", "\\\\", "||", "xx", ".."],
           edgecolor="black", linewidth=0.6)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=7)
    ax.set_yscale("log")
    ax.set_ylabel("Relay-hop sends (count, log scale)")
    ax.grid(True, axis="y", linewidth=0.4, alpha=0.4)
    fig.savefig(os.path.join(FIG_DIR, "fig_loss_breakdown.pdf"), format="pdf", bbox_inches="tight")
    plt.close(fig)
    print("wrote fig_loss_breakdown.pdf", dict(zip(labels, values)))


def main():
    df = pd.read_csv(os.path.join(DATA_DIR, "base_dutyOn.csv"))
    fig_turning_angle(df)
    fig_energy_efficiency(df)
    fig_pdr_thr_delay(df)
    fig_loss_breakdown(os.path.join(DATA_DIR, "run.log"))


if __name__ == "__main__":
    main()
