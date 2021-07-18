#!/bin/bash

set -e

# Linting
pylint --django-settings-module=dms.settings dms/*

# Static Analysis
bandit -r dms

# Security check
#safety check
pipenv check
