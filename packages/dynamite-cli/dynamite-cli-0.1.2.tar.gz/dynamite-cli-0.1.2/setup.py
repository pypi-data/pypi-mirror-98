# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dynamite_cli']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.3,<2.0.0', 'colorama>=0.4.4,<0.5.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['dynamite-cli = dynamite_cli.main:app']}

setup_kwargs = {
    'name': 'dynamite-cli',
    'version': '0.1.2',
    'description': '',
    'long_description': "# Dynamite-cli\n\nA cli to copy dynamo table items to another table\n\n## Requirements\nYou need [poetry](https://python-poetry.org/) as a dependency manager\n\n## Installation\n`pip install dynamite-cli`\n\n## Usage\nYou can print an help menu with `dynamite-cli --help`\n\nThe **source table**, **source region**, **source profile** and **destination table** are `required` fields  \nIf you don't specify a destination **region** and/or a destination **profile**, the source one are used.\n\nThe `profile` field is used to retrieve the credentials to connect to your AWS account. So you need at least one account configured in your `.aws/credentials` file (*aws_access_key_id*, and *aws_secret_access_key*)\n\n\n> NOTE: the tables should have the same schema\n\nExample:\n`dynamite-cli <SRC_TABLE> <SRC_REGION> <SRC_PROFILE> <DST_TABLE> [DST_REGION] [DST_PROFILE]`\n",
    'author': 'softwarebloat',
    'author_email': 'softwarebloat@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/softwarebloat/dynamite-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
