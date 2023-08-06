import pathlib
from setuptools import setup
HERE = pathlib.Path(__file__).parent
README = (HERE/"README.md").read_text()
setup(
    name="webappPP",
    version = "1.0.3",
    description="Algorithm for finance",
    long_description =README,
    long_description_content_type ="text/markdown",
    license ="MIT",
    packages = ["backtest"],
    install_requires=["pandas","numpy","pandas_datareader", "scipy","Flask", "seaborn"],
    entry_points={"console_scripts":["backtest=backtest.__main__:main"]}
)