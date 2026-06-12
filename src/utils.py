import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

def normalize_rows(matrix):
    """
    Ensure rows sum to 1 to represent true probability distributions.
    Safely handles rows that sum to 0 by leaving them unchanged or
    preventing division-by-zero crashes.

    """
    row_sums = matrix.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1.0  # Prevent division by zero
    return matrix / row_sums

def derive_passive_Q(P):
    """
    Derives the optimized listener association matrix Q from the
    speaker's active matrix P using Bayesian inference mapping.

    q_ji = p_ij / sum_k(p_kj)
    Takes the transpose at the end so rows represent Perceived Sounds
    and columns represent Decoded Objects.

    """
    col_sums = P.sum(axis=0, keepdims=True)
    col_sums[col_sums == 0] = 1.0  # Prevent division by zero
    return (P / col_sums).T

def save_plot(filename, dpi=300):
    """
    saves plot to /output.
    
    """
    output_path = Path(__file__).resolve().parent.parent / "output"
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / filename
    plt.savefig(file_path, dpi=dpi, bbox_inches='tight')

    print(f"Saved {filename} to: {file_path}")
