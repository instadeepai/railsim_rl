# railsim_rl

To run pre-commit hooks and mypy then download the following:

```
python3 -m pip install mypy==0.991
pip install pre-commit
pre-commit install
````

To run the pre-commit hooks on all files then you can run the following:
```
pre-commit run --all-files
```

To run mypy only you can run
```
mypy
````

Pre-commit hooks will run automatically at commit on staged files only.
