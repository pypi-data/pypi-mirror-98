# lintwork

[![Actions Status](https://github.com/craftslab/lintwork/workflows/CI/badge.svg?branch=master&event=push)](https://github.com/craftslab/lintwork/actions?query=workflow%3ACI)
[![Docker](https://img.shields.io/docker/pulls/craftslab/lintwork)](https://hub.docker.com/r/craftslab/lintwork)
[![License](https://img.shields.io/github/license/craftslab/lintwork.svg?color=brightgreen)](https://github.com/craftslab/lintwork/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/lintwork.svg?color=brightgreen)](https://pypi.org/project/lintwork)
[![Tag](https://img.shields.io/github/tag/craftslab/lintwork.svg?color=brightgreen)](https://github.com/craftslab/lintwork/tags)



## Introduction

*lintwork* is a lint worker of *[lintflow](https://github.com/craftslab/lintflow/)* written in Python.



## Prerequisites

- gRPC >= 1.36.0
- Python >= 3.7.0



## Run

- **Local mode**

```bash
git clone https://github.com/craftslab/lintwork.git

cd lintwork
pip install -Ur requirements.txt
python work.py --config-file="config.yml" --lint-project="project" --output-file="output.json"
```



- **Service mode**

```bash
git clone https://github.com/craftslab/lintwork.git

cd lintwork
pip install -Ur requirements.txt
python work.py --config-file="config.yml" --listen-url="127.0.0.1:9090"
```



## Docker

- **Local mode**

```bash
git clone https://github.com/craftslab/lintwork.git

cd lintwork
docker build --no-cache -f Dockerfile -t craftslab/lintwork:latest .
docker run -it -v /tmp:/tmp craftslab/lintwork:latest ./lintwork--config-file="config.yml" --lint-project="/tmp/project" --output-file="/tmp/output.json"
```



- **Service mode**

```bash
git clone https://github.com/craftslab/lintwork.git

cd lintwork
docker build --no-cache -f Dockerfile -t craftslab/lintwork:latest .
docker run -it -p 9090:9090 craftslab/lintwork:latest ./lintwork --config-file="config.yml" --listen-url="127.0.0.1:9090"
```



## Usage

```
usage: work.py [-h] --config-file CONFIG_FILE
               [--lint-project LINT_PROJECT | --listen-url LISTEN_URL]
               [--output-file OUTPUT_FILE] [-v]

Lint Work

optional arguments:
  -h, --help            show this help message and exit
  --config-file CONFIG_FILE
                        config file (.yml)
  --lint-project LINT_PROJECT
                        lint project (/path/to/project)
  --listen-url LISTEN_URL
                        listen url (host:port)
  --output-file OUTPUT_FILE
                        output file (.json|.txt|.xlsx)
  -v, --version         show program's version number and exit
```



## Settings

*lintwork* parameters can be set in the directory [config](https://github.com/craftslab/lintwork/blob/master/lintwork/config).

An example of configuration in [config.yml](https://github.com/craftslab/lintwork/blob/master/lintwork/config/config.yml):

```yaml
apiVersion: v1
kind: worker
metadata:
  name: lintwork
spec:
  aosp:
    sdk:
      - Correctness
      - Correctness:Messages
      - Security
      - Compliance
      - Performance
      - Performance:Application Size
      - Usability:Typography
      - Usability:Icons
      - Usability
      - Productivity
      - Accessibility
      - Internationalization
      - Internationalization:Bidirectional Text
```



## Design

![design](design.png)



## Errorformat

- **Error type**

```
E: Error
I: Information
W: Warning
```

- **JSON format**

```json
{
  "lintwork": [
    {
      "file": "name",
      "line": 1,
      "type": "Error",
      "details": "text"
    }
  ]
}
```

- **Text format**

```text
lintwork:{file}:{line}:{type}:{details}
```



## License

Project License can be found [here](LICENSE).



## Reference

- [Android lint](https://developer.android.com/studio/write/lint)
- [errorformat](https://github.com/reviewdog/errorformat)
- [gRPC](https://grpc.io/docs/languages/python/)
- [protocol-buffers](https://developers.google.com/protocol-buffers/docs/proto3)
- [reviewdog](https://github.com/reviewdog/reviewdog)
