from argparse import ArgumentParser
from glob import glob
from importlib import import_module
from inspect import isclass
from logging import getLogger
from os import path
from re import escape, sub
from sys import path as syspath
from typing import Dict

from pydantic import BaseModel
from pydantic2ts import generate_typescript_defs

logger = getLogger(__file__)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "search_path",
        type=str,
    )
    parser.add_argument(
        "output_path",
        type=str,
    )
    args = vars(parser.parse_args())
    types: Dict[str, str] = {}
    for file_path in [
        filename
        for filename in glob(path.join(args["search_path"], "**", "*.py"), recursive=True)
        if not filename.endswith("__init__.py")
    ]:
        module_path = path.dirname(file_path)
        relative_module_path = module_path.replace(args["search_path"], "")
        module_name = path.basename(file_path)[:-3]
        path_parts = [
            part
            for part in [
                sub(rf"^{escape(path.sep)}", "", relative_module_path),
                module_name,
            ]
            if part
        ]
        module_str = f"{path.sep.join(path_parts).replace(path.sep, '.')}"
        if args["search_path"] not in syspath:
            syspath.append(args["search_path"])
        try:
            logger.debug(f"importing {module_str}, with sys.path {syspath}")
            module = import_module(module_str)
        except Exception as e:
            logger.warning(
                f"unable to import type class from module '{module_str}', "
                f"so skipping. Some dependencies may be missing: {e}"
            )
            continue

        types = {
            **types,
            **{
                module_str: module_name
                for type_class in module.__dict__.values()
                if isclass(type_class) and type_class is not BaseModel and issubclass(type_class, BaseModel)
            },
        }

    for module_str, module_name in types.items():
        ts_path = path.join(args["output_path"], f"api_{module_name}.ts")
        logger.debug(f"generating TypeScript type for {module_str} to {ts_path}")
        try:
            generate_typescript_defs(module_str, ts_path)
        except Exception as e:
            logger.exception("Problem generating TypeScript definitions", e)
