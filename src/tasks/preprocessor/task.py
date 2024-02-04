"""Preprocessor Task."""

from gensim.models import Word2Vec
from keras.preprocessing.sequence import pad_sequences

import nltk
import pandas as pd
import joblib


class PreprocessorTask:
    """Preprocessor Task."""

    def __init__(
        self: "PreprocessorTask",
    ) -> None:
        """
        Initialize Preprocessor Task with a config file and a spark session.

        :param config: Settings configuration.
        """
        self._type_map = {"B2B": 0, "B2C": 1, "Hybrid": 2, "None": 3}

        nltk.download("stopwords")
        self._stop_words = set(nltk.corpus.stopwords.words("english"))

        self._embedding_columns = [
            "technologies",
            "specialties",
            "company_hubs",
            "industry",
            "categories",
        ]
        self._max_sequence_length = 5
        self._vector_size = 5
        self._embeddings_model_filename = "saved_models/word2vec_model_latest.pkl"

        nltk.download("stopwords")

    def run(
        self: "PreprocessorTask", df: pd.DataFrame, is_predict: bool = True
    ) -> pd.DataFrame:
        """
        Run preprocessor task.

        This method performs preprocessing on the given DataFrame.

        :param df: Input DataFrame.
        :param is_predict: Flag indicating whether the task is for prediction.
        :return: Processed DataFrame.
        """
        # Replace NaN values in 'technologies' column
        df.fillna("", inplace=True)

        # Tokenize and preprocess
        for column_name in self._embedding_columns:
            df[f"tokenized_{column_name}"] = df[column_name].apply(self._preprocess)

        if is_predict:
            # Load Word2Vec model
            embedings_model = self._load_model(self._embeddings_model_filename)
        else:
            # Combine all tokenized columns into a single list of sentences
            all_sentences = df[
                [f"tokenized_{column_name}" for column_name in self._embedding_columns]
            ].values.flatten()
            # Create Word2Vec model
            embedings_model = Word2Vec(
                sentences=all_sentences,
                vector_size=5,
                window=3,
                min_count=1,
                workers=4,
            )
            # Save Word2Vec model
            self._save_model(embedings_model, self._embeddings_model_filename)

            # Encode the 'type' column
            df["type_encoded"] = df["type"].map(self._type_map)

        # Create embeddings
        df = self._create_embeddings(df, self._embedding_columns, embedings_model)

        return df[[f"{column}_feature_{i+1}" for column in self._embedding_columns for i in range(25)]]

    def _preprocess(self: "PreprocessorTask", entry: str) -> list:
        """
        Tokenize and preprocess the input text.

        :param entry: Input text.
        :return: List of preprocessed words.
        """
        words = [word.strip().lower() for word in entry.split(",")]
        filtered_words = [word for word in words if word not in self._stop_words]
        return filtered_words

    def _create_embeddings(
        self: "PreprocessorTask",
        df: pd.DataFrame,
        column_names: list,
        word2vec_model: Word2Vec,
    ):
        """
        Create embeddings for specified columns.

        :param df: Input DataFrame.
        :param column_names: List of columns for creating embeddings.
        :param model: Word2Vec model.
        :return: DataFrame with embeddings.
        """
        for column_name in column_names:
            embeddings = df[f"tokenized_{column_name}"].apply(
                lambda entry: [
                    word2vec_model.wv[word]
                    for word in entry
                    if word in word2vec_model.wv
                ],
            )

            # Pad sequences
            padded_embeddings = pad_sequences(
                embeddings,
                maxlen=self._max_sequence_length,
                dtype="float32",
                padding="post",
                truncating="post",
            )

            # Flatten the embeddings
            flattened_embeddings = pd.DataFrame(
                padded_embeddings.reshape(-1, self._vector_size * self._max_sequence_length),
                columns=[
                    f"{column_name}_feature_{i+1}"
                    for i in range(self._vector_size * self._max_sequence_length)
                ],
            )

            # Concatenate the new DataFrame with your original DataFrame
            df = pd.concat([df, flattened_embeddings], axis=1)

        return df

    def _load_model(self: "PreprocessorTask", filename: str) -> Word2Vec:
        """
        Load Word2Vec model from file.

        :param filename: Filepath of the saved model.
        :return: Loaded Word2Vec model.
        """
        return joblib.load(filename)

    def _save_model(self: "PreprocessorTask", model: Word2Vec, filename: str) -> None:
        """
        Save Word2Vec model to file.

        :param model: Word2Vec model to be saved.
        :param filename: Filepath to save the model.
        :return: None
        """
        joblib.dump(model, filename)
