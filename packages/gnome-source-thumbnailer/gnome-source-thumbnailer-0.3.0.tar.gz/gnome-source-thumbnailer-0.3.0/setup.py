#!/usr/bin/python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gnome-source-thumbnailer",
    version="0.3.0",
    author="Zander Brown",
    author_email="zbrown@gnome.org",
    description="Thumbnails for your code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.gnome.org/ZanderBrown/gnome-source-thumbnailer",
    packages=["gnome_source_thumbnailer"],
    package_dir={"gnome_source_thumbnailer": "gnome_source_thumbnailer"},
    package_data={"gnome_source_thumbnailer": ["resources/*.svg"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Desktop Environment :: Gnome",
        "Operating System :: POSIX",
    ],
    entry_points={
        "console_scripts": [
            "gnome-source-thumbnailer = gnome_source_thumbnailer:main",
        ],
    },
    data_files=[("/usr/share/thumbnailers", ["gnome-source-thumbnailer.thumbnailer",])],
    python_requires=">=3.7",
    install_requires=['pygobject', 'pycairo']
)
