# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scrud_django', 'scrud_django.migrations', 'scrud_django.static']

package_data = \
{'': ['*']}

install_requires = \
['Whoosh>=2.7.4,<3.0.0',
 'django-cors-headers>=3.6.0,<4.0.0',
 'django-jsonfield-backport>=1.0.2,<2.0.0',
 'django-scoped-rbac>=0.3.0,<0.4.0',
 'django>=2.2.8,<3.0.0',
 'djangorestframework>=3.11.0,<4.0.0',
 'fastjsonschema>=2.14.5,<3.0.0',
 'python-decouple>=3.3,<4.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'safetydance-test>=0.1.4,<0.2.0']

setup_kwargs = {
    'name': 'scrud-django',
    'version': '0.3.3',
    'description': 'A Django REST Framework app for Semantic CRUD.',
    'long_description': None,
    'author': 'David Charboneau',
    'author_email': 'david@openteams.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/openteams/scrud-django',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
