from typing import Dict, Type
from .base import NoiseStrategy
from .steganographic import SteganographicNoise
from .latent_space import LatentSpaceNoise
from .kolmogorov import KolmogorovNoise
from .speckle import SpeckleNoise
from .point_cloud import PointCloudNoise
from .image_replace import ImageReplaceNoise
from ..core.types import NoiseType

_strategy_map: Dict[NoiseType, Type[NoiseStrategy]] = {
    NoiseType.STEGANOGRAPHIC: SteganographicNoise,
    NoiseType.LATENT_SPACE: LatentSpaceNoise,
    NoiseType.KOLMOGOROV: KolmogorovNoise,
    NoiseType.SPECKLE: SpeckleNoise,
    NoiseType.POINT_CLOUD: PointCloudNoise,
    NoiseType.IMAGE_REPLACE: ImageReplaceNoise
}

def create_noise_strategy(noise_type: NoiseType) -> NoiseStrategy:
    """create instance of specified noise strategy"""
    strategy_class = _strategy_map.get(noise_type)
    if not strategy_class:
        raise ValueError(f"Unknown noise type: {noise_type}")
    return strategy_class()
