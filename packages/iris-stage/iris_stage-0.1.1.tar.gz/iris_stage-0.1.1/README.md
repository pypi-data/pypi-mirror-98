# Iris Staging Client
[![PyPI version](https://badge.fury.io/py/iris-stage.svg)](https://pypi.org/project/iris-stage/) [![Lint](https://github.com/Incuvers/iris-staging/actions/workflows/lint.yaml/badge.svg)](https://github.com/Incuvers/iris-staging/actions/workflows/lint.yaml)

![img](/docs/img/Incuvers-black.png)

Modified: 2021-03

## Quickstart
Save AWS certs and IRIS machine certs to your home directory. See [.aws guide](.aws/README.md) and [.secrets guide](.secrets/README.md) for instructions.

Install the latest `iris-stage` package:
```bash
python3 -m pip install --upgrade pip
...
python3 -m pip install --no-cache iris-stage
```
Launch the staging client:
```bash
stage
```
Halt the client:
```bash
unstage
```

## Iris Stage Client Deployment
The recommended deployment method for the iris staging client is hosted on the [Incuvers/automation](https://github.com/Incuvers/automation) repository using ansible. Follow the setup instructions and proceed with the iris staging client deployment.

## Client Requirements
This client is designed to be run on an iris production machine. All the hardware and peripherals should be mounted and ready for integration testing.

### AWS Services
The AWS Python SDK `boto3` requires AWS user tokens and region information. To avoid passing these tokens at runtime and increasing the complexity of the build process I have required that the AWS credentials and configuration are bound to the staging client. Therefore these credentials will exist in the `$HOME` directory as described [here](.aws/README.md)

### IRIS Machine Credentials
The IRIS snap requires production grade machine credentials. I have required that the machine credentials are bound to the staging client in the `$HOME` directory as described [here](.secrets/README.md). These credentials must be production grade as the snap is built pointing to our production api.

## Development
A brief development guide is detailed [here](/docs/dev.md)