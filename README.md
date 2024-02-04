# Organization Type Predictor

## Challenge
The goal is to develop and expose a predictive model capable of detecting the type of an organization. The organization types include:

B2B (Business selling to other businesses): Example - Amplemarket
B2C (Business selling to consumers): Example - Ebay
Hybrid (Both B2B and B2C): Example - Microsoft (selling Windows to consumers and Azure to Businesses)
None of the above: Example - Unicef


## Repository Structure
- src/: Contains code and Jupyter notebooks for training the machine learning model.
    - src.ipynb: Notebook for training the model.
    - tasks/:
        - preprocessor
            - task.py
        - predictor
            - task.py
    - api/: Contains files related to the API.
        - app.py: Python script for the Flask API.
- saved_models/: Directory to store your trained machine learning models.
- presentation/: Contains presentation files.
    - project_presentation.pptx: PowerPoint presentation explaining the solution.
- README.md: This file, providing an overview of the project and its components.

## Requirements
To run the notebook and API, you need to install Poetry.

## Getting Started
Follow these steps to get started:
- Clone this repository.
- Navigate to the notebook/ directory and run the train_model.ipynb notebook to train the machine learning model.
- Run the following commands in the root
```bash
make install  # Installs dependencies using Poetry.
make run-api
```
- The API will be available at http://localhost:5000.


## Training the Model
Refer to the train_model.ipynb notebook for details on how to train the machine learning model using the provided dataset.

## API Usage
To make predictions using the API, send a POST request with features to http://localhost:5000/predict. For example:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"feature1": "value1", "feature2": "value2"}' http://localhost:5000/predict
```