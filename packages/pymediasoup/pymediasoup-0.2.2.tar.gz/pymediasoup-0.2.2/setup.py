# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymediasoup',
 'pymediasoup.handlers',
 'pymediasoup.handlers.sdp',
 'pymediasoup.models']

package_data = \
{'': ['*']}

install_requires = \
['aiortc>=1.2.0,<2.0.0',
 'h264-profile-level-id>=1.0.0,<2.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'pyee>=8.1.0,<9.0.0',
 'sdp-transform>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'pymediasoup',
    'version': '0.2.2',
    'description': 'mediasoup python client',
    'long_description': '# PyMediasoup\n[![Python](https://img.shields.io/pypi/pyversions/pymediasoup)](https://www.python.org/)\n[![Pypi](https://img.shields.io/pypi/v/pymediasoup)](https://pypi.org/project/pymediasoup/)\n[![License](https://img.shields.io/pypi/l/pymediasoup)](https://github.com/skymaze/pymediasoup/blob/main/LICENSE)\n\n\n[mediasoup](https://mediasoup.org/) python client\n\n\n## Install\n```bash\npip3 install pymediasoup\n```\n\n## Usage\nPyMediasoup API design is similar to the official [mediasoup-client](https://github.com/versatica/mediasoup-client)\n\n```python\nfrom pymediasoup import Device\nfrom pymediasoup import AiortcHandler\n\n# Create a device\n# In order to generate the correct parameters, here should contain all the tracks you want to use\ntracks = []\ndevice = Device(handlerFactory=AiortcHandler.createFactory(tracks=tracks))\n```\n\n## LICENSE\nMIT',
    'author': 'Jiang Yue',
    'author_email': 'maze1024@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/skymaze/pymediasoup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
