from iso_tools.bcp47.BCP47Info import BCP47Info
from multi_translit.toolkit.json_tools import load
from multi_translit.data_paths import data_path


def get_script_headings_dict():
    DScriptHeadings = load(data_path('translit', 'script_headings.json'))

    D = {}
    for region, DHeadings in list(DScriptHeadings.items()):
        for heading, L in list(DHeadings.items()):
            for iso in L:
                D[BCP47Info(iso)] = (region, heading)
    return DScriptHeadings, D
