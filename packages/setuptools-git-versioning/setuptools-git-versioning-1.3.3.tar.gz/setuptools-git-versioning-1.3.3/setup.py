from setuptools import setup, find_packages
from setuptools_git_versioning import version_from_git

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fh:
    requirements = fh.readlines()

setup(
    name="setuptools-git-versioning",
    version=version_from_git(),
    author="Camas",
    author_email="camas@hotmail.co.uk",
    description="Automatically set package version using git tag/hash",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dolfinus/setuptools-git-versioning",
    keywords='setuptools git version-control',
    packages=find_packages(),
    classifiers=[
        'Framework :: Setuptools Plugin',
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7,!=3.1,!=3.2',
    py_modules=['setuptools_git_versioning'],
    install_requires=requirements,
    entry_points={
        'distutils.setup_keywords': [
            'version_config = setuptools_git_versioning:parse_config',
        ],
    },
    include_package_data=True,
    zip_safe=False
)
