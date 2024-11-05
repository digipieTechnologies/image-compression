import base64
from django.shortcuts import render
from .forms import ImageUploadForm
from PIL import Image
from sklearn.decomposition import PCA
import numpy as np
from io import BytesIO
from PIL import Image

def load_image(uploaded_image):
    img = Image.open(uploaded_image).convert('RGB')
    return np.array(img)


def compress_image(img_array, n_components=2):

    img_reshaped = img_array.reshape(-1, 3)
    pca = PCA(n_components=n_components)

    img_pca = pca.fit_transform(img_reshaped)

    img_reconstructed = pca.inverse_transform(img_pca)

    img_reconstructed = img_reconstructed.reshape(img_array.shape)

    img_reconstructed = np.clip(img_reconstructed, 0, 255).astype(np.uint8)
    return img_reconstructed

def img_to_base64(img_array):

    img = Image.fromarray(img_array)
    buffered = BytesIO()
    img.save(buffered, format="JPEG", quality=90)  # You can specify quality here
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def upload_and_compress_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.cleaned_data['image']

            original_img_array = load_image(uploaded_image)
            compressed_img_array = compress_image(original_img_array, n_components=2)  # Adjust n_components as needed

            original_image_base64 = img_to_base64(original_img_array)
            compressed_image_base64 = img_to_base64(compressed_img_array)

            original_size_kb = round(len(original_image_base64) * 0.75 / 1024, 2)
            compressed_size_kb = round(len(compressed_image_base64) * 0.75 / 1024, 2)

            context = {
                'form': form,
                'original_image_base64': original_image_base64,
                'compressed_image_base64': compressed_image_base64,
                'original_size_kb': original_size_kb,
                'compressed_size_kb': compressed_size_kb,
            }
            return render(request, 'upload_image.html', context)
    else:
        form = ImageUploadForm()

    return render(request, 'upload_image.html', {'form': form})
