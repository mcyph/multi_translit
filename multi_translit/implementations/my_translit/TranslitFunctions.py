from unicodedata import lookup, name


def names_to_codepoints(s):
    L = []
    LSplit = s.split('{')
    
    for x, i in enumerate(LSplit):
        if x:
            name, _, leftover = i.partition('}')
            try:
                L.append(lookup(name))
                L.append(leftover)
            except KeyError:
                L.append(i)
        else:
            L.append(i)
    return ''.join(L)


def codepoints_to_names(s):
    return ''.join('{%s}' % name(str(i)) for i in s)


def remove(s):
    return ''


def null(s):
    return s


CODEPOINTS_TO_HEX_DICT = {
    'C': '\\u', # \u0061
    'Java': '\\u', # \u0061
    'Perl': '\\x{%s}', # \x{61}
    'Unicode': 'U+', # U+003E
    'XML': '&%s;', # &X;
    'XML10': '&%s;' # &X;
}


def pad(s):
    FIXME


def codepoints_to_hex(s, typ='Java'):
    # TODO: Add support for wide codepoints!
    format_ = CODEPOINTS_TO_HEX_DICT[typ]
    
    L = []
    if typ in ('Java', 'C', 'Unicode'):
        for c in s:
            ord_ = ord(c)
            L.append(format_+pad(hex(ord_), 4)[2:])
    else:
        for c in s:
            ord_ = ord(c)
            L.append(format_ % hex(ord_)[2:])
    return ''.join(L)


def hex_to_codepoints(s, typ='Java'):
    L = []
    format_ = CODEPOINTS_TO_HEX_DICT[typ]
    
    if typ in ('Java', 'C', 'Unicode'):
        pass
    else:
        first, last = format_.split('%s')
        for i in s.split(first):
            if last in i:
                pass
            else:
                pass

    return ''.join(L)
