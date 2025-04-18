from abc import ABC, abstractmethod
from typing import Tuple

class TextProcessor(ABC):
    @abstractmethod
    def process(self, text: str, noise_level: float) -> Tuple[str, str]:
        """Process text and return (modified_text, description)"""
        pass

class RegexTextProcessor(TextProcessor):
    def process(self, text: str, noise_level: float) -> Tuple[str, str]:
        """Replace characters using regex patterns based on noise level"""
        import re
        patterns = [
            (r'[aeiou]', '@'),  # Replace vowels
            (r'[0-9]', '#'),    # Replace numbers
            (r'[A-Z]', 'X'),    # Replace capitals
            (r'[a-z]', 'x'),    # Replace lowercase
        ]
        
        result = text
        description = []
        for pattern, repl in patterns[:int(noise_level * len(patterns))]:
            result = re.sub(pattern, repl, result)
            description.append(f"Applied {pattern} -> {repl}")
            
        return result, "\n".join(description)
