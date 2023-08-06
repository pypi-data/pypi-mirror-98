import distutils.cmd
import os
import subprocess

from setuptools import find_packages, setup


class BaseCommand(distutils.cmd.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


def create_command(text, commands):
    """Creates a custom setup.py command."""

    class CustomCommand(BaseCommand):
        description = text

        def run(self):
            for cmd in commands:
                subprocess.check_call(cmd)

    return CustomCommand


with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as readme:
    README = readme.read()


setup(
    name="opennsfw-standalone",
    version="0.0.1",
    packages=find_packages(),
    data_files=[
        (
            "",
            [
                "opennsfw_standalone/model/saved_model.pb",
                "opennsfw_standalone/model/variables/variables.data-00000-of-00001",
                "opennsfw_standalone/model/variables/variables.index",
            ],
        ),
    ],
    include_package_data=True,
    license="MIT License",
    description="Stand-alone wrapper for Yahoo's OpenNSFW model using Tensorflow.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/SectorLabs/opennsfw-standalone",
    author="Sector Labs",
    author_email="open-source@sectorlabs.ro",
    keywords=["nsfw", "machine learning", "tensorflow", "opennsfw", "yahoo"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.8",
    install_requires=[
        "tensorflow>=2.4.0,<2.5.0",
        "numpy>=1.19.0,<2.0.0",
    ],
    extras_require={
        "test": [
            "pytest==6.2.2",
            "pytest-cov==2.11.1",
            "tox==3.23.0",
        ],
        "analysis": [
            "black==20.8b1",
            "flake8==3.9.0",
            "autoflake==1.4",
            "autopep8==1.5.5",
            "isort==5.7.0",
            "docformatter==1.4",
        ],
    },
    cmdclass={
        "lint": create_command(
            "Lints the code",
            [["flake8", "setup.py", "opennsfw_standalone"]],
        ),
        "lint_fix": create_command(
            "Lints the code",
            [
                [
                    "autoflake",
                    "--remove-all-unused-imports",
                    "-i",
                    "-r",
                    "setup.py",
                    "opennsfw_standalone",
                ],
                ["autopep8", "-i", "-r", "setup.py", "opennsfw_standalone"],
            ],
        ),
        "format": create_command(
            "Formats the code", [["black", "setup.py", "opennsfw_standalone"]]
        ),
        "format_verify": create_command(
            "Checks if the code is auto-formatted",
            [["black", "--check", "setup.py", "opennsfw_standalone"]],
        ),
        "format_docstrings": create_command(
            "Auto-formats doc strings", [["docformatter", "-r", "-i", "."]]
        ),
        "format_docstrings_verify": create_command(
            "Verifies that doc strings are properly formatted",
            [["docformatter", "-r", "-c", "."]],
        ),
        "sort_imports": create_command(
            "Automatically sorts imports",
            [
                ["isort", "setup.py"],
                ["isort", "opennsfw_standalone"],
            ],
        ),
        "sort_imports_verify": create_command(
            "Verifies all imports are properly sorted.",
            [
                ["isort", "-c", "setup.py"],
                ["isort", "-c", "-rc", "opennsfw_standalone"],
            ],
        ),
        "fix": create_command(
            "Automatically format code and fix linting errors",
            [
                ["python", "setup.py", "format"],
                ["python", "setup.py", "format_docstrings"],
                ["python", "setup.py", "sort_imports"],
                ["python", "setup.py", "lint_fix"],
                ["python", "setup.py", "lint"],
            ],
        ),
        "verify": create_command(
            "Verifies whether the code is auto-formatted and has no linting errors",
            [
                ["python", "setup.py", "format_verify"],
                ["python", "setup.py", "format_docstrings_verify"],
                ["python", "setup.py", "sort_imports_verify"],
                ["python", "setup.py", "lint"],
            ],
        ),
        "test": create_command(
            "Runs all the tests",
            [
                [
                    "pytest",
                    "--cov=opennsfw_standalone",
                    "--cov-report=term",
                    "--cov-report=xml:reports/xml",
                    "--cov-report=html:reports/html",
                    "--junitxml=reports/junit/tests.xml",
                ]
            ],
        ),
    },
)
