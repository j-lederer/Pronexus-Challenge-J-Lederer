from flask import Flask, render_template, request
import pandas as pd
from utils.rank_experts import rank_experts_custom
from utils.openai_rank import rank_experts_openai

app = Flask(__name__)

# Load expert data
data = pd.read_csv('data/candidates.csv')

@app.route('/')
def index():
    return render_template('index.html', data=[])

@app.route('/rank', methods=['POST'])
def rank():
    job_description = request.form['job_description']
    custom_ranked = rank_experts_custom(data, job_description)
    openai_ranked = rank_experts_openai(data, job_description)

    return render_template('index.html', data=zip(custom_ranked, openai_ranked))

@app.route('/data')
def show_data():
    return render_template('data.html', data=data.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)