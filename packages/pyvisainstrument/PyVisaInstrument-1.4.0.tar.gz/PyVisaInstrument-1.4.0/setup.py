# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyvisainstrument', 'pyvisainstrument.testsuite']

package_data = \
{'': ['*']}

install_requires = \
['PyVISA-py>=0.5.2,<0.6.0',
 'PyVISA>=1.11.3,<2.0.0',
 'numpy>=1.20.1,<2.0.0',
 'pyserial>=3.5,<4.0',
 'zeroconf>=0.28.8,<0.29.0']

setup_kwargs = {
    'name': 'pyvisainstrument',
    'version': '1.4.0',
    'description': 'PyVisaInstrument provides boilerplate for various NI-VISA instruments.',
    'long_description': '# PyVisaInstrument\n\n![PyPI](https://img.shields.io/pypi/v/pyvisainstrument)\n\nProvides boilerplate for various NI-VISA instruments and utilizes pyvisa.\n\n- KeysightVNA\n- KeysightDAQ\n- KeysightPSU\n- NumatoRelay (TCP/TELNET and USB)\n\n## Installation\n\npip install pyvisainstrument\n\n## Contributing\n\nPlease read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.\n\n## Versioning\n\nWe use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://bitbucket.org/samteccmd/pyvisainstruments/commits/).\n\n## Maintainers\n\n- [Adam Page](adam.page@samtec.com)\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details\n',
    'author': 'Adam Page',
    'author_email': 'adam.page@samtec.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Samtec-ASH/pyvisainstrument',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
