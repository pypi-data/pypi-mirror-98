from setuptools import setup, find_packages

VERSION = "0.0.0rc1"

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as requirements_file:
    install_requires = [line.strip() for line in requirements_file]

setup_args = dict(
    name="commode-utils",
    version=VERSION,
    description="Set of useful functions and modules for Code Modelling",
    long_description_content_type="text/markdown",
    long_description=readme,
    install_requires=install_requires,
    license="Apache 2.0",
    packages=find_packages(),
    author="Egor Spirin",
    author_email="spirin.egor@gmail.com",
    keywords=[],
    url="https://github.com/SpirinEgor/commode-utils",
    download_url="https://pypi.org/project/commode-utils",
)

if __name__ == "__main__":
    setup(**setup_args)
