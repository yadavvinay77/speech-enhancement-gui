import numpy as np
from sklearn.mixture import GaussianMixture
from scipy.signal import stft, istft


def gmm_snr_classifier(
    noisy_signal, fs, n_components=2, frame_len_ms=20, frame_shift_ms=10
):
    """
    Simplified GMM-SNR speech enhancement.
    - Use STFT to get spectral features.
    - Fit a GMM to magnitude spectra (signal + noise).
    - Classify frames as speech/noise.
    - Apply soft mask based on posterior probabilities.
    """
    frame_len = int(fs * frame_len_ms / 1000)
    frame_shift = int(fs * frame_shift_ms / 1000)
    n_fft = 2 ** (frame_len - 1).bit_length()

    f, t, Zxx = stft(
        noisy_signal,
        fs,
        nperseg=frame_len,
        noverlap=frame_len - frame_shift,
        nfft=n_fft,
    )
    mag = np.abs(Zxx).T  # shape: (frames, freq_bins)

    # Fit GMM to magnitude spectra over all frames
    gmm = GaussianMixture(
        n_components=n_components, covariance_type="diag", max_iter=100
    )
    gmm.fit(mag)

    # Predict posterior probabilities of speech (component with higher mean power)
    means = gmm.means_.mean(axis=1)
    speech_comp = np.argmax(means)

    posteriors = gmm.predict_proba(mag)
    speech_probs = posteriors[:, speech_comp]

    # Create soft mask: emphasize frames with high speech probability
    mask = np.clip(speech_probs[:, None], 0.1, 1.0)

    enhanced_mag = mag * mask

    # Reconstruct complex spectrum with original phase
    enhanced_Zxx = (enhanced_mag.T * np.exp(1j * np.angle(Zxx))).T

    # Inverse STFT to time domain
    _, enhanced_signal = istft(
        enhanced_Zxx.T,
        fs,
        nperseg=frame_len,
        noverlap=frame_len - frame_shift,
        nfft=n_fft,
    )

    # Match original length
    enhanced_signal = enhanced_signal[: len(noisy_signal)]

    return enhanced_signal
