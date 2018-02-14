# -*- coding: utf-8 -*-
import json
from os import makedirs
from os.path import exists, dirname

from multi_translit.translit.gen_data.old2new.OldParser import get_D_old, LOrder
from multi_translit.translit.iter_translit_files import iter_translit_files
from toolkit.file_tools import file_write
from multi_translit.data_paths import data_path

from iso_convert import iso_convert

DFonts = {} # {script: font, ...}

# HACK: Remove the old, legacy format...
LIgnoredComments = [
    'provides(',
    'addISO(',
    'addType(',
    'addType(',
    'useMatchCase()',
    'useIgnoreCase()', # CHECK ME!
    'fonts('
]

DDirs = {
    '<=': u'<=',
    '=>': u'=>',
    '<=>': u'='
}

def get_str(o, before_o=None, after_o=None):
    assert not (before_o and after_o)

    if before_o and after_o:
        return '%s when after %s and before %s' % (
            escape_str(o),
            escape_str(after_o),
            escape_str(before_o)
        )
    elif before_o:
        return '%s when before %s' % (
            escape_str(o),
            escape_str(before_o)
        )
    elif after_o:
        return '%s when after %s' % (
            escape_str(o),
            escape_str(after_o)
        )
    else:
        return escape_str(o)


def escape_str(o):
    #print o
    def to_str(s):
        # ";" WARNING! ======================================================
        if len(s)>1 and s[0]=='$':
            return s#[1:] # $VARIABLE HACK!

        # TODO: Make it so that combining/rtl characters
        # are referenced by name, rather than the original
        # characters codepoints etc

        if not s:
            return '{{}}'

        from unicodedata import name, category, mirrored
        LOut = []
        for c in s:
            if (
                not category(unicode(c)) in {
                    'Mc', 'Cc', 'Cf', 'Zl', 'Zp', 'Zs', 'Mn'
                } and
                not mirrored(unicode(c)) and
                not c in '=,;'
            ):
                LOut.append(c)
            else:
                LOut.append('{{%s}}' % name(unicode(c)))

        return ''.join(LOut)
    
    is_list = isinstance(o, (list, tuple))
    if is_list and len(o)==1:
        o = o[0]
    
    elif is_list:
        return ','.join(to_str(i) for i in o)
    
    return to_str(o)


def D_conv_2_str(DConv):
    if len(DConv)==1 and 'allforms' in DConv:
        return get_str(DConv['allforms'])
    
    LRtn = []
    for key in LOrder:
        if key in DConv:
            LRtn.append('%s %s' % (key, get_str(DConv[key])))
    
    return ' or '.join(LRtn)


def old_2_new(path):
    LRtn = []
    a = LRtn.append
    DOld = get_D_old(path)
    
    if DOld['initial_comments'].strip():
        a(DOld['initial_comments'])
    
    if 'comment' in DOld:
        a('[comment]')
        a(DOld['comment'])
        a('')

    DSettings = {}

    if 'DSettings' in DOld:
        D = DOld['DSettings']
        
        # Add to the global list of fonts
        from_font, to_font = D['LFonts']
        from_iso = '%s:%s' % (
            D['LProvides'][0][0],
            D['LProvides'][0][1]
        )
        to_iso = '%s:%s' % (
            D['LProvides'][1][0],
            D['LProvides'][1][1]
        )
        DFonts[from_iso.partition(':')[2]] = from_font
        DFonts[to_iso.partition(':')[2]] = to_font

        if D['match_case']:
            DSettings['match_case'] = True

        DSettings['from_iso'] = iso_convert(*from_iso.split(':'))
        DSettings['to_iso'] = iso_convert(*to_iso.split(':'))

        if D['ignore_me']:
            DSettings['ignore_me'] = True
        
        if not D['both_ways']:
            DSettings['direction'] = "=>"
        else:
            DSettings['direction'] = "<=>"
        
        if D['ignore_case']:
            DSettings['ignore_case'] = True

        if D['from_sep']:
            DSettings['from_sep'] = D['from_sep']
        if D['to_sep']:
            DSettings['to_sep'] = D['to_sep']
    

    LComments = []
    DModifiers = {}
    for key in [
        'before_conversions:from_direction',
        'before_conversions:to_direction',
        'after_conversions:from_direction',
        'after_conversions:to_direction'
    ]:
        if not key in DOld:
            continue

        LOut = (
            DModifiers.setdefault(key.split(':')[1], {})
                      .setdefault(key.split(':')[0], [])
        )
        for i in DOld[key]:
            print 'CONVERSION:', i

            # Comment or blank
            cmd, _, blah = i.rstrip(')').partition('(')
            append = json.loads('["%s", %s]' % (cmd, blah) if blah.strip() else '["%s"]' % cmd)

            if append[0] == 'include':
                append[1] = iso_convert(*append[1].split(':'))
                append[2] = iso_convert(*append[2].split(':'))

            LOut.append(append)

    if DModifiers:
        DSettings['modifiers'] = DModifiers


    if DSettings:
        a('[settings]')
        if LComments and ''.join(LComments).strip():
            def pc(i):
                if i.startswith('#'):
                    return i
                elif not i.strip():
                    return i.strip()
                else:
                    return '# %s' % i.strip()

            a('\n'.join([pc(i) for i in LComments]).strip())
        a(json.dumps(DSettings, indent=4))
        a('')


    LOut = []
    LVariables = []

    for DLine in DOld['LLines']:
        #print DLine

        if not DLine:
            # A blank line
            LOut.append('')
            continue

        elif (
            len(DLine) == 1 and
            'variable' in DLine
        ):
            LVariables.append('%s = %s' % (
                DLine['variable'][0],
                get_str(DLine['variable'][1]))
            )
            continue

        elif (
            len(DLine) == 1 and
            'comment' in DLine
        ):
            # Only a comment for this line
            ignore = False
            for i in LIgnoredComments:
                if DLine['comment'].strip().strip('#').startswith(i):
                    ignore = True
            
            if not ignore and 'DSettings' in DOld:
                LOut.append('#%s' % DLine['comment'])
            continue


        LConv = []
        for from_, dir_, DConv in DLine['LConv']:
            if not DConv:
                continue # HACK!

            dir_ = DDirs[dir_]
            LConv.append('%s %s %s' % (
                get_str(from_, DLine.get('LBefore'), DLine.get('LAfter')),
                dir_,
                D_conv_2_str(DConv))
            )


        if 'comment' in DLine:
            if LConv:
                LOut.append(
                    '#%s\n%s\n' % (
                        DLine['comment'],
                        '\n'.join(LConv)
                    )
                )
            else:
                LOut.append('#%s' % DLine['comment'])
        else:
            LOut.append('\n'.join(LConv))


        if len(LConv) > 1 and 1:
            # Add a newline if more than one semicolon-separated
            # conversion on each line
            LOut.append('')


    out = '\n'.join(LVariables).strip()
    if out:
        a('[variables]')
        a(out)
        a('')

    out = '\n'.join(LOut).strip()
    if out:
        a('[conversions]')
        a(out)
        a('')
    
    return '\n'.join(i.strip('\r\n') for i in LRtn).replace('\r', '')


if __name__ == '__main__':
    # ['Translit/BySound/Syllabics/Oji-Cree.trn']
    for path in iter_translit_files(old_ver=True):
        print path
        path = path.replace('\\', '/')
        new_path = path.replace('/data/', '/data-new/')
        try: txt = old_2_new(path)
        except:
            print 'ERROR ON:', path
            from traceback import print_exc
            print_exc()
            #raise
        
        if not exists(dirname(new_path)):
            makedirs(dirname(new_path))
        
        file_write(new_path, txt)
    
    import codecs
    from pprint import pprint
    pprint(DFonts)
    
    with codecs.open(
        data_path(
            'translit_new',
            'translit-fonts.json'
        ),
        'wb',
        'utf-8'
    ) as f:

        f.write(json.dumps(DFonts, ensure_ascii=False, indent=4))
