#!/bin/bash

set -o nounset
set -o errexit


case "$OSTYPE" in
  darwin*)  COVERAGE="coverage-3.10" ;;
  linux*)   COVERAGE="python3-coverage" ;;
esac


$COVERAGE run --branch -m unittest discover
$COVERAGE report --show-missing
$COVERAGE erase
