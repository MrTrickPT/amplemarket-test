"""Models Metric Exporter Module."""

import click

from src.cli.commands.task import preprocessor, predictor


@click.group()
def cli() -> None:
    """Future python code."""


cli.add_command(preprocessor)
cli.add_command(predictor)
