from sklearn.feature_extraction.text import TfidfVectorizer

documents = [
    "Machine learning is fun",
    "Learning Python for machine learning"
]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

print(tfidf_matrix.toarray())