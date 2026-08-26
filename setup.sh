#!/bin/bash
python3 -m venv my_env
my_env/bin/python -m pip install --upgrade pip
my_env/bin/python -m pip install -r requirements.txt
my_env/bin/python -m ipykernel install --user --name=my_env --display-name "Python (my_env)"
echo "Setup fertig. Jupyter starten mit: my_env/bin/python -m notebook"