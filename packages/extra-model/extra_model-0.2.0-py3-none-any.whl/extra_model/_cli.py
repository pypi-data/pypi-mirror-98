import logging
import sys
from pathlib import Path

import click

from extra_model._errors import ExtraModelError
from extra_model._run import run
from extra_model._setup import setup

logger = logging.getLogger(__name__)


OUTPUT_PATH = "/io"
OUTPUT_FILENAME = "result.csv"
EMBEDDINGS_PATH = "/embeddings"


@click.command()
@click.argument("input_path", type=Path)
@click.argument("output_path", type=Path, default=OUTPUT_PATH)
@click.argument("output_filename", type=Path, default=OUTPUT_FILENAME)
@click.option("--debug", is_flag=True, help="Enable debug logging")
def entrypoint(
    input_path: Path, output_path: Path, output_filename: Path, debug: bool = False
) -> None:
    """Run the Extra algorithm for unsupervised topic extraction.

    INPUT_PATH is the path to the input parquet file with the user generated texts.

    OUTPUT_PATH is the path to the output directory. Default is `/io`.

    OUTPUT_FILENAME is the filename of the output file. Default is `result.csv`.
    The `.csv` file extension is not enforced. Please take care of this accordingly.
    """
    logging.getLogger("extra_model").setLevel("DEBUG" if debug else "INFO")

    try:
        run(input_path, output_path, output_filename)
        sys.exit(0)

    except ExtraModelError as e:
        logger.exception(e) if debug else logger.error(e)
        sys.exit(1)


@click.command()
@click.argument("output_path", type=Path, default=EMBEDDINGS_PATH)
def entrypoint_setup(output_path: Path) -> None:
    """Download resources.

    Will download and format glove embeddings.

    OUTPUT_PATH is the path to the output directory. Default is `/embeddings`.
    """
    try:
        setup(output_path)
        sys.exit(0)

    except ExtraModelError as e:
        logger.error(e)
        sys.exit(1)
