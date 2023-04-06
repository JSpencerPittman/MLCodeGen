CONDA UPDATE:
conda env export > conda_env.yml

Load Project:
conda env update --file conda_env.yml --prune
pyinstall --onefile --windowed main.py
mv dist/main main