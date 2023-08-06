# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

from setuptools import setup, find_packages

from pathlib import Path
import sys

module_path = str((Path(__file__).parent / "src/kubernetes_job").absolute())
sys.path.insert(0, module_path)
print(sys.path)

from __version__ import __version__


with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="kubernetes-job",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": ['kubernetes-job = kubernetes_job.__main__:execute']
    },
    version=__version__,
    description="Simple Kubernetes job creation; a Python library for starting a Kubernetes batch job as a normal Python function call.",
    long_description=long_descr,
    long_description_content_type="text/markdown",
    author="Roemer Claasen",
    author_email="roemer.claasen@gmail.com",
    url="https://gitlab.com/roemer/kubernetes-job",
    project_urls={
        "Documentation": "https://kubernetes-job.readthedocs.io",
    },
    install_requires=[
        "kubernetes>=12.0.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
