from openai import OpenAI
import pandas as pd
import re

client = OpenAI()

def rank_experts_openai(data, job_description):
    if isinstance(data, list):
        data = pd.DataFrame(data)

    ranking_prompt = "Rate the following experts for this job: " + job_description + "\n\n"

    for i, row in data.iterrows():
        ranking_prompt += f"{i+1}. Name: {row['name']}, Skills: {row['skills']}, Industry: {row['industry']}, Description: {row['description']}\n"

    ranking_prompt += "\nReturn relevance scores from 0 to 1 for each expert in the format: \n1: 0.9\n2: 0.8\n3: 0.95\n"

    ranking_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an expert in ranking candidates."},
                  {"role": "user", "content": ranking_prompt}],
        max_tokens=300
    )

    content = ranking_response.choices[0].message.content
    print("Ranking Response:\n", content)

    scores = re.findall(r"(\d+):\s*([\d.]+)", content)

    explanation_prompt = "Explain the relevance or no relevance of the following experts for this job: " + job_description + "\n\n"

    for i, row in data.iterrows():
        explanation_prompt += f"{i+1}. Name: {row['name']}, Skills: {row['skills']}, Industry: {row['industry']}, Description: {row['description']}\n"

    explanation_prompt += "\nProvide a brief explanation for each expert in the format:\n1: [explanation]\n2: [explanation]\n"

    explanation_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an expert in explaining candidate relevance."},
                  {"role": "user", "content": explanation_prompt}],
        max_tokens=500
    )

    explanation_content = explanation_response.choices[0].message.content
    print("Explanation Response:\n", explanation_content)

    explanations = re.findall(r"(\d+):\s*(.+)", explanation_content)

    ranked_experts = []
    for i, score in scores:
        idx = int(i) - 1
        explanation = next((exp[1] for exp in explanations if exp[0] == i), "No explanation available.")

        ranked_experts.append({
            'name': data.iloc[idx]['name'],
            'relevance': float(score),
            'description': data.iloc[idx]['description'],
            'skills': data.iloc[idx]['skills'],
            'industry': data.iloc[idx]['industry'],
            'explanation': explanation  # Add explanation to result
        })

    return sorted(ranked_experts, key=lambda x: x['relevance'], reverse=True)