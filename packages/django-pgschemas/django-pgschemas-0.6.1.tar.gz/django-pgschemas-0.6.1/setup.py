# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_pgschemas',
 'django_pgschemas.contrib',
 'django_pgschemas.contrib.channels',
 'django_pgschemas.contrib.files',
 'django_pgschemas.management',
 'django_pgschemas.management.commands',
 'django_pgschemas.postgresql_backend',
 'django_pgschemas.test']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.0,<4.0', 'psycopg2>=2.7,<3.0']

setup_kwargs = {
    'name': 'django-pgschemas',
    'version': '0.6.1',
    'description': 'Multi-tenancy on Django using PostgreSQL schemas.',
    'long_description': 'django-pgschemas\n================\n\n.. image:: https://img.shields.io/badge/packaging-poetry-purple.svg\n    :alt: Packaging: poetry\n    :target: https://github.com/sdispater/poetry\n\n.. image:: https://img.shields.io/badge/code%20style-black-black.svg\n    :alt: Code style: black\n    :target: https://github.com/ambv/black\n\n.. image:: https://badges.gitter.im/Join%20Chat.svg\n    :alt: Join the chat at https://gitter.im/django-pgschemas\n    :target: https://gitter.im/django-pgschemas/community?utm_source=share-link&utm_medium=link&utm_campaign=share-link\n\n.. image:: https://github.com/lorinkoz/django-pgschemas/workflows/code/badge.svg\n    :alt: Build status\n    :target: https://github.com/lorinkoz/django-pgschemas/actions\n\n.. image:: https://readthedocs.org/projects/django-pgschemas/badge/?version=latest\n    :alt: Documentation status\n    :target: https://django-pgschemas.readthedocs.io/\n\n.. image:: https://coveralls.io/repos/github/lorinkoz/django-pgschemas/badge.svg?branch=master\n    :alt: Code coverage\n    :target: https://coveralls.io/github/lorinkoz/django-pgschemas?branch=master\n\n.. image:: https://badge.fury.io/py/django-pgschemas.svg\n    :alt: PyPi version\n    :target: http://badge.fury.io/py/django-pgschemas\n\n.. image:: https://pepy.tech/badge/django-pgschemas/month\n    :alt: Downloads\n    :target: https://pepy.tech/project/django-pgschemas/month\n\n|\n\nThis app uses PostgreSQL schemas to support data multi-tenancy in a single\nDjango project. It is a fork of `django-tenants`_ with some conceptual changes:\n\n- There are static tenants and dynamic tenants. Static tenants can have their\n  own apps and urlconf.\n- Tenants can be simultaneously routed via subdomain and via subfolder on shared\n  subdomain.\n- Public is no longer the schema for storing the main site data. Public should\n  be used only for true shared data across all tenants. Table "overriding" via\n  search path is no longer encouraged.\n- Management commands can be run on multiple schemas via wildcards - the\n  multiproc behavior of migrations was extended to just any tenant command.\n\n.. _django-tenants: https://github.com/tomturner/django-tenants\n\n\nDocumentation\n-------------\n\nhttps://django-pgschemas.readthedocs.io/\n\nContributing\n------------\n\n- Join the discussion at https://gitter.im/django-pgschemas/community.\n- PRs are welcome! If you have questions or comments, please use the link\n  above.\n- To run the test suite run ``make`` or ``make coverage``. The tests for this\n  project live inside a small django project called ``dpgs_sandbox``. Database\n  password and database host can be set through the environment variables\n  ``DATABASE_PASSWORD`` and ``DATABASE_HOST``.\n\nCredits\n-------\n\n* Tom Turner for `django-tenants`_\n* Bernardo Pires for `django-tenant-schemas`_\n\n.. _django-tenants: https://github.com/tomturner/django-tenants\n.. _django-tenant-schemas: https://github.com/bernardopires/django-tenant-schemas\n',
    'author': 'Lorenzo Peña',
    'author_email': 'lorinkoz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lorinkoz/django-pgschemas',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
