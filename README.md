# Medical Diagnostic Tool

This Medical Diagnostic Tool is a Flask-based web application designed to diagnose potential diseases based on input symptoms from users. It provides disease descriptions and precautionary measures based on the matching results from the symptoms provided.

## Features

- **Symptom Input**: Users can input multiple symptoms which the system will process to predict potential diseases.
- **Disease Information**: The application returns a list of possible diseases, complete with descriptions and precautions.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.8 or newer installed on your machine.
- Pip for managing Python packages.

## Installation

Follow these steps to get your development environment running:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/medical-diagnostic-tool.git
   cd medical-diagnostic-tool
   ```

2. **Set up a Python virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Data Setup

Ensure the data files (`dataset.csv`, `symptom_Description.csv`, `symptom_precaution.csv`) are placed in the `data` directory within the project folder. These files should be properly formatted CSV files containing the necessary information about diseases, symptoms, descriptions, and precautions.

## Running the Application

To run the application, execute the following command in the root directory of the project:

```bash
flask run
```

This will start the Flask server on `http://127.0.0.1:5000/`, and you can access the web application by navigating to this address in your web browser.

## Using the Application

- **Home Page**: Navigate to the home page and enter symptoms separated by commas in the input field provided.
- **Submit**: Click the 'Diagnose' button to submit the symptoms. The application will process the input and display the results below the form.
- **View Results**: The results section will show a list of possible diseases along with their descriptions and recommended precautions.

## Troubleshooting

- **Data not found errors**: Ensure all data files are correctly placed in the `data` directory.
- **Python dependencies**: Make sure all required Python packages are installed by running `pip install -r requirements.txt`.

## Contributing

Contributions to the project are welcome! To contribute:
- Fork the repository.
- Create a new branch for your feature.
- Add your changes and commit them.
- Push the branch and open a pull request.

## License

This project is licensed under the [MIT License](LICENSE.md).