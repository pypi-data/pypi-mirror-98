import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yamltopy",
    version="1.0.0",
    author="Laszlo Szikszai",
    author_email="sziklaszlo@gmail.com",
    description="A CLI tool to convert YAML file to Python module for better load performance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/szikszail/yamltopy",
    project_urls={
        "Bug Tracker": "https://github.com/szikszail/yamltopy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    packages=["yamltopy"],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "yamltopy=yamltopy:main"
        ]
    }
)
