from setuptools import setup
from setuptools.command.install import install
import pathlib
import os

from vespy.ssl_utils import add_certificates

HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


class PostInstallCommand(install):

    def run(self):
        install.run(self)
        add_certificates()


setup(
    name='vespy',
    author="Emil Haldrup Eriksen",
    author_email="emil.h.eriksen@gmail.com",
    description="A small utility package",
    version=os.getenv("CI_COMMIT_TAG", "0.0.15"),
    url='https://github.com/',
    packages=['vespy'],
    package_data={"vespy": ['vespy/certificates/*']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'vespy=vespy.main:run'
        ]
    },
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires='>=3.6',
    install_requires=['certifi', 'requests'],
    cmdclass={
        'install': PostInstallCommand,
    }
)
