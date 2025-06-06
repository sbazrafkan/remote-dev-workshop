# analysis/main.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

def load_data(csv_path):
    """
    Reads a CSV with columns ['time', 'value'] and returns numpy arrays.
    """
    df = pd.read_csv(csv_path)
    # Ensure sorted by time
    df = df.sort_values('time')
    return df['time'].to_numpy(), df['value'].to_numpy()

def compute_fft(time_array, value_array):
    """
    Computes the FFT of the signal.
    Returns frequencies and amplitudes.
    """
    n = len(time_array)
    # Assuming uniform sampling:
    dt = time_array[1] - time_array[0]
    yf = fft(value_array)
    xf = fftfreq(n, dt)[:n // 2]
    amplitude = 2.0 / n * np.abs(yf[0 : n // 2])
    return xf, amplitude

def plot_time_series(time_array, value_array, output_path):
    plt.figure(figsize=(8, 4))
    plt.plot(time_array, value_array, lw=1.5)
    plt.title("Time Series Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_spectrum(freq_array, amplitude_array, output_path):
    plt.figure(figsize=(8, 4))
    plt.plot(freq_array, amplitude_array, lw=1.5)
    plt.title("Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def main():
    # 1. Define paths
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    data_path = os.path.join(project_root, "data", "sample_signal.csv")
    out_dir = os.path.join(project_root, "results")
    os.makedirs(out_dir, exist_ok=True)

    # 2. Load data
    time_array, value_array = load_data(data_path)

    # 3. Compute FFT
    freq_array, amplitude_array = compute_fft(time_array, value_array)

    # 4. Save plots
    time_plot_path = os.path.join(out_dir, "time_series.png")
    spec_plot_path = os.path.join(out_dir, "spectrum.png")

    plot_time_series(time_array, value_array, time_plot_path)
    plot_spectrum(freq_array, amplitude_array, spec_plot_path)

    print(f"Plots saved to: {time_plot_path} and {spec_plot_path}")

if __name__ == "__main__":
    main()