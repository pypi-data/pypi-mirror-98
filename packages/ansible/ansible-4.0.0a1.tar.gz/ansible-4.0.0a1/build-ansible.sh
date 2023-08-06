#!/bin/sh

VERSION="4.0.0a1"
MAJOR_MINOR="4.0"
MAJOR="4"

pip install --user --upgrade antsibull
git clone git@github.com:ansible-community/ansible-build-data
mkdir built

# Ansible-2.10
if test -e "ansible-build-data/${MAJOR_MINOR}" ; then
  BUILD_DATA_DIR="ansible-build-data/${MAJOR_MINOR}"
  BUILDFILE="ansible-${MAJOR_MINOR}.build"
  DEPSFILE="ansible-${VERSION}.deps"
else
  # Anything newer.  Uses semver so only the MAJOR is used.
  BUILD_DATA_DIR="ansible-build-data/${MAJOR}"
  BUILDFILE="ansible-${MAJOR}.build"
  DEPSFILE="ansible-${VERSION}.deps"
fi

antsibull-build rebuild-single "${VERSION}" --data-dir "${BUILD_DATA_DIR}" --build-file "${BUILDFILE}" --deps-file "${DEPSFILE}" --sdist-dir built --debian

#pip install twine
#twine upload "built/ansible-${VERSION}.tar.gz"