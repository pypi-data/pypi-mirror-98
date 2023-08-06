# cookiecutter-cosapp-project

Template for CoSApp project folder.

A CoSApp project folder is a valid Python package with special structure and configurations files.

Git repository: https://gitlab.com/cosapp/cosapp-utils/cookiecutter-cosapp-workspace

### Table of Contents

- [Requirements](#requirements)
- [Usage](#usage)
  - [Example](#example)
- [Documentation](#documentation)
- [History](#history)
- [Credits](#credits)
- [License](#license)

## Requirements

- [python](https://www.python.org/downloads/)
- [cookiecutter](https://github.com/audreyr/cookiecutter)

## Usage

    $ cookiecutter cookiecutter-cosapp-project

### Example

```
$ tree -a cookiecutter-cosapp-project
cookiecutter-cosapp-project
├───.gitignore
├───cosapp.json
├───HISTORY.md
├───LICENSE
├───MANIFEST.in
├───README.md
├───setup.cfg
├───setup.py
└───cosapp_project
    ├───__init__.py
    ├───_version.py
    ├───model.py
    ├───model.json
    ├───drivers
    │   ├───__init__.py
    │   └───.gitignore
    ├───ports
    │   ├───__init__.py
    │   └───.gitignore
    ├───ressources
    │   └───.gitkeep
    ├───studies
    │   ├───Untitled.ipynb
    │   └───.gitignore
    ├───systems
    │   ├───__init__.py
    │   └───.gitignore
    ├───tests
    |   └───.gitignore
    └───tools
        └───__init__.py
```

## Documentation

**cookiecutter.json** explained in-depth. See [cookiecutter.json](cookiecutter.json) for default values.

| Prompt                      | Explanation                                                                                                                            |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `full_name`                 | Your full name.                                                                                                                        |
| `email`                     | The email address you want associated with the repository.                                                                             |
| `project_name`              | The project name. This will be the _H1_ in the **README.md**.                                                                          |
| `project_slug`              | The project folder name which should only contain alphanumeric characters and dashes. This will be the local top-level directory name. |
| `project_short_description` | A short description about the project. This will be the content under the _H1_ in the **README.md**.                                   |
| `version`                   | Project first version.                                                                                                                 |
| `copyright_holder`          | The individual or company that holds the intellectual property copyright. This will be used in the **LICENSE** file.                   |
| `repository`                | Git server url on which to store the project.                                                                                          |

## History
- 2021/02/15
  Update License for publication as open-source software.

- 2019/02/26
  Add `tools` folder to store useful Python scripts, functions, classes,... not belonging to some
  CoSApp specific categories.

- 2019/01/08
  Reduce as much as possible the number of files at Python package setup level.

- 2018/07/03
  Remove Git operations to avoid problem with offline installation

- 2018/05/18
  First version modified from cookiecutter-git to fit CoSApp need

## Credits

Based on cookiecutter [cookiecutter-git](https://github.com/nathanurwin/cookiecutter-git).

That work was carry out by Nathan Urwin and Dylan Yates.

## License

Copyright (C) 2017-2021 Safran - All Rights Reserved
Licensed under the Apache License, Version 2.0. See [LICENSE](https://gitlab.com/cosapp/cosapp-utils/cookiecutter-cosapp-workspace/blob/master/LICENSE) file.
Written by the CoSApp Team
