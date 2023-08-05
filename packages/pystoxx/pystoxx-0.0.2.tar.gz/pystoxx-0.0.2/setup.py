import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
        name="pystoxx",
        version="0.0.2",
        author="Saleh Alkhalifa",
        author_email="alkhalifas@recursiv.tech",
        description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/recursivllc/pystoxx",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        packages=setuptools.find_packages(),
        python_requires='>3.6',
        )
