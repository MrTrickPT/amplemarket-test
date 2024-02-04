import joblib
import pandas as pd
from flask import Flask, jsonify, request

from tasks import PreprocessorTask, PredictorTask

app = Flask(__name__)

required_features = [
    "name",
    "alexa_rank",
    "city",
    "state",
    "country",
    "hq",
    "website",
    "employees_on_linkedin",
    "followers",
    "founded",
    "industry",
    "linkedin_url",
    "overview",
    "ownership_type",
    "sic_codes",
    "size",
    "specialties",
    "total_funding",
    "technologies",
    "company_hubs",
    "events",
    "categories",
]

numeric_features = [
    "alexa_rank",
    "employees_on_linkedin",
    "followers",
    "founded",
    "sic_codes",
    "total_funding",
]


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get input data from the request
        data = request.json

        # Validate input data
        __validate_input_data(data)

        # Convert data to dataframe
        df = pd.DataFrame([data])

        # Execute preprocessor task
        processed_df = PreprocessorTask().run(df, is_predict=True)

        # Execute predict task
        predict_df = PredictorTask().run(processed_df)

        # Extract 'name' column from the original DataFrame
        names = df['name'].tolist()

        # Extract 'predictions' column from the result DataFrame
        predictions = predict_df['predictions'].tolist()

        # Combine 'name' and 'predictions' into a list of dictionaries
        result_list = [{'name': name, 'predictions': prediction} for name, prediction in zip(names, predictions)]

        # Return the predictions as JSON
        return jsonify(result_list)

    except Exception as e:
        return jsonify({"error": str(e)})


def __validate_input_data(data):
    # Check if all required features are present
    if not all(feature in data for feature in required_features):
        raise ValueError("Missing one or more required features in the input data.")

    # Validate data types
    for feature, value in data.items():
        if feature in numeric_features:
            if not isinstance(value, (int, float)):
                raise ValueError(f"Invalid data type for {feature}. Expected numeric.")
        else:
            if not isinstance(value, str):
                raise ValueError(f"Invalid data type for {feature}. Expected string.")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
