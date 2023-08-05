import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyridl", # Replace with your own username
    version="0.1.0",
    author="Kyle Hall - IRICS",
    author_email="kjhall@iri.columbia.edu",
    description="mini, unofficial IRI Data Library API ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/hallkjc01/pyridl",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_dir={"pyridl": "src"},
    #packages=setuptools.find_packages(where="src"),
    packages=["pyridl"],
    python_requires=">=3.0",
)