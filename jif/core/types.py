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
    # Separate noise levels for each type
    semantic_noise_level: float = 0.5
    syntactic_noise_level: float = 0.5
    image_noise_level: float = 0.5
    
    # Method selection
    semantic_method: str = "NONE"
    syntactic_method: str = "NONE"
    image_method: str = "NONE"
    
    # Legacy support properties
    @property
    def semantic_noise(self) -> bool:
        return self.semantic_noise_level > 0
        
    @property
    def syntactic_noise(self) -> float:
        return self.syntactic_noise_level

    @property
    def image_noise(self) -> float:
        return self.image_noise_level
    
    # Other settings
    distribution: str = "pink"
    point_density: float = 0.5
    use_list_format: bool = False
    extra_params: Optional[Dict[str, Any]] = None
    use_image_replace: bool = False
