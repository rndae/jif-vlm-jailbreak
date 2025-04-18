from PIL import Image
from typing import Optional
from .types import JamConfig
from .processor_factory import ProcessorFactory
import logging

class NoiseGenerator:
    def __init__(self, config: Optional[JamConfig] = None):
        self.config = config or JamConfig()
        
    def generate(self, text: str) -> Image.Image:
        """Generate noisy image using configured processors"""
        # Get processors
        semantic_proc = ProcessorFactory.get_semantic_processor(self.config.semantic_method)
        syntactic_proc = ProcessorFactory.get_syntactic_processor(self.config.syntactic_method)
        image_proc = ProcessorFactory.get_image_processor(self.config.image_method)
        
        # Process text through pipeline
        processed_text = text
        
        if self.config.semantic_noise:
            processed_text = semantic_proc.process(processed_text, self.config)
            logging.info(f"Applied semantic processing: {self.config.semantic_method}")
            
        if self.config.syntactic_noise > 0:
            processed_text = syntactic_proc.process(processed_text, self.config)
            logging.info(f"Applied syntactic processing: {self.config.syntactic_method}")
        
        # Generate final image
        return image_proc.process(processed_text, self.config)
