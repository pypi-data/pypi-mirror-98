# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recital_client',
 'recital_client.api',
 'recital_client.api.background_tasks',
 'recital_client.api.document_viewer',
 'recital_client.api.entities',
 'recital_client.api.extract_configuration',
 'recital_client.api.extract_models',
 'recital_client.api.extract_predictions',
 'recital_client.api.extract_task_results',
 'recital_client.api.extract_tasks',
 'recital_client.api.file_items',
 'recital_client.api.file_versions',
 'recital_client.api.folders',
 'recital_client.api.folders_content',
 'recital_client.api.hierarchy',
 'recital_client.api.html_representations',
 'recital_client.api.indexing',
 'recital_client.api.indexing_tasks',
 'recital_client.api.metadata_import',
 'recital_client.api.metadata_value_assignment',
 'recital_client.api.named_entities',
 'recital_client.api.organizations',
 'recital_client.api.regex_validation',
 'recital_client.api.reports',
 'recital_client.api.search',
 'recital_client.api.search_bar_autocomplete',
 'recital_client.api.search_history',
 'recital_client.api.version_contents',
 'recital_client.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.1.0,<21.0.0',
 'httpx>=0.15.0,<0.16.0',
 'python-dateutil>=2.8.1,<3.0.0']

setup_kwargs = {
    'name': 'recital-client',
    'version': '0.1.0',
    'description': 'A client library for accessing recital',
    'long_description': '# recital-client\nA client library for accessing recital\n\n## Usage\nFirst, create a client:\n\n```python\nfrom recital_client import Client\n\nclient = Client(base_url="https://api.example.com")\n```\n\nIf the endpoints you\'re going to hit require authentication, use `AuthenticatedClient` instead:\n\n```python\nfrom recital_client import AuthenticatedClient\n\nclient = AuthenticatedClient(base_url="https://api.example.com", token="SuperSecretToken")\n```\n\nNow call your endpoint and use your models:\n\n```python\nfrom recital_client.models import MyDataModel\nfrom recital_client.api.my_tag import get_my_data_model\nfrom recital_client.types import Response\n\nmy_data: MyDataModel = get_my_data_model.sync(client=client)\n# or if you need more info (e.g. status_code)\nresponse: Response[MyDataModel] = get_my_data_model.sync_detailed(client=client)\n```\n\nOr do the same thing with an async version:\n\n```python\nfrom recital_client.models import MyDataModel\nfrom recital_client.async_api.my_tag import get_my_data_model\nfrom recital_client.types import Response\n\nmy_data: MyDataModel = await get_my_data_model.asyncio(client=client)\nresponse: Response[MyDataModel] = await get_my_data_model.asyncio_detailed(client=client)\n```\n\nThings to know:\n1. Every path/method combo becomes a Python module with four functions:\n    1. `sync`: Blocking request that returns parsed data (if successful) or `None`\n    1. `sync_detailed`: Blocking request that always returns a `Request`, optionally with `parsed` set if the request was successful.\n    1. `asyncio`: Like `sync` but the async instead of blocking\n    1. `asyncio_detailed`: Like `sync_detailed` by async instead of blocking\n     \n1. All path/query params, and bodies become method arguments.\n1. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)\n1. Any endpoint which did not have a tag will be in `recital_client.api.default`    \n\n## Building / publishing this Client\nThis project uses [Poetry](https://python-poetry.org/) to manage dependencies  and packaging.  Here are the basics:\n1. Update the metadata in pyproject.toml (e.g. authors, version)\n1. If you\'re using a private repository, configure it with Poetry\n    1. `poetry config repositories.<your-repository-name> <url-to-your-repository>`\n    1. `poetry config http-basic.<your-repository-name> <username> <password>`\n1. Publish the client with `poetry publish --build -r <your-repository-name>` or, if for public PyPI, just `poetry publish --build`\n\nIf you want to install this client into another project without publishing it (e.g. for development) then:\n1. If that project **is using Poetry**, you can simply do `poetry add <path-to-this-client>` from that project\n1. If that project is not using Poetry:\n    1. Build a wheel with `poetry build -f wheel`\n    1. Install that wheel from the other project `pip install <path-to-wheel>`',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
