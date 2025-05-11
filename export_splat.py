import torch
import numpy as np
from torch.serialization import add_safe_globals
from nerfstudio.scripts.exporter import entrypoint

# ✅ Allow additional NumPy types for safe deserialization
add_safe_globals([
    np.core.multiarray.scalar,
    np.dtype,
    np.float64,
    np.dtypes.Float64DType  # <- the one that caused your error
])

import sys
sys.argv = [
    "ns-export",
    "gaussian-splat",
    "--load-config", "outputs/apollo17-splating/unnamed/splatfacto/2025-05-10_121354/config.yml",
    "--output-dir", "renders/gaussian_splatting_output"
]

entrypoint()

