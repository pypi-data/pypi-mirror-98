import os
import re
import pathlib
import setuptools

readme = pathlib.Path("README.md").read_text(encoding="utf-8")


def valid_requirement(req):
    return not (re.match(r"^\s*$", req) or re.match("^#", req))


requirements_txt = open("requirements.txt").read().splitlines()
requirements = [req for req in requirements_txt if valid_requirement(req)]
if os.getenv("REQ_IGNORE_VERSIONS"):
    requirements = [req.split(">=")[0] for req in requirements]

setuptools.setup(
    name="squaddata",
    version="0.0.2",
    description="squad data",
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/linaro/lkft/reports/squaddata",
    author="LKFT",
    author_email="lkft@linaro.org",
    packages=["squaddata"],
    include_package_data=True,
    python_requires=">=3.6, <4",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "squad_report=squaddata.cli:report",
        ]
    },
)
