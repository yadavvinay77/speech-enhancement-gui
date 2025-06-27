import soundfile as sf
import numpy as np
import os


def load_audio(filepath):
    audio, fs = sf.read(filepath)
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)  # convert to mono if stereo
    return audio, fs


def save_audio(filepath, audio, fs):
    # Ensure audio is in float32 format to avoid clipping
    audio = np.clip(audio, -1.0, 1.0)
    sf.write(filepath, audio.astype(np.float32), fs)


def get_clean_filepath_from_noisy(noisy_filepath, clean_dir="data/clean"):
    filename = os.path.basename(noisy_filepath)
    sp_id = filename.split("_")[0]  # e.g., sp03 from sp03_babble_sn10.wav
    clean_filename = f"{sp_id}.wav"
    return os.path.join(clean_dir, clean_filename)
<<<<<<< HEAD
=======

def calculate_snr(clean, noisy):
    """
    Calculate Signal-to-Noise Ratio (SNR) between two signals.
    """
    noise = noisy - clean
    signal_power = np.sum(clean ** 2)
    noise_power = np.sum(noise ** 2)

    if noise_power == 0:
        return float('inf')  # No noise
    snr = 10 * np.log10(signal_power / noise_power)
    return snr

def calculate_segmental_snr(clean_signal, enhanced_signal, frame_len_ms=20, frame_shift_ms=10, fs=16000, eps=1e-10):
    """
    Calculate segmental SNR between clean_signal and enhanced_signal.
    Both signals must be same length.
    
    Params:
        clean_signal: np.array, reference clean/noisy input
        enhanced_signal: np.array, enhanced output signal
        frame_len_ms: int, frame length in ms
        frame_shift_ms: int, frame shift in ms
        fs: int, sampling frequency in Hz (default 16kHz)
        eps: small value to avoid log(0)
        
    Returns:
        segmental_snr: float, average segmental SNR in dB
    """
    # Ensure signals are same length
    min_len = min(len(clean_signal), len(enhanced_signal))
    clean_signal = clean_signal[:min_len]
    enhanced_signal = enhanced_signal[:min_len]

    frame_len = int(fs * frame_len_ms / 1000)
    frame_shift = int(fs * frame_shift_ms / 1000)

    # Number of frames
    num_frames = int(np.floor((min_len - frame_len) / frame_shift)) + 1
    seg_snrs = []

    for i in range(num_frames):
        start = i * frame_shift
        end = start + frame_len

        clean_frame = clean_signal[start:end]
        enhanced_frame = enhanced_signal[start:end]

        noise_frame = clean_frame - enhanced_frame

        # Calculate power
        clean_power = np.sum(clean_frame ** 2)
        noise_power = np.sum(noise_frame ** 2)

        if noise_power < eps:
            noise_power = eps

        # Segmental SNR for this frame in dB
        seg_snr = 10 * np.log10(clean_power / noise_power)
        # Clip to avoid extreme values
        seg_snr = np.clip(seg_snr, -10, 35)
        seg_snrs.append(seg_snr)

    # Average segmental SNR over frames
    return float(np.mean(seg_snrs))

from pesq import pesq as pesq_eval
from pesq import PesqError

def calculate_pesq(clean_signal, enhanced_signal, fs):
    """
    Calculate PESQ score between clean and enhanced signals.
    Returns PESQ score or None if error.
    """
    try:
        # pesq expects 16k or 8k Hz sample rates
        if fs not in [8000, 16000]:
            raise ValueError("PESQ only supports 8kHz or 16kHz sampling rates")

        score = pesq_eval(fs, clean_signal, enhanced_signal, 'wb')
        return score
    except (PesqError, ValueError) as e:
        print(f"PESQ calculation error: {e}")
        return None
>>>>>>> 1dcc848 (Initial commit - speech enhancement GUI and modules)
