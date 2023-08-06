from os import read
from cosapp_lab.module import CosappModuleServer
from cosapp_lab.utils.helpers import get_abs_dir, Suppressor, get_readme_from_path
from pathlib import Path
import importlib
from click.utils import echo
import json
from typing import Dict, Union, List
import sys
from ..module.module_server import MODULE_MODE
import logging

CODE_TEMPLATE = """
from {{name}} import _cosapp_lab_load_module
args_list = {{args}}
_cosapp_lab_load_module(*args_list)
"""

COSAPP_CONFIG_DIR = Path.home() / ".cosapp.d"
OKGREEN = "\033[92m"
ENDC = "\033[0m"


def _get_module_json_data() -> Dict:
    config_path = COSAPP_CONFIG_DIR / "app"
    if not config_path.exists():
        config_path.mkdir(parents=True, exist_ok=True)
    json_path = config_path / "cosapp_module.json"
    if json_path.is_file():
        with open(json_path, "r") as f:
            old_data = json.load(f)
    else:
        old_data = {}

    return old_data


def cosapp_module_list() -> None:
    old_data = _get_module_json_data()

    if len(old_data) == 0:
        echo("No CoSApp module registed")
    else:
        echo("CoSApp Lab version 0.14.0")
        for key, value in old_data.items():
            try:
                echo(
                    f'{OKGREEN}{key}{ENDC} {value["meta"]["version"]} - {value["title"]}'
                )
            except KeyError:
                echo(f'{OKGREEN}{key}{ENDC}              {value["title"]}')


def cosapp_module_update() -> None:
    old_data = list(_get_module_json_data())

    if len(old_data) == 0:
        echo("No CoSApp module registed")
    else:
        cosapp_module_remove(old_data)
        cosapp_module_register(old_data)


def cosapp_module_register(name_list: List[str]) -> Union[None, int]:
    old_data = _get_module_json_data()
    status = None
    for name in name_list:
        try:
            logging.disable(logging.CRITICAL)
            module = importlib.import_module(f"{name}")
            init_function = getattr(module, "_cosapp_lab_load_module")
            with Suppressor():
                init_function()
        except ModuleNotFoundError:
            echo(f" Can not import module named {name}, skipping.")
            continue
        except AttributeError:
            echo(f"{name} is not a CoSApp module, skipping.")
            continue
        except NotImplementedError:
            echo(f"Interface configuration is not implemented in {name}, skipping.")
            continue

        try:
            version = f"v{module.__version__}"
        except AttributeError:
            version = "Unknown"

        if name in old_data:
            echo(f"Module {name} already registed, skipping.")
            continue
        else:
            meta_function = getattr(module, "_cosapp_lab_module_meta")
            meta = meta_function()
            if meta is None:
                meta = {}
            if "version" not in meta:
                meta["version"] = version
            title = meta.get("title", name)
            code = CODE_TEMPLATE.replace("{{name}}", name)
            path = Path(module.__file__).parent
            readme = get_readme_from_path(path.parent)
            if readme is None:
                readme = get_readme_from_path(path)
            meta["readme"] = readme
            old_data[name] = {
                "code": code,
                "title": title,
                "meta": meta,
            }
            echo(f"{name} is successfully registed as CoSApp standalone module")
            status = 1
    json_path = COSAPP_CONFIG_DIR / "app" / "cosapp_module.json"
    with open(json_path, "w") as f:
        json.dump(old_data, f)

    return status


def cosapp_module_remove(nameList: List[str]) -> None:
    old_data = _get_module_json_data()
    for name in nameList:
        if name in old_data:
            del old_data[name]
            echo(f"{name} is successfully removed from standalone module list")
        else:
            echo(f"{name} can not be found, skipping.")
            continue
    json_path = COSAPP_CONFIG_DIR / "app" / "cosapp_module.json"
    with open(json_path, "w+") as f:
        json.dump(old_data, f)


def cosapp_load_file(file: str) -> None:

    file_path = get_abs_dir(Path().absolute(), file)
    try:
        with open(file_path, "r") as f:
            file_content = f.read()
    except FileNotFoundError:
        echo(f"No such file {file_path}")
        return
    CosappModuleServer.startup_code = file_content
    CosappModuleServer.title = f"CoSApp application - {file}"
    CosappModuleServer.module_mode = MODULE_MODE.SINGLE
    if "--arguments" in sys.argv:
        sys.argv.remove("--arguments")
    CosappModuleServer.launch_instance()


def cosapp_load_module(module: str, args: str = None) -> None:
    if args is not None:
        str_list = [f'"{str(x.strip())}"' for x in args.split(" ")]
        args_list = f'[{",".join(str_list)}]'
    else:
        args_list = "[]"
    old_data = _get_module_json_data()
    CosappModuleServer.all_module_data = old_data
    if module == "__all__":
        if "--all" in sys.argv:
            sys.argv.remove("--all")
        if "-a" in sys.argv:
            sys.argv.remove("-a")
        CosappModuleServer.startup_code = ""
        CosappModuleServer.title = ""
        CosappModuleServer.module_mode = MODULE_MODE.MULTIPLE
        CosappModuleServer.launch_instance()
    else:
        if module in old_data:
            title = old_data[module]["title"]
            if title is None:
                title = f"CoSApp application - {module}"
            CosappModuleServer.startup_code = old_data[module]["code"]
            CosappModuleServer.title = title
            CosappModuleServer.args_list = args_list
            CosappModuleServer.module_mode = MODULE_MODE.SINGLE
            if "--arguments" in sys.argv:
                sys.argv.remove("--arguments")
            if "-args" in sys.argv:
                sys.argv.remove("-args")
            CosappModuleServer.launch_instance()
        else:
            echo(f"Module {module} is not registed yet, start registering")
            check = cosapp_module_register(module)
            if check == 1:
                cosapp_load_module(module, args)
