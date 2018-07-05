from glob import glob
from json import loads
from codecs import open

from multi_translit.data_paths import data_path
from iso_tools import ISOTools


def get_D_comb():
    D = {}

    for path in glob(data_path('translit_combinations', '*.map')):
        with open(path, 'rb', 'utf-8') as f:
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
