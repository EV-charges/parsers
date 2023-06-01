import click

from settings import PARSERS_TYPES, ParserType
from src.chargemap.run import run as chargemap_run
from src.electromaps.run import run as electromaps_run
from src.utils.setup_logging import setup_logging


@click.command()
@click.option(
    '--name',
    type=click.Choice(PARSERS_TYPES),
    required=True,
    help='Parser name'
)
def run(name: ParserType) -> None:
    setup_logging()

    if name == ParserType.chargemap:
        chargemap_run()

    if name == ParserType.electromaps:
        electromaps_run()


if __name__ == '__main__':
    run()
