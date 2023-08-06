# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdapisp']

package_data = \
{'': ['*']}

install_requires = \
['aiocache>=0.11.1,<0.12.0',
 'aiosqlite>=0.17.0,<0.18.0',
 'databases>=0.4.2,<0.5.0',
 'fastapi>=0.63.0,<0.64.0',
 'pandas>=1.2.3,<2.0.0',
 'pytest>=6.2.2,<7.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'sqlalchemy>=1.4.0,<2.0.0',
 'typer[all]>=0.3.2,<0.4.0',
 'uvicorn>=0.13.4,<0.14.0']

entry_points = \
{'console_scripts': ['mdapisp = mdapisp.main:typer_app']}

setup_kwargs = {
    'name': 'mdapisp',
    'version': '0.1.1a3',
    'description': 'simple api for Make Data API Server Project',
    'long_description': '# mdapisp\n\n## Project description\n* This is a code snippet level code that roughly implements the CSV file upload and SQL Select Query functions.\n\n## Execution environment\n* written and tested in Python 3.7.3 (via pyenv virtual environment)\n* if you are using pip as your package manager\n```bash\n pip install mdapisp\n```\n* if you are using poetry as your package manager\n```bash\n poetry install\n```\n## How to run\n* The basic execution scenario is as follows:\n    1. Type the command in the terminal to run the application.\n        ```bash\n        mdapisp\n        ```\n    1. Open to fastapi swegger test page (default http://127.0.0.1:8000/docs#/) with a web browser\n    1. Upload human.csv, fruit.csv using Create Upload Csvfiles\n    1. Select query using Read Table\n    1. Check cache contents using Read Cache\n    1. Upload csvfile again and check cache contents\n\n##  architecture design & the reason for design\n* Focused on __minimum difficulty and minimum cost implementation__ to meet the requirements specification.\n    * only the logic for the api was written without implementing a web server (ex. nginx, apache, etc.), the database also used __sqlite__, and it was written as lightly as possible using __fastapi__ to avoid swegger implementation.\n\n## api specification\n* api.md\n* If you want to exact api specification, Please refer to `http://127.0.0.1:8000/redoc` or the __openapi.json__ file in the directory for the exact specification',
    'author': 'Minseong Kim',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
