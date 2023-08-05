# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ampel', 'ampel.ztf.archive', 'ampel.ztf.t0']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3,<1.4',
 'psycopg2-binary>=2.8.6,<3.0.0',
 'sqlalchemy-stubs>=0.4,<0.5']

entry_points = \
{'console_scripts': ['ampel-ztf-archive-consumer-groups = '
                     'ampel.ztf.archive.ArchiveDB:consumer_groups_command']}

setup_kwargs = {
    'name': 'ampel-ztf-archive',
    'version': '0.7.0a0',
    'description': 'ZTF alert archive for the Ampel system',
    'long_description': '\n\n<img align="left" src="https://desycloud.desy.de/index.php/s/6gJs9bYBG3tWFDz/preview" width="150" height="150"/>  \n<br>\n\n# ZTF alert archive for AMPEL\n\nThis package provides an API to store the elements of ZTF alerts in a postgres\ndatabase, de-duplicating repeated elements of the alert history. It also\nsupports basic history queries by object id, sky coordinates, and time.\n',
    'author': 'Jakob van Santen',
    'author_email': 'jakob.van.santen@desy.de',
    'maintainer': 'Jakob van Santen',
    'maintainer_email': 'jakob.van.santen@desy.de',
    'url': 'https://ampelproject.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
