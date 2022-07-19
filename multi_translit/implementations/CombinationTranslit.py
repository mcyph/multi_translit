import codecs
from glob import glob
from json import loads
from itertools import tee
from iso_tools.ISOTools import ISOTools

from multi_translit.data_paths import data_path
from multi_translit.abstract_base_classes.TranslitEngineBase import TranslitEngineBase


def get_D_comb():
    D = {}
    for path in glob(data_path('translit_combinations', '*.map')):
        with codecs.open(path, 'rb', 'utf-8') as f:
            for line in f:
                if not line.strip() or line[0] == '#':
                    continue

                L = loads(line)
                for iso in L:
                    ISOTools.verify_iso(iso)

                assert len(L) > 1
                assert not (L[0], L[-1]) in D

                D[L[0], L[-1]] = L
    return D


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

    def translit(self, from_: ISOCode, to: ISOCode, s: str):
        params = self.DEngines[from_, to]
        for x, y in pairwise(params):
            s = self.multi_translit.translit(x, y, s)
        return s
