import torch
from transformers import AutoProcessor, AutoModelForVision2Seq
from .domain import Question, Answer

class GraniteModel:
    def __init__(self):
        self.processor = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_path = "ibm-granite/granite-vision-3.2-2b"
        self.initialize_model()

    def initialize_model(self):
        self.processor = AutoProcessor.from_pretrained(self.model_path, use_fast=True)
        self.model = AutoModelForVision2Seq.from_pretrained(self.model_path).to(self.device)

    def _prepare_conversation(self, question: Question) -> list:
        conversation = [{"role": "user", "content": []}]
        
        if question.image:
            conversation[0]["content"].append(
                {"type": "image", "url": question.image}
            )
            
        conversation[0]["content"].append(
            {"type": "text", "text": question.text}
        )
        
        return conversation

    def generate_response(self, question: Question) -> Answer:
        if not self.model or not self.processor:
            self.initialize_model()

        conversation = self._prepare_conversation(question)
        
        inputs = self.processor.apply_chat_template(
            conversation,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.device)

        output = self.model.generate(**inputs, max_new_tokens=100)
        response_text = self.processor.decode(output[0], skip_special_tokens=True)

        return Answer(
            question=question,
            text=response_text,
            raw_response={"generated_text": response_text}
        )
