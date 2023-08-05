import setuptools
from os import sys

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

with open('README.md') as readme:
    long_description = readme.read()

setuptools.setup(
    name="tartiflette-middleware",
    version="1.0.2",
    author="Dave O'Connor",
    author_email="github@dead-pixels.org",
    description="Framework for middleware for Tartiflette, with context data assignment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daveoconnor/tartiflette-middleware",
    packages=setuptools.find_packages(include=[
        'tartiflette_middleware',
        'tartiflette_middleware.exceptions',
        'tartiflette_middleware.server',
    ]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        "tartiflette>=1.2",
    ],
    tests_require=[
        "aiohttp",
        "pytest>=6.0",
        "pytest-xdist>=1.34",
        "pytest-cov>=2.10",
    ],
    setup_requires=[] + pytest_runner,
)
