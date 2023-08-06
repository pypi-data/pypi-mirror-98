import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codepod-engine",
    version="0.0.2",
    author="Dr4g0n",
    description="Codepod Engine is a cloud-based compiler engine that can be deployed as a worker that consumes the input and produces the output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["codepod-engine=codepod.console:run"]},
    packages=setuptools.find_packages(),
    install_requires=["class-registry==2.1.2", "pika==1.2.0"],
    python_requires=">=3.6",
)
