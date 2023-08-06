import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Artist-Engineering_Geek",
    version="0.0.2",
    author="Nikhil Melgiri",
    author_email="nmelgiri@uwaterloo.ca",
    description="A bunch of GANs and data downloaders to make a custom AI artist",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Fatima-x-Nikhil/Artist",
    project_urls={
        "Bug Tracker": "https://github.com/Fatima-x-Nikhil/Artist/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
