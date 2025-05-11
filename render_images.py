import torch
import numpy as np
from torch.serialization import add_safe_globals
from nerfstudio.scripts import render as ns_render

# Allow required numpy types
add_safe_globals([np.core.multiarray.scalar, np.dtype, np.float64, np.int64])

# Patch torch.load to include weights_only=False only if not already passed
_original_load = torch.load
def safe_load(*args, **kwargs):
    kwargs.setdefault('weights_only', False)
    return _original_load(*args, **kwargs)
torch.load = safe_load

# Run renderer
ns_render.entrypoint()

