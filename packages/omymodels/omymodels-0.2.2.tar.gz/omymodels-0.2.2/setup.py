# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omymodels', 'omymodels.gino']

package_data = \
{'': ['*']}

install_requires = \
['simple-ddl-parser>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['omm = omymodels.cli:main']}

setup_kwargs = {
    'name': 'omymodels',
    'version': '0.2.2',
    'description': 'O! My Models (omymodels) is a library to generate from SQL DDL Python Models for GinoORM.',
    'long_description': '\nO! My Models\n------------\n\n\n.. image:: https://img.shields.io/pypi/v/omymodels\n   :target: https://img.shields.io/pypi/v/omymodels\n   :alt: badge1\n \n.. image:: https://img.shields.io/pypi/l/omymodels\n   :target: https://img.shields.io/pypi/l/omymodels\n   :alt: badge2\n \n.. image:: https://img.shields.io/pypi/pyversions/omymodels\n   :target: https://img.shields.io/pypi/pyversions/omymodels\n   :alt: badge3\n \n\nO! My Models (omymodels) is a library to generate from SQL DDL Python Models for GinoORM (I hope to add several more ORMs in future).\n\nYou provide an input like:\n\n.. code-block:: sql\n\n\n   CREATE TABLE "users" (\n     "id" SERIAL PRIMARY KEY,\n     "name" varchar,\n     "created_at" timestamp,\n     "updated_at" timestamp,\n     "country_code" int,\n     "default_language" int\n   );\n\n   CREATE TABLE "languages" (\n     "id" int PRIMARY KEY,\n     "code" varchar(2) NOT NULL,\n     "name" varchar NOT NULL\n   );\n\nand you will get output:\n\n.. code-block:: python\n\n\n       from gino import Gino\n\n\n       db = Gino()\n\n\n       class Users(db.Model):\n\n           __tablename__ = \'users\'\n\n           id = db.Column(db.Integer(), autoincrement=True, primary_key=True)\n           name = db.Column(db.String())\n           created_at = db.Column(db.TIMESTAMP())\n           updated_at = db.Column(db.TIMESTAMP())\n           country_code = db.Column(db.Integer())\n           default_language = db.Column(db.Integer())\n\n\n       class Languages(db.Model):\n\n           __tablename__ = \'languages\'\n\n           id = db.Column(db.Integer(), primary_key=True)\n           code = db.Column(db.String(2))\n           name = db.Column(db.String())\n\nHow to install\n^^^^^^^^^^^^^^\n\n.. code-block:: bash\n\n\n       pip install omymodels\n\nHow to use\n^^^^^^^^^^\n\nFrom cli\n~~~~~~~~\n\n.. code-block:: bash\n\n\n       omm path/to/your.ddl\n\n       # for example\n       omm tests/test_two_tables.sql\n\nYou can define target path where to save models with **-t**\\ , **--target** flag:\n\n.. code-block:: bash\n\n\n       # for example\n       omm tests/test_two_tables.sql -t test_path/test_models.py\n\nSmall library is used for parse DDL- https://github.com/xnuinside/simple-ddl-parser.\n\nWhat to do if types not supported in O! My Models and you cannot wait until PR will be approved\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\nFirst of all, to parse types correct from DDL to models - they must be in types mypping, for Gino it exitst in this file:\n\nomymodels/gino/types.py  **types_mapping**\n\nIf you need to use fast type that not exist in mapping - just do a path before call code with types_mapping.update()\n\nfor example:\n\n.. code-block:: python\n\n\n       from omymodels.gino import types  types_mapping\n       from omymodels import create_gino_models\n\n       types.types_mapping.update({\'your_type_from_ddl\': \'db.TypeInGino\'})\n\n       ddl = "YOUR DDL with your custom your_type_from_ddl"\n\n       models = create_gino_models(ddl)\n\nHow to contribute\n-----------------\n\nPlease describe issue that you want to solve and open the PR, I will review it as soon as possible.\n\nAny questions? Ping me in Telegram: https://t.me/xnuinside \n\nChangelog\n---------\n\n**v0.2.0**\n\n\n#. Valid generating columns in models: autoincrement, default, type, arrays, unique, primary key and etc.\n#. Added creating **table_args** for indexes\n',
    'author': 'Iuliia Volkova',
    'author_email': 'xnuinside@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xnuinside/omymodels',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
