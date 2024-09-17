# utils.py

import tensorflow as tf
import numpy as np
from PIL import Image
import io
import base64

def tensor_to_data_uri(tensor, format="PNG"):
    if not tf.executing_eagerly():
        raise RuntimeError("TensorFlow is not in eager execution mode.")

    img_array = tensor.numpy()

    if img_array.ndim == 3:
        pass  # Image is already in the correct shape
    elif img_array.ndim == 4:
        img_array = img_array[0]  # Remove batch dimension
    else:
        raise ValueError(f"Unsupported tensor shape: {img_array.shape}")

    if img_array.dtype != np.uint8:
        img_array = (img_array * 255).astype(np.uint8)

    img = Image.fromarray(img_array)
    buffer = io.BytesIO()
    img.save(buffer, format=format)
    img_bytes = buffer.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    data_uri = f"data:image/{format.lower()};base64,{img_base64}"
    return data_uri
