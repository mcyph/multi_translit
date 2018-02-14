# -*- coding: utf-8 -*-
from lang_data import ISOTools


DScriptsVariants = {
    'Latin': 'Latn',
    'IPA': 'Latn|FONIPA',
    'Japanese': 'Jpan',
    'Osmanya': 'Osma',
    'Yi': 'Yiii',
    'Hanunoo': 'Hano',
    'Canadian Syllabics': 'Cans',
    'Cyrillic': 'Cyrl',
    'Bopomofo': 'Bopo',
    'Thaana': 'Thaa',
    'Cherokee': 'Cher',
    'Braille': 'Brai',
    'Chinese (Unified)': 'Hani',
    'Hangul': 'Hang',
    'Tagbanwa': 'Tagb',
    'Kharoshti': 'Khar',
    'Buhid': 'Buhd',
    'Arabic': 'Arab',
    'Tai Le': 'Tale',
    'Ogham': 'Ogam',
    'Chinese (Simplified)': 'Hans',
    'Chinese (Traditional)': 'Hant',
    'Cypriot': 'Cprt',
    'Linear B': 'Linb',
    'Katakana': 'Kana',
    'Hiragana': 'Hira',
    'Kana': 'Hrkt',
    'Hebrew': 'Hebr',
    'Gothic': 'Goth',
    'Thai': 'Thai',
    'Georgian': 'Geor',

    "Armenian": "Armn",
    "Unknown": "Zzzz",
    "Old Italic": "Ital",
    "Lontara": "Bugi",

    "PinYin": "Latn|Numeric Pinyin",
    "Pinyin Accents": "Latn|x-Pinyin",
    "Kana": "Hrkt",
}


DFonts = {
    "Lontara": "Lontara",
    "GuoinII": "Latin",
    "Tongyong": "Latin",
    "Pinyin Accents": "Pinyin Accents",
    "Pinyin U Unaccented": "Latin",
    "Japanese": "Japanese",
    "Hiragana": "Hiragana",
    "IPA Tongyong": "IPA",
    "Kirghiz IPA (ALPHA)": "IPA",
    "Wade-Giles": "Latin",
    "Osmanya": "Osmanya",
    "IPA South (ALPHA)": "IPA",
    "Yi": "Yi",
    "Latin": "Latin",
    "Hanunoo": "Hanunoo",
    "Pinyin U Accented": "Latin",
    "Canadian Syllabics": "Canadian Syllabics",
    "Cyrillic": "Cyrillic",
    u"Latin Łacinka": "Latin",
    "French": "Latin",
    "Zhuyin": "Bopomofo",
    "Thaana": "Thaana",
    "Cherokee": "Cherokee",
    "Nanori": "Hiragana",
    "Latin KNAB": "Latin",
    "Romaji (Hepburn)": "Latin",
    "Latin UN": "Latin",
    "Latin UNGEGN": "Latin",
    "Thai": "Thai",
    "Latin Official": "Latin",
    "Latin ALA-LC": "Latin",
    "On": "Katakana",
    "Latin TITUS": "Latin",
    "Manyogana": "Chinese (Traditional)",
    "Braille": "Braille",
    "PinYin": "PinYin",
    "Hanja": "Chinese (Unified)",
    "Azerbaijani IPA (ALPHA)": "IPA",
    "Hangul": "Hangul",
    "Gwoyeu Romatzyh": "Latin",
    "Latin E-C Modern": "Latin",
    "Jyutping": "Latin",
    "Yale": "Latin",
    "Ugaritic": "Cyrillic",
    "Tagbanwa": "Tagbanwa",
    "Kharoshti": "Kharoshti",
    "Buhid": "Buhid",
    "Arabic": "Arabic",
    "Tai Le": "Tai Le",
    "Ogham": "Ogham",
    "CMU Pron": "Latin",
    "IPA": "IPA",
    "Cypriot": "Cypriot",
    "Chinese (Unified)": "Chinese (Unified)",
    "Hebrew": "Hebrew",
    "Komi IPA (ALPHA)": "IPA",
    "Dungan IPA (ALPHA)": "IPA",
    "Dargwa IPA (ALPHA)": "IPA",
    "IPA North (ALPHA)": "IPA",
    "Kana": "Kana",
    "Arabic Compatibility": "Arabic",
    "Old Italic": "Old Italic",
    "Kabardian IPA (ALPHA)": "IPA",
    "Gothic": "Gothic",
    "Latin (UNGEGN)": "Latin",
    "Kun": "Hiragana",
    "Katakana": "Katakana",
    "Guangdong": "Latin",
    "Linear B": "Linear B",
    "Latin ISO 11940": "Latin",
    "Latin ISO 9": "Latin",
    "Latin WWS": "Latin",
    "Latin Allworth": "Latin",
    "Latin BGN/PCGN": "Latin",
    "Even IPA (ALPHA)": "IPA",
    "Western": "Armenian",
    "Latin Old Official": "Latin",
    "Latin Official TDS 565": "Latin",
    "Latin Official WWS": "Latin",
    "Latin Roman Official": "Latin",
    "Latin IDS": "Latin",
    "Latin ISO 9 R": "Latin",
    "Latin ISO 9984": "Latin",
    "Latin IKE": "Latin",
    "Latin National": "Latin",
    "Latin Former Official": "Latin",
    "Latin AllWorth": "Latin",
    "Latin Emirova": "Latin",
}


def iso_convert(iso, variant):
    font = DFonts.get(variant)
    item = DScriptsVariants.get(
        variant, DScriptsVariants.get(font)
    )


    if not item:
        print '** SCRIPT WARNING:', iso, variant
        script = variant = None # WARNING!
    else:
        if '|' in item:
            script, _, variant = item.partition('|')
        else:
            script = item


    if variant and variant.startswith('%s ' % font):
        variant = variant[len(font)+1:]
    elif variant and font == variant:
        variant = None


    if iso == 'mol':
        iso = 'ro' # HACK!

    try:
        return ISOTools.join( #ISOTools.remove_unneeded_info
            part3=iso if not '?' in iso else 'und',
            script=script,
            variant=variant or None
        )
    except:
        print '** SCRIPT WARNING 2:', iso, script, variant
        return 'FIXME: %s,%s' % (iso, variant)
