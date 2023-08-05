import pathlib
from setuptools import setup
HERE = pathlib.Path(__file__).parent
README = (HERE/"README.md").read_text()
setup(
    name="FINANCEPP",
    version = "1.2.3",
    description="Algorithm for finance",
    long_description =README,
    long_description_content_type ="text/markdown",
    license ="MIT",
    packages = ["finance"],
    install_requires=["pandas","numpy","datetime","pandas_datareader"],
    entry_points={"console_scripts":["finance=finance.__main__:main"]}
)