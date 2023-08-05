import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymaketool",
    version="1.0.15-rc2",
    author="Ericson Joseph",
    author_email="ericsonjoseph@gmail.com",
    description="Python Makefile Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts = ['scripts/pymaketool', 'scripts/pymaketesting', 'scripts/pybuildanalyzer'],
    url="https://github.com/ericsonj/pymaketool",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
