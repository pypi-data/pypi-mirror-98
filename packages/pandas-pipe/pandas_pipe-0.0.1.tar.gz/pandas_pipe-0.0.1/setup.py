# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_pipe']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.2,<2.0.0', 'pandas>=1.1.5', 'scikit-lego>=0.6.1']

setup_kwargs = {
    'name': 'pandas-pipe',
    'version': '0.0.1',
    'description': 'routine pandas method chain links wrapped with scikit-lego',
    'long_description': '# Purpose\n[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)\n* a collection of pandas DataFrame methods and functions I commonly used decorated with [scikit-lego](https://scikit-lego.readthedocs.io/en/latest/index.html)\'s `@log_step` to enable logging within method chaining\n* Wanted to use the logging of common pandas methods across projects\n* Inspired from Vincent D. Warmerdam\'s PyData Eindhoven 2019 talk titled [Untitled12.ipynb](https://www.youtube.com/watch?v=yXGCKqo5cEY)\n* See the [docs for pandas pipelines of scikit-lego](https://scikit-lego.readthedocs.io/en/latest/pandas_pipeline.html) to view the general use case for `@log_step`\n*  See `examples/demo.ipynb` for a few workflows and links to other relevant SE questions\n```python\nIn [1]: import pandas as pd; import numpy as np; import logging\n\nIn [2]: import pandas_pipe\n\nIn [3]: stream_handler = logging.StreamHandler()\n\nIn [4]: pandas_pipe.logger.addHandler(stream_handler)\n\nIn [5]: dataf_input = pd.DataFrame(\n   ...:     {\n   ...:         "aaa": {0: 10, 1: 11, 2: 12, 3: 13},\n   ...:         "myid": {0: 1, 1: 2, 2: 3, 3: 4},\n   ...:         "num": {0: "1, 2, 3", 1: np.nan, 2: "1, 2", 3: np.nan},\n   ...:         "text": {0: "aa, bb, cc", 1: np.nan, 2: "cc, dd", 3: "ee"},\n   ...:         "states": {\n   ...:             0: "Wyoming; Illinois; New Hampshire",\n   ...:             1: "Pennsylvania",\n   ...:             2: "New York",\n   ...:             3: "Pennsylvania",\n   ...:         },\n   ...:     }\n   ...: )\n\nIn [6]: dataf_input\nOut[6]: \n   aaa  myid      num        text                            states\n0   10     1  1, 2, 3  aa, bb, cc  Wyoming; Illinois; New Hampshire\n1   11     2      NaN         NaN                      Pennsylvania\n2   12     3     1, 2      cc, dd                          New York\n3   13     4      NaN          ee                      Pennsylvania\n\nIn [7]: (\n   ...:     dataf_input.pipe(pandas_pipe.start_pipeline)\n   ...:     .pipe(pandas_pipe.explode_setup, columns=["num", "text"], delimiter=",")\n   ...:     .pipe(pandas_pipe.explode_setup, columns=["states"], delimiter=";")\n   ...:     .pipe(pandas_pipe.explode, column="num", ignore_index=False)\n   ...:     .pipe(pandas_pipe.explode, column="text", ignore_index=False)\n   ...:     .pipe(pandas_pipe.explode, column="states", ignore_index=False)\n   ...:     .pipe(pandas_pipe.drop_duplicates)\n   ...: )\n[start_pipeline(df)] time=0:00:00.000152 n_obs=4, n_col=5 names=[\'aaa\', \'myid\', \'num\', \'text\', \'states\']\n[explode_setup(df, columns = [\'num\', \'text\'], delimiter = \',\')] time=0:00:00.001107 n_obs=4, n_col=5 delta=(0, 0)\n[explode_setup(df, columns = [\'states\'], delimiter = \';\')] time=0:00:00.000466 n_obs=4, n_col=5 delta=(0, 0)\n[explode(df, column = \'num\', ignore_index = False)] time=0:00:00.003697 n_obs=7, n_col=5 delta=(+3, 0)\n[explode(df, column = \'text\', ignore_index = False)] time=0:00:00.002642 n_obs=15, n_col=5 delta=(+8, 0)\n[explode(df, column = \'states\', ignore_index = False)] time=0:00:00.002184 n_obs=33, n_col=5 delta=(+18, 0)\n[drop_duplicates(df)] time=0:00:00.001671 n_obs=33, n_col=5 delta=(0, 0)\nOut[7]: \n   aaa  myid  num text          states\n0   10     1    1   aa         Wyoming\n0   10     1    1   aa        Illinois\n0   10     1    1   aa   New Hampshire\n0   10     1    1   bb         Wyoming\n0   10     1    1   bb        Illinois\n0   10     1    1   bb   New Hampshire\n0   10     1    1   cc         Wyoming\n0   10     1    1   cc        Illinois\n0   10     1    1   cc   New Hampshire\n0   10     1    2   aa         Wyoming\n0   10     1    2   aa        Illinois\n0   10     1    2   aa   New Hampshire\n0   10     1    2   bb         Wyoming\n0   10     1    2   bb        Illinois\n0   10     1    2   bb   New Hampshire\n0   10     1    2   cc         Wyoming\n0   10     1    2   cc        Illinois\n0   10     1    2   cc   New Hampshire\n0   10     1    3   aa         Wyoming\n0   10     1    3   aa        Illinois\n0   10     1    3   aa   New Hampshire\n0   10     1    3   bb         Wyoming\n0   10     1    3   bb        Illinois\n0   10     1    3   bb   New Hampshire\n0   10     1    3   cc         Wyoming\n0   10     1    3   cc        Illinois\n0   10     1    3   cc   New Hampshire\n1   11     2  NaN  NaN    Pennsylvania\n2   12     3    1   cc        New York\n2   12     3    1   dd        New York\n2   12     3    2   cc        New York\n2   12     3    2   dd        New York\n3   13     4  NaN   ee    Pennsylvania\n```',
    'author': 'Benjamin Datko',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bdatko/panda_pipe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
