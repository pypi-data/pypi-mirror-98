# Businessman Package

How to update package:

Config token:

`~/.pypirc` :

```editorconfig
[testpypi]
    username = __token__
    password = <token>
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
