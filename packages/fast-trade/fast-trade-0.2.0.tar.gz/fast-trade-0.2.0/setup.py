import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="fast-trade",
    version="0.2.0",
    description="Analyze and backtest algorithmic trading strategies ohlcv data quickly and easily.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jrmeier/fast-trade",
    py_modules=["fast_trade"],
    keywords=[
        "backtesting",
        "currency",
        "ta",
        "pandas",
        "finance",
        "numpy",
        "analysis",
        "technical analysis",
    ],
    author="Jed Meier",
    author_email="fast_trade@jedm.dev",
    license="GNU AGPLv3",
    python_requires=">=3",
    entry_points={"console_scripts": ["ft = fast_trade.cli:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    packages=find_packages(include=["fast_trade"]),
    include_package_data=True,
    install_requires=[
        "cycler==0.10.0",
        "finta",
        "kiwisolver==1.3.1",
        "matplotlib==3.3.4",
        "numpy",
        "pandas",
        "Pillow==8.1.2",
        "pyparsing==2.4.7",
        "python-dateutil==2.8.1",
        "pytz",
        "six",
        "python-binance",
        'service_identity',
        'pyasn1'
    ],
)
