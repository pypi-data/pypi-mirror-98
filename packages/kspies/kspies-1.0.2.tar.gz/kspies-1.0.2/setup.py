import setuptools
from numpy.distutils.core import setup, Extension

print(setuptools.find_packages())

lib = Extension(
        name='kspies.kspies_fort',
        sources=['kspies/kspies_fort.f90'],
        library_dirs=['/usr/lib/'],
        include_dirs=['/usr/include'],
        libraries=['lapack']
        )

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="kspies", # Replace with your own username
    version="1.0.2",
    author="Seungsoo Nam,  Ryan J. McCarty, Hansol Park, Eunji Sim",
    author_email="skaclitz@yonsei.ac.kr",
    description="This is a python based Kohn-Sham Inversion Evaluation Software package for use with pySCF.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ssnam92.github.io/KSPies/",
    packages=setuptools.find_packages(),
    ext_modules = [lib],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Unix",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.6',
)
