__version__ = "0.1.6-dev3"
__license__ = "Apache-2.0 License"
__title__ = "cardanopy"

import click

from .run import run
from .create import create
from .cli import cli
from .docker import docker
from .k8s import k8s
from .generate import generate_cmd
# from .config import config

@click.group()
@click.version_option(version=__version__)
@click.pass_context
def main(ctx):
    pass


# export
main.add_command(run)
main.add_command(create)
main.add_command(cli)
main.add_command(docker)
main.add_command(k8s)
main.add_command(generate_cmd)
# disable config cli for now (might remove)
# main.add_command(config)
