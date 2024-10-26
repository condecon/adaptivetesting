import setuptools

setuptools.setup(
    name="adaptivetesting",
    version="1.0.0",
    author="Jonas Engicht",
    author_email="jonas.engicht@uni-jena.de",
    maintainer="Jonas Engicht",
    maintainer_email="jonas.engicht@uni-jena.de",
    description="A Python package for Computerized Adaptive Testing",
    long_description="""
adaptivetesting is a Python package that can be used to simulate and evaluate CAT scenarios as well as implement them in real-world testing scenarios from a single codebase.
""",
    long_description_content_type="text",
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
    license="Mozilla Public License Version 2.0"
)
