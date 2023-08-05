import sys
from argparse import ArgumentParser

from loguru import logger

from ..utils import RED_TAG as RED
from ..utils import RESET_TAG as RST
from . import BaseAutoNLPCommand


def train_command_factory(args):
    return TrainCommand(args.project)


class TrainCommand(BaseAutoNLPCommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        train_parser = parser.add_parser("train", description="🚀 Start the training for your project!")
        train_parser.add_argument("--project", type=str, default=None, required=True, help="The project name")
        train_parser.set_defaults(func=train_command_factory)

    def __init__(self, name: str):
        self._name = name

    def run(self):
        from ..autonlp import AutoNLP

        logger.info(f"Starting Training For Project: {self._name}")

        client = AutoNLP()
        try:
            project = client.get_project(name=self._name)
        except ValueError:
            logger.error(f"Project {self._name} not found! You can create it using the create_project command.")
            sys.exit(1)
        project.train()
        print(f"🚀 Awesome!! Monitor you training progress here: {RED}autonlp project_info --name {project.name}{RST}")
