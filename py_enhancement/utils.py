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
