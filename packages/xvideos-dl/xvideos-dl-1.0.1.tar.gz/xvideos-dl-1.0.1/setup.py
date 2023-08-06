# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xvideos_dl']

package_data = \
{'': ['*']}

install_requires = \
['cursor>=1.3.4,<2.0.0',
 'requests>=2.25.0,<3.0.0',
 'rich>=9.8.2,<10.0.0',
 'typer[all]>=0.3.2,<0.4.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['xvideos-dl = xvideos_dl.__main__:app']}

setup_kwargs = {
    'name': 'xvideos-dl',
    'version': '1.0.1',
    'description': 'CLI to download videos from https://xvideos.com',
    'long_description': '# xvideos-dl\n\n<div align="center">\n\n[![Build status](https://github.com/lonsty/xvideos-dl/workflows/build/badge.svg?branch=master&event=push)](https://github.com/lonsty/xvideos-dl/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/xvideos-dl.svg)](https://pypi.org/project/xvideos-dl/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/lonsty/xvideos-dl/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/lonsty/xvideos-dl/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/lonsty/xvideos-dl/releases)\n[![License](https://img.shields.io/github/license/lonsty/xvideos-dl)](https://github.com/lonsty/xvideos-dl/blob/master/LICENSE)\n\nCLI to download videos from https://xvideos.com\n\n</div>\n\n## Usage\n\n- Install xvideos-dl\n\n```bash\npip install -U xvideos-dl\n```\n\n- Get CLI help\n\n```bash\nxvideos-dl --help\n```\n\n- Download video\n\n```bash\nxvideos-dl https://www.xvideos.com/video37177493/asian_webcam_2_camsex4u.life\n```\n\n## Release History\n\n### 1.0.1\n\nNew features:\n\n- Download videos from playlist\n- Show download speed\n\n### 1.0.0\n\nInitial release on PyPY.\n\n<hr>\n\n## For Contributors\n\n### Initial\n\n1. Fork and clone this repo:\n\n```bash\ngit clone https://github.com/lonsty/xvideos-dl\n```\n\n2. If you don\'t have `Poetry` installed run:\n\n```bash\nmake download-poetry\n```\n\n3. Initialize poetry and install `pre-commit` hooks:\n\n```bash\nmake install\n```\n\n### Makefile usage\n\n[`Makefile`](https://github.com/lonsty/xvideos-dl/blob/master/Makefile) contains many functions for fast assembling and convenient work.\n\n<details>\n<summary>1. Download Poetry</summary>\n<p>\n\n```bash\nmake download-poetry\n```\n\n</p>\n</details>\n\n<details>\n<summary>2. Install all dependencies and pre-commit hooks</summary>\n<p>\n\n```bash\nmake install\n```\n\nIf you do not want to install pre-commit hooks, run the command with the NO_PRE_COMMIT flag:\n\n```bash\nmake install NO_PRE_COMMIT=1\n```\n\n</p>\n</details>\n\n<details>\n<summary>3. Check the security of your code</summary>\n<p>\n\n```bash\nmake check-safety\n```\n\nThis command launches a `Poetry` and `Pip` integrity check as well as identifies security issues with `Safety` and `Bandit`. By default, the build will not crash if any of the items fail. But you can set `STRICT=1` for the entire build, or you can configure strictness for each item separately.\n\n```bash\nmake check-safety STRICT=1\n```\n\nor only for `safety`:\n\n```bash\nmake check-safety SAFETY_STRICT=1\n```\n\nmultiple\n\n```bash\nmake check-safety PIP_STRICT=1 SAFETY_STRICT=1\n```\n\n> List of flags for `check-safety` (can be set to `1` or `0`): `STRICT`, `POETRY_STRICT`, `PIP_STRICT`, `SAFETY_STRICT`, `BANDIT_STRICT`.\n\n</p>\n</details>\n\n<details>\n<summary>4. Check the codestyle</summary>\n<p>\n\nThe command is similar to `check-safety` but to check the code style, obviously. It uses `Black`, `Darglint`, `Isort`, and `Mypy` inside.\n\n```bash\nmake check-style\n```\n\nIt may also contain the `STRICT` flag.\n\n```bash\nmake check-style STRICT=1\n```\n\n> List of flags for `check-style` (can be set to `1` or `0`): `STRICT`, `BLACK_STRICT`, `DARGLINT_STRICT`, `ISORT_STRICT`, `MYPY_STRICT`.\n\n</p>\n</details>\n\n<details>\n<summary>5. Run all the codestyle formaters</summary>\n<p>\n\nCodestyle uses `pre-commit` hooks, so ensure you\'ve run `make install` before.\n\n```bash\nmake codestyle\n```\n\n</p>\n</details>\n\n<details>\n<summary>6. Run tests</summary>\n<p>\n\n```bash\nmake test\n```\n\n</p>\n</details>\n\n<details>\n<summary>7. Run all the linters</summary>\n<p>\n\n```bash\nmake lint\n```\n\nthe same as:\n\n```bash\nmake test && make check-safety && make check-style\n```\n\n> List of flags for `lint` (can be set to `1` or `0`): `STRICT`, `POETRY_STRICT`, `PIP_STRICT`, `SAFETY_STRICT`, `BANDIT_STRICT`, `BLACK_STRICT`, `DARGLINT_STRICT`, `ISORT_STRICT`, `MYPY_STRICT`.\n\n</p>\n</details>\n\n<details>\n<summary>8. Build docker</summary>\n<p>\n\n```bash\nmake docker\n```\n\nwhich is equivalent to:\n\n```bash\nmake docker VERSION=latest\n```\n\nMore information [here](https://github.com/lonsty/xvideos-dl/tree/master/docker).\n\n</p>\n</details>\n\n<details>\n<summary>9. Cleanup docker</summary>\n<p>\n\n```bash\nmake clean_docker\n```\n\nor to remove all build\n\n```bash\nmake clean\n```\n\nMore information [here](https://github.com/lonsty/xvideos-dl/tree/master/docker).\n\n</p>\n</details>\n\n## 📈 Releases\n\nYou can see the list of available releases on the [GitHub Releases](https://github.com/lonsty/xvideos-dl/releases) page.\n\nWe follow [Semantic Versions](https://semver.org/) specification.\n\nWe use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.\n\nFor Pull Request this labels are configured, by default:\n\n|               **Label**               |  **Title in Releases**  |\n| :-----------------------------------: | :---------------------: |\n|       `enhancement`, `feature`        |       🚀 Features       |\n| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |\n|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |\n|              `breaking`               |   💥 Breaking Changes   |\n|            `documentation`            |    📝 Documentation     |\n|            `dependencies`             | ⬆️ Dependencies updates |\n\nYou can update it in [`release-drafter.yml`](https://github.com/lonsty/xvideos-dl/blob/master/.github/release-drafter.yml).\n\nGitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/lonsty/xvideos-dl)](https://github.com/lonsty/xvideos-dl/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/lonsty/xvideos-dl/blob/master/LICENSE) for more details.\n\n## 📃 Citation\n\n```\n@misc{xvideos-dl,\n  author = {xvideos-dl},\n  title = {CLI to download videos from https://xvideos.com},\n  year = {2021},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/lonsty/xvideos-dl}}\n}\n```\n\n## Credits\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).\n',
    'author': 'xvideos-dl',
    'author_email': 'lonsty@sina.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lonsty/xvideos-dl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
