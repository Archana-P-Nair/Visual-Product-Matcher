# 🎯 Visual Product Matcher

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey?style=for-the-badge&logo=flask)
![PyTorch](https://img.shields.io/badge/PyTorch-1.9%2B-red?style=for-the-badge&logo=pytorch)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0%2B-orange?style=for-the-badge&logo=tensorflow)

**A smart deep learning system that matches query product images with similar products from a database using computer vision and similarity matching techniques.** 🚀

</div>

## 📖 Overview

🎨 **Visual Product Matcher** is an intelligent system that helps users find visually similar products by analyzing product images. It uses state-of-the-art deep learning models to extract features from images and compute similarity scores to find the best matches. Perfect for e-commerce, fashion, and retail applications! 🛍️

## ✨ Features

- **🔍 CLIP-Powered Matching** - Uses OpenAI's CLIP model for state-of-the-art image-text understanding
- **🧠 Deep Feature Extraction** - Leverages CLIP's vision transformer for robust image embeddings  
- **⚡ FAISS Integration** - High-performance similarity search using Facebook's FAISS library
- **🌐 Flask Web Interface** - User-friendly web application for image upload and URL input
- **📊 Multiple Input Methods** - Support for both file upload and image URLs
- **🛒 E-commerce Focused** - Designed for product matching with metadata support
- **📈 Scalable Indexing** - Efficient FAISS index for large product databases
- **🎯 Cosine Similarity** - Normalized embeddings for accurate similarity scoring

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### 📥 Setup Instructions

1. **Clone the repository** 📂
   ```bash
   git clone https://github.com/Archana-P-Nair/Visual_Product_Matcher.git
   cd Visual_Product_Matcherpython -m venv venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt

2. **🌐 Running the Web Application**
Start the Flask server 🚀:
 ```bash
python app.py
 ```
3. Access the application 🌍:
   
Open your browser and navigate to http://127.0.0.1:5000/

5. Using the application 🎯:

📤 Upload a query product image
🔍 The system will return the most similar products from the database
📊 View similarity scores and visual comparisons


https://github.com/user-attachments/assets/ea1dee4c-4a85-4883-8838-405b1fe246a6


