# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nullpom']

package_data = \
{'': ['*']}

install_requires = \
['lightgbm>=3.1.1,<4.0.0',
 'matplotlib==3.2.2',
 'pandas>=1.1,<1.2',
 'scikit-learn>=0.24.1,<0.25.0']

setup_kwargs = {
    'name': 'nullpom',
    'version': '0.1.0',
    'description': 'Library to easily run Null Importances.',
    'long_description': '[![Test with pytest](https://github.com/tenajima/nullpom/actions/workflows/pytest.yml/badge.svg)](https://github.com/tenajima/nullpom/actions/workflows/pytest.yml)\n[![Format with black](https://github.com/tenajima/nullpom/actions/workflows/black.yml/badge.svg)](https://github.com/tenajima/nullpom/actions/workflows/black.yml)\n\n# nullpom\n\nLibrary to easily run Null Importances.\n\n## About Null Importances\n\nNull Importances is feature selection process using target permutation tests actual importance significance against the distribution of feature importances when fitted to noise (shuffled target).\n\n### Detail\n- [paper](https://academic.oup.com/bioinformatics/article/26/10/1340/193348)\n- [kaggle notebook](https://www.kaggle.com/ogrellier/feature-selection-with-null-importances)\n- [japanese article](https://qiita.com/trapi/items/1d6ede5d492d1a9dc3c9)\n\n# Output\n![output](https://raw.githubusercontent.com/tenajima/nullpom/main/img/distribution_of_importance.png)\n\n# Basic usage\n\n```python\nfrom nullpom import run_null_importance\n\nresult = run_null_importance(\n    {"objective": "binary", "seed": 42},\n     X_train=X_train,\n    X_valid=X_valid,\n    y_train=y_train,\n    y_valid=y_valid,\n)\n```\n\n# Install\n```sh\npip install nullpom\n```\n',
    'author': 'tenajima',
    'author_email': 'tenajima@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tenajima/nullpom',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
