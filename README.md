# Exercise auto checker
Simple python script to simplify the process of running the same unit-tests over different implementations where each 
implementation is placed in a different directory.

Originally I used this script tp grade students Python projects (The script is very convenient to check Python 
exercises, where I want to execute the same unit tests suite against different solutions).

## Installation
1. Use `pip` to install all the requirements
    ```bash
    pip install -r requirements.txt
    ``` 

## Usage
1. Add all your test files and resources into your "test" directory.
2. Place all the exercises under your "exercises" directory (each exercise in different folder).
3. Execute:
    ```bash
    python ex_checker.py --ex_dir=ExChecker/ex --tests_dir=ExChecker/tests
    ```
## Example
See the `example` directory.

## Author
Nir Moshe
