import torch
import torch.nn.functional as F
from transformers import BertTokenizer, BertModel
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from .base import NoiseStrategy
from ..core.types import JamConfig
from ..utils.image import get_default_font, create_text_image


class LatentSpaceNoise(NoiseStrategy):
    def __init__(self):
        # Use tiny BERT for faster processing
        self.tokenizer = BertTokenizer.from_pretrained('prajjwal1/bert-tiny')
        self.model = BertModel.from_pretrained('prajjwal1/bert-tiny')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        
        # Cache vocab embeddings
        with torch.no_grad():
            self.vocab_embeddings = self.model.embeddings.word_embeddings.weight

    def _get_similar_words(self, embedding: torch.Tensor, noise_level: float, top_k: int = 10) -> str:
        """Find similar words using cosine similarity and noise-based threshold"""
        with torch.no_grad():
            # Calculate cosine similarity with all vocab words
            similarity = F.cosine_similarity(
                embedding.unsqueeze(0), 
                self.vocab_embeddings,
                dim=1
            )
            
            # Get top-k similar words
            values, indices = similarity.topk(top_k)
            
            # Scale threshold based on noise level (higher noise = lower threshold)
            threshold = 1.0 - noise_level
            valid_indices = indices[values > threshold]
            
            if len(valid_indices) == 0:
                return self.tokenizer.decode([indices[0].item()]).strip()
                
            # Randomly select from valid candidates
            chosen_idx = valid_indices[torch.randint(len(valid_indices), (1,))].item()
            return self.tokenizer.decode([chosen_idx]).strip()

    def _decode_to_text(self, embeddings: torch.Tensor, noise_level: float = 0.5) -> str:
        """Convert embeddings back to text with noise-based word selection"""
        result_tokens = []
        for emb in embeddings:
            word = self._get_similar_words(emb, noise_level)
            if word and word not in ['[PAD]', '[UNK]', '[CLS]', '[SEP]']:
                result_tokens.append(word)
        return ' '.join(result_tokens)

    def _inject_latent_noise(self, embeddings: torch.Tensor, noise_level: float) -> torch.Tensor:
        # Scale noise based on embedding norm to maintain relationships
        embedding_norms = embeddings.norm(dim=-1, keepdim=True)
        noise = torch.randn_like(embeddings) * noise_level * 0.1
        noise = noise * embedding_norms
        
        noisy_embeddings = embeddings + noise
        # Normalize to keep embeddings in similar space
        return F.normalize(noisy_embeddings, dim=-1) * embedding_norms

    def _transform_text(self, text: str, noise_level: float) -> str:
        """Transform text using latent space noise"""
        tokens = self.tokenizer(
            text, 
            return_tensors='pt',
            add_special_tokens=False
        )
        
        with torch.no_grad():
            embeddings = self.model.embeddings.word_embeddings(tokens['input_ids'].to(self.device))
            noisy_embeddings = self._inject_latent_noise(embeddings[0], noise_level)
            return self._decode_to_text(noisy_embeddings, noise_level)

    def apply(self, text: str, config: JamConfig) -> Image.Image:
        # First transform the text
        transformed_text = self._transform_text(text, config.semantic_noise_level)
        print(f"Latent transformation: {text} -> {transformed_text}")
        
        # Then create image
        return create_text_image(
            transformed_text,
            width=800, 
            height=800,
            font_size=60
        )
