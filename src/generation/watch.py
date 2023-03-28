import time
from argparse import ArgumentParser
from subprocess import Popen
from logging import getLogger

from generation.debouncer import debounce

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


logger = getLogger(__file__)

def generate(search_path: str, output_path: str):
    # execute within new process to avoid module caching
    # caching results in the initial version of the module being used repeatedly
    # https://github.com/phillipdupuis/pydantic-to-typescript/issues/7
    Popen(
        ["python", "-m", "generation.generate", search_path, output_path],
    ).communicate()


class Event(FileSystemEventHandler):
    def __init__(self, search_path: str, output_path: str):
        self.search_path = search_path
        self.output_path = output_path

    def on_modified(self, event):
        if "__pycache__" in event.src_path:
            logger.debug("ignoring __pycache__ modify event")
            return
        self.execute(event)

    @debounce(wait_time=1)
    def execute(self, event):
        logger.debug(f"invoking file modified handler with event {event}")
        generate(self.search_path, self.output_path)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "search_path",
        help="Absolute path of parent directory to all Pydantic type definitions",
        type=str,
        default="/",
    )
    parser.add_argument(
        "output_path",
        help="Absolute path target for generated types",
        type=str,
        default="/tstypes",
    )
    args = vars(parser.parse_args())
    logger.debug("initial invocation of modified handler")
    generate(args["search_path"], args["output_path"])
    observer = Observer()
    observer.schedule(
        Event(args["search_path"], args["output_path"]),
        args["search_path"],
        recursive=True,
    )
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
