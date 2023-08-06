import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from consolebundle.CommandManager import CommandManager
from consolebundle.ConsoleArgumentParser import ConsoleArgumentParser
from pyfonycore.bootstrap.config import config_reader


def run_command():
    _load_dot_env()
    arguments_parser = _create_arguments_parser()

    known_args = arguments_parser.parse_known_args()[0]

    bootstrap_config = config_reader.read()
    container = bootstrap_config.container_init_function(known_args.env, bootstrap_config)
    command_manager: CommandManager = container.get("consolebundle.CommandManager")

    logger = container.get("consolebundle.logger")
    logger.warning("Running command in {} environment".format(known_args.env.upper()))

    if len(sys.argv) < 2:
        logger.error("Command not specified, example usage: console mynamespace:mycommand")

        print("\n[Available commands]:")

        for existing_command in command_manager.get_commands():
            logger.info(existing_command.get_command() + " - " + existing_command.get_description())

        sys.exit(1)

    try:
        command = command_manager.get_by_name(known_args.command_name)
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)

    command.configure(arguments_parser)
    arguments_parser.set_command_name(known_args.command_name)

    known_args = arguments_parser.parse_known_args()[0]
    command.run(known_args)


def _create_arguments_parser():
    arguments_parser = ConsoleArgumentParser()
    arguments_parser.add_argument(dest="command_name")

    env_kwargs = dict(required=False, help="Environment")

    if "APP_ENV" in os.environ:
        env_kwargs["default"] = os.environ["APP_ENV"]

    arguments_parser.add_argument("-e", "--env", **env_kwargs)

    return arguments_parser


def _load_dot_env():
    dot_env_file_path = Path.cwd() / ".env"

    if dot_env_file_path.exists():
        load_dotenv(dotenv_path=str(dot_env_file_path))


if __name__ == "__main__":
    run_command()
