import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_experts_custom(data, job_description):
    vectorizer = TfidfVectorizer()
    corpus = data['skills'] + ' ' + data['industry']
    X = vectorizer.fit_transform(corpus)

    job_vec = vectorizer.transform([job_description])
    similarities = cosine_similarity(job_vec, X).flatten()

    data['score'] = similarities
    ranked_data = data.sort_values(by='score', ascending=False)
    return ranked_data.to_dict(orient='records')