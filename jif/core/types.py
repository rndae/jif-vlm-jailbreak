from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Dict, Any

class NoiseType(Enum):
    STEGANOGRAPHIC = auto()
    LATENT_SPACE = auto()
    KOLMOGOROV = auto()
    SPECKLE = auto()
    POINT_CLOUD = auto()
    IMAGE_REPLACE = auto()  # Add this line

@dataclass
class JamConfig:
    syntactic_noise: float = 0.5
    semantic_noise: bool = True
    noise_type: NoiseType = NoiseType.STEGANOGRAPHIC
    distribution: str = "pink"
    num_trials: int = 5
    point_density: float = 0.5
    use_list_format: bool = False
    extra_params: Optional[Dict[str, Any]] = None
    
    # Add new processor configuration
    semantic_method: str = "NONE"
    syntactic_method: str = "NONE"
    image_method: str = "NONE"
    
    # For image replacement
    use_image_replace: bool = False
