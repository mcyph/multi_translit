from abc import ABC, abstractmethod


class MultiTranslitBase(ABC):
    @abstractmethod
    def get_scripts_dict(self):
        """
        Get a dictionary map from the "from script" to potentially
        many "to scripts".
        For example, there may be many conversions from Latin to
        Hiragana, Cyrillic etc.

        :return: {from script: [to script 1, ...], ...}
        """
        pass

    @abstractmethod
    def get_possible_conversions_list(self, from_,
                                   remove_variant=False):
        """
        Get all possible conversions from iso `from_`.
        For example, ja_Kana-JP will also look for ja_Kana and Kana.

        :param from_: the from ISO code
        :param remove_variant: if True, then VARIANT, LANG, and
                               TERRITORY are ignored in the supplied
                               iso code. This can be useful for e.g.
                               when Hiragana can be represented in
                               multiple ways - ja_Hira-JP
                               can normally be just shortened to Hira,
                               for instance, as Hiragana isn't normally
                               associated with other languages than
                               Japanese (and Japan).
        :return: a list of [(from_iso, to_iso), ...]
        """
        pass

    @abstractmethod
    def get_best_conversions_list(self, from_iso, to_iso):
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
        pass

    @abstractmethod
    def get_best_conversion(self, from_iso, to_iso,
                            default=KeyError):
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
        pass

    @abstractmethod
    def get_all_transliterations(self, from_, s):
        """
        Transliterate `s` into all possible combinations.

        :param from_: the ISO code to convert from
        :param s: the text to convert
        :return: a list of [((from_iso, to_iso), converted_text), ...), ...]
        """
        pass

    @abstractmethod
    def translit(self, from_, to, s):
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
        pass
