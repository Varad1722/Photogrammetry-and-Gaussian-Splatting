import torch
import numpy as np
from torch.serialization import add_safe_globals
from pathlib import Path

# Add all necessary numpy globals
add_safe_globals([
    np.core.multiarray.scalar,  # previously required
    np.dtype,                   # previously required
    np.float64,                 # may help with Float64DType
    np.dtypes.Float64DType      # specifically required now
])

from nerfstudio.scripts.viewer.run_viewer import RunViewer

viewer = RunViewer(load_config=Path("/home/ubuntu/gsplat-env/outputs/apollo17-splating/unnamed/splatfacto/2025-05-10_121354/config.yml"))
viewer.main()

