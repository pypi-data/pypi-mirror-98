"""Installation script for sixrunr application."""
from pathlib import Path
from setuptools import setup, find_packages

DESCRIPTION = (
    "python library for sixoclock's softwares to run"
)
APP_ROOT = Path(__file__).parent
README = (APP_ROOT / "README.md").read_text(encoding='utf-8')
AUTHOR = "sixoclock"
AUTHOR_EMAIL = "r_d@sixoclock.net"
PROJECT_URLS = {
    "Documentation": "https://aaronluna.dev/series/flask-api-tutorial/",
    "Bug Tracker": "https://github.com/a-luna/flask-api-tutorial/issues",
    "Source Code": "https://github.com/a-luna/flask-api-tutorial",
}


INSTALL_REQUIRES = [
    "pyyaml",
    "paramiko",
    "cwltool",
]
EXTRAS_REQUIRE = {
    "dev": [
        "pre-commit",
        "pydocstyle",
        "pytest",
        "tox",
    ]
}

setup(
    name="sixrunr",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    version="0.1.2",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    license="Apache-2.0 License",
    url="https://github.com/6-oclock/sixrunr",
    project_urls=PROJECT_URLS,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    entry_points={
          'console_scripts': [ "sixrunr=cwltool.main:main" ]
      },
)
