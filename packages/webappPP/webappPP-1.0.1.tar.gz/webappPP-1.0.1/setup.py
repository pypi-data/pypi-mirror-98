import pathlib
from setuptools import setup
HERE = pathlib.Path(__file__).parent
README = (HERE/"README.md").read_text()
setup(
    name="webappPP",
    version = "1.0.1",
    description="Algorithm for finance",
    long_description =README,
    long_description_content_type ="text/markdown",
    license ="MIT",
    packages = ["backtest"],
    install_requires=["pandas","numpy","datetime","pandas_datareader", "os", "scipy", "pathlib","Flask","base64", "seaborn","threading","webbrowser"],
    entry_points={"console_scripts":["finance=finance.__main__:main"]}
)