#!/bin/bash

set -e

# Security check
#safety check
pipenv check

# Linting
pylint --django-settings-module=dms.settings dms/*

# Static Analysis
bandit -r dms
