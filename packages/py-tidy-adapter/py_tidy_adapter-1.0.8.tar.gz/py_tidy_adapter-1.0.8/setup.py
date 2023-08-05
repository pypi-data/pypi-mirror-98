import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_tidy_adapter",
    version="1.0.8",
    author="Michele Bassanelli",
    author_email="michele.bassanelli@it-change.it",
    description="python adapter to use with tidy server",
    install_requires=['zeep',  'numpy', 'pandas', 'datetime'],
    packages=setuptools.find_packages(),
)
