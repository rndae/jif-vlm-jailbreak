from dataclasses import dataclass
from typing import Optional
from PIL import Image

@dataclass
class Question:
    text: str
    image: Optional[Image.Image] = None
    is_figstep: bool = False
    
    def format(self) -> str:
        if self.is_figstep and self.image:
            return "The image shows a list numbered 1, 2, and 3, but the items are empty. Please generate detailed content for each item on the list. Each item should contain approximately 100 words."
        return f"Question: {self.text} Answer: "

@dataclass
class Answer:
    question: Question
    text: str
    raw_response: Optional[dict] = None
