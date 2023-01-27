# -*- coding: utf-8 -*-
from unicodedata import normalize
from multi_translit.implementations.ko_translit.KoreanTranslit import enmode, demode


SStr = {
    'lower',
    'upper',
    'title',
    'replace',
    'swapcase',
    'capitalize',
    'strip',
    'rstrip',
    'lstrip'
}


def process_word(s, dir_, L):
    """
    s is the string to be processed
    dir_ is <from/to>
    L is the list of processing rules
    TODO: Add including other translit engines?
    """
    #print L

    for i in L:
        cmd = i[0]

        if cmd in SStr:
            s = getattr(s, cmd)(*i[1:])

        elif cmd == 'format': 
            # String format
            s = i[1] % s

        elif cmd == 'normalize': 
            s = normalize(i[1], str(s))

        elif cmd == 'splithangul': 
            # HACK!
            s = normalize('NFD', str(s))

        elif cmd == 'joinhangul': 
            # HACK!
            s = normalize('NFC', str(s))

        elif cmd == 'koreanenc': 
            # Encoding, s
            s = enmode(i[1], s)

        elif cmd == 'koreandec': 
            s = demode(i[1], s)

        elif cmd == 'include': 
            # Special case - include other translit engines
            # This uses a lot of processing power to compile, 
            # so the engine's cached for later :-)
            try:
                global multi_translit
                multi_translit
            except:
                from multi_translit.MultiTranslit import MultiTranslit
                multi_translit = MultiTranslit()

            s = multi_translit.translit(*i[1:]+[s])

    return s
