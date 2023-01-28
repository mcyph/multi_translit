# -*- coding: utf-8 -*-
import warnings

from iso_tools.bcp47.BCP47Info import BCP47Info

from multi_translit.toolkit.patterns.Singleton import Singleton
from multi_translit.implementations.KoTranslit import KoTranslit
from multi_translit.implementations.MyTranslit import MyTranslit
from multi_translit.implementations.ICUTranslit import ICUTranslit
from multi_translit.implementations.MecabTranslit import MecabTranslit
from multi_translit.implementations.CombinationTranslit import CombinationTranslit

from speedysvc.service_method import service_method


class MultiTranslit(Singleton):
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
            for from_iso, to_iso in engine.get_possible_conversions_list():
                if (from_iso, to_iso) in DEngines:
                    warnings.warn(f"Warning: iso combination {from_iso}/"
                                  f"{to_iso} has already been assigned")
                    continue
                DEngines[from_iso, to_iso] = engine
        return DEngines

    @service_method()
    def get_scripts_dict(self):
        """
        Get a dictionary map from the "from script" to potentially
        many "to scripts".
        For example, there may be many conversions from Latin to
        Hiragana, Cyrillic etc.

        :return: {from script: [to script 1, ...], ...}
        """
        D = {}
        for from_, to in self.DEngines:
            D.setdefault(from_, []).append(to)
        return D

    @service_method(decode_params={'from_': lambda x: BCP47Info(x)},
                    encode_params={'from_': lambda x: str(x)})
    def get_possible_conversions_list(self,
                                      from_: BCP47Info,
                                      remove_variant: bool = False):
        """
        Get all possible conversions from iso `from_`.
        For example, ja-Kana-JP will also look for ja-Kana and Kana.

        :param from_: the from ISO code
        :param remove_variant: if True, then VARIANT, LANG, and
                               TERRITORY are ignored in the supplied
                               iso code. This can be useful for e.g.
                               when Hiragana can be represented in
                               multiple ways - ja-Hira-JP
                               can normally be just shortened to Hira,
                               for instance, as Hiragana isn't normally
                               associated with other languages than
                               Japanese (and Japan).
        :return: a list of [(from_iso, to_iso), ...]
        """

        # OPEN ISSUE: Add exceptions for e.g. Latin which have
        #             many false positives?
        from_ = ISOTools.remove_unneeded_info(from_)
        L = []
        DScripts = self.get_scripts_dict()

        LAdd = [
            VARIANT,
            TERRITORY | VARIANT,
            VARIANT | LANG,
            VARIANT | LANG | TERRITORY
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

    @service_method(decode_params={'from_iso': lambda x: BCP47Info(x),
                                   'to_iso': lambda x: BCP47Info(x)},
                    encode_params={'from_iso': lambda x: str(x),
                                   'to_iso': lambda x: str(x)})
    def get_best_conversion(self,
                            from_iso: BCP47Info,
                            to_iso: BCP47Info,
                            default='KeyError'):
        """
        Uses get_best_conversions_list to find the best conversion
        for a given script combination.

        :param from_iso: the ISO code to convert from
        :param to_iso: the ISO code to convert to
        :param default: the default value to return if a conversion
                        not found - raises a KeyError by default
        :return: a tuple of (from_iso, to_iso) - the combination
                 of ISOs to pass to the `translit` method.
        """
        default = KeyError if default == 'KeyError' else default
        L = self.get_best_conversions_list(from_iso, to_iso)

        if L:
            return L[0]
        elif default == KeyError:
            raise KeyError((from_iso, to_iso))
        else:
            return default

    @service_method(decode_params={'from_iso': lambda x: BCP47Info(x),
                                   'to_iso': lambda x: BCP47Info(x)},
                    encode_params={'from_iso': lambda x: str(x),
                                   'to_iso': lambda x: str(x)})
    def get_best_conversions_list(self,
                                  from_iso: BCP47Info,
                                  to_iso: BCP47Info):
        """
        Guesses the best conversions, e.g. so that if the script of the
        to_iso isn't specified, it'll still find the closest conversions.

        This isn't 100% accurate, but should hopefully be good enough
        in most cases.

        For instance, while a generic Cyrillic to Latin conversion might
        be possible, a more specific Ukrainian/Russian Cyrillic to Latin
        conversion might be able to give better results. This method
        attempts to find the best/most appropriate conversions possible.

        :param from_iso: the ISO code to convert from
        :param to_iso: the ISO code to convert to
        :return: the default value to return if a conversion
                 not found - raises a KeyError by default
        """
        return_list = []
        from_iso = ISOTools.remove_unneeded_info(from_iso) # FIXME!!
        to_iso = ISOTools.remove_unneeded_info(to_iso)

        for xx, (conv_from_iso, conv_to_iso) in enumerate(
            self.get_possible_conversions_list(
                from_iso, remove_variant=True
            )
        ):
            for yy, i_to_iso in enumerate(ISOTools.get_L_removed(
                to_iso,
                [
                    NONE,
                    TERRITORY,
                    LANG,
                    TERRITORY | LANG,
                    VARIANT,
                    TERRITORY | VARIANT,
                    VARIANT | LANG,
                    VARIANT | LANG | TERRITORY
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

                    return_list.append((
                        # Note this proritizes items which remove the
                        # VARIANT last, as there's a chance
                        # e.g. there's a variant in the Latin system used
                        (len_diff1, xx), (len_diff2, yy),
                        (conv_from_iso, conv_to_iso)
                    ))

        return_list.sort()
        return [i[-1] for i in return_list]

    @service_method(decode_params={'from_': lambda x: BCP47Info(x)},
                    encode_params={'from_': lambda x: str(x)})
    def get_all_transliterations(self,
                                 from_: BCP47Info,
                                 s: str):
        """
        Transliterate `s` into all possible combinations.

        :param from_: the ISO code to convert from
        :param s: the text to convert
        :return: a list of [((from_iso, to_iso), converted_text), ...), ...]
        """
        L = []
        for i_from, i_to in self.get_possible_conversions_list(from_):
            L.append(((i_from, i_to), self.translit(i_from, i_to, s)))
        return L

    @service_method(decode_params={'from_': lambda x: BCP47Info(x),
                                   'to': lambda x: BCP47Info(x)},
                    encode_params={'from_': lambda x: str(x),
                                   'to': lambda x: str(x)})
    def translit(self,
                 from_: BCP47Info,
                 to: BCP47Info,
                 s: str):
        """
        Convert from iso code `from_` to iso code `to`
        (i.e. convert the alphabet of `s` from `from_` to `to`)
        from_ might be e.g. 'Latn' for Latin script, and to
        might be 'Hira' for Japanese Hiragana.

        :param from_: the iso code to convert from
        :param to: the iso code to convert to
        :param s: the text to convert
        :return: the converted text
        """
        engine = self.DEngines[from_, to]
        return engine.translit(from_, to, s)

    @service_method()
    def get_script_headings_dict(self):
        from multi_translit.utils.get_script_headings_dict import get_script_headings_dict
        return get_script_headings_dict()


#MultiTranslit = MultiTranslit()

#translit = MultiTranslit.translit
#get_scripts_dict = MultiTranslit.get_scripts_dict
#get_possible_conversions_list = MultiTranslit.get_possible_conversions_list
#get_L_all_conversions = MultiTranslit.get_all_transliterations
