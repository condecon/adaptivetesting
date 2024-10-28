import setuptools

with open("README.md", "r") as file:
    long_description = file.read()
    file.close()


setuptools.setup(
    name="adaptivetesting",
    version="1.0.0-rc1",
    author="Jonas Engicht",
    author_email="jonas.engicht@uni-jena.de",
    maintainer="Jonas Engicht",
    maintainer_email="jonas.engicht@uni-jena.de",
    description="adaptivetesting is a Python package that can be used to simulate and evaluate custom CAT scenarios as well as implement them in real-world testing scenarios from a single codebase",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/condecon/adaptivetesting",
    packages=["adaptivetesting", 
              "adaptivetesting.data",
              "adaptivetesting.implementations",
              "adaptivetesting.math",
              "adaptivetesting.models",
              "adaptivetesting.services",
              "adaptivetesting.simulation",
              "adaptivetesting.tests"],
    install_requires=[
        "numpy>=1.20.0"
    ],
    license="Mozilla Public License Version 2.0",
    keywords=["statistics", "psychology", "item-response-theory", "computerized-adaptive-testing"],
    python_requires=">3.10"
)
