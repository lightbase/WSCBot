from setuptools import setup, find_packages

requires = [
    'ConfigParser',
    'requests',
    ]

setup(
    name="WSCBot",
    version="1.1.2b5",
    author="Lightbase",
    author_email="breno.brito@lightbase.com.br",
    url="https://pypi.python.org/pypi/LBConverter",
    description="Daemon for the neo-lightbase service",
    license="GPLv2",
    keywords="Converter extractor lightbase daemon",
    install_requires=requires,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: No Input/Output (Daemon)",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: Portuguese (Brazilian)",
        "Programming Language :: Python :: 3.2",
        "Topic :: Database :: Database Engines/Servers",
    ]
)
