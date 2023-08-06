from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name="jotly",
    version="0.0.1",
    description="A Plotly wrapper for easy EDA graphing",
    author="Adam Rose",
    author_email="adrotog@gmail.com",
    url="https://github.com/adamerose/jotly",
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    exclude_package_data={'': ['.gitignore']},
    # Using this instead of MANIFEST.in - https://pypi.org/project/setuptools-git/
    setup_requires=['setuptools-git'],
    install_requires=[
        "plotly",
        "plotly-express",
    ],
)
