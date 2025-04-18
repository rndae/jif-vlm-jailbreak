import re
import random
from ..core.processors import SyntacticProcessor
from ..core.types import JamConfig
from ..strategies.kolmogorov import KolmogorovNoise

class ShuffleProcessor(SyntacticProcessor):
    """Simple text transformer using regex and shuffling"""
    def __init__(self):
        self.symbols = list("~!#$%^&*()_+")
    
    def _shuffle_word(self, word: str, noise_level: float) -> str:
        if len(word) <= 3 or random.random() > noise_level:
            return word
            
        # Keep first and last letter, shuffle middle
        middle = list(word[1:-1])
        if random.random() < noise_level * 0.3:  # 30% chance to drop a letter
            if len(middle) > 1:
                middle.pop(random.randrange(len(middle)))
        random.shuffle(middle)
        return word[0] + ''.join(middle) + word[-1]
    
    def process(self, text: str, config: JamConfig) -> str:
        if config.syntactic_noise <= 0:
            return text
            
        words = text.split()
        result = []
        
        for word in words:
            # Replace vowels with symbols
            if random.random() < config.syntactic_noise:
                word = re.sub(r'[aeiou]', 
                            lambda _: random.choice(self.symbols), 
                            word)
            
            # Random case changes
            if random.random() < config.syntactic_noise * 0.3:
                word = ''.join(c.upper() if random.random() < 0.3 else c 
                             for c in word)
            
            # Shuffle letters maintaining readability
            word = self._shuffle_word(word, config.syntactic_noise)
            
            result.append(word)
        
        result_text = ' '.join(result)
        print(f"Syntactic processing (Shuffle): {text} -> {result_text}")
        return result_text

class KolmogorovProcessor(SyntacticProcessor):
    """Uses Kolmogorov noise for text transformation"""
    def __init__(self):
        self.kolmogorov = KolmogorovNoise()
    
    def process(self, text: str, config: JamConfig) -> str:
        if config.syntactic_noise <= 0:
            return text
        result = self.kolmogorov._transform_text(text, config.syntactic_noise)
        print(f"Syntactic processing (Kolmogorov): {text} -> {result}")
        return result

class NoneSyntacticProcessor(SyntacticProcessor):
    """Pass-through processor that makes no changes"""
    def process(self, text: str, config: JamConfig) -> str:
        return text
