# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flow_py_sdk',
 'flow_py_sdk.cadence',
 'flow_py_sdk.client',
 'flow_py_sdk.frlp',
 'flow_py_sdk.proto',
 'flow_py_sdk.proto.flow']

package_data = \
{'': ['*']}

install_requires = \
['betterproto[compiler]>=1.2.5,<2.0.0',
 'ecdsa>=0.16.1,<0.17.0',
 'grpcio-tools>=1.33.2,<2.0.0',
 'rlp>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['examples = examples.main:run']}

setup_kwargs = {
    'name': 'flow-py-sdk',
    'version': '0.1.1',
    'description': 'A python SKD for the flow blockchain',
    'long_description': '# flow-py-sdk\n\nAnother unofficial flow blockchain python sdk.\n\nUnder development! I do not recommend you use this.\n\nIf you do want to used do:\n\n`pip install flow-py-sdk`\n\n## Prerequisites\n\n- [poetry](https://python-poetry.org/docs/)\n- python 3.9^\n\n## Examples\n\nFirst, install the [Flow CLI](https://docs.onflow.org/flow-cli).\n\nStart the Flow Emulator in the main directory of this repository:\n\n- `flow emulator start`\n- `poetry build` (only the first time)\n- `poetry install`\n- `poetry run examples`\n\n## TODO\n\n### Docs\n\n- [ ] Create docs folder\n- [ ] Usage example docs:\n    - [ ] using the emulator\n    - [ ] create account\n- [ ] contribution docs\n\n### Examples\n\n- [ ] move examples folder to root folder\n- [ ] make each example runnable separately\n- [ ] write instructions for running examples\n- [ ] add more comments to examples\n- [ ] add more examples\n\n### Tests\n\n- [ ] add cadence decode/encode tests\n- [ ] add more tests\n- [ ] add CI for tests\n\n### Implementation\n\n- [ ] decode event payload from grpc\n- [ ] implement TODOs in cadence decode/encode\n- [ ] add an easy way to subscribe to blockchain events\n',
    'author': 'Janez Podhostnik',
    'author_email': 'janez.podhostnik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/janezpodhostnik/flow-py-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
