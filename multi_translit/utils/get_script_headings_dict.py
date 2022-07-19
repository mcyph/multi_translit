from iso_tools.ISOCode import ISOCode
from multi_translit.toolkit.json_tools import load
from multi_translit.data_paths import data_path


def get_script_headings_dict():
    DScriptHeadings = load(data_path('translit', 'script_headings.json'))

    D = {}
    for region, DHeadings in list(DScriptHeadings.items()):
        for heading, L in list(DHeadings.items()):
            for iso in L:
                D[ISOCode(iso)] = (region, heading)
    return DScriptHeadings, D
