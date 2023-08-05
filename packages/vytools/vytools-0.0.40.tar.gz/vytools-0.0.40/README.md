Tools for working with vy 

**Installation and Setup**

```bash
pip install vytools
```

To take advantage of autocompletion add the following to your ~/.bashrc file 

```bash
eval "$(register-python-argcomplete vytools)"
```

**Configuration**

vytools searches a set of directories for specialized "vy" components. These directories comprise the vy "context" which must be specified before vy can be used. In addition "secrets" directories and a "jobs" directory may need to be specified.

***CONTEXT PATHS***

Point to directories (comma separated) which contain the vy components with command line:
```bash
vytools --contexts "/some/path/to/contexts/dir,/path/to/another/contexts/dir"
```

Or in a python script
```python
import vytools
vytools.CONFIG.set('contexts',['/some/path/to/contexts/dir','/path/to/another/contexts/dir'])
```

***SECRETS***

Point to secrets directories (comma separated) with command line:
```bash
vytools --secrets "/some/path/to/secrets/dir,/path/to/another/secrets/dir"
```

Or in a python script
```python
import vytools
vytools.CONFIG.set('secrets',['/some/path/to/secrets/dir','/path/to/another/secrets/dir'])
```

A directory can be specified which contains files to be used with [docker build secrets](https://docs.docker.com/develop/develop-images/build_enhancements/#new-docker-build-secret-information). The filename in the directory is the secret id. The contents of the file are the actual secret. For example a file named "SOME_SECRET_ACCESS_TOKEN" and containing text "9s79fup9sdfu9f" could be used by a vy "stage" with this syntax:

```dockerfile
RUN --mount=type=secret,id=SOME_SECRET_ACCESS_TOKEN wget --header="Authorization: Bearer $(cat /run/secrets/SOME_SECRET_ACCESS_TOKEN)" https://some_url/some_artifact.tar.gz
```

***JOBS***
Vy places artifacts from each job into a jobs directory. Point to a default directory which will be populated with jobs artifacts:
```bash
vytools --jobs "/some/path/to/jobs/dir"
```

or use python
```python
import vytools
vytools.CONFIG.set('jobs','/some/path/to/jobs/dir')
```

**Table of Contents**

- [Usage](#usage)

## History

- Test


