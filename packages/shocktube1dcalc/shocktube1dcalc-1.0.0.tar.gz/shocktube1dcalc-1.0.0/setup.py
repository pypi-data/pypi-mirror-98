# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shocktube1dcalc']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=7.19.0,<8.0.0',
 'matplotlib>=3.3.3,<4.0.0',
 'numpy>=1.19.5,<2.0.0',
 'scipy>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'shocktube1dcalc',
    'version': '1.0.0',
    'description': '1D shocktube caculator to provide analytic solutions',
    'long_description': "[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# 1D shocktube caculator\nThis tool provides 1D Shock Tube solutions. You may output analytic solutions, or numeric solutions backed by CESE\nmethod, *Sin-Chung Chang, “The Method of Space-Time Conservation Element and Solution Element – A New Approach for\nSolving the Navier-Stokes and Euler Equations”, Journal of Computational Physics, Volume 119, Issue 2, July 1995, Pages 295-324. doi: 10.1006/jcph.1995.1137*.\n\n## Getting Started\n\n### Prerequisites\n* [Python](https://www.python.org/downloads/)\n* numpy\n* scipy\n\n## Usage\n### Analytic Solution\n```python\nfrom shocktube1dcalc import solver_analytic\n\n# by default it will create a the shock tube based on Sod's classic condition.\nshocktube = solver_analytic.ShockTube()\n\nimport numpy as np\nmesh = np.linspace(-0.5, 0.5, 50)\n\nanalytic_solution = shocktube.get_analytic_solution(\n    mesh, t=0.4\n)\n```\n\n\nYou may customize the physical status of the shocktube via:\n```python\nshocktube = solver_analytic.ShockTube(rho_left=1.0, u_left=0.0, p_left=1.0, rho_right=0.125, u_right=0.0, p_right=0.1)\n```\n\n\n### Numeric Solution\n```python\nfrom shocktube1dcalc import cese\n\nelapsed_time = 0.4\ncese_grid_size_t = 0.004\n# multiply 2 for half grids, so total iteration number should be double\niteration_number = round(elapsed_time / cese_grid_size_t * 2)\n\nshocktube = cese.ShockTube(iteration=iteration_number, grid_size_t=cese_grid_size_t)\nshocktube.run_cese_iteration()\n\nnumeric_solution = shocktube.data.solution\n```\n\n## Contributing\nSee [Contributing](contributing.md)\n\n## Authors\nTaihsiang Ho (tai271828) <tai271828@gmail.com>\n\n\nCreated from [Lee-W/cookiecutter-python-template](https://github.com/Lee-W/cookiecutter-python-template/tree/0.7.1) version 0.7.1\n",
    'author': 'Taihsiang Ho (tai271828)',
    'author_email': 'tai271828@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
