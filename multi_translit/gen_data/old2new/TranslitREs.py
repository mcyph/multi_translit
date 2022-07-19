import re

DREs = {
    'self': r'.*?\sself\((?P<char>.*?)\).*?',
    'initial': r'.*?\sinitial\((?P<char>.*?)\).*?',
    'medial': r'.*?\smedial\((?P<char>.*?)\).*?',
    'final': r'.*?\sfinal\((?P<char>.*?)\).*?',
    'allforms': r'.*?\sallforms\((?P<char>.*?)\).*?',
    'sylinitial': r'.*?\ssylinitial\((?P<char>.*?)\).*?',
    'sylfinal': r'.*?\ssylfinal\((?P<char>.*?)\).*?',
    'others': r'.*?\sothers\((?P<char>.*?)\).*?'
}

for k, v in DREs:
    DREs[k] = re.compile(v, re.UNICODE)

from multi_translit.translit.Defines import DDefKeys

for k in DDefKeys:
    if k in DREs:
        DREs[DDefKeys[k]] = DREs[k]
del k, v
