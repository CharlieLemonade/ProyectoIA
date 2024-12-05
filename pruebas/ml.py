from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Cargar los datos
file_path = 'restaurants-in-torreon.csv'  # Cambia la ruta si es necesario
data = pd.read_csv(file_path)

# Procesar columnas relevantes
data['combined_info'] = (
    data['description'].fillna('') + ' ' +
    data['cuisines'].fillna('') + ' ' +
    data['meal_types'].fillna('') + ' ' +
    data['top_tags'].fillna('') + ' ' +
    data['dining_options'].fillna('')
)

# Crear la aplicación Flask
app = Flask(__name__)
#CORS(app)  # Habilitar CORS para permitir solicitudes desde otros dominios
#CORS(app, resources={r"/recommend": {"origins": "http://localhost:3000"}})
#CORS(app, resources={r"/recommend": {"origins": "*"}})
CORS(app, resources={r"/recommend": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}}, supports_credentials=True)
# Función para recomendar restaurantes
def recommend_restaurants(prompt, data, top_n=5):
    # Vectorización de texto
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(data['combined_info'])
    user_query_vector = vectorizer.transform([prompt])

    # Calcular similitudes
    similarities = cosine_similarity(user_query_vector, tfidf_matrix).flatten()
    data['similarity'] = similarities

    # Métrica combinada para priorizar restaurantes
    data['score'] = data['rating'] * np.log(data['reviews'] + 1)
    sorted_data = data.sort_values(by=['similarity', 'score'], ascending=[False, False])

    # Seleccionar los primeros top_n resultados con nombre y descripción
    recommendations = sorted_data[['name', 'description', 'rating', 'reviews', 'featured_image']].head(top_n).reset_index(drop=True)
    return recommendations


@app.route('/recommend', methods=['POST', 'OPTIONS'])
def recommend():
    if request.method == 'OPTIONS':
        # Respuesta a preflight
        return jsonify({"message": "Preflight check successful"}), 200
    
    # Tu lógica para POST aquí
    request_data = request.get_json()
    prompt = request_data.get("prompt", "")
    return jsonify({"message": f"Received prompt: {prompt}"})

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)