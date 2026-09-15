"""
Shared plotting style for all WSN comparative figures.

Colourblind-safe categorical palette (Okabe-Ito) + distinct markers/linestyles
per scheme, so figures stay legible in greyscale print (Springer LNCS/LNEE).
Vector PDF output sized for a single-column page (~4.5in wide).
"""
import matplotlib
import matplotlib.pyplot as plt

SCHEMES = ["IAGAPC-Enhanced", "AGAPC", "EGATS-N", "RCGA-ABC", "DGA-M", "CGAPD"]

# Okabe-Ito palette (colourblind-safe)
_COLORS = {
    "IAGAPC-Enhanced": "#0072B2",  # blue
    "AGAPC": "#E69F00",            # orange
    "EGATS-N": "#009E73",          # green
    "RCGA-ABC": "#D55E00",         # vermillion
    "DGA-M": "#CC79A7",            # pink
    "CGAPD": "#999999",            # grey
}
_MARKERS = {
    "IAGAPC-Enhanced": "o",
    "AGAPC": "s",
    "EGATS-N": "^",
    "RCGA-ABC": "D",
    "DGA-M": "v",
    "CGAPD": "<",
}
_LINESTYLES = {
    "IAGAPC-Enhanced": "-",
    "AGAPC": "--",
    "EGATS-N": "-.",
    "RCGA-ABC": ":",
    "DGA-M": (0, (3, 1, 1, 1)),
    "CGAPD": (0, (5, 1)),
}

_HATCHES = {
    "IAGAPC-Enhanced": "//",
    "AGAPC": "\\\\",
    "EGATS-N": "||",
    "RCGA-ABC": "--",
    "DGA-M": "xx",
    "CGAPD": "..",
}

FIG_WIDTH_IN = 4.5
FIG_HEIGHT_IN = 3.2


def bar_by_scheme(ax, schemes, means, errs=None, log=False):
    """Grouped single-series bar chart, one bar per scheme, greyscale-safe
    (distinct hatch per scheme, not colour alone)."""
    x = range(len(schemes))
    bars = ax.bar(
        x, means,
        yerr=errs, capsize=3,
        color=[_COLORS[s] for s in schemes],
        hatch=[_HATCHES[s] for s in schemes],
        edgecolor="black", linewidth=0.6,
    )
    ax.set_xticks(list(x))
    ax.set_xticklabels(schemes, rotation=30, ha="right", fontsize=8)
    if log:
        ax.set_yscale("log")
    return bars


def setup_rcparams():
    matplotlib.rcParams.update({
        "font.size": 9,
        "axes.labelsize": 9,
        "axes.titlesize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 7.5,
        "lines.linewidth": 1.4,
        "lines.markersize": 4.5,
        "pdf.fonttype": 42,  # embed as TrueType, not Type3 (Springer requirement-friendly)
        "ps.fonttype": 42,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.autolayout": True,
    })


def new_figure():
    setup_rcparams()
    fig, ax = plt.subplots(figsize=(FIG_WIDTH_IN, FIG_HEIGHT_IN))
    return fig, ax


def plot_scheme_series(ax, x, y, scheme, yerr=None, label=None):
    kwargs = dict(
        color=_COLORS[scheme],
        marker=_MARKERS[scheme],
        linestyle=_LINESTYLES[scheme],
        label=label or scheme,
    )
    if yerr is not None:
        ax.errorbar(x, y, yerr=yerr, capsize=2, **kwargs)
    else:
        ax.plot(x, y, **kwargs)


def finalize_and_save(fig, ax, xlabel, ylabel, out_path, legend_loc="best"):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(loc=legend_loc, frameon=False)
    ax.grid(True, linewidth=0.4, alpha=0.4)
    fig.savefig(out_path, format="pdf", bbox_inches="tight")
    plt.close(fig)
