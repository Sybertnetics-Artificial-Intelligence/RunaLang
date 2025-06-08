from setuptools import setup, find_packages

setup(
    name="runa",
    version="0.1.0",
    description="Runa Programming Language",
    author="Sybernetics AI Solutions",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "runa=runa.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 