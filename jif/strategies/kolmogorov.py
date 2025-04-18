import numpy as np
import torch
from transformers import BertTokenizer, BertModel
from PIL import Image
from .base import NoiseStrategy
from ..core.types import JamConfig
from ..utils.image import create_text_image

class KolmogorovNoise(NoiseStrategy):
    def __init__(self):
        # Use small BERT model for embeddings
        self.tokenizer = BertTokenizer.from_pretrained('prajjwal1/bert-tiny')
        self.model = BertModel.from_pretrained('prajjwal1/bert-tiny')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

    def _apply_kolmogorov_noise(self, embeddings: torch.Tensor, noise_level: float) -> torch.Tensor:
        """Apply Fokker-Planck equation with Kolmogorov noise term"""
        # Parameters for Fokker-Planck equation
        D = noise_level  # Diffusion coefficient
        drift = 0.1      # Drift coefficient
        dt = 0.01       # Time step
        
        # Generate Wiener process increment (random fluctuations)
        dW = torch.randn_like(embeddings) * np.sqrt(dt)
        
        # Fokker-Planck equation with Kolmogorov noise
        # dP/dt = -drift * ∇P + D * ∇²P + noise
        drift_term = -drift * embeddings
        diffusion_term = D * dW
        
        # Update embeddings using the stochastic differential equation
        noisy_embeddings = embeddings + drift_term * dt + diffusion_term
        
        # Normalize to prevent explosion
        noisy_embeddings = noisy_embeddings / noisy_embeddings.norm(dim=-1, keepdim=True)
        
        return noisy_embeddings

    def _get_similar_word(self, embedding: torch.Tensor) -> str:
        """Find similar word using noisy embedding"""
        with torch.no_grad():
            # Get similarity with vocabulary
            similarity = torch.matmul(
                embedding, 
                self.model.embeddings.word_embeddings.weight.T
            )
            word_idx = similarity.argmax().item()
            return self.tokenizer.convert_ids_to_tokens(word_idx)

    def _transform_text(self, text: str, noise_level: float) -> str:
        """Transform text using Kolmogorov noise process"""
        tokens = self.tokenizer(text, return_tensors='pt', add_special_tokens=False)
        with torch.no_grad():
            # Get embeddings
            embeddings = self.model.embeddings.word_embeddings(
                tokens['input_ids'].to(self.device)
            )
            
            # Apply Kolmogorov noise
            noisy_embeddings = self._apply_kolmogorov_noise(embeddings[0], noise_level)
            
            # Generate new text
            transformed_words = []
            for emb in noisy_embeddings:
                word = self._get_similar_word(emb)
                transformed_words.append(word)
            
            return ' '.join(transformed_words)

    def _generate_code(self, text: str) -> str:
        """Generate encoded version of text using Kolmogorov-like patterns"""
        return self._transform_text(text, 0.5)  # Use transform_text with fixed noise level

    def apply(self, text: str, config: JamConfig) -> Image.Image:
        # Transform text using Kolmogorov noise
        transformed_text = self._transform_text(text, config.syntactic_noise)
        
        # Show transformation for debugging
        print(f"Original text: {text}")
        print(f"Transformed text: {transformed_text}")
        
        # Add Python code representation
        code_representation = f"""
# Kolmogorov noise transformation:
text = "{text}"
noise_level = {config.syntactic_noise}
transformed = apply_kolmogorov_noise(text)  # Result: {transformed_text}
"""
        
        # Create image with both transformed text and code
        final_text = f"{transformed_text}\n\n{code_representation}"
        return create_text_image(
            final_text,
            width=800, 
            height=800,
            font_size=60
        )
