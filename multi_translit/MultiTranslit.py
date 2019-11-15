# -*- coding: utf-8 -*-
from iso_tools import ISOTools, NONE, LANG, TERRITORY, VARIANT

from multi_translit.implementations.CombinationTranslit import CombinationTranslit
from multi_translit.implementations.ICUTranslit import ICUTranslit
from multi_translit.implementations.KoTranslit import KoTranslit
from multi_translit.implementations.MecabTranslit import MecabTranslit
from multi_translit.implementations.MyTranslit import MyTranslit
from multi_translit.abstract_base_classes.MultiTranslitBase import MultiTranslitBase


join = ISOTools.join
split = ISOTools.split


class MultiTranslit(MultiTranslitBase):
    def __init__(self):
        L = self.LEngines = []

        L.append(MyTranslit())
        L.append(ICUTranslit())
        L.append(KoTranslit())
        L.append(MecabTranslit(self))

        # Get the engines before the combination, as the combination
        # engine needs to know which engines are available
        self.DEngines = self.__get_D_engines()
        L.append(CombinationTranslit(self))

        # Update DEngines after the combinations have been added
        self.DEngines = self.__get_D_engines()

    def __get_D_engines(self):
        """
        Get a dict of {(from, to): params, ...}
        for all available transliteration engines
        """
        DEngines = {}
        for engine in self.LEngines:
            for from_iso, to_iso in engine.get_L_possible_conversions():
                if (from_iso, to_iso) in DEngines:
                    import warnings
                    warnings.warn(f"Warning: iso combination {from_iso}/"
                                  f"{to_iso} has already been assigned")
                    continue

                DEngines[from_iso, to_iso] = engine

        if True:
            for from_, to in DEngines:
                ISOTools.verify_iso(from_)
                ISOTools.verify_iso(to)

        return DEngines

    def get_D_scripts(self):
        """
        Get a dictionary map from the "from script" to potentially many "to scripts"
        for example, there may be many conversions from Latin to Hiragana, Cyrillic etc.

        :return: {from script: [to script 1, ...], ...}
        """
        D = {}
        for from_, to in self.DEngines:
            D.setdefault(from_, []).append(to)
        return D

    def get_L_possible_conversions(self, from_, remove_variant=False):
        """
        Find all possible conversions for a given ISO combination

        For example, ja_Kana_JP will also look for ja_Kana and Kana
        """
        # OPEN ISSUE: Add exceptions for e.g. Latin which have many false positives?
        from_ = ISOTools.remove_unneeded_info(from_)
        L = []
        DScripts = self.get_D_scripts()

        LAdd = [
            VARIANT, TERRITORY|VARIANT, VARIANT|LANG,
            VARIANT|LANG|TERRITORY
        ] if remove_variant else []

        for s in ISOTools.get_L_removed(
            from_,
            [
                NONE, TERRITORY, LANG,
                TERRITORY|LANG
            ] + LAdd,
            rem_dupes=True
        ):
            if s in DScripts:
                L.extend((s, v) for v in DScripts[s])
        return L

    def get_best_conversion(self, from_iso, to_iso, default=KeyError):
        """
        When converting between one script and another, it might be
        possible to convert

        :param from_iso:
        :param to_iso:
        :param default:
        :return:
        """
        L = self.get_L_best_conversions(from_iso, to_iso)
        if L:
            return L[0]
        elif default == KeyError:
            raise KeyError((from_iso, to_iso))
        else:
            return default

    def get_L_best_conversions(self, from_iso, to_iso):
        LRtn = []
        from_iso = ISOTools.remove_unneeded_info(from_iso)
        to_iso = ISOTools.remove_unneeded_info(to_iso)
        #print from_iso, to_iso

        for xx, (conv_from_iso, conv_to_iso) in enumerate(self.get_L_possible_conversions(
            from_iso,
            remove_variant=True
        )):
            for yy, i_to_iso in enumerate(ISOTools.get_L_removed(
                to_iso,
                [
                    NONE, TERRITORY, LANG,
                    TERRITORY|LANG,

                    VARIANT, TERRITORY|VARIANT, VARIANT|LANG,
                    VARIANT|LANG|TERRITORY
                ],
                rem_dupes=True
            )):
                #print 'try:', from_iso, to_iso, i_to_iso, conv_from_iso, conv_to_iso
                if i_to_iso == conv_to_iso:
                    len_diff1 = -len([_ for _ in ISOTools.split(conv_from_iso) if _])
                    len_diff2 = -len([_ for _ in ISOTools.split(conv_to_iso) if _])

                    LRtn.append((
                        # Note this proritizes items which remove the VARIANT last, as
                        # there's a chance e.g. there's a variant in the Latin system used
                        (len_diff1, xx), (len_diff2, yy),
                        (conv_from_iso, conv_to_iso)
                    ))

        LRtn.sort()
        return [i[-1] for i in LRtn]

    def get_L_all_conversions(self, from_, s):
        L = []
        for i_from, i_to in self.get_L_possible_conversions(from_):
            L.append(((i_from, i_to), self.translit(i_from, i_to, s)))
        return L

    def translit(self, from_, to, s):
        engine = self.DEngines[from_, to]
        return engine.translit(from_, to, s)


MultiTranslit = MultiTranslit()

translit = MultiTranslit.translit
get_D_scripts = MultiTranslit.get_D_scripts
get_L_possible_conversions = MultiTranslit.get_L_possible_conversions
get_L_all_conversions = MultiTranslit.get_L_all_conversions


if __name__ == '__main__':
    from pprint import pprint
    pprint(MultiTranslit.DEngines)
    #raise

    #print 'BEST CONVERSION:', Translit.get_best_conversion('ja_Jpan-AU|VARIANT', 'ja_Latn')
    #print 'BEST CONVERSION:', Translit.get_best_conversion('ja_Jpan-AU', 'ja_Latn')

    #print Translit.translit('Latn', 'ja_Kana', 'nihongo')

    print(MultiTranslit.translit('ja', 'ja_Latn|FONIPA', 'aa'))

    txt = '私はボブ。日本語で書きますよ！どうしてそんなことを言うの？'
    print(MultiTranslit.translit('ja', 'ja_Kana', txt))
    print(MultiTranslit.translit('ja', 'ja_Hira', txt))
    print(MultiTranslit.translit('ja', 'Latn', txt))

    print([i for i in MultiTranslit.DEngines if 'ja' in i[0]])

    txt = '''(sŏ-ul=yŏn-hap-nyu-sŭ) i-chun-sŏ ki-cha = 4ㆍ11 ch'ong-sŏn kong-ch'ŏn tang-si'''
    txt_ko = '(서울=연합뉴스) 이준서 기자 = 4ㆍ11 총선 공천 당시'
    for system in SKoTypes:
        latin = MultiTranslit.translit('ko', 'ko_Latn|%s' % system, txt_ko)
        print(latin)
        print(MultiTranslit.translit('ko_Latn|%s' % system, 'ko_Hang', latin))
