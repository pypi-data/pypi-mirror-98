import setuptools
from configparser import ConfigParser

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

config = ConfigParser()
config.read('setup.cfg')
metadata = config['metadata']

setuptools.setup(
    name=metadata['name'],
    version=metadata['version'],
    author=metadata['author'],
    author_email=metadata['author_email'],
    description=metadata['description'],
    long_description=long_description,
    long_description_content_type=metadata['long_description_content_type'],
    url=metadata['url'],
    project_urls={
        "Bug Tracker": "https://github.com/LuckyKarter/filecreate/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
      #  "Operating System :: Microsoft :: Windows",
    ],
    packages=setuptools.find_packages(),
    python_requires=config['options']['python_requires'],
)
