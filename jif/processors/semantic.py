import re
from ..core.processors import SemanticProcessor
from ..core.types import JamConfig
from ..core.text_processor import RegexTextProcessor

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
