import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from py_enhancement import specsub, logmmse, wiener, subspace, gmm_snr
from py_enhancement.utils import load_audio, save_audio

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


class SpeechEnhancementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Enhancement GUI")
        self.root.geometry("520x230")

        self.input_file = tk.StringVar()
        self.method_var = tk.StringVar(value="specsub")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Noisy Audio File:").pack(pady=5)
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=5, fill="x", padx=10)
        tk.Entry(input_frame, textvariable=self.input_file, width=50).pack(
            side="left", padx=5
        )
        tk.Button(input_frame, text="Browse", command=self.browse_file).pack(
            side="left"
        )

        tk.Label(self.root, text="Enhancement Method:").pack(pady=5)
        methods = ["specsub", "logmmse", "wiener", "subspace", "gmm_snr"]
        tk.OptionMenu(self.root, self.method_var, *methods).pack()

        tk.Button(self.root, text="Enhance", command=self.run_enhancement).pack(pady=15)

        self.status_label = tk.Label(self.root, text="", wraplength=500)
        self.status_label.pack()

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select noisy WAV file", filetypes=[("WAV files", "*.wav")]
        )
        if filename:
            self.input_file.set(filename)
            self.status_label.config(text="")

    def run_enhancement(self):
        infile = self.input_file.get()
        if not infile or not os.path.isfile(infile):
            messagebox.showerror("Error", "Please select a valid noisy WAV file.")
            return

        method = self.method_var.get()
        self.status_label.config(text="Processing... Please wait.")
        self.root.update()

        try:
            noisy_audio, fs = load_audio(infile)

            if method == "specsub":
                enhanced_audio = specsub.spectral_subtraction(noisy_audio, fs)
            elif method == "logmmse":
                enhanced_audio = logmmse.logmmse(noisy_audio, fs)
            elif method == "wiener":
                enhanced_audio = wiener.wiener_filter(noisy_audio, fs)
            elif method == "subspace":
                enhanced_audio = subspace.subspace_method(noisy_audio, fs)
            elif method == "gmm_snr":
                enhanced_audio = gmm_snr.gmm_snr_classifier(noisy_audio, fs)
            else:
                raise ValueError("Unknown enhancement method.")

            base_name = os.path.splitext(os.path.basename(infile))[0]
            out_path = os.path.join(RESULTS_DIR, f"{base_name}_{method}_enhanced.wav")

            save_audio(out_path, enhanced_audio, fs)

            self.status_label.config(text=f"Enhancement done! Saved to:\n{out_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Enhancement failed:\n{str(e)}")
            self.status_label.config(text="")


def main():
    root = tk.Tk()
    app = SpeechEnhancementGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
