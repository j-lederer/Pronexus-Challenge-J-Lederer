import pandas as pd

def process_csv_to_standard_format(file_path):

    data = pd.read_csv(file_path)

    data['name'] = data['firstName'] + ' ' + data['lastName']
    data['skills'] = data['linkedinSkillsLabel'].fillna('')
    data['industry'] = data['companyIndustry'].fillna('')
    

    data['description'] = (
        data['linkedinJobTitle'].fillna('') + " " +
        data['linkedinJobDescription'].fillna('') + " " +
        data['linkedinHeadline'].fillna('') + " " +
        data['linkedinSchoolDescription'].fillna('')
    )


    data['description'] = data['description'].str.strip()
    data['description'] = data['description'].replace('', 'No description available')

    return data[['name', 'skills', 'industry', 'description']]