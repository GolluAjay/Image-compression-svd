from flask import send_file
from PIL import Image
import numpy as np

def compress_image_svd(image, k):
    # Convert image to grayscale for SVD
    original_image = image.convert('L')
    image_matrix = np.array(original_image)
    
    # Apply SVD
    U, S, Vt = np.linalg.svd(image_matrix, full_matrices=False) 
    
    # Keep only the top-k singular values
    U_k = U[:, :k]
    S_k = np.diag(S[:k])
    Vt_k = Vt[:k, :]
    
    # Reconstruct the image using top-k components
    compressed_image_matrix = np.dot(U_k, np.dot(S_k, Vt_k))
    
    # Convert matrix to image
    compressed_image = Image.fromarray(np.clip(compressed_image_matrix, 0, 255).astype('uint8'))

    # Calculate Frobenius Norm of the approximation error
    frobenius_norm = np.linalg.norm(image_matrix - compressed_image_matrix, 'fro')
    
    return compressed_image, frobenius_norm, S.size