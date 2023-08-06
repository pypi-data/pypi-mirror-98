# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beth',
 'beth.ai',
 'beth.evaluation',
 'beth.models',
 'beth.players',
 'beth.tree']

package_data = \
{'': ['*']}

install_requires = \
['black>=20.8b1,<21.0',
 'chess>=1.4.0,<2.0.0',
 'comet-ml>=3.3.3,<4.0.0',
 'ipykernel>=5.4.3,<6.0.0',
 'ipython>=7.20.0,<8.0.0',
 'ipywidgets>=7.6.3,<8.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.3.4,<4.0.0',
 'numpy>=1.20.1,<2.0.0',
 'openpyxl>=3.0.6,<4.0.0',
 'pandas>=1.2.2,<2.0.0',
 'pytest>=6.2.2,<7.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'seaborn>=0.11.1,<0.12.0',
 'snakeviz>=2.1.0,<3.0.0',
 'torch>=1.7.1,<2.0.0',
 'tqdm>=4.56.2,<5.0.0',
 'xlrd>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'beth',
    'version': '0.2.0',
    'description': 'Open source chess AI framework',
    'long_description': "# ♟ Welcome to ``beth`` documentation\n\n![](assets/beth_home.png)\n\n``beth`` is an open source chess AI framework. Like many, I re-discovered the game of chess by watching the Netflix show **the Queen's Gambit**. As a Data Scientist, it made we want to learn and explore the beauty of the game. \n\nAt first my goal was to develop algorithms to help me learn chess. But over time, it lead to developing more and more features. What you will find is my personal experiments open sourced as a chess framework. I hope this framework to be ideal for chess programmers in Python to ease the development of new algorithms and engines.\n\n\n> This repo is under active development, many features are still experimental.\n> But please fill free to fork or PR\n\n## Installation\nYou can install the library from PyPi with: \n```\npip install beth\n```\nOr clone and install from source\n\n## Features\n- Definition of a game environment using ``python-chess`` framework, with move parsing, board-to-numpy abstractions, PGN records, move replay. \n- Playing chess in Jupyter notebooks with widgets \n- Different player abstractions: ``HumanPlayer()``, ``RandomPlayer()``, ``AIPlayer()`` - to play Human vs AI, Human vs Human, or AI vs AI. \n- Connection to Stockfis engine to evaluate engine performances, available with ``StockfishAI()`` object abstraction\n- Rules-based engine ``TreeSearchAI()`` with minimax tree search, alpha beta pruning, move ordering and board heuristics (~ELO 1000)\n- First attempt of ML engine with a LSTM Neural Network to predict next moves\n\n### Next roadmap features\nIf you are interested, please drop an issue or a PR, or contact me by [email](mailto:theo.alves.da.costa@gmail.com). Meanwhile the roadmap for ``beth`` is:\n\n- Implementing a GUI (or connecting to an existing one) to ease experimentation\n- ELO or TrueSkill measurement for any engine\n- Improving minimax engine speed\n- Developing ML engines:\n  - Self supervised learning with Transformers\n  - Reinforcement Learning\n\n\n## Repo Structure\n```\n- beth/\n- data/\n    - raw/\n    - processed/\n- docs/                             # Documentation folder and website (.md, .ipynb) using Mkdocs\n- notebooks/                        # Jupyter notebooks only (.ipynb)\n- tests/                            # Unitary testing using pytest\n- .gitignore\n- LICENSE                           # MIT License\n- poetry.lock                       # Poetry lock file\n- pyproject.toml                    # Configuration file to export and package the library using Poetry\n```",
    'author': 'Theo Alves Da Costa',
    'author_email': 'theo.alves.da.costa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/theolvs/beth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.8,<4.0.0',
}


setup(**setup_kwargs)
