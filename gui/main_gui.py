<<<<<<< HEAD
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
=======
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sounddevice as sd
import threading
import time
>>>>>>> 1dcc848 (Initial commit - speech enhancement GUI and modules)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from py_enhancement import specsub, logmmse, wiener, subspace, gmm_snr
<<<<<<< HEAD
from py_enhancement.utils import load_audio, save_audio
=======
from py_enhancement.utils import load_audio, save_audio, calculate_snr
>>>>>>> 1dcc848 (Initial commit - speech enhancement GUI and modules)

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


<<<<<<< HEAD
class SpeechEnhancementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Enhancement GUI")
        self.root.geometry("520x230")
=======
class SpeechEnhancementDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Enhancement Dashboard")
        self.root.geometry("1280x720")
>>>>>>> 1dcc848 (Initial commit - speech enhancement GUI and modules)

        self.input_file = tk.StringVar()
        self.method_var = tk.StringVar(value="specsub")

<<<<<<< HEAD
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
=======
        self.noisy_audio = None
        self.fs = None
        self.enhanced_outputs = {}

        self.playing_audio = False
        self.playback_line = None
        self.playback_thread = None
        self.current_playback_ax = None
        self.current_audio = None

        self.build_gui()

    def build_gui(self):
        # File selection
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(top_frame, text="Noisy Audio File:").pack(side="left")
        tk.Entry(top_frame, textvariable=self.input_file, width=80).pack(side="left", padx=5)
        tk.Button(top_frame, text="Browse", command=self.browse_file).pack(side="left")

        # Method selector & control
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(control_frame, text="Method:").pack(side="left")
        methods = ["specsub", "logmmse", "wiener", "subspace", "gmm_snr"]
        tk.OptionMenu(control_frame, self.method_var, *methods).pack(side="left", padx=5)

        tk.Button(control_frame, text="Enhance & Compare", command=self.process_all_models).pack(side="left", padx=5)
        tk.Button(control_frame, text="Play Noisy", command=self.play_noisy).pack(side="left", padx=5)
        tk.Button(control_frame, text="Exit", command=self.root.quit).pack(side="right", padx=5)

        self.status_label = tk.Label(self.root, text="", wraplength=1200)
        self.status_label.pack()

        # Create matplotlib figure with 4x2 subplots
        self.fig, self.axes = plt.subplots(4, 2, figsize=(14, 12))
        self.fig.tight_layout(pad=3)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Connect pick events for clicking plots
        for ax_row in self.axes:
            for ax in ax_row:
                ax.set_picker(True)
        self.canvas.mpl_connect("pick_event", self.on_plot_click)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path:
            self.input_file.set(file_path)
            self.noisy_audio, self.fs = load_audio(file_path)
            self.enhanced_outputs = {}
            self.status_label.config(text="File loaded. Ready to enhance.")
            self.update_plots()

    def play_audio(self, audio, ax=None):
        if audio is not None and self.fs is not None:
            # Stop existing playback & thread
            sd.stop()
            self.playing_audio = False
            if self.playback_thread and self.playback_thread.is_alive():
                self.playback_thread.join()

            self.playing_audio = True
            self.current_audio = audio
            self.current_playback_ax = ax

            # Start audio playback
            sd.play(audio, self.fs)

            # Start playback line update thread if axis is provided
            if ax is not None:
                audio_length_sec = len(audio) / self.fs
                self.playback_thread = threading.Thread(
                    target=self.update_playback_line, args=(ax, audio_length_sec), daemon=True
                )
                self.playback_thread.start()

    def update_playback_line(self, ax, audio_length):
        start_time = time.time()
        while self.playing_audio:
            elapsed = time.time() - start_time
            if elapsed > audio_length:
                break
            pos = int(elapsed * self.fs)

            # Remove old line
            if self.playback_line is not None:
                self.playback_line.remove()

            # Draw vertical red line at current playback position
            self.playback_line = ax.axvline(x=pos, color='r')

            self.canvas.draw_idle()
            time.sleep(0.05)

        # Clean up line after playback ends
        if self.playback_line is not None:
            self.playback_line.remove()
            self.playback_line = None
            self.canvas.draw_idle()

        self.playing_audio = False
        self.current_playback_ax = None
        self.current_audio = None

    def play_noisy(self):
        self.play_audio(self.noisy_audio, self.axes[0, 0])

    def on_plot_click(self, event):
        ax = event.artist.axes
        title = ax.get_title()

        if "Noisy" in title:
            self.play_audio(self.noisy_audio, ax)
        else:
            for method in self.enhanced_outputs:
                if method in title:
                    self.play_audio(self.enhanced_outputs[method], ax)
                    break

    def process_all_models(self):
        infile = self.input_file.get()
        if not infile or not os.path.isfile(infile):
            messagebox.showerror("Error", "Please select a valid WAV file.")
            return

        methods = {
            "specsub": specsub.spectral_subtraction,
            "logmmse": logmmse.logmmse,
            "wiener": wiener.wiener_filter,
            "subspace": subspace.subspace_method,
            "gmm_snr": gmm_snr.gmm_snr_classifier,
        }

        if self.noisy_audio is None:
            self.noisy_audio, self.fs = load_audio(infile)

        self.enhanced_outputs = {}

        try:
            for name, func in methods.items():
                out = func(self.noisy_audio, self.fs)
                self.enhanced_outputs[name] = out

                out_path = os.path.join(RESULTS_DIR, f"{os.path.basename(infile).split('.')[0]}_{name}.wav")
                save_audio(out_path, out, self.fs)

            self.status_label.config(text="Enhancement completed for all models.")
            self.update_plots()
        except Exception as e:
            messagebox.showerror("Error", f"Enhancement failed:\n{str(e)}")

    def update_plots(self):
        # Clear all axes
        for ax_row in self.axes:
            for ax in ax_row:
                ax.cla()
                ax.set_xticks([])
                ax.set_yticks([])

        if self.noisy_audio is not None:
            # Plot Noisy signal (subplot 1)
            self.axes[0, 0].set_title("Noisy Signal")
            self.axes[0, 0].plot(self.noisy_audio, color='blue')

            # Plot selected enhanced signal (subplot 2)
            selected = self.method_var.get()
            self.axes[0, 1].set_title(f"Enhanced Signal: {selected}")
            if selected in self.enhanced_outputs:
                self.axes[0, 1].plot(self.enhanced_outputs[selected], color='green')

            # Plot remaining enhanced signals (subplots 3 to 6)
            idx = 0
            for name, sig in self.enhanced_outputs.items():
                if name != selected:
                    r = 1 + idx // 2
                    c = idx % 2
                    self.axes[r, c].set_title(f"Enhanced: {name}")
                    self.axes[r, c].plot(sig, color='orange')
                    idx += 1

            # Plot SNR bar chart (subplot 7)
            self.axes[3, 0].set_title("SNR Comparison (dB)")
            snrs = {
                name: calculate_snr(self.noisy_audio, enhanced)
                for name, enhanced in self.enhanced_outputs.items()
            }
            names = list(snrs.keys())
            scores = list(snrs.values())
            self.axes[3, 0].bar(names, scores, color='purple')
            self.axes[3, 0].set_ylim([min(0, min(scores) - 5), max(scores) + 5])

            # Plot stats table (subplot 8)
            self.axes[3, 1].set_title("Performance Metrics")
            self.axes[3, 1].axis('off')
            cell_text = []
            rows = []
            for name in names:
                row = [f"{snrs[name]:.2f}"]
                cell_text.append(row)
                rows.append(name)

            self.axes[3, 1].table(
                cellText=cell_text,
                rowLabels=rows,
                colLabels=["SNR (dB)"],
                loc='center',
                cellLoc='center'
            )

        self.canvas.draw()
>>>>>>> 1dcc848 (Initial commit - speech enhancement GUI and modules)


def main():
    root = tk.Tk()
<<<<<<< HEAD
    app = SpeechEnhancementGUI(root)
=======
    app = SpeechEnhancementDashboard(root)
>>>>>>> 1dcc848 (Initial commit - speech enhancement GUI and modules)
    root.mainloop()


if __name__ == "__main__":
    main()
