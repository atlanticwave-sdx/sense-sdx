# README

## Overview

This document provides instructions for installing dependencies and running unit tests for the `sense-sdx` module.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/sense-sdx.git
    cd sense-sdx
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the required dependencies along with the test dependencies using `pip`:
    ```bash
    pip install .[test]
    ```

    Alternatively, you can install in editable mode with test dependencies:
    ```bash
    pip install -e .[test]
    ```

    ## Running Unit Tests

    To run the unit tests for the `sense-sdx` module, use the following command:

    ```bash
    python -m unittest discover -s tests
    ```

    This command will automatically discover and execute all test cases in the `tests` directory. Ensure that you are in the root directory of the repository when running this command.

    To run an individual test case, specify the test module and test class/method. For example:

    ```bash
    python -m unittest tests.test_module.TestClass.test_method
    ```

    Replace `tests.test_module`, `TestClass`, and `test_method` with the appropriate module, class, and method names for the test you want to run.
