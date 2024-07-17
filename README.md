# Jenkins_Helper Python Script

## Introduction

> ###### This Python script provides a helper class, `Jenkins_Helper`, for interacting with a Jenkins server. Jenkins is an open-source automation server that enables developers to build, test, and deploy their software.

## Purpose

> ###### The `Jenkins_Helper` class is designed to simplify the process of connecting to a Jenkins server and performing operations. It encapsulates the details of establishing a connection and provides a high-level interface for interacting with the server.

## Required Arguments

> ###### The `Jenkins_Helper` constructor requires the following arguments:

> > - `JENKINS_URL` (str): The URL of the Jenkins server to connect to. default is `http://localhost:8080/`.
> > - `JENKINS_USERNAME` (str): The JENKINS_USERNAME to authenticate with. default is `admin`.
> > - `JENKINS_PASSWORD` (str): The JENKINS_PASSWORD to authenticate with. default is `admin`.
> > - `RESTORE` (bool): A flag indicating whether to restore the Jenkins configuration from a backup file. default is `False`.
> > - `BACKUP` (bool): A flag indicating whether to create a backup of the Jenkins configuration. default is `True`.
> > - `FILE_NAME` (str): The name of the backup file to create or restore from. default is `jenkins_data.json`.
> > - `BUILD_DEPTH` (int): The depth of the build history to include in the backup or restore operation. default is `3`.

## Prerequisites

> ###### Before you can use this script, you need to have the following installed:

> > - Python 3.x
> > - `requirements.txt` file containing the required packages. You can install the required packages by running the following command:

```bash
pip install -r requirements.txt
```

## Usage

```
python .\Jenkins_helper.py --JENKINS_URL=http://localhost:8080/ --JENKINS_USERNAME=USERNAME --JENKINS_PASSWORD=PASSWORD2 --RESTORE --FILE_NAME=jenkins_data.json --BUILD_DEPTH=3
# OR
python .\Jenkins_helper.py --JENKINS_URL=http://localhost:8080/ --JENKINS_USERNAME=USERNAME --JENKINS_PASSWORD=PASSWORD2 --BACKUP --FILE_NAME=jenkins_data.json --BUILD_DEPTH=3
```
## Output

> ###### The output of the script will depend on the specific operations you perform. For example, if you run the script with the `--RESTORE` option, it will restore the Jenkins configuration from a backup file and display a message indicating that the operation was successful. If you run the script with the `--BACKUP` option, it will create a backup of the Jenkins configuration and display a message indicating that the operation was successful.

## _Note_:
> ###### The `Jenkins_Helper` class provides a high-level interface for interacting with a Jenkins server. It encapsulates the details of establishing a connection and provides methods for performing operations such as creating a backup of the Jenkins configuration and restoring it from a backup file.
> Make sure to replace the `JENKINS_URL`, `JENKINS_USERNAME`, and `JENKINS_PASSWORD` with your Jenkins server details.


## Conclusion

> ###### The `Jenkins_Helper` class provides a convenient way to interact with a Jenkins server from Python. It encapsulates the details of establishing a connection and provides a high-level interface for performing operations on the server.

## References

> > - Jenkins: https://www.jenkins.io/
> > - python-jenkins package: https://pypi.org/project/python-jenkins/