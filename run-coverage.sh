#!/usr/bin/bash

# Run tests on application.
# Show coverage report if all tests pass.

# From the excellent Ned Batchelder
# https://coverage.readthedocs.io/

set -o nounset
set -o errexit
set +o xtrace


#Find coverage command in Debian/Ubuntu or Mac OS + MacPorts
if [ -x "$(command -v python3-coverage)" ]; then
    COVERAGE=python3-coverage
elif [ -x "$(command -v coverage-3.9)" ]; then
    COVERAGE=coverage-3.9
else
    echo "No Python coverage command found"
    exit 1
fi


# Find coverage command in Debian/Ubuntu or Mac OS + MacPorts
if [ -x "$(command -v python3-coverage)" ]; then
    COVERAGE=python3-coverage
elif [ -x "$(command -v coverage-3.12)" ]; then
    COVERAGE=coverage-3.12
else
    echo "No Python coverage command found"
    exit 1
fi


# Run unit tests under the supervision of 'coverage.py'
$COVERAGE run --branch --source cine,tests --module unittest --catch --failfast
$COVERAGE report --show-missing
$COVERAGE erase
