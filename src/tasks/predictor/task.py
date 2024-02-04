import pandas as pd
import joblib


class PredictorTask:
    """Predictor Task."""

    def __init__(self: "PredictorTask") -> None:
        """
        Initialize Predictor Task with the filename of the pre-trained model.

        :param model_filename: Filename of the pre-trained model.
        """
        self._model_filename = "saved_models/rf_model_latest.pkl"

        self._type_map = {0:"B2B", 1:"B2C", 2:"B2B B2C", 3:"None"}


    def run(self: "PredictorTask", df: pd.DataFrame) -> pd.DataFrame:
        """
        Run predictor task.

        :param df: Input DataFrame for predictions.
        :return: DataFrame with predictions.
        """
        # Load the pre-trained model
        model = joblib.load(self._model_filename)

        # Perform predictions
        predictions = model.predict(df)

        # Map numeric predictions to corresponding values
        df["predictions"] = pd.Series(predictions).map(self._type_map)

        return df
