from imblearn.over_sampling import SMOTE
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Cargar datos
file_path = 'restaurants-in-torreon.csv'
data = pd.read_csv(file_path)

# Preprocesamiento
data['combined_info'] = (
    data['description'].fillna('') + ' ' +
    data['cuisines'].fillna('') + ' ' +
    data['meal_types'].fillna('') + ' ' +
    data['top_tags'].fillna('') + ' ' +
    data['dining_options'].fillna('')
)
data['relevant'] = (data['rating'] >= 4.0).astype(int)

# Vectorización
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['combined_info'])
y = data['relevant']

# Balanceo con SMOTE ajustando n_neighbors
smote = SMOTE(random_state=42, k_neighbors=2)
X_balanced, y_balanced = smote.fit_resample(X, y)

# División de datos
X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=0.2, random_state=42)

# Entrenar modelo
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# Evaluación
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred, zero_division=1))

# Función para predecir relevancia basada en similaridad
def predict_relevance(prompt, vectorizer, model, data):
    # Transformar el prompt y los textos del dataset a vectores TF-IDF
    prompt_vector = vectorizer.transform([prompt])
    data_vectors = vectorizer.transform(data['combined_info'])
    
    # Calcular la similitud de coseno entre el prompt y los restaurantes
    similarities = cosine_similarity(prompt_vector, data_vectors).flatten()
    
    # Agregar la similitud al DataFrame
    data_copy = data.copy()
    data_copy['similarity'] = similarities
    
    # Ordenar por similitud y mostrar los primeros 5 resultados
    recommendations = data_copy.sort_values(by='similarity', ascending=False)
    return recommendations[['name', 'description', 'rating', 'reviews', 'similarity']].head(5)
# Prompts for testing
prompts = [
    "I want an affordable pizza",
    "Italian restaurants near downtown",
    "Healthy vegetarian food",
    "Burgers with good reviews"
]
# Probar cada prompt
for prompt in prompts:
    print(f"Prompt: {prompt}")
    try:
        resultado = predict_relevance(prompt, vectorizer, model, data)
        print("Recomendaciones:")
        print(resultado)
    except Exception as e:
        print(f"Error en la predicción: {e}")
    print("-" * 50)