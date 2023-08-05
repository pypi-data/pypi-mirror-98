# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Reachability Analysis
#
# (C) 2020 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------

import setuptools
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='vehicle_pedestrian',
      version='0.0.1',
      description='Vehicle and pedestrian interaction',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/ga74kud/vehicle_pedestrian',
      author='Michael Hartmann',
      author_email='michael.hartmann@v2c2.at',
      license='GNU GENERAL PUBLIC LICENSE',
      packages=setuptools.find_packages(),
      install_requires=[
          "scipy",
          "numpy",
          "reachab",
          "matplotlib",
          "argparse",
          "shapely"
        ],
      zip_safe=False,
      classifiers = [
          "Programming Language :: Python :: 3",
          "Operating System :: OS Independent",
                             ],
      python_requires = ">=3.6",
)
