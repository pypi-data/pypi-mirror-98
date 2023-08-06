# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyopenfisheries']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.5,<3.0']

setup_kwargs = {
    'name': 'pyopenfisheries',
    'version': '0.1.1',
    'description': ' PyOpenFisheries makes it even easier to access the OpenFisheries API in Python. A good usecase of this library is to gather data to plot in a Jupyter Notebook, or to collect data to run time-series analysis on.',
    'long_description': '# PyOpenFisheries\n\nPyOpenFisheries makes it even easier to access the [OpenFisheries API](https://github.com/OpenFisheries/api.openfisheries.org) in Python.\n\nA good usecase of this library is to gather data to plot in a Jupyter Notebook, or to collect data to run time-series analysis on.\n\n![Screenshot](Sphinx-docs/example.png)\n\n\nLearn more about [OpenFisheries.org](openfisheries.org).\n\n#### this package depends on [Requests](https://pypi.org/project/requests/).\n\n\n# Documentation\n## pyopenfisheries.pyopenfisheries module\n\n\n### class pyopenfisheries.pyopenfisheries.PyOpenFisheries(\\*\\*kwargs)\nBases: `object`\n\nBase class for accessing the OpenFisheries API.\nUseful for gathering data for plots or analysis.\n\nReturns:\n\n    instance: base OpenFisheries API wrapper\n\nExamples:\n\n\n    >>> open_fish_conn = PyOpenFisheries()\n    >>> skipjack_tuna = open_fish_conn.annual_landings(species="SKJ").filter_years(start_year=1970,end_year=1991)\n    >>> print(skipjack_tuna.landings)\n    [{\'year\': 1970, \'catch\': 402166}...{\'year\': 1991, \'catch\': 1575170}]\n    >>> print(skipjack_tuna.summarize())\n    Landings of SKJ globally from 1970 to 1991\n\n\nAttributes:\n\n    landings: List of dictionaries containing the year and landing count.\n    species: if present - three-letter ASFIS species code (i.e. “SKJ” - Skipjack Tuna).\n    country: if present - ISO-3166 alpha 3 country code (i.e. “USA” - United States).\n    start_year: if present - start year of filtered landings data.\n    end_year : if present - end year of filtered landings data.\n\n\n#### annual_landings(species=None, country=None)\nGathers annual fishery landings filtered by either species or\ncountry. If neither fish nor country are specified, then this\nwill return global aggregate landings data.\n\nArgs:\n\n    species: three-letter ASFIS species code (i.e. “SKJ” - Skipjack Tuna)\n    country: ISO-3166 alpha 3 country code (i.e. “USA” - United States)\n\nReturns:\n\n    instance: PyOpenFisheries instance with landings populated\n\n\n#### filter_years(start_year=1950, end_year=2018)\nFilters annual fishing data to within a time-frame.\n\nArgs:\n\n    start_year: 4 digit integer year (i.e. 1980)\n    end_year: 4 digit integer year (i.e. 2015)\n\nReturns:\n\n    instance: PyOpenFisheries instance with years filtered.\n\n\n#### summarize()\nSummarizes what has been returned from OpenFisheries.\n\n#### label()\nUseful as a legend / for plots.\n',
    'author': 'Henry Kobin',
    'author_email': 'henry.kobin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HenryKobin/PyOpenFisheries',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
