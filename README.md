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


### Docker commands

## Build docker image
docker build . -f railsim.Dockerfile -t rl_railsim_cuda

## Start the container
docker run -it --name rl_railsim -v .:/app rl_railsim

docker run -it --name railsim_cuda -v .:/app railsim_cuda
2


 
pip install grpcio-tools

## protoc commaand to compile the proto file and generate the python classes
python -m grpc_tools.protoc --proto_path=DummyEnv/src/main/proto --python_out=RL/env_wrapper2 --grpc_python_out=RL/env_wrapper2 railsim.proto --pyi_out=RL/env_wrapper2


