from setuptools import setup, find_packages 

setup(
    name="vladmir",
    version=0.1,
    description="A command line tool in order to predict alzheimer patient",
    author="Jean Rodrigues",
    author_email="eujean@live.com",
    packages=find_packages(),
    python_requires = ">=3.12",
    entry_points = {
        "console_scripts": [
            "vladmir-process = Vladmir.Processing.processing:main",
            "vladmir-train = Vladmir.application.training:main",
            "vladmir-predict = Vladmir.application.prediction:main"
        ],
    },)