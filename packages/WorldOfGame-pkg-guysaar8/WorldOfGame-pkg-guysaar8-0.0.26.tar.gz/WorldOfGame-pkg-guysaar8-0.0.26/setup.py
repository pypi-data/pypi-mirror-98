from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="WorldOfGame-pkg-guysaar8",
    version="0.0.26",
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
    packages=['worldofgames'],
    package_data={'': ['account_db.json']},
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts":[
            "worldofgames=worldofgames.MainGame:log",
        ]
    },
)

