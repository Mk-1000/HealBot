from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load datasets and collect all unique symptoms
def load_data():
    try:
        dataset = pd.read_csv('data/dataset.csv')
        descriptions = pd.read_csv('data/symptom_Description.csv')
        precautions = pd.read_csv('data/symptom_precaution.csv')
    except Exception as e:
        print("Error loading data files:", e)
        return None, None, None, set()  # Return empty structures in case of failure

    all_symptoms = set()
    # Normalize symptom fields in the dataset and collect unique symptoms
    for col in dataset.columns:
        if 'Symptom' in col:
            dataset[col] = dataset[col].str.lower().str.strip()
            all_symptoms.update(dataset[col].dropna().unique())
    
    return dataset, descriptions, precautions, all_symptoms

def load_medicine_data():
    try:
        medicines_df = pd.read_csv('data/medicines.csv')
    except Exception as e:
        print("Error loading medicine data file:", e)
        medicines_df = pd.DataFrame()  # Return empty dataframe in case of failure
    return medicines_df

def diagnose_symptoms(symptoms, dataset, descriptions, precautions):
    possible_diseases = pd.DataFrame()
    for col in dataset.columns:
        if 'Symptom' in col:
            matches = dataset[dataset[col].isin(symptoms)]
            possible_diseases = pd.concat([possible_diseases, matches])

    possible_diseases = possible_diseases.drop_duplicates(subset='Disease')
    disease_list = possible_diseases['Disease'].unique()
    results = []

    for disease in disease_list:
        desc_query = descriptions[descriptions['Disease'] == disease]
        description = desc_query['Description'].values[0] if not desc_query.empty else "Description not available"
        precaution_query = precautions[precautions['Disease'] == disease]
        precaution_list = precaution_query.iloc[0].to_dict() if not precaution_query.empty else {}

        results.append({
            'disease': disease,
            'description': description,
            'precautions': {k: v for k, v in precaution_list.items() if 'Precaution_' in k}
        })

    return results

def find_matching_medicines(user_input, df):
    user_input_lower = user_input.lower()
    matches = df[df['name'].str.lower().str.contains(user_input_lower)]
    return matches

# Load data
dataset, descriptions, precautions, all_symptoms = load_data()
medicines_df = load_medicine_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/symptoms', methods=['GET'])
def get_symptoms():
    return jsonify(list(all_symptoms))

@app.route('/diagnose', methods=['POST'])
def diagnose():
    try:
        data = request.get_json()  # Assuming JSON input
        symptoms_input = data['symptoms']
    except TypeError:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    if not symptoms_input:
        return jsonify({"error": "No symptoms provided"}), 400

    # Normalize and split symptoms
    if isinstance(symptoms_input, str):
        symptoms = [symptom.strip().lower() for symptom in symptoms_input.split(',')]
    else:
        symptoms = [symptom.strip().lower() for symptom in symptoms_input]

    results = diagnose_symptoms(symptoms, dataset, descriptions, precautions)
    return jsonify(results)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        user_input = request.form['medicine_name']
        matching_medicines = find_matching_medicines(user_input, medicines_df)
        if not matching_medicines.empty:
            result = matching_medicines[['id', 'name', 'price(₹)', 'Is_discontinued', 'manufacturer_name', 'type', 'pack_size_label', 'short_composition1', 'short_composition2']].to_dict(orient='records')
            return jsonify(result)
        else:
            return jsonify({'message': 'No matching medicines found.'})
    return render_template('search.html')

# Route to fetch all medicines
@app.route('/medicines', methods=['GET'])
def get_medicines():
    medicines_df = load_medicine_data()
    medicines_list = medicines_df.to_dict(orient='records')
    return jsonify(medicines_list)

if __name__ == '__main__':
    app.run(debug=True)
