# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlvtk',
 'mlvtk.base',
 'mlvtk.base.callbacks',
 'mlvtk.base.normalize',
 'mlvtk.base.plot']

package_data = \
{'': ['*']}

install_requires = \
['h5py>=2.10.0,<2.11.0',
 'pandas>=1.1.3,<1.2.0',
 'plotly>=4.9.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'tensorflow>=2.3.2,<2.4.2',
 'tqdm>=4.50.2,<4.51.0']

setup_kwargs = {
    'name': 'mlvtk',
    'version': '1.0.3',
    'description': 'loss surface visualization tool',
    'long_description': '# MLVTK  [![PyPI - Python Version](https://img.shields.io/badge/python-3.6.1%20|%203.7%20|%203.8%20|%203.9-brightgreen)](https://badge.fury.io/py/mlvtk) ![PyPI](https://img.shields.io/pypi/v/mlvtk?color=brightgreen&label=PyPI)\n### A loss surface visualization tool\n\n\n<img alt="Png" src="https://raw.githubusercontent.com/tm-schwartz/mlvtk/dev/visuals/adamax.png" width="80%" />\n\n_Simple DNN trained on MNIST data set, using Adamax optimizer_\n\n---\n\n<img alt="Gif" src="https://raw.githubusercontent.com/tm-schwartz/mlvtk/dev/visuals/gifs/sgd3.gif" width="80%" />\n\n_Simple DNN trained on MNIST, using SGD optimizer_\n\n---\n\n<img alt="Gif" src="https://raw.githubusercontent.com/tm-schwartz/mlvtk/dev/visuals/gifs/adam2.gif" width="80%" />\n\n_Simple DNN trained on MNIST, using Adam optimizer_\n\n---\n\n<img alt="Gif" src="https://raw.githubusercontent.com/tm-schwartz/mlvtk/dev/visuals/gifs/sgd1.gif" width="80%" />\n\n_Simple DNN trained on MNIST, using SGD optimizer_\n\n\n\n\n## Why?\n\n- :shipit: **Simple**: A single line addition is all that is needed.\n- :question: **Informative**: Gain insight into what your model is seeing.\n- :notebook: **Educational**: *See* how your hyper parameters and architecture impact your\n  models perception.\n\n\n## Quick Start\n\nRequires | version\n-------- | -------\npython | >= 3.6.1 \ntensorflow | >= 2.3.1, <  2.4.2\nplotly | >=4.9.0\n\nInstall locally (Also works in google Colab!):\n```sh\npip install mlvtk\n```\n\nOptionally for use with jupyter notebook/lab:\n\n*Notebook*\n---\n```sh\npip install "notebook>=5.3" "ipywidgets==7.5"\n```\n\n*Lab*\n---\n```sh\npip install jupyterlab "ipywidgets==7.5"\n\n# Basic JupyterLab renderer support\njupyter labextension install jupyterlab-plotly@4.10.0\n\n# OPTIONAL: Jupyter widgets extension for FigureWidget support\njupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget@4.10.0\n```\n\n### Basic Example\n\n```python\nfrom mlvtk.base import Vmodel\nimport tensorflow as tf\nimport numpy as np\n\n# NN with 1 hidden layer\ninputs = tf.keras.layers.Input(shape=(None,100))\ndense_1 = tf.keras.layers.Dense(50, activation=\'relu\')(inputs)\noutputs = tf.keras.layers.Dense(10, activation=\'softmax\')(dense_1)\n_model = tf.keras.Model(inputs, outputs)\n\n# Wrap with Vmodel\nmodel = Vmodel(_model)\nmodel.compile(optimizer=tf.keras.optimizers.SGD(),\nloss=tf.keras.losses.CategoricalCrossentropy(), metrics=[\'accuracy\'])\n\n# All tf.keras.(Model/Sequential/Functional) methods/properties are accessible\n# from Vmodel\n\nmodel.summary()\nmodel.get_config()\nmodel.get_weights()\nmodel.layers\n\n# Create random example data\nx = np.random.rand(3, 10, 100)\ny = np.random.randint(9, size=(3, 10, 10))\nxval = np.random.rand(1, 10, 100)\nyval = np.random.randint(9, size=(1,10,10))\n\n# Only difference, model.fit requires validation_data (tf.data.Dataset, or\n# other container\nhistory = model.fit(x, y, validation_data=(xval, yval), epochs=10, verbose=0)\n\n# Calling model.surface_plot() returns a plotly.graph_objs.Figure\n# model.surface_plot() will attempt to display the figure inline\n\nfig = model.surface_plot()\n\n# fig can save an interactive plot to an html file,\nfig.write_html("surface_plot.html")\n\n# or display the plot in jupyter notebook/lab or other compatible tool.\nfig.show()\n```\n',
    'author': 'tm-schwartz',
    'author_email': 'tschwartz@csumb.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
