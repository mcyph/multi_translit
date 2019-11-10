# -*- coding: utf-8 -*-
from itertools import tee
from PyICU import Transliterator, UTransDirection, ICUError

from multi_translit.data_paths import data_path
from toolkit.json_tools import load

from iso_tools import ISOTools, NONE, LANG, TERRITORY, VARIANT

from multi_translit.translit.korean import enmode, demode, SKoTypes
from multi_translit.translit.get_D_translit_mappings import get_D_translit_mappings
from multi_translit.translit.icu.combinations import get_D_comb
from multi_translit.translit.my_engine.TranslitEngine import TranslitEngine

DTranslitMappings = get_D_translit_mappings()
DComb = get_D_comb()


ENGINE_ICU = 0
ENGINE_MECAB = 1
ENGINE_KO = 2
ENGINE_MINE = 3
ENGINE_CJKLIB = 4
ENGINE_COMBINATION = 5


join = ISOTools.join
split = ISOTools.split


def pairwise(iterable):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class MultiTranslit:
    def __init__(self):
        self.DEngines = self.get_D_engines()
        self.DICU = {} # FIXME! =================================================
        self._remove_invalid()

    def _remove_invalid(self):
        for from_key, to_key in list(self.DEngines.keys()):
            if self.DEngines[from_key, to_key][0] != ENGINE_ICU:
                continue

            # Remove invalid engines (somewhat hackish, but oh well...)
            try:
                self.translit(from_key, to_key, 'a')
            except ICUError:
                del self.DEngines[from_key, to_key]

    def mapping_to_iso(self, part3, script=None, variant=None, other=None):
        if other:
            if not part3 and other[0] and other[0] != 'ben':
                part3 = other[0]

        r = join(part3, script, variant=variant)

        DMap = {
          'zh_Hani': 'zh',
          'Hani': 'zh',
          'ja_Zyyy': 'ja_Hrkt',
          'zh_Bopo|Zhuyin': 'zh_Bopo',
          'Bopo': 'zh_Bopo',
          'zh_Latn': 'zh_Latn|x-Pinyin'
        }

        if r in DMap:
            r = DMap[r]

        return r

    def get_D_engines(self):
        """
        Get a dict of {(from, to): params, ...}
        for all available translteration engines
        """
        D = {}

        DMappings = load(data_path('translit', 'script_mappings.json'))
        LUnknownScripts = []

        for engine in Transliterator.getAvailableIDs():
            #print engine
            from_, _, to = engine.partition('-')
            to = to.replace('/', '-')

            try:
                from_key = self.mapping_to_iso(*DMappings[from_], other=DMappings[to])
            except KeyError as e:
                LUnknownScripts.append('%s-%s' % (from_, to))
                continue

            try:
                to_key = self.mapping_to_iso(*DMappings[to], other=DMappings[from_])
            except KeyError as e:
                LUnknownScripts.append('%s-%s' % (to, from_))
                continue

            SIgnore = {
                'ko_Zyyy',
                'th_Zyyy',
                'el_Zyyy',
                'cs_Zyyy',
                'es_Zyyy',
                'ko_Zyyy',
                'zh_Zyyy',
                'ar_Zyyy',
                'he_Zyyy',
                'syr_Zyyy',
                'hy_Zyyy',
                'ka_Zyyy',
                'pl_Zyyy',
                'ro_Zyyy',
                'ru_Zyyy',
                'am_Zyyy', # TODO: Add latin -> amharic
                'sk_Zyyy'
            }

            if from_key in SIgnore or to_key in SIgnore:
                continue

            D[from_key, to_key] = (
                ENGINE_ICU,
                (engine, UTransDirection.FORWARD)
            )

            if not (to_key, from_key) in D:
                if 'Zyyy' in from_key and not 'Zyyy' in str(to_key):
                    #print('IGNORED:', from_key, to_key)
                    # HACK: Disable "to common"
                    continue

                D[to_key, from_key] = (
                    ENGINE_ICU,
                    (engine, UTransDirection.REVERSE)
                )

        if LUnknownScripts:
            from warnings import warn
            warn(
                "Scripts in ICU not recognised by multi_translit engine: %s"
                % ', '.join(LUnknownScripts)
            )

        # Add internal python transliterators
        #print DTranslitMappings

        with open(data_path('translit', 'ignored_isos.txt'), 'r') as f:
            # HACK: Ignore these (mostly fairly uncommonly used) transliteration systems
            # as they probably have errors/I don't have much time to maintain them
            SIgnoredISOs = f.read().split('\n')

        for from_iso, L in list(DTranslitMappings.items()):
            for path, to_iso, direction in L:

                if ISOTools.split(from_iso).lang in SIgnoredISOs:
                    continue
                elif ISOTools.split(to_iso).lang in SIgnoredISOs:
                    continue

                D[from_iso, to_iso] = (
                    ENGINE_MINE,
                    (path, direction)
                )

        # Add Korean internal conversions
        for system in SKoTypes:
            D['ko', 'ko_Latn|%s' % system] = (
                ENGINE_KO, (system, enmode)
            )

            D['ko_Latn|%s' % system, 'ko'] = (
                ENGINE_KO, (system, demode)
            )

        # Add Japanese internal conversions
        D['ja', 'ja_Hira'] = (
            ENGINE_MECAB, ('ja_Kana', 'ja_Hira', False)
        )

        D['ja', 'ja_Kana'] = (
            ENGINE_MECAB, (None, None, False)
        ) # Already Katakana!

        D['ja', 'Latn'] = (
            ENGINE_MECAB, ('ja_Kana', 'ja_Latn', True)
        )

        # Add combination engines
        for (from_iso, to_iso), L in list(DComb.items()):
            for (x, y) in pairwise(L):
                assert (x, y) in D, (x, y)

            #if (from_iso, to_iso) in D:
            #    print('overwriting translit:', (from_iso, to_iso), L)

            D[from_iso, to_iso] = (
                ENGINE_COMBINATION, L
            )

        if True:
            [(ISOTools.verify_iso(from_), ISOTools.verify_iso(to)) for from_, to in D]
        return D

    def get_D_scripts(self):
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
        L = self.get_L_best_conversions(
            from_iso, to_iso,
        )

        if L:
            return L[0]
        elif default == KeyError:
            raise KeyError((from_iso, to_iso))
        else:
            return default

    def get_L_best_conversions(self, from_iso, to_iso):
        """
        Guesses the best conversions, e.g. so that if the script of the
        to_iso isn't specified, it'll still find the closest conversions

        This isn't 100% accurate, but should hopefully be good enough in most cases
        """
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
        """
        Convert `s` into all possible combinations
        """
        L = []
        for i_from, i_to in self.get_L_possible_conversions(from_):
            L.append(((i_from, i_to), self.translit(i_from, i_to, s)))
        return L

    def translit(self, from_, to, s):
        """
        Convert the alphabet of `s` from `from_` to `to`
        """
        typ, params = self.DEngines[from_, to]


        if typ == ENGINE_ICU:
            if not params in self.DICU:
                self.DICU[params] = Transliterator.createInstance(*params)

            return self.DICU[params].transliterate(s)

        elif typ == ENGINE_MECAB:
            try:
                global to_katakana
                to_katakana
            except:
                from mecab.word_boundaries import to_katakana

            r = to_katakana(s, wa_hack=params[2])
            if params[0]:
                r = self.translit(params[0], params[1], r)
            return str(r)

        elif typ == ENGINE_KO:
            system, fn = params
            return fn(system, s)

        elif typ == ENGINE_MINE:
            te = TranslitEngine(
                data_path('translit_new', params[0]),
                params[1]
            )
            return te.convert(s)

        elif typ == ENGINE_COMBINATION:
            #print params
            for x, y in pairwise(params):
                #print x, y
                s = self.translit(x, y, s)
            return s


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