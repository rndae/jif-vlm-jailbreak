import torch
from transformers import pipeline
from .domain import Question, Answer

class FalconModel:
    def __init__(self):
        self.pipe = None
        self.initialize_model()

    def initialize_model(self):
        self.pipe = pipeline(
            "text-generation",
            model="tiiuae/Falcon3-7B-Base",
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        
    def _process_image_input(self, question: Question) -> str:
        # Here you would implement image processing logic
        # For now returning the text prompt
        return question.format()

    def generate_response(self, question: Question) -> Answer:
        if not self.pipe:
            self.initialize_model()
            
        prompt = self._process_image_input(question) if question.image else question.format()
        response = self.pipe(prompt)
        
        return Answer(
            question=question,
            text=response[0]['generated_text'].split("Answer: ")[-1].strip(),
            raw_response=response[0]
        )