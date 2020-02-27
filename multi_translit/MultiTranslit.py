# -*- coding: utf-8 -*-
from multi_translit.toolkit.patterns.Singleton import Singleton
from multi_translit.toolkit.documentation.copydoc import copydoc
from iso_tools.ISOTools import ISOTools, NONE, LANG, TERRITORY, VARIANT

from multi_translit.implementations.CombinationTranslit import CombinationTranslit
from multi_translit.implementations.ICUTranslit import ICUTranslit
from multi_translit.implementations.KoTranslit import KoTranslit
from multi_translit.implementations.MecabTranslit import MecabTranslit
from multi_translit.implementations.MyTranslit import MyTranslit
from multi_translit.abstract_base_classes.MultiTranslitBase import MultiTranslitBase


class MultiTranslit(MultiTranslitBase,
                    Singleton,
                    ):
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
                    warnings.warn(
                        f"Warning: iso combination {from_iso}/"
                        f"{to_iso} has already been assigned"
                    )
                    continue

                DEngines[from_iso, to_iso] = engine

        if True:
            for from_, to in DEngines:
                ISOTools.verify_iso(from_)
                ISOTools.verify_iso(to)

        return DEngines

    @copydoc(MultiTranslitBase.get_D_scripts)
    def get_D_scripts(self):
        D = {}
        for from_, to in self.DEngines:
            D.setdefault(from_, []).append(to)
        return D

    @copydoc(MultiTranslitBase.get_L_possible_conversions)
    def get_L_possible_conversions(self, from_, remove_variant=False):
        # OPEN ISSUE: Add exceptions for e.g. Latin which have
        #             many false positives?
        from_ = ISOTools.remove_unneeded_info(from_)
        L = []
        DScripts = self.get_D_scripts()

        LAdd = [
            VARIANT,
            TERRITORY|VARIANT,
            VARIANT|LANG,
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

    @copydoc(MultiTranslitBase.get_best_conversion)
    def get_best_conversion(self, from_iso, to_iso, default=KeyError):
        L = self.get_L_best_conversions(from_iso, to_iso)
        if L:
            return L[0]
        elif default == KeyError:
            raise KeyError((from_iso, to_iso))
        else:
            return default

    @copydoc(MultiTranslitBase.get_L_best_conversions)
    def get_L_best_conversions(self, from_iso, to_iso):
        LRtn = []
        from_iso = ISOTools.remove_unneeded_info(from_iso)
        to_iso = ISOTools.remove_unneeded_info(to_iso)

        for xx, (conv_from_iso, conv_to_iso) in enumerate(
            self.get_L_possible_conversions(
                from_iso, remove_variant=True
            )
        ):
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
                if i_to_iso == conv_to_iso:
                    len_diff1 = -len([
                        _ for _ in ISOTools.split(conv_from_iso) if _
                    ])
                    len_diff2 = -len([
                        _ for _ in ISOTools.split(conv_to_iso) if _
                    ])

                    LRtn.append((
                        # Note this proritizes items which remove the
                        # VARIANT last, as there's a chance
                        # e.g. there's a variant in the Latin system used
                        (len_diff1, xx), (len_diff2, yy),
                        (conv_from_iso, conv_to_iso)
                    ))

        LRtn.sort()
        return [i[-1] for i in LRtn]

    @copydoc(MultiTranslitBase.get_all_transliterations)
    def get_all_transliterations(self, from_, s):
        L = []
        for i_from, i_to in self.get_L_possible_conversions(from_):
            L.append(((i_from, i_to), self.translit(i_from, i_to, s)))
        return L

    @copydoc(MultiTranslitBase.translit)
    def translit(self, from_, to, s):
        engine = self.DEngines[from_, to]
        return engine.translit(from_, to, s)


#MultiTranslit = MultiTranslit()

#translit = MultiTranslit.translit
#get_D_scripts = MultiTranslit.get_D_scripts
#get_L_possible_conversions = MultiTranslit.get_L_possible_conversions
#get_L_all_conversions = MultiTranslit.get_all_transliterations
