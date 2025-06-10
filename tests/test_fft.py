# tests/test_fft.py

import numpy as np
import pytest
from src.main import compute_fft

def generate_sine_wave(freq=5.0, sample_rate=100.0, duration=1.0):
    """
    Creates a pure sine wave at `freq` Hz sampled at `sample_rate` Hz.
    Returns (time_array, value_array).
    """
    t = np.arange(0, duration, 1.0 / sample_rate)
    y = np.sin(2 * np.pi * freq * t)
    return t, y

def test_fft_peak_at_frequency():
    freq_true = 7.0
    t, y = generate_sine_wave(freq=freq_true, sample_rate=200.0, duration=1.0)
    xf, amp = compute_fft(t, y)

    # The peak should appear at xf ≈ freq_true
    idx_peak = np.argmax(amp)
    freq_peak = xf[idx_peak]
    assert pytest.approx(freq_true, rel=1e-2) == freq_peak