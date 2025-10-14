from flask import Flask, render_template, request, jsonify
import torch
import faiss
import numpy as np
from PIL import Image
import io
import requests
import base64
import pandas as pd
import os
from transformers import CLIPProcessor, CLIPModel

app = Flask(__name__)

# Load CLIP model and processor
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Load FAISS index and metadata
index = faiss.read_index('products/index.faiss')
ids = np.load('products/ids.npy')
df = pd.read_csv('products/styles.csv')
metadata = df.set_index('id').to_dict('index')

def get_embedding(image):
    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.get_image_features(**inputs)
        emb = outputs.cpu().numpy()
        emb /= np.linalg.norm(emb)
    return emb.flatten()


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            # Get image from file or URL
            if 'file' in request.files and request.files['file'].filename:
                file = request.files['file']
                img_bytes = file.read()
                image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            elif 'url' in request.form and request.form['url']:
                url = request.form['url']
                response = requests.get(url)
                response.raise_for_status()
                image = Image.open(io.BytesIO(response.content)).convert("RGB")
            else:
                return jsonify({'error': 'No image provided'}), 400
                # Encode uploaded image for display
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            # Get embedding and search
            emb = get_embedding(image)
            k = min(10, len(ids))  # Limit to top 10 results
            distances, indices = index.search(np.array([emb]).astype('float32'), min(10, len(ids)))
            results = []
            for i, idx in enumerate(indices[0]):
                prod_id = ids[idx]
                score = distances[0][i]
                if score > 0.5:
                    prod = metadata.get(prod_id, {})
                    results.append({
                        'id': prod_id,
                        'name': prod.get('name', 'Unknown'),
                        'category': prod.get('category', 'Unknown'),
                        'score': round(score, 2),
                        'image': f'/static/images/{prod_id}.jpg'
                    })
            print(f"All matches: {[(r['name'], r['category'], r['score']) for r in results]}")  # Debug

            return render_template('index.html', uploaded_img=img_str, results=results)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


