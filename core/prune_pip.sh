#!/bin/bash
pip freeze | grep -v -f requirements.txt | grep -vE "^-e" | xargs pip uninstall -y