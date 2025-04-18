"""jif - jammed image & figures package for text-to-image generation with controlled noise"""

from .core.generator import NoiseGenerator
from .core.types import NoiseType, JamConfig
from .strategies import *

__version__ = "0.1.0"
