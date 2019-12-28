import os
from multi_translit.toolkit.paths.data_paths import DataPaths

dir_path = os.path.dirname(os.path.realpath(__file__))

data_paths = DataPaths(dir_path, {
    "translit": "multi_translit/data/translit",
    "translit_old": "multi_translit/data/translit_old",
    "translit_new": "multi_translit/data/translit_new",
    "icu_translit": "multi_translit/data/icu_translit",
    "translit_combinations": "multi_translit/data/translit_combinations",
})
data_path = data_paths.data_path
