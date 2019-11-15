from multi_translit.abstract_base_classes.TranslitEngineBase import TranslitEngineBase
from multi_translit.translit.korean import enmode, demode, SKoTypes


class KoTranslit(TranslitEngineBase):
    def __init__(self):
        """
        A Korean transliterator, adapted from the
        Perl Encode::Korean module
        """
        TranslitEngineBase.__init__(self)

    def get_D_engines(self):
        # Add Korean internal conversions
        D = {}
        for system in SKoTypes:
            D['ko', 'ko_Latn|%s' % system] = (system, enmode)
            D['ko_Latn|%s' % system, 'ko'] = (system, demode)
        return D

    def translit(self, from_, to, s):
        params = self.DEngines[from_, to]
        system, fn = params
        return fn(system, s)
