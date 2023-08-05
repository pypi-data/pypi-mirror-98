# starfish-py

![](https://github.com/datacraft-dsc/starfish-py/workflows/testing/badge.svg)
[![GitHub contributors](https://img.shields.io/github/contributors/datacraft-dsc/starfish-py.svg)](https://github.com/datacraft-dsc/starfish-py/graphs/contributors)
[![datacraft-chain Version](https://img.shields.io/badge/datacraft--chain-release-blue.svg)](https://github.com/datacraft-dsc/datacraft-chain)

---

## Table of Contents

  - [About](#about)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Quickstart](#quickstart)
  - [Environment variables](#environment-variables)
  - [Testing](#testing)
  - [New Version](#new-version)
  - [Mailing Lists](#mailing-list)
  - [Maintainers](#maintainers)
  - [License](#license)

---

## About

Starfish is an open-sourced developer toolkit for the data economy. Available in flavours of Java, Python, and Clojure, it allows developers, data scientists and enterprises to create, interact, integrate and manage a data supply line through standardised and simple-to-use APIs.

Based on an underlying data ecosystem standard, Starfish provides high-level APIs for common tasks within the data economy, for example, registering/publishing an asset, for subsequent use in a data supply line. In this case, an asset can be any data set, model or data service. The high-level API also allows developers to invoke operation on an asset, e.g. computing a predictive model or anonymising sensitive personal information, among other capabilities.

Starfish works with blockchain networks, such as Ocean Protocol, and common web services through agents, allowing unprecedented flexibility in asset discovery and data supply line management.

Starfish-py provides user access and tools to work with the Ocean Protocol Network, delegating certain functions via the python library squid-py.

While we strive to deliver code at a high quality, please note, that there exist parts of the library that still need thorough testing.
Contributions – whether it is in the form of new features, better documentation or tests – are welcome.

## Prerequisites

Python >= 3.6

## Development

1. Clone this repo

    ```bash
    clone https://github.com/datacraft-dsc/starfish-py.git
    cd starfish-py
    ```

1. Set up a virtual environment

    ```bash
    virtualenv venv
    source venv/bin/activate
    ```

1. Install package requirements for starfish

    ```bash
    make install
    ```

1. Run the unit tests, without any supporting software/libraries outside of starfish

    ```bash
    make test_unit
    ```

1. Create the local testing environment using [datacraft-chain](https://github.com/datacraft-dsc/datacraft-chain).

    In a seperate terminal session you need to clone and checkout ```datacraft-chain``` repository, by doing the following:
    ```
    git clone https://github.com/datacraft-dsc/datacraft-chain.git
    cd datacraft-chain
    ./start_datacraft_chain.sh test
    ```

1. Run the integration tests

    ```
    pytest tests/integration
    ```

1. Run the all tests

    ```bash
    make tests
    ```

## Documentation

1. Build Sphinx documentation

    To build the Syphinx auto documentation, you need to do the following:
    ```bash
    make docs
    ```

The [documentation](https://datacraft-dsc.github.io/starfish-py) for this repo.


## Testing

Automatic tests are setup via github actions.
Our test use pytest framework.
The testing uses a datacraft-chain docker image and surfer server.
See [github actions for testing](https://github.com/datacraft-dsc/starfish-py/blob/release/.github/workflows/testing.yml)

## New Version

The `bumpversion.sh` script helps to bump the project version. You can execute the script using as first argument {major|minor|patch} to bump accordingly the version.

## Mailing Lists

  * [starfish-qa](developer@datacraft.sg) -- General questions regarding the usage of Starfish.

## Release Process

See [Release Process](https://github.com/datacraft-dsc/starfish-py/blob/develop/RELEASE_PROCESS.md)


## Maintainers

 [Developer Datacraft team](developer@datacraft-dsc.sg)


## License

```
Copyright 2018-2021 Datacraft Pte. Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
