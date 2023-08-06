# mdapisp

## Project description
* This is a code snippet level code that roughly implements the CSV file upload and SQL Select Query functions.

## Execution environment
* written and tested in Python 3.7.3 (via pyenv virtual environment)
* if you are using pip as your package manager
```bash
 pip install mdapisp
```
* if you are using poetry as your package manager
```bash
 poetry install
```
## How to run
* The basic execution scenario is as follows:
    1. Type the command in the terminal to run the application.
        ```bash
        mdapisp
        ```
    1. Open to fastapi swegger test page (default http://127.0.0.1:8000/docs#/) with a web browser
    1. Upload human.csv, fruit.csv using Create Upload Csvfiles
    1. Select query using Read Table
    1. Check cache contents using Read Cache
    1. Upload csvfile again and check cache contents

##  architecture design & the reason for design
* Focused on __minimum difficulty and minimum cost implementation__ to meet the requirements specification.
    * only the logic for the api was written without implementing a web server (ex. nginx, apache, etc.), the database also used __sqlite__, and it was written as lightly as possible using __fastapi__ to avoid swegger implementation.

## api specification
* api.md
* If you want to exact api specification, Please refer to `http://127.0.0.1:8000/redoc` or the __openapi.json__ file in the directory for the exact specification