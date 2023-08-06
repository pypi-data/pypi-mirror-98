import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()




setup(
    name="anis-package",
    version="1.0.0",
    description="this is a test package",
    long_description=README,
    long_description_content_type="text/markdown",
    author="anisanis611",
    author_email="anis.dhouieb@gmail.com",
    license="MIT",
    packages=["pkg1", "pkg2"],
    entry_points={
        "console_scripts": [
            "mymain=reader.__main__:main",
        ]
    }

)