from flask import Flask, render_template, request
import pandas as pd
from dotenv import load_dotenv
from utils.my_rank import rank_experts_custom
from utils.openai_rank import rank_experts_openai
from utils.process_csv import process_csv_to_standard_format

app = Flask(__name__)

data = pd.read_csv('data/candidates.csv').to_dict(orient='records')
data2 = pd.read_csv('data/result.csv').to_dict(orient='records')
processed_data = process_csv_to_standard_format('data/result.csv').to_dict(orient='records')
print("processed data: ", processed_data)

@app.route('/')
def index():
    return render_template('index.html', data=[])

@app.route('/rank', methods=['POST'])
def rank():
    job_description = request.form['job_description']
    data_source = request.form['data_source']
    
    if data_source == 'synthetic':
        custom_ranked = rank_experts_custom(data, job_description)
        openai_ranked = rank_experts_openai(data, job_description)
    else:
        custom_ranked = rank_experts_custom(processed_data, job_description)
        openai_ranked = rank_experts_openai(processed_data, job_description)

    print("Custom Ranked:", custom_ranked)
    print("OpenAI Ranked:", openai_ranked)
    custom_ranked = sorted(custom_ranked, key=lambda x: x['score'], reverse=True)
    openai_ranked = sorted(openai_ranked, key=lambda x: x['relevance'], reverse=True)
  
    return render_template('index.html', custom = custom_ranked, openai =openai_ranked, job_description=job_description)

@app.route('/data')
def show_data():
    return render_template('data.html', data=data)

@app.route('/data2')
def show_data2():
    return render_template('data.html', data=data2)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=10000)
    app.run(debug=True)