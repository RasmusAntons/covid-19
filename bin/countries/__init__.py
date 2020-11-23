import os
import importlib
impl = {}
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    impl[module[:-3]] = importlib.import_module(f'.{module[:-3]}', 'bin.countries')
del module
