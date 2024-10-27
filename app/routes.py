from flask import render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from flask import Blueprint
from flask_socketio import emit
from PIL import Image
import numpy as np
from io import BytesIO
from . import socketio
from .services import compress_image_svd

# Create a blueprint for routes
routes = Blueprint('routes', __name__)

k_value = 100  # Default value for k

@routes.route('/')
def home():
    return render_template('upload.html')

@socketio.on('upload_image')
def handle_image_upload(data):
    global k_value

    # Decode the received image file from bytes
    file = BytesIO(data['file'])  
    k = int(data['k']) if 'k' in data else k_value  # Use received k value or default

    # Open the image file
    image = Image.open(file)
    
    # Determine original format
    original_format = image.format  # e.g., 'JPEG', 'PNG'

    # Compress the image
    compressed_image,  Fro_Norm, size= compress_image_svd(Image.open(file), k)

    # Save the compressed image to a BytesIO object
    img_io = BytesIO()
    compressed_image.save(img_io, format=original_format)  # Use original format
    img_io.seek(0)
    
    # Emit the compressed image back as bytes
    emit('compressed_image', {'file': img_io.getvalue(), 'fro_norm' : Fro_Norm, 'range' : size})