import numpy as np
from scipy.linalg import eigh


def subspace_method(
    noisy_signal, fs, frame_len_ms=20, frame_shift_ms=10, noise_eigen_thresh=0.9
):
    """
    Simplified Subspace method for speech enhancement.
    Assumes noise subspace eigenvalues are smaller and signal subspace eigenvalues larger.
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

    enhanced_signal = np.zeros(len(noisy_signal) + frame_len)
    window_sum = np.zeros(len(noisy_signal) + frame_len)

    for i, frame in enumerate(frames_win):
<<<<<<< HEAD
        # Estimate covariance matrix
        R = np.cov(frame)

        # Eigen decomposition
        eigvals, eigvecs = eigh(R)

        # Sort eigenvalues descending
=======
        # FIXED: Use outer product instead of np.cov to get square matrix
        R = np.outer(frame, frame)

        eigvals, eigvecs = eigh(R)
>>>>>>> 1dcc848 (Initial commit - speech enhancement GUI and modules)
        idx = eigvals.argsort()[::-1]
        eigvals = eigvals[idx]
        eigvecs = eigvecs[:, idx]

<<<<<<< HEAD
        # Determine signal/noise subspace cutoff index
=======
>>>>>>> 1dcc848 (Initial commit - speech enhancement GUI and modules)
        total_energy = np.sum(eigvals)
        energy_sum = 0
        k = 0
        for val in eigvals:
            energy_sum += val
            k += 1
            if energy_sum / total_energy >= noise_eigen_thresh:
                break

<<<<<<< HEAD
        # Construct signal subspace projection matrix
        Us = eigvecs[:, :k]
        Ps = Us @ Us.T

        # Project noisy frame onto signal subspace
=======
        Us = eigvecs[:, :k]
        Ps = Us @ Us.T

>>>>>>> 1dcc848 (Initial commit - speech enhancement GUI and modules)
        enhanced_frame = Ps @ frame

        start = i * frame_shift
        enhanced_signal[start : start + frame_len] += enhanced_frame * window
        window_sum[start : start + frame_len] += window**2

<<<<<<< HEAD
    # Normalize
=======
>>>>>>> 1dcc848 (Initial commit - speech enhancement GUI and modules)
    nonzero = window_sum > 1e-6
    enhanced_signal[nonzero] /= window_sum[nonzero]

    return enhanced_signal[: len(noisy_signal)]
