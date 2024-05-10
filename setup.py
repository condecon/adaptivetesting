import setuptools

setuptools.setup(
    name="adaptivetesting",
    version="0.0.1",
    author="Jonas Engicht",
    author_email="dev@condecon.de",
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
