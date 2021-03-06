import json
from multi_translit.data_paths import data_path


# NOTE: See also iter_translit_files.py for the
# "translit-mappings.json" generation script


def get_D_translit_mappings():
    with open(
        data_path('translit_new', 'translit-mappings.json'),
        'r', encoding='utf-8'
    ) as f:
        return json.loads(f.read())

