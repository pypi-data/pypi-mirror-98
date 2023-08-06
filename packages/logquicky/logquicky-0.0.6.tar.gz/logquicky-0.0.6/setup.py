from setuptools import setup, find_packages

package_name = "logquicky"

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name=package_name,
    packages=[package_name],
    setup_requires=["setuptools-git-versioning"],
    version_config={
        "starting_version": "0.0.6",
        "dirty_template": "{tag}",
    },
    license="GPLv3",
    description="Nicer python logging in one line",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Igor Schouten",
    author_email="igor@igorschouten.com",
    url="https://github.com/ischouten/logquicky",
    keywords=["Logging", "Colored output"],
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",  # Options: "3 - Alpha", "4 - Beta", "5 - Production/Stable"
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
