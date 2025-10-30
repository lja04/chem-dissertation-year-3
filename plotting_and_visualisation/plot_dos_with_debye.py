import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# === EDIT THESE FILE PATHS ===
input_file = "selces-QR-19-2745-3.res.dos"     # e.g. "sallib-QR-9-5798-3.res.dos"
output_file = "selces-QR-19-2745-3-DOS-PLOT.png"       # e.g. "sallib_dos_plot.png"
# ==============================

def plot_dos_with_debye(filename, output_filename, save=True):
    # Read frequencies from the .dos file
    frequencies = []
    with open(filename, 'r') as f:
        for line in f:
            try:
                parts = line.strip().split()
                if len(parts) == 2:
                    freq = float(parts[1])
                    if freq > 0:
                        frequencies.append(freq)
            except ValueError:
                continue

    frequencies = np.array(frequencies)

    if len(frequencies) == 0:
        print("No valid frequency data found in the file.")
        return

    # Estimate the density of states using KDE
    kde = gaussian_kde(frequencies, bw_method=0.1)
    freq_range = np.linspace(0, max(frequencies) + 10, 500)
    dos_kde = kde(freq_range)

    # Generate the Debye approximation (normalized for comparison)
    omega_D = max(frequencies)
    debye_dos = 3 * (freq_range ** 2) / (omega_D ** 3)
    debye_dos[freq_range > omega_D] = 0

    # Plotting
    plt.figure(figsize=(8, 5))
    plt.plot(freq_range, dos_kde, label="Phonon DoS (KDE)", linewidth=2, color='gold')
    plt.plot(freq_range, debye_dos, label="Debye Approximation (ω²)", linestyle="--", linewidth=2, color='darkorange')
    plt.fill_between(freq_range, np.minimum(dos_kde, debye_dos), alpha=0.3, color='grey', label="Debye-filled region")
    plt.xlabel("Frequency (cm⁻¹)")
    plt.ylabel("Density of States (a.u.)")
    plt.legend()
    plt.grid()
    plt.tight_layout()

    if save:
        plt.savefig(output_filename)
        print(f"Plot saved as {output_filename}")
    else:
        plt.show()

# Run it
plot_dos_with_debye(input_file, output_file, save=True)
