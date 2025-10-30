import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# === USER SETTINGS ===
input_file = "taxnir-QR-2-14787-3.res.dos"  # e.g., "taxnir-QR-2-14787-3.res.dos"
output_file = "figure7_phonon_dos.png"  # where to save the plot

# === LOAD PHONON FREQUENCIES ===
frequencies = []
recording = False

with open(input_file, "r") as f:
    for line in f:
        if "Phonon frequencies" in line:
            recording = True
            continue
        if recording and line.strip():
            try:
                freq = float(line.strip().split()[1])
                if freq > 10:  # remove 0 or near-zero modes
                    frequencies.append(freq)
            except:
                continue

frequencies = np.array(frequencies)

# === BANDWIDTH OPTIONS ===
std_freq = np.std(frequencies)
bandwidth_small = std_freq / 60
bandwidth_optimal = std_freq / 20
bandwidth_large = std_freq / 5

kde_small = gaussian_kde(frequencies, bw_method=bandwidth_small / frequencies.std(ddof=1))
kde_opt = gaussian_kde(frequencies, bw_method=bandwidth_optimal / frequencies.std(ddof=1))
kde_large = gaussian_kde(frequencies, bw_method=bandwidth_large / frequencies.std(ddof=1))

x_vals = np.linspace(0, max(frequencies) + 10, 1000)

# === PLOT ===
plt.figure(figsize=(10, 6))
plt.plot(x_vals, kde_small(x_vals), label='Small bandwidth (Overfit)', linestyle='--', color='orange')
plt.plot(x_vals, kde_opt(x_vals), label='Optimal bandwidth (std/20)', color='red', linewidth=2)
plt.plot(x_vals, kde_large(x_vals), label='Large bandwidth (Over-smoothed)', linestyle=':', color='green')

plt.xlabel("Phonon Frequency (cm$^{-1}$)")
plt.ylabel("Density")
plt.ylim(0, 0.06)  # <<< LIMIT y-axis values
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(output_file, dpi=300)
plt.show()