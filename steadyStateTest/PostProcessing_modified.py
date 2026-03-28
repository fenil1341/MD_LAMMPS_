"""
LAMMPS Log File Energy Plotter
--------------------------------
Parses one or more LAMMPS log files and plots PotEng and KinEng vs Step.

Usage:
    # Single file
    python plot_lammps_energy.py lammps.log

    # Multiple files
    python plot_lammps_energy.py run1.log run2.log run3.log

    # Glob pattern (Unix/Mac/Linux)
    python plot_lammps_energy.py logs/*.log

    # Optional: save figure instead of showing it
    python plot_lammps_energy.py lammps.log --save output.png
"""

import argparse
import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np


# ──────────────────────────────────────────────
# Parsing
# ──────────────────────────────────────────────

def parse_lammps_log(filepath: Path) -> dict[str, list[float]]:
    """
    Extract thermo data from a LAMMPS log file.
    Handles multiple run blocks with different columns.
    Returns the LONGEST block found (usually the production run).
    """
    blocks = []          # list of completed blocks
    current_data = {}
    current_header = []
    inside_table = False

    with open(filepath, "r", errors="replace") as fh:
        for line in fh:
            stripped = line.strip()

            if re.match(r"^\s+Step\s+", line, re.IGNORECASE):
                # Save previous block if it had data
                if current_data and any(len(v) > 0 for v in current_data.values()):
                    blocks.append({k: np.array(v) for k, v in current_data.items()})
                # Start a new block
                current_header = stripped.split()
                current_data = {col: [] for col in current_header}
                inside_table = True
                continue

            if inside_table:
                parts = stripped.split()
                if not parts:
                    inside_table = False
                    continue
                try:
                    values = [float(p) for p in parts]
                except ValueError:
                    inside_table = False
                    continue
                if len(values) != len(current_header):
                    inside_table = False
                    continue
                for col, val in zip(current_header, values):
                    current_data[col].append(val)

    # Save the last block
    if current_data and any(len(v) > 0 for v in current_data.values()):
        blocks.append({k: np.array(v) for k, v in current_data.items()})

    if not blocks:
        return {}

    # Return the longest block (most timesteps = production run)
    return max(blocks, key=lambda b: len(next(iter(b.values()))))
# ──────────────────────────────────────────────
# Plotting
# ──────────────────────────────────────────────

STYLE = {
    # "figure.facecolor": "#0f1117",
    # "axes.facecolor": "#181c27",
    # "axes.edgecolor": "#3a3f55",
    # "axes.labelcolor": "#d0d4e8",
    "axes.grid": True,
    "grid.color": "#b1b2be97",
    # "grid.linewidth": 0.6,
    # "xtick.color": "#8890b0",
    # "ytick.color": "#8890b0",
     "text.color": "#d0d4e8",
    # "legend.facecolor": "#1e2235",
    # "legend.edgecolor": "#3a3f55",
    # "legend.labelcolor": "#d0d4e8",
    "lines.linewidth": 2,
    # "font.family": "monospace",
}

PALETTE = [
    "#56cfb2", "#f0a500", "#e05c97", "#5b8dee",
    "#a17fe0", "#f76c6c", "#4ecdc4", "#ffd166",
]


def plot_energy(
    datasets: dict[str, dict[str, np.ndarray]],
    save_path: str | None = None,
) -> None:
    """
    Plot PotEng and KinEng vs Step for all provided datasets.

    Parameters
    ----------
    datasets : {label: {column: array}}
    save_path : file path to save the figure, or None to show interactively
    """
    with plt.rc_context(STYLE):
        fig, axes = plt.subplots(
            2, 1,
            figsize=(8, 6),
            sharex=True,
            gridspec_kw={"hspace": 0.08},
        )

        ax_pot, ax_kin = axes
        

        for idx, (label, data) in enumerate(datasets.items()):
            # color = PALETTE[idx % len(PALETTE)]

            step = 0.001*data.get("Step")
            if step is None:
                print(f"[WARN] '{label}': no 'Step' column found — skipped.")
                continue

            # ── Potential Energy ──────────────────────
            pot_key = next(
                (k for k in data if k.lower() in ("poteng")),
                None,
            )   # , "pe", "e_pair"
            if pot_key is not None:
                ax_pot.plot(step, data[pot_key]/atoms, color="b", label=label, alpha=0.9 ) #color=color, , linewidth=2
                            
                            
            else:
                print(f"[WARN] '{label}': no PotEng column found.")

            # ── Kinetic Energy ────────────────────────
            kin_key = next(
                (k for k in data if k.lower() in ("kineng")),
                None,
            )   #   , "ke", "e_kin"
            if kin_key is not None:
                ax_kin.plot(step, data[kin_key]/atoms, color="r", label=label, alpha=0.9 ) # color=color, , linewidth=2
            else:
                print(f"[WARN] '{label}': no KinEng column found.")

        # ── Axes labels & formatting ──────────────────
        for ax in axes:
            ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.3g"))
            if len(datasets) > 1:
                ax.legend(fontsize=8, loc="best")
                
        
        ax_pot.set_ylabel("Potential Energy", fontsize=11)
        ax_kin.set_ylabel("Kinetic Energy", fontsize=11)
        ax_kin.set_xlabel("time (ps)", fontsize=11)
        
        ax_pot.set_ylim(-22,-23)
        # ax_kin.set_ylim(1,2)
        # ax_pot.set_ylim(min(data[pot_key])+0.1*min(data[pot_key]), max(data[pot_key])-0.1*max(data[pot_key]))
        # ax_kin.set_ylim(min(data[kin_key])+0.2*min(data[kin_key]), max(data[kin_key])-0.2*max(data[kin_key]))
        # ax_kin.set_xlim(0,max(step))

        # ax_pot.set_ylim(np.mean(data[pot_key])-0.1*np.mean(data[pot_key]), np.mean(data[pot_key])+0.1*np.mean(data[pot_key]))
        # ax_kin.set_ylim(np.mean(data[kin_key])-0.1*np.mean(data[kin_key]), np.mean(data[kin_key])+0.1*np.mean(data[kin_key]))


        # Shared title
        # if len(datasets) == 1:
        #     title = f"LAMMPS Energy — {next(iter(datasets))}"
        # else:
        #     title = f"LAMMPS Energy — {len(datasets)} runs"

        # fig.suptitle(title, fontsize=13, fontweight="bold",
        #               y=0.97) # color="#e8ecff"

        # Subtle top-left annotation
        # fig.text(0.01, 0.01, "LJ reduced units", fontsize=7,
                #  color="b", ha="left")

        # plt.tight_layout(rect=[0, 0.02, 1, 0.96])

        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches="tight")
            print(f"Figure saved → {save_path}")
        else:
            plt.show()


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Plot PotEng & KinEng from LAMMPS log files."
    )
    parser.add_argument(
        "logfiles",
        nargs="+",
        help="One or more LAMMPS log files (supports glob patterns on Unix).",
    )
    parser.add_argument(
        "--save",
        metavar="FILE",
        default=None,
        help="Save figure to FILE instead of displaying it (e.g. plot.png).",
    )
    args = parser.parse_args()

    datasets: dict[str, dict[str, np.ndarray]] = {}

    for path_str in args.logfiles:
        path = Path(path_str)
        if not path.is_file():
            print(f"[ERROR] File not found: {path}")
            sys.exit(1)

        print(f"Parsing {path} …", end=" ")
        data = parse_lammps_log(path)

        if not data:
            print("no thermo data found — skipped.")
            continue

        n = len(next(iter(data.values())))
        print(f"{n} thermo rows read.")
        datasets[path.name] = data

    if not datasets:
        print("[ERROR] No valid data found in any log file.")
        sys.exit(1)

    plot_energy(datasets, save_path=args.save)


# if __name__ == "__main__":
#     main()

if __name__ == "__main__":
    # ── Add your log file paths here ──────────────────
    atoms = 1680
    log_file_name = r"\log.lammps"
    log_files = [
        
        # r"F:\sla_hiwi\lammps_testRuns\steadyStateTest\LJTut\initial\log.lammps"
        # r"F:\sla_hiwi\lammps_testRuns\steadyStateTest\LJTut\modified\log.lammps"
        # r"F:\sla_hiwi\lammps_testRuns\steadyStateTest\LJTut\modified\log.lammps"
        # r"F:\sla_hiwi\lammps_testRuns\steadyStateTest\nanoshear_Tut\equilibrate\log.lammps"
        r"F:\sla_hiwi\lammps_testRuns\steadyStateTest\nanoshear_Tut\zeroShear\log.lammps"

    ] 

    # ── Optional: set a save path or leave as None to show interactively ──
    save_path = None  # e.g. r"C:\path\to\output\energy.png"

    # ─────────────────────────────────────────────────
    datasets = {}
    for path_str in log_files:
        path = Path(path_str)
        if not path.is_file():
            print(f"[ERROR] File not found: {path}")
            sys.exit(1)
        print(f"Parsing {path} …", end=" ")
        data = parse_lammps_log(path)
        if not data:
            print("no thermo data found — skipped.")
            continue
        n = len(next(iter(data.values())))
        print(f"{n} thermo rows read.")
        datasets[path.name] = data

    if not datasets:
        print("[ERROR] No valid data found in any log file.")
        sys.exit(1)

    plot_energy(datasets, save_path=save_path)