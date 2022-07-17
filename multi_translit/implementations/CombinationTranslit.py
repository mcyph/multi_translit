from itertools import tee
from multi_translit.abstract_base_classes.TranslitEngineBase import TranslitEngineBase
from multi_translit.translit.icu.combinations import get_D_comb
DComb = get_D_comb()


def pairwise(iterable):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class CombinationTranslit(TranslitEngineBase):
    def __init__(self, multi_translit):
        """

        :param multi_translit:
        """
        self.multi_translit = multi_translit
        TranslitEngineBase.__init__(self)

    def get_D_engines(self):
        # Add combination engines
        SPossible = set()
        for from_iso, L in self.multi_translit.get_scripts_dict().items():
            for to_iso in L:
                SPossible.add((from_iso, to_iso))

        D = {}
        for (from_iso, to_iso), L in list(DComb.items()):
            for (x, y) in pairwise(L):
                assert ((x, y) in D) or ((x, y) in SPossible), (x, y)

            # if (from_iso, to_iso) in D:
            #    print('overwriting translit:', (from_iso, to_iso), L)
            D[from_iso, to_iso] = L
        return D

    def translit(self, from_, to, s):
        params = self.DEngines[from_, to]
        for x, y in pairwise(params):
            s = self.multi_translit.translit(x, y, s)
        return s
