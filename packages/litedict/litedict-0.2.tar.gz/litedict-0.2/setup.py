import setuptools
from pathlib import Path
import re


def get_version(fn) -> str:
    code = Path(fn).read_text()
    match = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", code)
    assert match is not None
    return match.group(1)


version = get_version("./litedict.py")

setuptools.setup(
    name="litedict",
    version=version,
    author="Ricardo Ander-Egg Aguilar",
    author_email="rsubacc@gmail.com",
    description="Simple dictionary built on top of SQLite",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/litements/litedict",
    py_modules=["litedict"],
    classifiers=["Operating System :: OS Independent",],
    python_requires=">=3.6",
)
