import numpy as np


def wiener_filter(noisy_signal, fs, frame_len_ms=20, frame_shift_ms=10):
    """
    Basic Wiener filter implementation.
    """
    frame_len = int(fs * frame_len_ms / 1000)
    frame_shift = int(fs * frame_shift_ms / 1000)
    n_fft = 2 ** (frame_len - 1).bit_length()

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

    noise_mag = np.mean(mag[:5, :], axis=0)

    # Wiener gain
    gain = mag**2 / (mag**2 + noise_mag**2)
    enhanced_mag = gain * mag

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
