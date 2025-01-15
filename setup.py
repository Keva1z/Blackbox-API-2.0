from setuptools import setup, find_packages

setup(
    name="blackboxapi",
    version="0.6.0",
    packages=find_packages(),
    install_requires=[
        "﻿aiohappyeyeballs==2.4.4"
        "aiohttp==3.11.11"
        "aiosignal==1.3.2"
        "aiosqlite==0.20.0"
        "attrs==24.3.0"
        "Brotli==1.1.0"
        "certifi==2024.12.14"
        "charset-normalizer==3.4.1"
        "frozenlist==1.5.0"
        "greenlet==3.1.1"
        "idna==3.10"
        "multidict==6.1.0"
        "pillow==11.1.0"
        "propcache==0.2.1"
        "requests==2.32.3"
        "SQLAlchemy==2.0.37"
        "typing_extensions==4.12.2"
        "urllib3==2.3.0"
        "yarl==1.18.3"
        "setuptools==75.8.0"
    ],
    python_requires=">=3.8",
    author="Keva1z",
    author_email="Keva1z@yandex.ru",
    description="Python library for Blackbox AI API integration with image support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Keva1z/blackboxapi",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
