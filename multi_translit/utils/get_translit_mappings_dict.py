import json
from iso_tools.bcp47.BCP47Info import BCP47Info
from multi_translit.data_paths import data_path


# NOTE: See also iter_translit_files.py for the
# "translit-mappings.json" generation script


def get_D_translit_mappings():
    with open(
        data_path('translit_new', 'translit-mappings.json'),
        'r', encoding='utf-8'
    ) as f:
        out = {}
        for k, items in json.loads(f.read()).items():
            items_out = []
            for relative_path, other_iso, direction in items:
                items_out.append((relative_path,
                                  BCP47Info(other_iso),
                                  direction))
            out[BCP47Info(k)] = items_out
        return out

