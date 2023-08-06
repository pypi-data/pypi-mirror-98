# Maquette Py

This project contains the Python implementation of Maquette which includes the CLI and a SDK


## Developing maquette-py

`maquette-py` uses [Poetry](https://python-poetry.org/) for dependency management and is packaged with [PyInstaller](https://www.pyinstaller.org/). The minimal requirements for a developer workspace are [Conda](https://docs.conda.io/en/latest/miniconda.html) and [Poetry](https://python-poetry.org/docs/#installation).

```
$ git clone $REPOSITORY_URL
$ cd maquette-py
$ conda create -p ./environment python=3.8

$ poetry install
```

## Maquette CLI
The CLI is documented within the CLI. Sounds funny but a good starting point is following command
```
$ mq --help
```
###Projects
#### Report Code Quality
```
$ mq projects report-cq [packge_names, script.py, ...]
```
the `report-cq` command sends code quality information to the Maquette Hub...

to report the Pytest-Coverage, pytest has to be run previously with following parameters
```
$ python -m pytest cov=<your-packages> > test/test-report.log
```

## Maquette SDK