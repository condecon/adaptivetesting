from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import glob
import os

# Recursively find all .pyx files
pyx_files = glob.glob("adaptivetesting/**/*.pyx", recursive=True)

# Convert each file into an Extension
extensions = [
    Extension(
        name=os.path.splitext(path.replace("/", ".").replace("\\", "."))[0],
        sources=[path],
    )
    for path in pyx_files
]

setup(
    name="adaptivetesting",
    packages=find_packages(where="."),
    ext_modules=cythonize(extensions, language_level="3"),
)
