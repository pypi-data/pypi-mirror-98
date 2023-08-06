# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nesim']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nesim',
    'version': '0.0.4',
    'description': 'Paquete de python que permite simular de una red de computadoras.',
    'long_description': '# nesim\n\nPaquete de python diseñado para simular una red de computadoras.\n\n## Instalación\n\n```cmd\npip install nesim\n```\n\n## Documentación\n\nPara más información visite nuestra [documentación official](https://nesim.readthedocs.io/en/latest/).\n\n## Autores\n\n- Jorge Morgado Vega, [jorge.morgadov@gmail.com](jorge.morgadov@gmail.com)\n- Roberto García Rodríguez, [roberto.garcia@estudiantes.matcom.uh.cu](roberto.garcia@estudiantes.matcom.uh.cu)\n',
    'author': 'Jorge Morgado Vega',
    'author_email': 'jorge.morgadov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jmorgadov/nesim',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
