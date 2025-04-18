from typing import Optional, Type
from .processors import (
    TextProcessor, SemanticProcessor, SyntacticProcessor,
    ImageProcessor, DefaultImageProcessor
)
from ..processors.semantic import RegexSemanticProcessor, NoneSemanticProcessor
from ..processors.syntactic import KolmogorovProcessor, ShuffleProcessor, NoneSyntacticProcessor
from ..processors.image import SpeckleProcessor, PointCloudProcessor, NoneImageProcessor

class ProcessorFactory:
    _semantic_processors = {
        'REGEX': RegexSemanticProcessor,
        'NONE': NoneSemanticProcessor,
    }
    
    _syntactic_processors = {
        'KOLMOGOROV': KolmogorovProcessor,
        'SHUFFLE': ShuffleProcessor,
        'NONE': NoneSyntacticProcessor,
    }
    
    _image_processors = {
        'SPECKLE': SpeckleProcessor,
        'POINT_CLOUD': PointCloudProcessor,
        'NONE': NoneImageProcessor,
    }
    
    @classmethod
    def get_semantic_processor(cls, name: str = 'NONE') -> SemanticProcessor:
        return cls._semantic_processors.get(name.upper(), NoneSemanticProcessor)()
        
    @classmethod
    def get_syntactic_processor(cls, name: str = 'NONE') -> SyntacticProcessor:
        return cls._syntactic_processors.get(name.upper(), NoneSyntacticProcessor)()
        
    @classmethod
    def get_image_processor(cls, name: str = 'NONE') -> ImageProcessor:
        return cls._image_processors.get(name.upper(), DefaultImageProcessor)()
