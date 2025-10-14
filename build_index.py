import torch
import faiss
import numpy as np
from PIL import Image
import os
import pandas as pd
from transformers import CLIPProcessor, CLIPModel

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Starting model initialization...")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
print("Model initialization completed.")

# Load the styles.csv file
df = pd.read_csv('products/styles.csv')
print(f"Loaded styles.csv with {len(df)} rows. Columns: {df.columns.tolist()}")  # Debug

embeddings = []
ids = []

# Process each row to generate embeddings
print("Starting image processing with model...")
for idx, row in df.iterrows():
    img_path = f'products/images/{row["id"]}.jpg'
    if os.path.exists(img_path):
        try:
            image = Image.open(img_path).convert("RGB")
            inputs = processor(images=image, return_tensors="pt").to(device)
            with torch.no_grad():
                outputs = model.get_image_features(**inputs)
                emb = outputs.cpu().numpy()
                emb /= np.linalg.norm(emb)  # Normalize for cosine similarity
            embeddings.append(emb.flatten())
            ids.append(row["id"])
            print(f"Processed image for ID {row['id']} - {row['name'][:30]}... ({row['category']})")
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
    else:
        print(f"Image not found: {img_path}")
print("Image processing with model completed.")

# Convert to numpy array and build FAISS index
if embeddings:
    embeddings = np.array(embeddings).astype('float32')
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # Inner product for normalized cosine
    index.add(embeddings)
    faiss.write_index(index, 'products/index.faiss')
    np.save('products/ids.npy', ids)
    print("Index built with", len(ids), "products.")
else:
    print("No embeddings generated. Check image files and styles.csv.")