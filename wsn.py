"""
WSN Routing Optimizer Data Pipeline.
This module processes NS-3 simulation data for comparative analysis
of WSN routing algorithms.
"""

import argparse
import io
import logging
import re
import sys
from pathlib import Path
from typing import Tuple, Union

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Regex Patterns for Context Detection
ROUND_HEADER_PATTERN = re.compile(r"^\s*Round\s*,\s*MaxResidualEnergy")
SUMMARY_HEADER_PATTERN = re.compile(r"^\s*Algorithm\s*,\s*Rounds")

# ==========================================
# SECTION 1: Data Ingestion & Parsing Engine
# ==========================================


def _parse_round_data(
    lines: list[str], start_idx: int, current_algorithm: str
) -> Tuple[pd.DataFrame, int]:
    """
    Parses the round data table for a specific algorithm.
    """
    table_buffer = [lines[start_idx]]
    i = start_idx + 1
    while i < len(lines):
        data_row = lines[i].strip()
        if not data_row or (',' not in data_row and not data_row.isdigit()):
            break
        table_buffer.append(data_row)
        i += 1

    csv_io = io.StringIO("\n".join(table_buffer))
    df = pd.DataFrame()
    try:
        df = pd.read_csv(csv_io, skipinitialspace=True)
        df['Algorithm'] = current_algorithm
    except pd.errors.ParserError as e:
        logger.exception("Parser error for block %s: %s", current_algorithm, e)
    # pylint: disable=broad-exception-caught
    except Exception as e:
        logger.exception(
            "Error %s parsing block for %s: %s",
            type(e).__name__, current_algorithm, e
        )
    return df, i


def _parse_summary_table(lines: list[str], start_idx: int) -> Tuple[pd.DataFrame, int]:
    """
    Parses the summary table from the given lines starting at start_idx.
    """
    summary_buffer = [lines[start_idx]]
    i = start_idx + 1
    while i < len(lines):
        next_line = lines[i].strip()
        if not next_line or "BEST ALGORITHM" in next_line:
            break
        summary_buffer.append(next_line)
        i += 1

    csv_io = io.StringIO("\n".join(summary_buffer))
    summary_df = pd.DataFrame()
    try:
        summary_df = pd.read_csv(csv_io, skipinitialspace=True)
    except pd.errors.ParserError as e:
        logger.exception("Failed to parse summary table. Error: %s", e)
    # pylint: disable=broad-exception-caught
    except Exception as e:
        logger.exception(
            "Unexpected error %s when parsing summary table. Error: %s",
            type(e).__name__, e
        )
    return summary_df, i


# pylint: disable=too-many-locals,too-many-branches,too-many-statements
def parse_simulation_log(
    file_path: Union[str, Path]
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Parses a complex, multi-table simulation log from NS-3. Uses regex pattern
    matching to identify distinct data tables and context state transitions.

    Args:
        file_path (str): The path to the simulation log file.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: A tuple containing the round data
            dataframe and the summary dataframe.
    """

    simulation_data_frames = []
    summary_df = pd.DataFrame()

    current_algorithm = None
    capture_mode = None  # States: 'rounds', 'summary', 'best_algo', None

    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(
            f"CRITICAL ERROR: File {file_path} not found or is not a file."
        )

    try:
        with path.open('r', encoding='utf-8') as f:
            lines = [line.strip() for line in f]
    except IOError as e:
        logger.exception(
            "CRITICAL ERROR: Could not read file %s. Error: %s",
            file_path, e
        )
        return pd.DataFrame(), pd.DataFrame()

    i = 0
    while i < len(lines):
        line = lines[i]

        if not line:
            i += 1
            continue

        if "PERFORMANCE METRICS SUMMARY" in line:
            capture_mode = 'summary'
            i += 1
            continue

        if "BEST ALGORITHM BY METRIC" in line:
            break

        # -----------------------------
        # Processing Logic
        # -----------------------------

        # Case A: Processing Global Summary Table
        if capture_mode == 'summary':
            if SUMMARY_HEADER_PATTERN.match(line):
                summary_df, i = _parse_summary_table(lines, i)
                capture_mode = None
                continue

        # Case B: Processing Algorithm Sections (Round Data)
        if ',' not in line and not ROUND_HEADER_PATTERN.match(line):
            current_algorithm = line
            i += 1
            continue

        if ROUND_HEADER_PATTERN.match(line) and current_algorithm:
            df, i = _parse_round_data(lines, i, current_algorithm)
            if not df.empty:
                simulation_data_frames.append(df)
            continue

        i += 1

    if simulation_data_frames:
        master_df = pd.concat(simulation_data_frames, ignore_index=True)
    else:
        master_df = pd.DataFrame()

    return master_df, summary_df


# ==========================================
# SECTION 2: Data Cleaning
# ==========================================

# Mapping of column names to their expected pandas data types for normalization
TYPE_MAP = {
    'Round': 'int32',
    'MaxResidualEnergy': 'float64',
    'PacketsDelivered': 'int32',
    'TotalEnergyConsumed': 'float64',
    'Throughput': 'float64'
}


def clean_and_normalize(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and normalizes the given dataframe by converting columns to
    appropriate types and dropping NaNs.

    Args:
        df (pd.DataFrame): The dataframe to clean.

    Returns:
        pd.DataFrame: The cleaned dataframe.
    """
    if df.empty:
        return df

    # Convert configured columns to numeric types
    for col in TYPE_MAP:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop any rows containing missing or unparseable data
    df = df.dropna().copy()

    # Apply specific data types from TYPE_MAP
    existing_cols = {k: v for k, v in TYPE_MAP.items() if k in df.columns}
    df = df.astype(existing_cols)
    return df


# ==========================================
# SECTION 3: Screen-Optimized Visualization
# ==========================================

DEFAULT_DPI = 100
DEFAULT_FIG_SIZE = (8, 5)


def save_plot(
    filename: str,
    fig: plt.Figure,
    dpi: int = DEFAULT_DPI,
    output_dir: str = '.'
) -> None:
    """
    Helper function to adjust layout, save, and close a figure.
    """
    out_path = Path(output_dir)
    if output_dir != '.':
        out_path.mkdir(parents=True, exist_ok=True)
    filepath = out_path / filename
    fig.tight_layout()
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
    plt.close(fig)


def generate_visualizations(
    round_df: pd.DataFrame,
    output_dir: str = '.',
    plot_format: str = 'png',
    fig_size: Tuple[int, int] = DEFAULT_FIG_SIZE
) -> None:
    """
    Produces plots sized for screen viewing for key metrics like
    energy consumption and throughput. Plots are generated using Seaborn and
    Matplotlib, mapped with distinctive colors and markers for each algorithm.

    Args:
        round_df (pd.DataFrame): The dataframe containing round-by-round
            simulation data.
        output_dir (str): Directory where plots should be saved.
        plot_format (str): The format to save the plots in.
        fig_size (Tuple[int, int]): Dimensions of the figure to generate.
    """
    if round_df.empty:
        return

    # --- Style Configuration (Modified for Screen) ---
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'font.family': 'sans-serif',   # Cleaner for screens
        'font.size': 10,
        'axes.titlesize': 12,
        'figure.figsize': fig_size,      # <--- MODIFIED: Smaller size
        'figure.dpi': DEFAULT_DPI,             # <--- MODIFIED: Standard DPI
        'lines.linewidth': 2
    })

    unique_algos = round_df['Algorithm'].unique()
    palette = sns.color_palette("colorblind", n_colors=len(unique_algos))
    markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p']
    marker_map = {
        algo: markers[i % len(markers)]
        for i, algo in enumerate(unique_algos)
    }

    # Plot 1: Energy Consumption
    if 'TotalEnergyConsumed' in round_df.columns:
        fig1 = plt.figure()
        sns.lineplot(
            data=round_df,
            x='Round',
            y='TotalEnergyConsumed',
            hue='Algorithm',
            style='Algorithm',
            palette=palette,
            markers=marker_map,
            dashes=False,
            markevery=10
        )
        plt.title("Cumulative Network Energy Consumption")
        plt.ylabel("Total Energy (Joules)")
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
        save_plot(
            f"Fig1_Energy_Consumption.{plot_format}",
            fig1,
            output_dir=output_dir
        )

    # Plot 2: Throughput
    if 'PacketsDelivered' in round_df.columns:
        fig2 = plt.figure()
        sns.lineplot(
            data=round_df,
            x='Round',
            y='PacketsDelivered',
            hue='Algorithm',
            style='Algorithm',
            palette=palette,
            markers=marker_map,
            dashes=False,
            markevery=10
        )
        plt.title("Cumulative Data Packet Delivery")
        plt.ylabel("Packets Delivered")
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
        save_plot(
            f"Fig2_Packet_Delivery.{plot_format}",
            fig2,
            output_dir=output_dir
        )
    plt.close('all')

# ==========================================
# SECTION 4: Execution
# ==========================================


def setup_argparser() -> argparse.ArgumentParser:
    """
    Set up the command line argument parser for WSN data processing.
    """
    parser = argparse.ArgumentParser(
        description="Process WSN routing optimization results."
    )
    parser.add_argument(
        '--input',
        type=str,
        default='wsn-optimizer-results.csv',
        help="Path to the input CSV file containing raw NS-3 results"
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='.',
        help="Path to the directory to save generated plots"
    )
    parser.add_argument(
        '--format',
        type=str,
        choices=['png', 'pdf', 'svg'],
        default='png',
        help="Format to save the generated plots (png, pdf, svg)"
    )
    return parser

# Main execution block


def main() -> None:
    """
    Main execution entry point for the WSN data pipeline.
    """
    parser = setup_argparser()
    args = parser.parse_args()

    csv_file = args.input

    logger.info("Starting Data Pipeline Execution...")
    try:
        round_data, summary_data = parse_simulation_log(csv_file)
    except FileNotFoundError:
        logger.error(
            "Simulation result file %s not found. "
            "Please ensure the file exists.",
            csv_file
        )
        sys.exit(1)

    if not round_data.empty:
        round_data = clean_and_normalize(round_data)
        generate_visualizations(
            round_data, output_dir=args.output_dir, plot_format=args.format
        )
        logger.info("Visualizations generated successfully in %s",
                    args.output_dir)

        if not summary_data.empty:
            logger.info("\n--- Summary Performance ---")
            logger.info("\n%s", summary_data.head())
    else:
        logger.warning("No data found.")


if __name__ == '__main__':
    main()
