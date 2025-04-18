import math
from collections import Counter

def compute_complexity(text: str) -> float:
    """compute simple complexity score based on character distribution"""
    if not text:
        return 0.0
        
    # count character frequencies
    char_counts = Counter(text.lower())
    total_chars = len(text)
    
    # calculate entropy as complexity measure
    entropy = 0
    for count in char_counts.values():
        prob = count / total_chars
        entropy -= prob * math.log2(prob)
        
    return entropy
