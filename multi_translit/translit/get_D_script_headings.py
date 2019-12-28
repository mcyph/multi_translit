from multi_translit.toolkit.json_tools import load
from multi_translit.data_paths import data_path



def get_D_script_headings():
    DScriptHeadings = load(data_path(
        'translit', 'script_headings.json'
    ))

    D = {}
    for region, DHeadings in list(DScriptHeadings.items()):
        for heading, L in list(DHeadings.items()):
            for iso in L:
                D[iso] = (region, heading)
    return DScriptHeadings, D
