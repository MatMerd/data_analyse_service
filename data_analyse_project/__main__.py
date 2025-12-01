import argparse
import enum
import logging

import uvicorn

# import uvloop
from data_analyse_project.settings._init import load_settings
from data_analyse_project.web.application import create_app


class ExamSimulator:
    def __init__(self) -> None:
        self._settings = load_settings()

    @property
    def app_name(self) -> str:
        return "AiTools"

    def startup(self) -> None:
        # uvloop.install()
        logging.basicConfig(
            level=self._settings.log_level,
            format="%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
        )
        logging.getLogger("data_analyse_project").setLevel(self._settings.app_log_level)

    def run_server(self) -> None:
        self.startup()

        app = create_app()

        uvicorn.run(
            app=app,
            host=self._settings.asgi_host,
            port=self._settings.asgi_port,
            log_config=None,
            loop="asyncio",
        )


class Commands(enum.StrEnum):
    server = "server"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)


def main() -> None:
    exam_simulator = ExamSimulator()
    parser = argparse.ArgumentParser(prog=exam_simulator.app_name)
    parser.add_argument(
        "run",
        choices=list(Commands),
        help="Command(s) to execute",
    )
    args = parser.parse_args()

    match Commands(args.run):
        case Commands.server:
            exam_simulator.run_server()


if __name__ == "__main__":
    main()
