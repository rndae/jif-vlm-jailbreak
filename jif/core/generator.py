from PIL import Image
from typing import List, Optional, Tuple
from .types import JamConfig, NoiseType
from ..strategies.base import NoiseStrategy
from ..strategies.factory import create_noise_strategy
from ..utils.text import compute_complexity
import logging

class NoiseGenerator:
    def __init__(self, config: Optional[JamConfig] = None):
        self.config = config or JamConfig()
        self._strategy = create_noise_strategy(self.config.noise_type)
        
    def _process_text(self, text: str) -> Tuple[str, str]:
        """Apply text-level transformations first"""
        description = []
        
        # Apply semantic noise if enabled
        if self.config.semantic_noise:
            entropy = compute_complexity(text)
            description.append(f"Text complexity score: {entropy:.2f}")
            
            # Add semantic transformations here if needed
            
        description = "\n".join(description)
        return text, description

    def generate(self, text: str) -> Image.Image:
        """Generate noisy image with text preprocessing"""
        # Process text first
        processed_text, desc = self._process_text(text)
        if desc:
            logging.info(f"Text processing:\n{desc}")
            
        # Apply visual noise strategy
        return self._strategy.apply(processed_text, self.config)
    
    def best_trial(self, text: str, num_trials: int = 5) -> List[Image.Image]:
        """generate multiple variations using different strategies"""
        results = []
        strategies = [
            create_noise_strategy(noise_type) 
            for noise_type in NoiseType
        ]
        
        for strategy in strategies[:num_trials]:
            try:
                result = strategy.apply(text, self.config)
                results.append(result)
            except Exception:
                continue
                
        return results
