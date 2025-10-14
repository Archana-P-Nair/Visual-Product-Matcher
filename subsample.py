import pandas as pd
import os
import requests
from io import BytesIO
from PIL import Image
import random

# List of CSV files for diversity
csv_files = [
    'All Electronics.csv', 'All Appliances.csv', 'Clothing.csv', 'All Books.csv',
    'All Grocery and Gourmet Foods.csv', 'Amazon Fashion.csv', 'All Home and Kitchen.csv',
    'All Sports Fitness and Outdoors.csv', 'Toys and Games.csv', 'Watches.csv'
]

data_dir = 'C:/Users/Archana Nair/OneDrive/Desktop/visual-product-matcher/pythonProject1/archive'  # Adjust path as needed
all_products = []

for file in csv_files:
    file_path = os.path.join(data_dir, file)
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            # Clean and identify image column
            df = df.dropna(subset=['name', 'main_category']).drop_duplicates(subset=['name']).head(25)
            # Try multiple possible image column names
            image_cols = ['image', 'image_link', 'img_url', 'image_url']  # Add more if needed
            img_col = next((col for col in image_cols if col in df.columns), None)
            if not img_col:
                print(f"No image column found in {file}, skipping image fetch.")
                continue

            for _, row in df.iterrows():
                all_products.append({
                    'id': len(all_products),
                    'name': row['name'],
                    'category': row['main_category'],
                    'image': row[img_col]  # Store the image URL
                })
            print(f"Loaded {len(df)} from {file} with image column {img_col}")
        except Exception as e:
            print(f"Error loading {file}: {e}")

# Limit to 300 for efficiency (min 50 required)
df = pd.DataFrame(all_products[:300])
os.makedirs('products/images', exist_ok=True)
df.to_csv('products/styles.csv', index=False)

# Fetch and save images
fetched_count = 0
for idx, row in df.iterrows():
    img_url = row['image']
    img_id = str(row['id'])
    img_path = f'products/images/{img_id}.jpg'
    if os.path.exists(img_path):
        continue
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(img_url, headers=headers, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert("RGB")
        img.save(img_path, 'JPEG', quality=85)
        fetched_count += 1
        print(f"Fetched image for {row['name'][:50]}... ({row['category']})")
    except Exception as e:
        print(f"Failed to fetch {img_url}: {e}")
        # Fallback dummy
        img = Image.new('RGB', (300, 300),
                        color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        img.save(img_path, 'JPEG')
        print(f"Used dummy for {row['name']}")

print(f"Subsampled {len(df)} diverse products with {fetched_count} images fetched.")