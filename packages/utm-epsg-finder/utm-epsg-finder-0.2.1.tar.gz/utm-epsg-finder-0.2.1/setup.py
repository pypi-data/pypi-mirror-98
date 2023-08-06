# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['utm_epsg_finder']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'geopandas>=0.8.2,<0.9.0',
 'pathlib>=1.0.1,<2.0.0',
 'pyproj>=3.0.0,<4.0.0',
 'rasterio>=1.2.1,<2.0.0',
 'twine>=3.3.0,<4.0.0',
 'utm>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['utm-epsg-finder = utm_epsg_finder.cli:main']}

setup_kwargs = {
    'name': 'utm-epsg-finder',
    'version': '0.2.1',
    'description': 'Python Boilerplate contains all the boilerplate you need to create a modern Python package.',
    'long_description': "# UTM EPSG Finder\n[![PyPI - Version](https://img.shields.io/pypi/v/utm-epsg-finder.svg)](https://pypi.python.org/pypi/utm-epsg-finder)\n[![PyPI - License](https://img.shields.io/pypi/l/utm-epsg-finder.svg)](https://pypi.python.org/pypi/utm-epsg-finder)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/utm-epsg-finder.svg)](https://pypi.python.org/pypi/utm-epsg-finder)\n[![Tests](https://github.com/GIS-Consultant/utm-epsg-finder/workflows/tests/badge.svg)](https://github.com/GIS-Consultant/utm-epsg-finder/actions?workflow=tests)\n[![codecov](https://codecov.io/gh/GIS-Consultant/utm-epsg-finder/branch/master/graph/badge.svg?token=CFA8VDHT8W)](https://codecov.io/gh/GIS-Consultant/utm-epsg-finder)\n[![Read the Docs](https://readthedocs.org/projects/utm-epsg-finder/badge/)](https://utm-epsg-finder.readthedocs.io/)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\n## Description\n**UTM EPSG Finder** allow the user to find the UTM's [EPSG](https://epsg.org/home.html) code from his vectors in [EPSG:4326](http://epsg.io/4326) and [ESPG:3857](http://epsg.io/3857).\nSometimes is useful to know the projected EPSG; as example when you will calculate the polygon's area or the distance between two points. In this case if your vectors are in 4326 or worst in 3857\nyou can't return a correct value. Remember that with Pseudo-Mercator is not optimal calculate area but if you use an UTM EPSG the output value from area calculation is more correct.\n\n**UTM EPSG Finder** is based on:\n- [GeoPandas](https://pypi.org/project/geopandas/)\n- [pyproj](https://pypi.org/project/pyproj/)\n- [shapely](https://shapely.readthedocs.io/en/latest/project.html)  \n- [rasterio](https://rasterio.readthedocs.io/en/latest/index.html)\n- [utm](https://pypi.org/project/utm/)\n\n\n## Feature\n- [x] Get UTM EPSG for lines\n- [x] Get UTM EPSG for points\n- [x] Get UTM EPSG for polygons\n- [x] Get UTM EPSG for raster\n\n## More\n* GitHub repo: <https://github.com/GIS-Consultant/utm-epsg-finder.git>\n* Documentation: <https://utm-epsg-finder.readthedocs.io>\n* Free software: MIT\n\n\n## Credits\n\nThis package was created with [Cookiecutter][cookiecutter] and the [fedejaure/cookiecutter-modern-pypackage][cookiecutter-modern-pypackage] project template.\n\n[cookiecutter]: https://github.com/cookiecutter/cookiecutter\n[cookiecutter-modern-pypackage]: https://github.com/fedejaure/cookiecutter-modern-pypackage\n\nThanks to [g2giovanni](https://github.com/g2giovanni) for the help to setting up the package.\n",
    'author': 'Massimiliano Moraca',
    'author_email': 'info@massimilianomoraca.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GIS-Consultant/utm-epsg-finder',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<3.10',
}


setup(**setup_kwargs)
