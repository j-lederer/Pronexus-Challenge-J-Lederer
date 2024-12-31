from transformers import pipeline
from fuzzywuzzy import fuzz
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

def extract_keywords(job_description):
    vectorizer = CountVectorizer(ngram_range=(1, 2), stop_words='english')
    vectorizer.fit([job_description])
    return vectorizer.get_feature_names_out()

def extract_experience(description):
    import re
    match = re.search(r'(\d+)\+?\s*years?', description, re.IGNORECASE)
    return int(match.group(1)) if match else 0

def rank_experts_custom(data, job_description):
    model = pipeline("feature-extraction", model="sentence-transformers/all-MiniLM-L6-v2")

    if isinstance(data, list):
        data = pd.DataFrame(data)
    
    job_embedding = model(job_description)[0][0]
    keywords = extract_keywords(job_description)
    job_exp = extract_experience(job_description)

    ranked_experts = []

    for _, expert in data.iterrows():
        combined_text = f"{expert['skills']} {expert['industry']} {expert['description']}"
        expert_embedding = model(combined_text)[0][0]

        # Cosine similarity
        similarity = sum(a * b for a, b in zip(job_embedding, expert_embedding)) / (
            (sum(a ** 2 for a in job_embedding) ** 0.5) * (sum(b ** 2 for b in expert_embedding) ** 0.5)
        )

        # Fuzzy matching
        fuzzy_score = fuzz.token_set_ratio(job_description, combined_text)

        # Skill keyword
        boost = sum(1 for kw in keywords if kw in expert['skills'].lower())

        # Industry similarity 
        industry_similarity = fuzz.token_set_ratio(job_description, expert['industry']) / 100
        industry_boost = industry_similarity * 0.2
        
        expert_exp = extract_experience(expert['description'])
        exp_boost = min((expert_exp / job_exp), 1) if job_exp > 0 else 0

        final_score = (fuzzy_score / 100) * 0.4 + similarity * 0.4
        final_score += boost * 0.05 + industry_boost + exp_boost * 0.15 

        ranked_experts.append({
            'name': expert['name'],
            'score': round(final_score, 2),
            'description': expert['description'],
            'skills': expert['skills'],
            'industry': expert['industry'],
            'explanation': f"Keyword Match: {boost}, Industry Relevance: {round(industry_boost, 2)}, "
                           f"Overall Text Match: {fuzzy_score}, Deep Similarity: {round(similarity, 2)}, "
                           f"Experience Boost: {round(exp_boost * 0.15, 2)}"
        })
    
    return sorted(ranked_experts, key=lambda x: x['score'], reverse=True)