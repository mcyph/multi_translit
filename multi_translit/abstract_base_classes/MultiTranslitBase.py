from abc import ABC, abstractmethod


class MultiTranslitBase(ABC):
    @abstractmethod
    def get_D_scripts(self):
        """

        :return:
        """
        pass

    @abstractmethod
    def get_L_possible_conversions(self, from_,
                                   remove_variant=False):
        """
        Get all possible conversions from iso `from_`.

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
    def get_best_conversion(self, from_iso, to_iso,
                            default=KeyError):
        """

        :param from_iso:
        :param to_iso:
        :param default:
        :return:
        """
        pass

    @abstractmethod
    def get_L_best_conversions(self, from_iso, to_iso):
        """
        Guesses the best conversions, e.g. so that if the script of the
        to_iso isn't specified, it'll still find the closest conversions.

        This isn't 100% accurate, but should hopefully be good enough
        in most cases.

        :param from_iso:
        :param to_iso:
        :return:
        """
        pass

    @abstractmethod
    def get_L_all_conversions(self, from_, s):
        """
        Convert `s` into all possible combinations.

        :param from_:
        :param s:
        :return:
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

    # TODO: Should this be moved here?
    #@abstractmethod
    #def get_D_script_headings(self):
    #    """

    #    :return:
    #    """
    #    pass
