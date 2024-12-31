import openai
import os

def rank_experts_openai(data, job_description):
    api_key = os.getenv("OPENAI_API_KEY")  # Fetch key from .env
    client = openai.Client(api_key=api_key)

    experts = []
    for _, row in data.iterrows():
        desc = row['description']

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert recruiter."},
                {"role": "user", "content": f"Rank this expert for the job: {job_description}. Expert description: {desc}"}
            ],
            max_tokens=100
        )
        
        ranked_expert = response.choices[0].message.content.strip()
        experts.append((row['name'], ranked_expert))

    return experts