#!/usr/bin/env bash
set -e

trap error_handler ERR

error_handler() {
  exitcode=$?
  echo -e "$SET_ERROR_TEXT $BASH_COMMAND failed!!! $RESET_FORMATTING"
  # Some more clean up code can be added here before exiting
  exit $exitcode
}


echo "Running black ..." && python -m black library_app
echo "Running isort ..." && python -m isort library_app tests --profile black
echo "Running flake8 ..." && python -m flake8 library_app
echo "Running bandit ..." && python -m bandit library_app
echo "Running mypy ..." && python -m mypy library_app