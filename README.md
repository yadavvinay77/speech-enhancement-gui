# Speech Enhancement GUI

A Python-based GUI application for real-time speech enhancement using multiple noise reduction models. Includes audio playback, comparative visualization, and objective speech quality metrics.

---

## Features

- Visualize raw noisy speech and multiple enhanced outputs side-by-side using 4x2 subplots
- Play audio directly by clicking on any signal plot, highlighting the playing segment
- Compare objective metrics (e.g., SNR, segmental SNR) with bar charts and summary tables
- Support for multiple enhancement algorithms such as GMM-SNR, LogMMSE, Spectral Subtraction, Subspace, Wiener filtering
- Integrated CI/CD pipeline with GitHub Actions to automatically run tests and checks on push or pull requests

---

## Getting Started

### Prerequisites

- Python 3.9+ (recommended)
- Install dependencies:

```bash
pip install -r requirements.txt


## Features
- Spectral Subtraction
- LogMMSE (placeholder)
- Wiener Filter (placeholder)
- Subspace (placeholder)
- GUI for audio enhancement

## Usage
- Run `runner.py` for command-line enhancement
- Run `gui/main_gui.py` for GUI

## Dataset
Supports NOIZEUS dataset format with clean and noisy speech files.

## Requirements

---

## Project Structure
├── gui/                   # GUI source code
├── py_enhancement/        # Speech enhancement algorithms
├── results/               # Sample audio outputs
├── .github/               # GitHub Actions CI workflows
├── requirements.txt       # Python dependencies
├── README.md              # This file

---

## Usage
Click any waveform subplot to play the corresponding audio

The active playing segment is visually highlighted in the plot

The 7th subplot displays bar plots comparing objective metrics

The 8th subplot shows a table of the statistics for quick reference

---

## Contributing
- Feel free to fork the repository and open pull requests. Please follow the existing code style and include tests for new features.

---

## License
- MIT License — see LICENSE file for details.

---

## Contact
- # Vinaykumar Yadav — GitHub | yadavvinay77@gmail.com

---

## Acknowledgements
- Inspired by research in speech enhancement and signal processing

- Built using Python, Matplotlib, and PyQt5

- Would you like me to generate a more detailed or minimal ver