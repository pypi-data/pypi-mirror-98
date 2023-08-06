# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hydrus',
 'hydrus.data',
 'hydrus.data.migrations',
 'hydrus.samples',
 'hydrus.tests',
 'hydrus.tests.functional',
 'hydrus.tests.unit']

package_data = \
{'': ['*']}

install_requires = \
['Flask-Cors>=3.0.8,<3.1.0',
 'Flask-RESTful>=0.3.7,<0.4.0',
 'Flask-SocketIO>=4.2.1,<4.3.0',
 'Flask>=1.1.1,<1.2.0',
 'Jinja2>=2.10.3,<2.11.0',
 'Mako>=1.1.0,<1.2.0',
 'MarkupSafe>=1.1.1,<1.2.0',
 'PyYAML>=5.2,<5.3',
 'SQLAlchemy>=1.3.12,<1.4.0',
 'Werkzeug>=0.16.0,<0.17.0',
 'alembic>=1.0.10,<1.1.0',
 'aniso8601>=3.0.2,<3.1.0',
 'appdirs>=1.4.3,<1.5.0',
 'blinker>=1.4,<1.5',
 'certifi>=2019.11.28,<2019.12.0',
 'click>=7.1.2,<7.2.0',
 'flake8>=3.8.3,<3.9.0',
 'gevent-websocket>=0.10.1,<0.11.0',
 'gevent>=20.12.0,<20.13.0',
 'greenlet>=0.4.17,<0.5.0',
 'hydra_openapi_parser>=0.2',
 'hydra_python_core>=0.2',
 'itsdangerous>=1.1.0,<1.2.0',
 'lifter>=0.4.1,<0.5.0',
 'packaging>=19.2,<19.3',
 'pep8>=1.7.1,<1.8.0',
 'persisting-theory>=0.2.1,<0.3.0',
 'psycopg2-binary>=2.8.6,<2.9.0',
 'pyparsing>=2.4.6,<2.5.0',
 'pytest>=5.4.1,<5.5.0',
 'python-dateutil>=2.8.1,<2.9.0',
 'python-editor>=1.0.4,<1.1.0',
 'python-engineio>=3.11.2,<3.12.0',
 'python-socketio>=4.4.0,<4.5.0',
 'pytz>=2019.3,<2019.4',
 'six>=1.13.0,<1.14.0',
 'thespian>=3.9.11,<3.10.0']

setup_kwargs = {
    'name': 'hydrus',
    'version': '0.4.1',
    'description': 'Hydra Ecosystem Flagship Server. Deploy REST data for Web 3.0',
    'long_description': None,
    'author': 'Hydra Ecosystem',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5.2,<4.0.0',
}


setup(**setup_kwargs)
