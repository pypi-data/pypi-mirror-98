#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'pybuilder-anybadge',
        version = '0.1.2',
        description = 'Pybuilder plugin for anybadge badge generator',
        long_description = "[![GitHub Workflow Status](https://github.com/soda480/pybuilder-anybadge/workflows/build/badge.svg)](https://github.com/soda480/pybuilder-anybadge/actions)\n[![Code Coverage](https://codecov.io/gh/soda480/pybuilder-anybadge/branch/main/graph/badge.svg)](https://codecov.io/gh/soda480/pybuilder-anybadge)\n[![Code Grade](https://www.code-inspector.com/project/20103/status/svg)](https://frontend.code-inspector.com/project/20103/dashboard)\n[![PyPI version](https://badge.fury.io/py/pybuilder-anybadge.svg)](https://badge.fury.io/py/pybuilder-anybadge)\n\n# pybuilder-anybadge #\n\nA pybuilder plugin that generates badges for your project using `anybadge`, for more information refer to the [anybadge pypi page](https://pypi.org/project/anybadge/).\n\nTo add this plugin into your pybuilder project, add the following line near the top of your build.py:\n```python\nuse_plugin('pypi:pybuilder_anybadge')\n```\n\n**NOTE** if you are using Pybuilder version `v0.11.x`, then specify the following version of the plugin:\n```python\nuse_plugin('pypi:pybuilder_anybadge', '~=0.1.2')\n```\n\n### Pybuilder anybadge properties ###\n\nThe pybuilder task `pyb anybadge` will use anybadge to generate badges for your project by processing reports produced from various plugins; the badges that are currently supported are:\n- **complexity** - requires the [pybuilder_radon](https://pypi.org/project/pybuilder-radon/) plugin. Generate badge using cyclomatic complexity score of your most complicated function.\n- **severity** - requires the [pybuilder_bandit](https://pypi.org/project/pybuilder-bandit/) plugin. Generate badge using number of security vulnerabilities discovered by severity.\n- **coverage** - requires the `coverage` plugin. Generate badge for overall unit test coverage.\n- **python** - Generate badge for version of Python being used\n\nThe plugin will write the respective badges to the `docs/images` folder. The following plugin properties are available to further configure badge generation.\n\nName | Type | Default Value | Description\n-- | -- | -- | --\nanybadge_exclude | str | '' | Comma delimited string of badges to exclude from processing, valid values are 'complexity', 'severity', 'coverage' and 'python'\nanybadge_add_to_readme | bool | False | Specify if plugin should add badges to the README.md file (see below for example). **Note** the plugin will add the badge references but you must commit/push the changes (including svg files in the docs/images folder)\nanybadge_complexity_use_average | bool | False | Use overall average complexity as score when generating complexity badge\n\nThe plugin properties are set using `project.set_property`, the following is an example of how to set the properties:\n\n```Python\nproject.set_property('anybadge_exclude', 'severity,coverage')\nproject.set_property('anybadge_add_to_readme', True)\nproject.set_property('anybadge_complexity_use_average', False)\n```\n\nThe following badges were generated for this project using the `pybuilder_anybadge` plugin:\n\n![coverage](https://raw.githubusercontent.com/soda480/pybuilder-anybadge/main/docs/images/coverage.svg)\n![severity](https://raw.githubusercontent.com/soda480/pybuilder-anybadge/main/docs/images/severity.svg)\n![complexity](https://raw.githubusercontent.com/soda480/pybuilder-anybadge/main/docs/images/complexity.svg)\n![python](https://raw.githubusercontent.com/soda480/pybuilder-anybadge/main/docs/images/python.svg)\n\n### Development ###\n\nClone the repository and ensure the latest version of Docker is installed on your development server.\n\nBuild the Docker image:\n```sh\ndocker image build \\\n-t \\\npybanybadge:latest .\n```\n\nRun the Docker container:\n```sh\ndocker container run \\\n--rm \\\n-it \\\n-v $PWD:/pybuilder-anybadge \\\npybanybadge:latest \\\n/bin/sh\n```\n\nExecute the build:\n```sh\npyb -X\n```",
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Other Environment',
            'Environment :: Plugins',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development :: Build Tools'
        ],
        keywords = '',

        author = 'Emilio Reyes',
        author_email = 'soda480@gmail.com',
        maintainer = '',
        maintainer_email = '',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/soda480/pybuilder-anybadge',
        project_urls = {},

        scripts = [],
        packages = ['pybuilder_anybadge'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = ['anybadge'],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
