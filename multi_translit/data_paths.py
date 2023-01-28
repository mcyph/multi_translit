import os
from multi_translit.toolkit.paths.data_paths import DataPaths

dir_path = os.path.dirname(os.path.realpath(__file__))

data_paths = DataPaths(dir_path, {
    "translit": "multi_translit/data",
    "translit_new": "multi_translit/data/my_translit",
    "icu_translit": "multi_translit/data/icu_translit",
    "translit_combinations": "multi_translit/data",
})
data_path = data_paths.data_path
