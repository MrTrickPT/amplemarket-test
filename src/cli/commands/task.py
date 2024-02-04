"""Validation group."""

import click

from src.tasks.registry import TaskRegistry


@click.group()
def task() -> None:
    """Validate group."""


@task.command()
@click.option(
    "--csv-path",
    "-c",
    required=True,
    help="CSV file location.",
)
@click.option(
    "--is-predict",
    "-p",
    default=True,
    type=bool,
    show_default=True,
    help="Flag indicating whether the task is for prediction.",
)
@click.option(
    "--output-path",
    "-o",
    default="output.csv",
    help="Output file location to save the processed DataFrame.",
)
def preprocessor(csv_path, is_predict, output_path) -> None:
    """
    Cli initializer for preprocessor task.

    :param csv_path: CSV file location
    :param is_predict: Flag indicating whether the task is for prediction
    :param output_path: Output file location to save the processed DataFrame

    :return:
    """
    df = pd.read_csv(csv_path)

    preprocessor_class = TaskRegistry.get("preprocessor")
    preprocessor_instance = preprocessor_class()
    processed_df = preprocessor_instance.run(df, is_predict)

    # Save the processed DataFrame to a file
    processed_df.to_csv(output_path, index=False)


@task.command()
@click.option(
    "--input-path",
    "-i",
    required=True,
    help="Input file location containing data for prediction.",
)
@click.option(
    "--output-path",
    "-o",
    default="predictions.csv",
    help="Output file location to save the predictions DataFrame.",
)
def predictor(input_path, output_path) -> None:
    """
    Cli initializer for predictor task.

    :param input_path: Input file location containing data for prediction.
    :param output_path: Output file location to save the predictions DataFrame.

    :return:
    """
    input_df = pd.read_csv(input_path)

    predictor_class = TaskRegistry.get("predictor")
    predictor_instance = predictor_class()
    predictions_df = predictor_instance.run(input_df)

    # Save the predictions DataFrame to a file
    predictions_df.to_csv(output_path, index=False)
