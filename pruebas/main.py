import spacy

nlp = spacy.load("es_core_news_sm")
texto = "Hola, ¿cómo estás? Este es un ejemplo sencillo de NLP en Python."
doc = nlp(texto)

tokens_palabras = [token.text for token in doc]
print("Palabras Tokenizadas:", tokens_palabras)