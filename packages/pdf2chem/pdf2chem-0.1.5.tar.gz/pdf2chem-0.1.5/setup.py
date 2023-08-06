# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pdf2chem']
install_requires = \
['CIRpy>=1.0.2,<2.0.0',
 'ChemDataExtractor>=1.3.0,<2.0.0',
 'DateTime>=4.3,<5.0',
 'pandas==1.1.5',
 'textract>=1.6.3,<2.0.0']

setup_kwargs = {
    'name': 'pdf2chem',
    'version': '0.1.5',
    'description': 'A curator for chemistry-related pdf files',
    'long_description': '# pdf2chem\n\n![](https://github.com/johngoeltz/pdf2chem/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/johngoeltz/pdf2chem/branch/main/graph/badge.svg)](https://codecov.io/gh/johngoeltz/pdf2chem) ![Release](https://github.com/johngoeltz/pdf2chem/workflows/Release/badge.svg) [![Documentation Status](https://readthedocs.org/projects/pdf2chem/badge/?version=latest)](https://pdf2chem.readthedocs.io/en/latest/?badge=latest)\n\nA curator for chemistry-related pdf files\n\n## Installation\n\n```bash\n$ pip install pdf2chem\n$ cde data download\n```\n\n```Jupyter_or_Colab\nin Jupyter or Colab\n\n!pip install pdf2chem\n!cde data download\nimport pdf2chem as p2c\n```\n\n\n## Features\n\n- This version allows the user to curate a folder of chemistry-related pdf files, extracting known chemicals mentioned in the files to csv files with the names as written in the pdf and the SMILES string for each chemical.  Other outputs (e.g., InChI or other known names for the chemical) are possible and may be incorporated into future versions.\n\n- The package should automatically detect local vs. hosted runtimes and choose the compatible pdf extraction method in textract.\n\n## Dependencies\n\n- The package directly uses cirpy, ChemDataExtractor, pandas, os, re, time, datetime, and sys in addition to native Python 3.  Many of these in turn have a fair few dependencies of their own.\n\n## Usage\n\n- Place pdf files of interest (typically journal articles) in an accessible folder.\nExecute p2c.curate_folder()\nIf the files are not in the current directory, pass the directory to the function as an argument, e.g.\np2c.curate_folder(\'C:/Users/kfrog/literature\')\nThe files will then be analyzed internally before a list of words and phrases suspected to be known chemicals is sent to NIH\'s servers to be resolved.  Chemicals found and their SMILES strings will be aggregated in a csv file for each pdf.\nAfter each pdf is processed, the data from each csv file will be combined to an aggregated csv file for all the papers in that run.\n\n- Please note: this program depends on both stable internet access and uptime/responsiveness at NIH\'s servers.  The latter are often slower or down entirely on the weekends, and sometimes this is seen during the week as well.  We appreciate the team there making the databases as accessible as they do.\n\n## Documentation\n\nThe official documentation is hosted on Read the Docs: https://pdf2chem.readthedocs.io/en/latest/\n\n## Contributors\n\nWe welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/johngoeltz/pdf2chem/graphs/contributors).\n\n### Credits\n\nThis package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).\n\nThis package makes heavy use of ChemDataExtractor and CIRpy, packages developed by Swain and Cole and released under the MIT license.\nSwain, M. C., & Cole, J. M. "ChemDataExtractor: A Toolkit for Automated Extraction of Chemical Information from the Scientific Literature", J. Chem. Inf. Model. 2016, 56 (10), pp 1894–1904 10.1021/acs.jcim.6b00207\n',
    'author': 'johngoeltz',
    'author_email': '80011540+johngoeltz@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/johngoeltz/pdf2chem',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
