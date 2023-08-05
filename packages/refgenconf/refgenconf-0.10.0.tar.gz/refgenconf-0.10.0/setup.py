from setuptools import setup
import sys

PACKAGE_NAME = "refgenconf"

# Ordinary dependencies
DEPENDENCIES = []
with open("requirements/requirements-all.txt", "r") as reqs_file:
    for line in reqs_file:
        if not line.strip():
            continue
        # DEPENDENCIES.append(line.split("=")[0].rstrip("<>"))
        DEPENDENCIES.append(line)

# Additional keyword arguments for setup().
extra = {"install_requires": DEPENDENCIES}
if sys.version_info >= (3,):
    extra["use_2to3"] = True

with open("refgenconf/_version.py", "r") as versionfile:
    version = versionfile.readline().split()[-1].strip("\"'\n")

# Handle the pypi README formatting.
try:
    import pypandoc

    long_description = pypandoc.convert_file("README.md", "rst")
    msg = "\033[032mPandoc conversion succeeded.\033[0m"
except (IOError, ImportError, OSError):
    msg = "\033[0;31mWarning: pandoc conversion failed!\033[0m"
    long_description = open("README.md").read()


setup(
    name=PACKAGE_NAME,
    packages=[PACKAGE_NAME],
    version=version,
    description="A standardized configuration object for reference genome assemblies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    license="BSD2",
    keywords="bioinformatics, sequencing, ngs",
    test_suite="tests",
    include_package_data=True,
    tests_require=(["pytest"]),
    setup_requires=(
        ["pytest-runner"] if {"test", "pytest", "ptr"} & set(sys.argv) else []
    ),
    url="https://refgenie.databio.org",
    author=u"Nathan Sheffield, Vince Reuter, Michal Stolarczyk",
    **extra
)

print(msg)
