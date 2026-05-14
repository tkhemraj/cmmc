"""
CMMC Artifact Gathering Tool
Collects compliance data from Windows endpoints for CMMC assessment
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cmmc-gatherer",
    version="1.0.0",
    author="CMMC Team",
    description="CMMC artifact gathering tool for Windows environments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cmmc-gatherer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pywin32>=300",
        "ldap3>=2.9.1",
    ],
    entry_points={
        "console_scripts": [
            "cmmc-gatherer=cmmc_gatherer.cli:main",
        ],
    },
)
