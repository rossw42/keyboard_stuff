#!/usr/bin/env python3
"""Setup script for Through-Hole Keyboard Generator (THKG)"""

from setuptools import setup, find_packages

setup(
    name="thkg",
    version="0.1.0",
    description="Through-Hole Keyboard Generator - Automated keyboard design tool",
    author="THKG Contributors",
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=6.0",
        "click>=8.0",
        "ezdxf>=1.0",
        "kle-serial>=0.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=5.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "thkg=thkg.cli:main",
        ],
    },
)
