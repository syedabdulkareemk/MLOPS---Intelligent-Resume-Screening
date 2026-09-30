import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Union

class TextEncoder:
    """
    Semantic encoder using SentenceTransformers.
    Optimized for CPU usage and deterministic outputs.
    """
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        # all-MiniLM-L6-v2 is small, fast, and CPU-friendly
        self.model = SentenceTransformer(model_name)
    
    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Encodes a list of texts into semantic embeddings.
        Returns a numpy array of embeddings.
        """
        if isinstance(texts, str):
            texts = [texts]
        # convert_to_numpy ensures we get CPU-friendly numpy arrays
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings
