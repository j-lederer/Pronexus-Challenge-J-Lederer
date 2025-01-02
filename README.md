
Web:
https://pronexus-challenge-j-lederer.onrender.com

There is a slight bug. Sometimes when you press Generate Top Leads, the OpenAI table doesn't populate. If you attempt it a few more times it will work. Most of the time, it properly populates.

Local:
Installation and Setup

1. Clone the Repository:
git clone https://github.com/j-lederer/Pronexus-Challenge-J-Lederer.git
cd Pronexus-Challenge-J-Lederer

2. Set Up Virtual Environment:
python -m venv venv  
source venv/bin/activate  

3. Install Required Packages:
pip install -r requirements.txt  

4. Set Up Environment Variables:

Create a .env file in the root directory and add OpenAI API key:
OPENAI_API_KEY= The key I provided.

5. Run the Application:
flask run  


Thesis:
Approach Overview

The solution is structured around a dual-ranking system that utilizes:
	1.	A Custom Machine Learning Model – This model analyzes job descriptions and candidate profiles, computing relevance through text embeddings, cosine similarity, and fuzzy matching. The main focus is on the similarity between the job description and the candidates profile in terms of meaning and text similarity. Keywords, the candidate's indistry, and experiance are also accounted for.
	2.	OpenAI’s GPT Model – GPT provides additional ranking and explanatory text, offering context for each candidate’s position.

Data Retrieval and Processing


I obtained a list of 843 candidates using Phantombuser's Linkedin Export Search and Linkedin Profile Scraper. It searches Linkedin for "Open to work" and then runs another automation to scrape the users' profile data. Regular scraping of Linkedin profiles violates Linkedin's terms of service so this was the best option. Unfortunately the free trial only allowed me to download 10 profiles.

Candidate data is downloaded and ingested in CSV format the received fields are distilled into the following columns: Name, Skills, Industry, Description. This data is pre-processed to standardize text, remove stop words, and extract essential information. The job description provided by the recruiter is processed similarly to ensure consistency.

Key Steps in Data Processing:
	•	Embedding Generation: The sentence-transformers model converts job descriptions and candidate profiles into vector embeddings. This enables the system to compute similarity scores by measuring how closely two embeddings align.
	•	Keyword Extraction: Using CountVectorizer from scikit-learn, the tool identifies critical keywords from the job description, emphasizing skills and industry-specific terms.
	•	Experience Parsing: A regular expression parser extracts years of experience from candidate descriptions, ensuring candidates with matching or higher experience receive score boosts.

Candidate Matching and Scoring

The core ranking process uses multiple factors to assess candidate relevance:
	1.	Cosine Similarity (40%) – Measures the closeness between job description embeddings and candidate embeddings.
	2.	Fuzzy Matching (40%) – Evaluates text similarity, allowing partial matches between skills, industry, and descriptions.
	3.	Keyword Matching (5%) – Rewards candidates whose skills align with extracted keywords from the job description.
	4.	Industry Relevance (10-20%) – Candidates in similar industries receive incremental boosts, even if the industries do not match exactly.
	5.	Experience Matching (Up to 15%) – Candidates with sufficient or greater experience receive additional weight in scoring.

Explanation Generation

After ranking, the system generates explanations for each candidate using the data calculated by the custom algorithm and OpenAI’s GPT. This provides recruiters with justifications for each score and insight into the decision-making process.


Tools and Technologies
	•	Backend: Flask (Python)
	•	Machine Learning:
        •	sentence-transformers – Text embedding and similarity comparison
        •	fuzzywuzzy – Fuzzy string matching
        •	scikit-learn – Keyword extraction
	•	AI Model: OpenAI’s gpt-3.5-turbo
	•	Frontend: HTML/CSS for recruiter interface