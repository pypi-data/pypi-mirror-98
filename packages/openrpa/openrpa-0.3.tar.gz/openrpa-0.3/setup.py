# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openrpa']

package_data = \
{'': ['*']}

install_requires = \
['craft-text-detector>=0.3.3,<0.4.0',
 'mss>=6.1.0,<7.0.0',
 'numpy>=1.20.1,<2.0.0',
 'opencv-python>=4.5.1.48,<5.0.0.0',
 'pynput>=1.7.3,<2.0.0',
 'pytesseract>=0.3.7,<0.4.0',
 'regex>=2020.11.13,<2021.0.0']

setup_kwargs = {
    'name': 'openrpa',
    'version': '0.3',
    'description': 'Pixel based automation library testbed',
    'long_description': '# OpenRPA\nPixel based automation library\n\n<pre>\nchannels:\n  - conda-forge\n  - pytorch\n  - fcakyon\ndependencies:\n  - python=3.7.5\n  - python-mss=6.1.0\n  - numpy=1.20.1\n  - craft-text-detector=0.3.3\n  - tesseract=4.1.1\n  - pytesseract=0.3.7\n  - opencv=4.5.1\n  - regex=2020.11.13\n  - pynput=1.7.1\n  - pyobjc-core=6.2.2\n</pre>',
    'author': 'Teppo Koskinen',
    'author_email': 'teppo@robocorp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
