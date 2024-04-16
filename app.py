from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load datasets
def load_data():
    dataset = pd.read_csv('data/dataset.csv')
    descriptions = pd.read_csv('data/symptom_Description.csv')
    precautions = pd.read_csv('data/symptom_precaution.csv')
    
    # Normalize symptom fields in the dataset
    for i in range(1, 18):  # Adjust the range based on your dataset columns
        symptom_col = f'Symptom_{i}'
        if symptom_col in dataset.columns:
            dataset[symptom_col] = dataset[symptom_col].str.lower().str.strip()
    return dataset, descriptions, precautions

dataset, descriptions, precautions = load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.get_json()  # Assuming JSON input
    symptoms_input = data['symptoms']
    
    # Normalize and split symptoms if they are passed as a single string
    if isinstance(symptoms_input, str):
        symptoms = [symptom.strip().lower() for symptom in symptoms_input.split(',')]
    else:
        symptoms = [symptom.strip().lower() for symptom in symptoms_input]

    print("Received symptoms:", symptoms)  # Debug: print received symptoms

    # Initialize an empty DataFrame to collect possible diseases
    possible_diseases = pd.DataFrame()

    # Check each symptom column for matches
    for i in range(1, 18):  # Adjust the range based on your dataset columns
        column_name = f'Symptom_{i}'
        if column_name in dataset.columns:
            matches = dataset[dataset[column_name].isin(symptoms)]
            possible_diseases = pd.concat([possible_diseases, matches])

    possible_diseases = possible_diseases.drop_duplicates(subset='Disease')
    print("Matching diseases:", possible_diseases)  # Debug: print matched diseases

    disease_list = possible_diseases['Disease'].unique()
    results = []
    for disease in disease_list:
        desc_query = descriptions[descriptions['Disease'] == disease]
        if not desc_query.empty:
            description = desc_query['Description'].values[0]
            precaution_list = precautions[precautions['Disease'] == disease].iloc[0].to_dict()
            results.append({
                'disease': disease,
                'description': description,
                'precautions': {k: v for k, v in precaution_list.items() if 'Precaution_' in k}
            })
        else:
            results.append({
                'disease': disease,
                'description': "Description not available",
                'precautions': {}
            })

    print("Results:", results)  # Debug: print results to be returned
    return jsonify(results)



if __name__ == '__main__':
    app.run(debug=True)
