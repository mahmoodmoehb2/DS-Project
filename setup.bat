@echo off
python -m venv my_env
my_env\Scripts\python.exe -m pip install --upgrade pip
my_env\Scripts\python.exe -m pip install -r requirements.txt
my_env\Scripts\python.exe -m ipykernel install --user --name=my_env --display-name "Python (my_env)"
echo.
echo Setup fertig. Jupyter starten mit: my_env\Scripts\python.exe -m notebook