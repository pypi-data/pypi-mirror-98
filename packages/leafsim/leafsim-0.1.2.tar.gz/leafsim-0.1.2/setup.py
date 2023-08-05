# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leaf']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.5,<3.0',
 'numpy>=1.20.0,<2.0.0',
 'pandas>=1.2.1,<2.0.0',
 'simpy>=4.0.0,<5.0.0',
 'tqdm>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'leafsim',
    'version': '0.1.2',
    'description': 'A simulator for Large Energy-Aware Fog computing environments.',
    'long_description': '# LEAF [![PyPI version](https://img.shields.io/pypi/v/leafsim.svg?color=52c72b)](https://pypi.org/project/leafsim/) [![Supported versions](https://img.shields.io/pypi/pyversions/leafsim.svg)](https://pypi.org/project/leafsim/) [![License](https://img.shields.io/pypi/l/leafsim.svg)](https://pypi.org/project/leafsim/)\n\nLEAF is a simulator for **L**arge **E**nergy-**A**ware **F**og computing environments.\nIt enables then modeling of complex application graphs in distributed, heterogeneous, and resource-constrained infrastructures.\nA special emphasis was put on the modeling of energy consumption (and soon carbon emissions).\n\nPlease visit the official [documentation](https://leaf.readthedocs.io) for more information and examples on this project.\n\n\n<p align="center">\n  <img src="/docs/_static/infrastructure.png">\n</p>\n\nThis Python implementation was ported from the [original Java protoype](https://www.github.com/birnbaum/leaf).\nAll future development will take place in this repository.\n\n\n## Installation\n\nYou can use LEAF either by directly cloning this repository or installing the latest release via [pip](https://pip.pypa.io/en/stable/quickstart/):\n\n```\n$ pip install leafsim\n```\n\n## What can I do with it?\n\nLEAF enables a high-level modeling of cloud, fog and edge computing environments.\nIt builds on top of [networkx](https://networkx.org/), a library for creating and manipulating complex networks,\nand [SimPy](https://simpy.readthedocs.io/en/latest/), a process-based discrete-event simulation framework.\n\nBesides allowing research on scheduling and placement algorithms on resource-constrained environments,\nLEAF puts a special focus on:\n\n- **Dynamic networks**: Simulate mobile nodes which can join or leave the network during the simulation.\n- **Power consumption modeling**: Model the power usage of individual compute nodes, network traffic and applications.\n- **Energy-aware algorithms**: Implement dynamically adapting task placement strategies, routing policies, and other energy-saving mechanisms.\n- **Scalability**: Model the execution of thousands of compute nodes and applications in magnitudes faster than real time.\n\nPlease visit the official [documentation](https://leaf.readthedocs.io) for more information and examples on this project.\n\n\n## Publications\n\nThe paper behind LEAF is accepted for publication:\n- Philipp Wiesner and Lauritz Thamsen. "[LEAF: Simulating Large Energy-Aware Fog Computing Environments](https://arxiv.org/abs/2103.01170)" To appear in the Proceedings of the *5th IEEE International Conference on Fog and Edge Computing (ICFEC)*. IEEE, 2021.\n',
    'author': 'Philipp Wiesner',
    'author_email': 'wiesner@tu-berlin.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dos-group/leaf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.9,<4.0.0',
}


setup(**setup_kwargs)
