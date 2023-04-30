import click

from src.chargemap.run import run as chargemap_run
from src.plugshare.run import run as plugshare_run
from settings import PARSERS_TYPES, ParserType


@click.command()
@click.option(
    '--name',
    type=click.Choice(PARSERS_TYPES),
    required=True,
    help='Parser name'
)
def run(name: ParserType):
    if name == ParserType.chargemap:
        chargemap_run()

    if name == ParserType.plugshare:
        plugshare_run()


if __name__ == '__main__':
    run()
