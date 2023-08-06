# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recital',
 'recital.api',
 'recital.api.background_tasks',
 'recital.api.document_viewer',
 'recital.api.extract_configuration',
 'recital.api.extract_models',
 'recital.api.extract_predictions',
 'recital.api.extract_task_results',
 'recital.api.extract_tasks',
 'recital.api.file_items',
 'recital.api.file_versions',
 'recital.api.folders',
 'recital.api.folders_content',
 'recital.api.hierarchy',
 'recital.api.html_representations',
 'recital.api.indexing',
 'recital.api.indexing_tasks',
 'recital.api.metadata_import',
 'recital.api.metadata_value_assignment',
 'recital.api.named_entities',
 'recital.api.organizations',
 'recital.api.regex_validation',
 'recital.api.reports',
 'recital.api.search',
 'recital.api.search_bar_autocomplete',
 'recital.api.search_history',
 'recital.api.version_contents',
 'recital.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.1.0,<21.0.0',
 'httpx>=0.15.4,<0.18.0',
 'python-dateutil>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'recital-client',
    'version': '0.2.1',
    'description': 'A client library for accessing recital',
    'long_description': '# reciTAL Client\n\nA client library for accessing reciTAL\'s API. :tada:\n\n## Installation\n\nIt\'s easy. Don\'t worry.:smiley:\n\nYou just need to run the following:\n\n```bash\npip install recital\n```\n\n## Usage\n\nFirst, you\'ll need to create the client:\n\n```python\nfrom recital import RecitalClient\n\nclient = RecitalClient(username="username", password="password")\n```\n\nNow call your endpoint and use your models:\n\n```python\nfrom recital.models import MyDataModel\nfrom recital.api.my_tag import get_my_data_model\nfrom recital.types import Response\n\nmy_data: MyDataModel = get_my_data_model.sync(client=client)\n# or if you need more info (e.g. status_code)\nresponse: Response[MyDataModel] = get_my_data_model.sync_detailed(client=client)\n```\n\nOr do the same thing with an async version:\n\n```python\nfrom recital.models import MyDataModel\nfrom recital.api.my_tag import get_my_data_model\nfrom recital.types import Response\n\nmy_data: MyDataModel = await get_my_data_model.asyncio(client=client)\nresponse: Response[MyDataModel] = await get_my_data_model.asyncio_detailed(client=client)\n```\n\nThings to know:\n1. Every path/method combo becomes a Python module with four functions:\n    1. `sync`: Blocking request that returns parsed data (if successful) or `None`\n    1. `sync_detailed`: Blocking request that always returns a `Request`, optionally with `parsed` set if the request was successful.\n    1. `asyncio`: Like `sync` but the async instead of blocking\n    1. `asyncio_detailed`: Like `sync_detailed` by async instead of blocking\n\n1. All path/query params, and bodies become method arguments.\n1. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)\n1. Any endpoint which did not have a tag will be in `recital.api.default`\n\n## Building / publishing this Client\nThis project uses [Poetry](https://python-poetry.org/) to manage dependencies  and packaging.  Here are the basics:\n1. Update the metadata in pyproject.toml (e.g. authors, version)\n1. If you\'re using a private repository, configure it with Poetry\n    1. `poetry config repositories.<your-repository-name> <url-to-your-repository>`\n    1. `poetry config http-basic.<your-repository-name> <username> <password>`\n1. Publish the client with `poetry publish --build -r <your-repository-name>` or, if for public PyPI, just `poetry publish --build`\n\nIf you want to install this client into another project without publishing it (e.g. for development) then:\n1. If that project **is using Poetry**, you can simply do `poetry add <path-to-this-client>` from that project\n1. If that project is not using Poetry:\n    1. Build a wheel with `poetry build -f wheel`\n    1. Install that wheel from the other project `pip install <path-to-wheel>`\n',
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
