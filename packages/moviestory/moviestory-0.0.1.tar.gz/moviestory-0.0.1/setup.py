from setuptools import setup

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
  name = "moviestory",
  version = "0.0.1",
  description = "A war against with humans and demons",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  author = "TravisRaney69", # put user name here
  author_email = "trraney328@oxboe.com", # put email here
  license = "GNU General Public License v3 (GPLv3)",
  packages=['moviestory'],
  classifiers = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
  "Operating System :: OS Independent",
],
  zip_safe=True,
  python_requires = ">=3.0",
)
'''
kk
'''