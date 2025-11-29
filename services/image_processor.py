"""Serviço de processamento de imagem."""
from dataclasses import dataclass
from io import BytesIO
from typing import Optional

from PIL import Image
from transformers import Pipeline


@dataclass
class ImageResult:
    """Resultado da análise de imagem."""
    original_image: Image.Image
    processed_image: Image.Image
    emotion: str
    confidence: float
    filename: str


def preprocess_grayscale(image: Image.Image) -> Image.Image:
    """
    Converte imagem para escala de cinza (mantendo 3 canais RGB).
    
    Isso ajuda o modelo a focar nas características faciais,
    removendo informação de cor que pode ser ruído.
    """
    return image.convert('L').convert('RGB')


def analyze_facial_emotion(
    pipe: Pipeline,
    image_bytes: bytes,
    filename: str,
    use_grayscale: bool = False
) -> ImageResult:
    """
    Analisa emoções faciais em uma imagem.
    
    Args:
        pipe: Pipeline de classificação facial.
        image_bytes: Bytes da imagem.
        filename: Nome do arquivo.
        use_grayscale: Se deve aplicar pré-processamento grayscale.
    
    Returns:
        ImageResult com os dados da análise.
    """
    image = Image.open(BytesIO(image_bytes))
    processed = preprocess_grayscale(image) if use_grayscale else image
    
    result = pipe(processed)[0]
    
    return ImageResult(
        original_image=image,
        processed_image=processed,
        emotion=result['label'],
        confidence=result['score'] * 100,
        filename=filename
    )