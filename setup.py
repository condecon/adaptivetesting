import setuptools

setuptools.setup(
    name="adaptivetesting",
    version="1.0.0",
    author="Jonas Engicht",
    author_email="jonas.engicht@uni-jena.de",
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
        "numpy"
    ]
)
