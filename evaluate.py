import numpy as np
import soundfile as sf
import os


def snr(clean, enhanced):
    noise = clean - enhanced
    snr_value = 10 * np.log10(np.sum(clean**2) / np.sum(noise**2))
    return snr_value


def evaluate_file(clean_file, enhanced_file):
    clean, fs1 = sf.read(clean_file)
    enhanced, fs2 = sf.read(enhanced_file)
    assert fs1 == fs2, "Sampling rates do not match."

    min_len = min(len(clean), len(enhanced))
    clean = clean[:min_len]
    enhanced = enhanced[:min_len]

    snr_val = snr(clean, enhanced)

    return {
        "SNR": snr_val,
        # You can add PESQ, STOI, or other metrics if you have implementations
    }


def batch_evaluate(clean_dir, enhanced_dir):
    results = {}
    for filename in os.listdir(enhanced_dir):
        if filename.endswith(".wav"):
            enhanced_file = os.path.join(enhanced_dir, filename)
            sp_id = filename.split("_")[0] + ".wav"
            clean_file = os.path.join(clean_dir, sp_id)

            if os.path.isfile(clean_file):
                results[filename] = evaluate_file(clean_file, enhanced_file)
    return results
