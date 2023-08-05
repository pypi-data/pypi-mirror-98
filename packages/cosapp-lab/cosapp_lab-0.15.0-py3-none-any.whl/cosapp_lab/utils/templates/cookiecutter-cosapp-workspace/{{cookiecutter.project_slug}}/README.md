# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

This work is licensed under the [following terms](LICENSE).

## Structure

### Root folder

- `setup.py`, `setup.cfg` and `MANIFEST.in`: Configuration of the project to be a valid Python package
- `cosapp.json`: Parameters to allow the managment of the project by the UI
- `HISTORY.md`: Changes log from one version to another
- `LICENSE`: License on which falls this work
- `.gitignore`: Filters files to be versionned

### {{cookiecutter.project_slug}} folder

This folder is the one containing meaningful code for the project.

- `ports` folder: Contains all `cosapp.ports.Port` classes created in the project
- `systems` folder: Contains all `cosapp.systems.System` classes created in the project
- `drivers` folder: Contains all `cosapp.drivers.Driver` classes created in the project
- `studies` folder: Contains all Python scripts and Notebooks to carry out meaningful simulation
- `resources` folder: Contains all tables, data files,... required by the model
- `tools` folder: Contains all Python scripts providing functions, classes, etc. useful to execute the model
- `tests` folder: Contains all Python scripts testing the validity of the systems
- `_version.py`: Version of the project

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter)
and the [cookiecutter-cosapp-project](https://gitlab.com/cosapp/cosapp-utils/cookiecutter-cosapp-workspace)
project template.
