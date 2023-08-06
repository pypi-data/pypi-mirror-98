# Businessman Package

How to update package:

Config token:

`~/.pypirc` :

```shell
[testpypi]
    username = __token__
    password = <token>
```

```shell
[gitlab]
  repository = https://gitlab.example.com/api/v4/projects/businessman/packages/pypi
  username = python package
  password = irsadqVsa-TRNkfkwvYe

```

execute setup:

```shell
python setup.py sdist bdist_wheel
```

release a new version:

```shell
python -m twine upload --repository testpypi dist/*
```

install package:

```shell
pip install -i https://test.pypi.org/simple/ businessman 
```
