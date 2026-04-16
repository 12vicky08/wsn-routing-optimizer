import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import re

# ==========================================
# SECTION 1: Data Ingestion & Parsing Engine
# ==========================================

def parse_simulation_log(file_path):
    """
    Parses a complex, multi-table simulation log from NS-3.
    """
    
    simulation_data_frames = []
    summary_df = pd.DataFrame()
    
    current_algorithm = None
    capture_mode = None  # States: 'rounds', 'summary', 'best_algo', None
    
    # Regex Patterns for Context Detection
    round_header_pattern = re.compile(r"^\s*Round\s*,\s*MaxResidualEnergy")
    summary_header_pattern = re.compile(r"^\s*Algorithm\s*,\s*Rounds")
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"CRITICAL ERROR: File {file_path} not found.")
        return pd.DataFrame(), pd.DataFrame()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
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
            if summary_header_pattern.match(line):
                summary_buffer = [line]
                i += 1
                while i < len(lines):
                    next_line = lines[i].strip()
                    if not next_line or "BEST ALGORITHM" in next_line:
                        break
                    summary_buffer.append(next_line)
                    i += 1
                
                csv_io = io.StringIO("\n".join(summary_buffer))
                try:
                    summary_df = pd.read_csv(csv_io)
                except pd.errors.ParserError as e:
                    print(f"Warning: Failed to parse summary table. Error: {e}")
                
                capture_mode = None 
                continue

        # Case B: Processing Algorithm Sections (Round Data)
        if ',' not in line and not round_header_pattern.match(line):
            current_algorithm = line
            i += 1
            continue
            
        if round_header_pattern.match(line) and current_algorithm:
            table_buffer = [line] 
            i += 1
            while i < len(lines):
                data_row = lines[i].strip()
                if not data_row or (',' not in data_row and not data_row.isdigit()):
                    break
                table_buffer.append(data_row)
                i += 1
            
            csv_io = io.StringIO("\n".join(table_buffer))
            try:
                df = pd.read_csv(csv_io)
                df['Algorithm'] = current_algorithm 
                simulation_data_frames.append(df)
            except Exception as e:
                print(f"Warning: Error parsing block for {current_algorithm}: {e}")
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

def clean_and_normalize(df):
    if df.empty: return df
    
    type_map = {
        'Round': 'int32',
        'MaxResidualEnergy': 'float64',
        'PacketsDelivered': 'int32',
        'TotalEnergyConsumed': 'float64',
        'Throughput': 'float64'
    }
    
    for col, _ in type_map.items():
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df.dropna(inplace=True)
    return df

# ==========================================
# SECTION 3: Screen-Optimized Visualization
# ==========================================

def generate_visualizations(round_df, summary_df):
    """
    Produces plots sized for screen viewing (8x5 inches)
    """
    del summary_df
    if round_df.empty: return

    # --- Style Configuration (Modified for Screen) ---
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'font.family': 'sans-serif',   # Cleaner for screens
        'font.size': 10,
        'axes.titlesize': 12,
        'figure.figsize': (8, 5),      # <--- MODIFIED: Smaller size
        'figure.dpi': 100,             # <--- MODIFIED: Standard DPI
        'lines.linewidth': 2
    })
    
    unique_algos = round_df['Algorithm'].unique()
    palette = sns.color_palette("colorblind", n_colors=len(unique_algos))
    markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p']
    marker_map = {algo: markers[i % len(markers)] for i, algo in enumerate(unique_algos)}

    # Plot 1: Energy Consumption
    plt.figure()
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
    plt.tight_layout()
    plt.show()

    # Plot 2: Throughput
    plt.figure()
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
    plt.tight_layout()
    plt.show()

# ==========================================
# SECTION 4: Execution
# ==========================================

csv_file = 'wsn-optimizer-results.csv'

print("Starting Data Pipeline...")
round_data, summary_data = parse_simulation_log(csv_file)

if not round_data.empty:
    round_data = clean_and_normalize(round_data)
    generate_visualizations(round_data, summary_data)
    
    print("\n--- Summary Performance ---")
    print(summary_data.head())
else:
    print("No data found.")