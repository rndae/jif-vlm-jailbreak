import re
import torch
from ..core.processors import SemanticProcessor
from ..core.types import JamConfig
from ..core.text_processor import RegexTextProcessor
from ..strategies.latent_space import LatentSpaceNoise

class RegexSemanticProcessor(SemanticProcessor):
    """Uses RegexTextProcessor for semantic transformations"""
    def __init__(self):
        self.text_processor = RegexTextProcessor()
    
    def process(self, text: str, config: JamConfig) -> str:
        modified_text, _ = self.text_processor.process(text, config.syntactic_noise)
        return modified_text

class NoneSemanticProcessor(SemanticProcessor):
    """Pass-through processor that makes no changes"""
    def process(self, text: str, config: JamConfig) -> str:
        return text

class LatentSpaceProcessor(SemanticProcessor):
    """Uses LatentSpace noise for semantic text transformations"""
    def __init__(self):
        self.latent_noise = LatentSpaceNoise()
    
    def process(self, text: str, config: JamConfig) -> str:
        if config.semantic_noise_level <= 0:
            return text
        # Only transform text, don't generate image yet
        transformed = self.latent_noise._transform_text(text, config.semantic_noise_level)
        print(f"Semantic processing: {text} -> {transformed}")
        return transformed
