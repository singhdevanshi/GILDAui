from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gilda-ui",
    version="1.0.0",
    author="GILDA Development Team",
    description="Gunshot Detection System Frontend for Raspberry Pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Security",
    ],
    python_requires=">=3.7",
    install_requires=[
        # Core requirements - keeping minimal for Raspberry Pi
    ],
    extras_require={
        "enhanced": [
            "customtkinter>=5.0.0",
            "tkintermapview>=1.24",
        ],
        "audio": [
            "pyaudio>=0.2.11",
            "scipy>=1.9.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-tk>=0.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gilda-ui=src.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "src": ["assets/**/*"],
    },
)