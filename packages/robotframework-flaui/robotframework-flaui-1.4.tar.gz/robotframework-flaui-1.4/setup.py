import os
from setuptools import setup, find_packages, Distribution

# https://www.appveyor.com/docs/environment-variables/
repo_tag = os.environ.get('APPVEYOR_REPO_TAG', 'false')
tag_version = os.environ.get('APPVEYOR_REPO_TAG_NAME', '0')
build_version = os.environ.get('APPVEYOR_BUILD_VERSION', '0')
build_number = os.environ.get('APPVEYOR_BUILD_NUMBER', '0')
release = True

print('---------------------Branch Informations---------------------')
print('Release: ' + str(release))
print('APPVEYOR_REPO_TAG: ' + repo_tag)
print('APPVEYOR_REPO_TAG_NAME: ' + tag_version)
print('APPVEYOR_BUILD_VERSION: ' + build_version)
print('APPVEYOR_BUILD_NUMBER: ' + build_number)
print('-------------------------------------------------------------')


class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""

    # pylint: disable=no-self-use
    def has_ext_modules(self):
        """Distribution which always forces a binary package with platform name"""
        return True


LONG_DESCRIPTION = ''
with open("Readme.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

REQUIREMENTS = []
with open("requirements.txt", "r") as f:
    REQUIREMENTS = list(filter(lambda s: s != "", f.read().split("\n")))

if release:
    VERSION = "{}".format("1.4")
else:
    VERSION = "{}rc{}".format(build_version, build_number)

setup(name="robotframework-flaui",
      version=VERSION,
      description="Windows GUI testing library for Robot Framework",
      long_description=LONG_DESCRIPTION,
      long_description_content_type="text/markdown",
      author="G DATA CyberDefense AG",
      author_email="opensource@gdata.de",
      install_requires=REQUIREMENTS,
      packages=find_packages("src"),
      package_dir={"FlaUILibrary": "src/FlaUILibrary"},
      package_data={"FlaUILibrary": ["bin/*.dll"]},
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: Microsoft",
      ],
      distclass=BinaryDistribution,
      platforms=['Windows']
      )
