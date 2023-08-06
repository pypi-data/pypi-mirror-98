# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['injecta',
 'injecta.autowiring',
 'injecta.compiler',
 'injecta.config',
 'injecta.container',
 'injecta.dtype',
 'injecta.generator',
 'injecta.mocks',
 'injecta.module',
 'injecta.package',
 'injecta.parameter',
 'injecta.schema',
 'injecta.service',
 'injecta.service.argument',
 'injecta.service.argument.validator',
 'injecta.service.class_',
 'injecta.service.parser',
 'injecta.service.resolved',
 'injecta.tag',
 'injecta.testing']

package_data = \
{'': ['*'],
 'injecta.config': ['YamlConfigReaderTest/basic/*',
                    'YamlConfigReaderTest/search/_config/*',
                    'YamlConfigReaderTest/search/mypackage/*',
                    'YamlConfigReaderTest/search/mypackage/subpackage/*']}

install_requires = \
['PyYAML>=5.1,<6.0', 'python-box>=3.4,<4.0', 'tomlkit>=0.5.8,<1.0.0']

setup_kwargs = {
    'name': 'injecta',
    'version': '0.10.0b1',
    'description': 'Dependency Injection Container Library',
    'long_description': "# Injecta\n\nDependency Injection (DI) Container written in Python. Main component of the [Pyfony Framework](https://github.com/pyfony/pyfony).\n\n## Installation\n\n```\n$ pip install injecta\n```\n\n## Simple container initialization\n\n(The following steps are covered in the [ContainerInitializerTest](src/injecta/container/ContainerInitializerTest.py))\n\nTo start using Injecta, create a simple `config.yaml` file to define your DI services:\n\n```yaml\nparameters:\n  api:\n    endpoint: 'https://api.mycompany.com'\n\nservices:\n    mycompany.api.ApiClient:\n      arguments:\n        - '@mycompany.api.Authenticator'\n\n    mycompany.api.Authenticator:\n      class: mycompany.authenticator.RestAuthenticator\n      arguments:\n        - '%api.endpoint%'\n        - '%env(API_TOKEN)%'\n```\n\nThen, initialize the container:\n\n```python\nfrom injecta.container.ContainerBuilder import ContainerBuilder\nfrom injecta.config.YamlConfigReader import YamlConfigReader\nfrom injecta.container.ContainerInitializer import ContainerInitializer\n\nconfig = YamlConfigReader().read('/path/to/config.yaml')\n\ncontainerBuild = ContainerBuilder().build(config)\n\ncontainer = ContainerInitializer().init(containerBuild)\n```\n\nUse `container.get()` to finally retrieve your service:\n\n```python\nfrom mycompany.api.ApiClient import ApiClient\n\napiClient = container.get('mycompany.api.ApiClient') # type: ApiClient   \napiClient.get('/foo/bar')\n```\n\n## Advanced examples\n\n1. [Configuring services using parameters](docs/parameters.md)\n1. [Service autowiring](docs/autowiring.md)\n1. [Using service factories](docs/factories.md)\n1. [Tagged services](docs/tagging.md)\n",
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyfony/injecta',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
