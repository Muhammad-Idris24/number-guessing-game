from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="number_guessing_game",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A professional number guessing game with CLI and GUI interfaces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/number-guessing-game",
    packages=find_packages(include=["game*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Games/Entertainment :: Puzzle Games"
    ],
    python_requires=">=3.6",
    install_requires=[
        "PySimpleGUI>=4.60.0",  # Only if you're using the GUI version
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "pdoc3>=0.10.0"
        ],
    },
    entry_points={
        "console_scripts": [
            "guess-number=main:main",  # Creates 'guess-number' terminal command
        ],
    },
    include_package_data=True,
)