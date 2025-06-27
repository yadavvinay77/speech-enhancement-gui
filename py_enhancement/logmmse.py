import numpy as np


def logmmse(noisy_signal, fs, frame_len_ms=20, frame_shift_ms=10, alpha=0.98):
    """
    Simplified LogMMSE speech enhancement.
    Note: This is a basic implementation for demonstration and may need refinement.
    """
    frame_len = int(fs * frame_len_ms / 1000)
    frame_shift = int(fs * frame_shift_ms / 1000)
<<<<<<< HEAD
    n_fft = 2 ** (frame_len - 1).bit_length()
=======
    n_fft = 2 ** ((frame_len - 1).bit_length())
>>>>>>> 1dcc848 (Initial commit - speech enhancement GUI and modules)

    def enframe(signal, frame_len, frame_shift):
        num_frames = int(np.ceil((len(signal) - frame_len) / frame_shift)) + 1
        pad_len = (num_frames - 1) * frame_shift + frame_len
        padded = np.append(signal, np.zeros(pad_len - len(signal)))
        frames = np.lib.stride_tricks.as_strided(
            padded,
            shape=(num_frames, frame_len),
            strides=(padded.strides[0] * frame_shift, padded.strides[0]),
        )
        return frames

    frames = enframe(noisy_signal, frame_len, frame_shift)
    window = np.hamming(frame_len)
    frames_win = frames * window

    spectrum = np.fft.rfft(frames_win, n=n_fft)
    mag = np.abs(spectrum)
    phase = np.angle(spectrum)

    # Noise estimate: average over first 5 frames
    noise_mag = np.mean(mag[:5, :], axis=0)

    enhanced_mag = np.zeros_like(mag)
    xi_prev = np.ones(mag.shape[1])

    for i in range(mag.shape[0]):
        gamma = (mag[i] ** 2) / (noise_mag**2)
        xi = alpha * xi_prev + (1 - alpha) * np.maximum(gamma - 1, 0)
        vk = xi * gamma / (1 + xi)
<<<<<<< HEAD
        gain = (
            xi / (1 + xi) * np.exp(0.5 * np.exp1 * np.exp(-vk))
        )  # approx. gain factor
=======
        # FIXED: replaced np.exp1 with np.e
        gain = (xi / (1 + xi)) * np.exp(0.5 * np.e * np.exp(-vk))
>>>>>>> 1dcc848 (Initial commit - speech enhancement GUI and modules)
        enhanced_mag[i] = gain * mag[i]
        xi_prev = xi

    enhanced_spectrum = enhanced_mag * np.exp(1j * phase)
    enhanced_frames = np.fft.irfft(enhanced_spectrum, n=n_fft)[:, :frame_len]

    enhanced_signal = np.zeros((frames.shape[0] - 1) * frame_shift + frame_len)
    window_sum = np.zeros_like(enhanced_signal)

    for i in range(frames.shape[0]):
        start = i * frame_shift
        enhanced_signal[start : start + frame_len] += enhanced_frames[i] * window
        window_sum[start : start + frame_len] += window**2

    nonzero = window_sum > 1e-6
    enhanced_signal[nonzero] /= window_sum[nonzero]

    return enhanced_signal[: len(noisy_signal)]
