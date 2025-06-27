import os
from py_enhancement import specsub
from py_enhancement.utils import load_audio, save_audio


NOISY_DIR = "data/noisy"
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)


def batch_process_specsub():
    for root, _, files in os.walk(NOISY_DIR):
        for file in files:
            if file.endswith(".wav"):
                noisy_path = os.path.join(root, file)
                print(f"Processing {noisy_path}...")
                noisy_audio, fs = load_audio(noisy_path)
                enhanced_audio = specsub.spectral_subtraction(noisy_audio, fs)
                base_name = os.path.splitext(file)[0]
                out_path = os.path.join(
                    RESULTS_DIR, f"{base_name}_specsub_enhanced.wav"
                )
                save_audio(out_path, enhanced_audio, fs)
                print(f"Saved enhanced file to {out_path}")


if __name__ == "__main__":
    batch_process_specsub()
