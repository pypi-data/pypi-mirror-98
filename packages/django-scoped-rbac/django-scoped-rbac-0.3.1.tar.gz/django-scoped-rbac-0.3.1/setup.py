# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scoped_rbac', 'scoped_rbac.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django-rest-framework-condition>=0.1.0,<0.2.0',
 'django>=2.2.8,<3.0.0',
 'djangorestframework>=3.11.0,<4.0.0',
 'drf-extensions>=0.6.0,<0.7.0',
 'psycopg2>=2.8.6,<3.0.0',
 'scrudful>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'django-scoped-rbac',
    'version': '0.3.1',
    'description': 'A rich and flexible Django application for role-based access control within distinct access control scopes supporting Django Rest Framework.',
    'long_description': None,
    'author': 'David Charboneau',
    'author_email': 'david@adadabase.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/openteams/django-scoped-rbac',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
