# python-download-files-by-map
download files using a json tree map

## Installation
```
pip install download-files-by-map
```

## Usage
```
$ download-files-by-map jsonfile
```
## map file format
- map file is a json file, with the following structure, it is either:
  - a file object
  - a folder object
  - an array of file and/or folder objects
- Sample map file: [sample-map.json](sample-map.json)
### file object
- file object contains 3 attributes:
  - type - must be equal to 'file'
  - local_filename - filename to save into local directory tree
  - remote_url - url to the remote file to be retrieved

- Example:
```
  {
  "remote_url": "http://download-server-123/file1.txt",
  "local_filename": "file1.txt",
  "type": "file"
  }
```
### folder object
- folder object contains 3 attributes:
  - type - must be equal to 'folder'
  - local_filename - directory name to be created in local
  - children - an array contains files and/or folders to be children of current folder
```
  {
    "type": "folder",
    "local_filename": "sample",
    "children": [
      ... files or folders object
    ]
  },

```


## Links
- https://pypi.org/project/download-files-by-map/
- https://github.com/siakhooi/python-download-files-by-map
- https://sonarcloud.io/project/overview?id=siakhooi_python-download-files-by-map

## Badges
![GitHub](https://img.shields.io/github/license/siakhooi/python-download-files-by-map?logo=github)
![GitHub last commit](https://img.shields.io/github/last-commit/siakhooi/python-download-files-by-map?logo=github)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/siakhooi/python-download-files-by-map?logo=github)
![GitHub issues](https://img.shields.io/github/issues/siakhooi/python-download-files-by-map?logo=github)
![GitHub closed issues](https://img.shields.io/github/issues-closed/siakhooi/python-download-files-by-map?logo=github)
![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/siakhooi/python-download-files-by-map?logo=github)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed-raw/siakhooi/python-download-files-by-map?logo=github)
![GitHub top language](https://img.shields.io/github/languages/top/siakhooi/python-download-files-by-map?logo=github)
![GitHub language count](https://img.shields.io/github/languages/count/siakhooi/python-download-files-by-map?logo=github)
![Lines of code](https://img.shields.io/tokei/lines/github/siakhooi/python-download-files-by-map?logo=github)
![GitHub repo size](https://img.shields.io/github/repo-size/siakhooi/python-download-files-by-map?logo=github)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/siakhooi/python-download-files-by-map?logo=github)

![Workflow](https://img.shields.io/badge/Workflow-github-purple)
![workflow](https://github.com/siakhooi/python-download-files-by-map/actions/workflows/build.yaml/badge.svg)
![workflow](https://github.com/siakhooi/python-download-files-by-map/actions/workflows/workflow-deployments.yml/badge.svg)

![Release](https://img.shields.io/badge/Release-github-purple)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/siakhooi/python-download-files-by-map?label=GPR%20release&logo=github)
![GitHub all releases](https://img.shields.io/github/downloads/siakhooi/python-download-files-by-map/total?color=33cb56&logo=github)
![GitHub Release Date](https://img.shields.io/github/release-date/siakhooi/python-download-files-by-map?logo=github)

![Quality-Sonar](https://img.shields.io/badge/Quality-SonarCloud-purple)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_python-download-files-by-map&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=siakhooi_python-download-files-by-map)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_python-download-files-by-map&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=siakhooi_python-download-files-by-map)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_python-download-files-by-map&metric=bugs)](https://sonarcloud.io/summary/new_code?id=siakhooi_python-download-files-by-map)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_python-download-files-by-map&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=siakhooi_python-download-files-by-map)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_python-download-files-by-map&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=siakhooi_python-download-files-by-map)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_python-download-files-by-map&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=siakhooi_python-download-files-by-map)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_python-download-files-by-map&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=siakhooi_python-download-files-by-map)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_python-download-files-by-map&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=siakhooi_python-download-files-by-map)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_python-download-files-by-map&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=siakhooi_python-download-files-by-map)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_python-download-files-by-map&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=siakhooi_python-download-files-by-map)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=siakhooi_python-download-files-by-map&metric=coverage)](https://sonarcloud.io/summary/new_code?id=siakhooi_python-download-files-by-map)
![Sonar Violations (short format)](https://img.shields.io/sonar/violations/siakhooi_python-download-files-by-map?server=https%3A%2F%2Fsonarcloud.io)
![Sonar Violations (short format)](https://img.shields.io/sonar/blocker_violations/siakhooi_python-download-files-by-map?server=https%3A%2F%2Fsonarcloud.io)
![Sonar Violations (short format)](https://img.shields.io/sonar/critical_violations/siakhooi_python-download-files-by-map?server=https%3A%2F%2Fsonarcloud.io)
![Sonar Violations (short format)](https://img.shields.io/sonar/major_violations/siakhooi_python-download-files-by-map?server=https%3A%2F%2Fsonarcloud.io)
![Sonar Violations (short format)](https://img.shields.io/sonar/minor_violations/siakhooi_python-download-files-by-map?server=https%3A%2F%2Fsonarcloud.io)
![Sonar Violations (short format)](https://img.shields.io/sonar/info_violations/siakhooi_python-download-files-by-map?server=https%3A%2F%2Fsonarcloud.io)
![Sonar Violations (long format)](https://img.shields.io/sonar/violations/siakhooi_python-download-files-by-map?format=long&server=http%3A%2F%2Fsonarcloud.io)

[![Generic badge](https://img.shields.io/badge/Funding-BuyMeACoffee-33cb56.svg)](https://www.buymeacoffee.com/siakhooi)
[![Generic badge](https://img.shields.io/badge/Funding-Ko%20Fi-33cb56.svg)](https://ko-fi.com/siakhooi)

![visitors](https://hit-tztugwlsja-uc.a.run.app/?outputtype=badge&counter=ghmd-python-download-files-by-map)
