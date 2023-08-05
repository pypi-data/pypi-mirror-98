from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="naas",
    version="1.3.8",
    scripts=["scripts/naas"],
    author="Martin Donadieu",
    author_email="martindonadieu@gmail.com",
    license="BSD",
    description="Scheduler system for notebooks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cashstory/naas",
    packages=find_packages(exclude=["tests"]),
    package_data={
        "naas": ["runner/assets/*.html", "runner/assets/*.png", "runner/assets/*.svg"],
    },
    setup_requires=["wheel"],
    extras_require={
        "dev": [
            "syncer>=1,<2",
            "backports.zoneinfo>=0,<1",
            "pytest>=5,<7",
            "pytest-tornasync",
            "pytest-mock>=3,<4",
            "pytest-sanic>=1,<2",
            "pytest-asyncio>=0,<1",
            "requests-mock>=1,<2",
            "twine>=3,<4",
            "flake8>=3,<4",
            "pre-commit",
            "black==20.8b1",
            "imgcompare>=2,<3",
            "commitizen>=2,<3",
            "pytest-cov>=2,<3",
        ]
    },
    install_requires=[
        "nbconvert>=6,<7",
        "nest_asyncio>1=,<2",
        "ipywidgets>=7,<8",
        "papermill>=2,<3",
        "pretty-cron>=1,<2",
        "APScheduler>=3,<4",
        "pycron>=3,<4",
        "aiohttp>=3,<4",
        "html5lib>=1,<2",
        "Pillow>=8,<9",
        "markdown2>=2,<3",
        "pandas>=1,<2",
        "escapism>=1,<2",
        "notebook>=6,<7",
        "ipython>=7,<8",
        "ipykernel>=5,<6",
        "requests>=2,<3",
        "sentry-sdk>=0,<2",
        "sanic>=20,<21",
        "sanic-openapi>=0,<1",
        "argparse>=1,<2",
        "nbclient>=0,<1",
        "beautifulsoup4>=4,<5",
        "tzdata"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: BSD License",
        "Framework :: Jupyter",
        "Operating System :: OS Independent",
    ],
)
