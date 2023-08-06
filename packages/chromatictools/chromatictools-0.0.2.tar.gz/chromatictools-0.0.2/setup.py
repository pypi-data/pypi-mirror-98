import setuptools
from chromatictools import __version__ as version


with open("README.md", "r") as f:
  readme = f.read()


setuptools.setup(
  name="chromatictools",
  version=version,
  author="Marco Tiraboschi",
  author_email="marco.tiraboschi@unimi.it",
  maintainer="Marco Tiraboschi",
  maintainer_email="marco.tiraboschi@unimi.it",
  description="chromatictools",
  long_description=readme,
  long_description_content_type="text/markdown",
  url="https://github.com/ChromaticIsobar/chromatictools",
  packages=setuptools.find_packages(
    include=["chromatictools", "chromatictools.*"]
  ),
  include_package_data=True,
  setup_requires=[
    "wheel",
  ],
  install_requires=[
    "gin-config",
    "numpy",
  ],
  extras_require={
    "notebooks": [
      "jupyter",
      "matplotlib",
      "seaborn",
      "tqdm",
    ],
    "docs": [
      "sphinx",
      "sphinx_rtd_theme",
      "m2r2",
      "recommonmark",
    ],
    "lint": [
      "pylint",
    ],
    "cov": [
      "coverage",
    ],
  },
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)

