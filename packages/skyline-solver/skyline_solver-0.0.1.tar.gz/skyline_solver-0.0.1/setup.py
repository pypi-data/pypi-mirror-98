from setuptools import find_packages
import setuptools

from numpy.distutils.core import setup, Extension

ext1 = Extension(name='skyline',
                 sources=['skyline_solver/skyline/skyline.f90'],
                 f2py_options=['--quiet'],
                 #extra_f90_compile_args =['-static']
                )

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name="skyline_solver",
      version="0.0.1",
      author="Mojtaba Farrokh",
      email="farrokh959@gmail.com",
      description="A Skyline solver for linear sets",
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=["skyline_solver","skyline_solver/skyline"], #find_packages(where="src"),
      ext_modules=[ext1],
      install_requires = ["numpy"],
      python_requires='>=3')
