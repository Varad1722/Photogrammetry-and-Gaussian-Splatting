import numpy as np
import torch

# Allowlist required NumPy internals
from torch.serialization import add_safe_globals
add_safe_globals([
    np.core.multiarray.scalar,
    np.dtype,
    np.float64,
    np.int64
])

# Safe override to torch.load to ensure weights_only=False if not provided
_original_load = torch.load

def patched_load(*args, **kwargs):
    if "weights_only" not in kwargs:
        kwargs["weights_only"] = False
    return _original_load(*args, **kwargs)

torch.load = patched_load

# Import AFTER patch
from nerfstudio.scripts.viewer import run_viewer

if __name__ == "__main__":
    run_viewer.entrypoint()

