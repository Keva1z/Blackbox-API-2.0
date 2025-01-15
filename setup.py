from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Try different encodings for requirements.txt
encodings = ['utf-8', 'utf-16', 'latin-1', 'ascii']
for encoding in encodings:
    try:
        with open("requirements.txt", "r", encoding=encoding) as fh:
            requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
        break
    except UnicodeDecodeError:
        continue
    except Exception as e:
        print(f"Error reading requirements.txt: {e}")
        requirements = [
            "aiohappyeyeballs>=2.4.4",
            "aiohttp>=3.11.11",
            "aiosqlite>=0.20.0",
            "pillow>=11.1.0",
            "requests>=2.32.3",
            "SQLAlchemy>=2.0.37"
        ]
        break

setup(
    name="blackbox-api",
    version="2.0.0",
    author="Keva1z",
    author_email="",  # Add your email if you want
    description="A Python wrapper for the Blackbox AI API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Keva1z/Blackbox-API-2.0",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    include_package_data=True,
) 