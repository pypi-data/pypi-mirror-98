import pathlib
from setuptools import setup
HERE = pathlib.Path(__file__).parent
README = (HERE/"README.md").read_text()
setup(
    name="CARNETORDREKB",
    version = "1.0.0",
    description="Algorithm for finance",
    long_description =README,
    long_description_content_type ="text/markdown",
    license ="MIT",
    packages = ["carnetordre"],
    install_requires=[],
    entry_points={"console_scripts":["carnetordre=carnetordre.__main__:main"]}
)