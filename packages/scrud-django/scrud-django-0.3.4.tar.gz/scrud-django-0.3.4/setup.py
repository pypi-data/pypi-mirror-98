# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scrud_django', 'scrud_django.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django-cors-headers>=3.6.0,<4.0.0',
 'django-jsonfield>=1.4.1,<2.0.0',
 'django-scoped-rbac>=0.3.0,<0.4.0',
 'django>=2.2.8,<3.0.0',
 'djangorestframework>=3.11.0,<4.0.0',
 'fastjsonschema>=2.14.5,<3.0.0',
 'psycopg2>=2.8.6,<3.0.0',
 'python-decouple>=3.3,<4.0',
 'python-dotenv>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'scrud-django',
    'version': '0.3.4',
    'description': 'A Django REST Framework app for Semantic CRUD.',
    'long_description': None,
    'author': 'David Charboneau',
    'author_email': 'david@openteams.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.6,<4.0.0',
}


setup(**setup_kwargs)
