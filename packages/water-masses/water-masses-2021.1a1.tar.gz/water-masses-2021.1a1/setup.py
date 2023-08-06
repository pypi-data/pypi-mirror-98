# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['water_masses', 'water_masses.tracmass']

package_data = \
{'': ['*'], 'water_masses': ['data/*']}

install_requires = \
['cf-xarray>=0.5.1,<0.6.0',
 'cftime>=1.2.1,<1.3.0',
 'cmocean>=2.0,<3.0',
 'dask>=2020.12.0,<2021.0.0',
 'h5netcdf>=0.10.0,<0.11.0',
 'intake-xarray>=0.4.0,<0.5.0',
 'intake>=0.6.0,<0.7.0',
 'matplotlib>=3.3.2,<4.0.0',
 'nc-time-axis>=1.2.0,<2.0.0',
 'netcdf4==1.5.4',
 'numpy>=1.19.2,<2.0.0',
 'pandas>=1.1.3,<2.0.0',
 'scipy>=1.5.4,<1.6.0',
 'statsmodels>=0.12.0,<0.13.0',
 'xarray>=0.16.1,<0.17.0']

setup_kwargs = {
    'name': 'water-masses',
    'version': '2021.1a1',
    'description': 'On the origin of water masses in the northern European shelf seas from a Lagrangian perspective',
    'long_description': '# WIP: water-masses\n\n[![Build Status](https://travis-ci.com/shelf-sea/water-masses.svg?branch=master)](https://travis-ci.com/shelf-sea/water-masses)\n[![Coverage](https://coveralls.io/repos/github/shelf-sea/water-masses/badge.svg?branch=master)](https://coveralls.io/github/shelf-sea/water-masses?branch=master)\n[![Python Version](https://img.shields.io/pypi/pyversions/water-masses.svg)](https://pypi.org/project/water-masses/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nOn the origin of water masses in the northern European shelf seas from a Lagrangian perspective\n\n\n## Features\n\n- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n- Add yours!\n\n\n## Installation\n\n```bash\npip install water-masses\n# or\npoetry add git+https://github.com/shelf-sea/water-masses.git#master\n```\n\n\n## Example\n\nShowcase how your project can be used:\n\n```python\nfrom water_masses.example import some_function\n\nprint(some_function(3, 4))\n# => 7\n```\n\n## License\n\n[gpl3](https://github.com/shelf-sea/water-masses/blob/master/LICENSE)\n\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [5a686829afd7b6f54cb2170ed3072eee8e296ec0](https://github.com/wemake-services/wemake-python-package/tree/5a686829afd7b6f54cb2170ed3072eee8e296ec0). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/5a686829afd7b6f54cb2170ed3072eee8e296ec0...master) since then.\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shelf-sea/water-masses',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
