try:
    import sourcedefender
except ModuleNotFoundError:
    pass
import os
from setuptools import setup, find_namespace_packages

PROJECT = "mAdvisor"
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def package_pye_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.pye'):
                paths.append(os.path.join('..', path, filename))
    return paths
pye_files = package_pye_files(f"./{PROJECT}")
PACKAGE_DATA = {
    PROJECT: ["./resources/*"] + pye_files
}

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.read().splitlines()
exec(open('mAdvisor/version.py').read())
setup(
    name=PROJECT,
    version=__version__,
    author="Marlabs Inc.",
    author_email="mAdvisor_AutoML@marlabs.com",
    description="An automated AI/ML solution from Marlabs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer='Rahul Sivankutty',
    maintainer_email="Rahul.Sivankutty@marlabs.com",
    url="https://www.marlabs.com/platforms/cognitive-computing-AI-ML-platform/",
    packages=find_namespace_packages(include=[f"{PROJECT}*"]),
    package_data=PACKAGE_DATA,
    include_package_data=True,
    install_requires=REQUIREMENTS,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
