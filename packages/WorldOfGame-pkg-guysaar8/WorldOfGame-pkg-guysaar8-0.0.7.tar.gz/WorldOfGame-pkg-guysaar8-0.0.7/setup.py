from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="WorldOfGame-pkg-guysaar8",
    version="0.0.7",
    description="Python Games package",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Guy Saar",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    pacjage_data={"worldofgames":["account_db.json"]},
    include_package_data=True,
    install_requires=["requests", "random", "os", "time", "json","sys"],
)

