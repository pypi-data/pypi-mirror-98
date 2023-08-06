import os
import re
import sys
from io import open

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


def read(f):
    return open(f, "r", encoding="utf-8").read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join(package, "__init__.py"),)
    ).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


# Inspired by the example at https://pytest.org/latest/goodpractises.html
class NoseTestCommand(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Run nose ensuring that argv simulates running nosetests directly
        import nose

        nose.run_exit(argv=["nosetests"])


version = get_version("ppmutils")

setup(
    name="ppm-utils",
    version=version,
    url="https://github.com/hms-dbmi/ppm-utils",
    author="HMS DBMI Tech-core",
    author_email="dbmi-tech-core@hms.harvard.edu",
    packages=find_packages(exclude=["tests*"]),
    license="Creative Commons Attribution-Noncommercial-Share Alike license",
    install_requires=read("requirements.txt").splitlines(),
    tests_require=read("requirements-test.txt").splitlines(),
    extras_require={
        "test": read("requirements-test.txt").splitlines(),
        "dev": read("requirements-dev.txt").splitlines(),
    },
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",  # example license
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    cmdclass={"test": NoseTestCommand},
)

try:
    from semantic_release import setup_hook

    setup_hook(sys.argv)
except ImportError:
    pass
