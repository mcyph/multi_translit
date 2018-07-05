from json import load, dump
from iso_tools import ISOTools

DOut = {}

for heading, L in load(open('script_headings.json', 'rb')).items():
    for key in L:
        while key.count('|') != 2:
            key += '|'

        script, lang, variant = key.split('|')
        print script, lang, variant

        DOut.setdefault(heading, []).append(ISOTools.join(part3=lang, script=script, variant=variant))

dump(DOut, open('script_headings-2.json', 'wb'), indent=4)
