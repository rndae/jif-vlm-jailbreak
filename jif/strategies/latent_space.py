import torch
from transformers import BertTokenizer, BertModel
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from .base import NoiseStrategy
from ..core.types import JamConfig
from ..utils.image import get_default_font

class LatentSpaceNoise(NoiseStrategy):
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

    def _inject_latent_noise(self, embeddings: torch.Tensor, noise_level: float) -> torch.Tensor:
        noise = torch.randn_like(embeddings) * noise_level
        return embeddings + noise
    
    def _decode_to_text(self, embeddings: torch.Tensor) -> str:
        with torch.no_grad():
            similarity = torch.matmul(embeddings, self.model.embeddings.word_embeddings.weight.T)
            word_ids = torch.argmax(similarity, dim=-1)
            return ' '.join(self.tokenizer.convert_ids_to_tokens(word_ids))

    def apply(self, text: str, config: JamConfig) -> Image.Image:
        tokens = self.tokenizer(text, return_tensors='pt')
        with torch.no_grad():
            embeddings = self.model.embeddings.word_embeddings(tokens['input_ids'].to(self.device))
            noisy_embeddings = self._inject_latent_noise(embeddings, config.syntactic_noise)
            perturbed_text = self._decode_to_text(noisy_embeddings[0])

        img = Image.new('RGB', (800, 400), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), perturbed_text, font=get_default_font(), fill='black')
        
        return img
