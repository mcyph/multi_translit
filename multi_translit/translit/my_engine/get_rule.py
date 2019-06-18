from re import compile, sub
from collections import namedtuple
from unicodedata import lookup

def strip_re(s):
    r = ''.join(i.strip() for i in s.split('\n'))
    return r % {'string_re': string_re}

string_re = (
    ur'''(([^ ]|\{\{.*?\}\})+)(,([^ ]|\{\{.*?\}\})+)*'''
)

conv = strip_re(ur'''
  ^(
    (
      (?P<a>%(string_re)s)|
      allforms (?P<a2>%(string_re)s)|
      initial (?P<initial>%(string_re)s)|
      medial (?P<medial>%(string_re)s)|
      final (?P<final>%(string_re)s)|
      self (?P<self>%(string_re)s)|
      others (?P<others>%(string_re)s)
    )
    ( or )?
  )+?$
''')

before_after = strip_re(ur'''
  ^(
    (
      after (?P<after>%(string_re)s)|
      before (?P<before>%(string_re)s)
    )
    ( and (
      after (?P<after2>%(string_re)s)|
      before (?P<before2>%(string_re)s)
    ))*
  )*?$
''')


conv_re = compile(conv)
before_after_re = compile(before_after)


Rule = namedtuple(
    'Rule', ['direction', 'from_side', 'to_side']
)
Side = namedtuple(
    'Side', ['conditions', 'conversions']
)
Conditions = namedtuple(
    'Conditions', ['LBefore', 'LAfter']
)
Conversions = namedtuple(
    'Conversions', ['LSelf', 'LInitial', 'LMedial', 'LFinal']
)


def _reverse_sign(s):
    if s == '=':
        return s
    elif s == '=>':
        return '<='
    else:
        assert s == '<=', s
        return '=>'


def get_rule(line, reverse=False, ci_conditions=False):
    #print 'get_rule', line.encode('utf-8')
    for token in ('=>', '=', '<='):
        if token in line:
            side1, token, side2 = line.partition(' %s ' % token)
            token = token.strip()

            if reverse:
                side1, side2 = side2, side1
                token = _reverse_sign(token)

            if token == '<=':
                # only for the other direction, so ignore
                continue

            return Rule(token.strip(), get_D(side1, ci_conditions), get_D(side2, ci_conditions))

    raise Exception(line)


def process_val(s):
    #print 'PROCESS VAL!'
    def fn(match):
        #print 'MATCH!', match
        s = match.group()
        if not s.strip('{}'):
            # blank string!
            return ''
        #print 'DO LOOKUP!'
        return lookup(s[2:-2])

    import re
    #print 'SUB!'
    s = re.sub(r'\{\{.*?\}\}', fn, s, flags=re.UNICODE)
    #print 'OK:', s.encode('utf-8')
    #print s
    return s


def get_D(s, ci_conditions):
    #print 'get_D', s.encode('utf-8')

    def _process_dict(DRtn, i_D):
        #print i_D

        for k, v in sorted(i_D.items()):
            if v is not None:
                LVals = [
                    process_val(i) for i in v.split(',')
                ]


                if k in ('LBefore', 'LAfter') and ci_conditions:
                    LVals = [i.lower() for i in LVals]


                if k.rstrip('2') == 'a':
                    for i_k in ('LInitial', 'LMedial', 'LFinal', 'LSelf'):
                        #assert not DRtn[i_k], ('allforms', DRtn, LVals)
                        DRtn[i_k] = LVals
                else:
                    set_key = 'L'+k.rstrip('2').title()
                    #assert not DRtn[set_key], (set_key, DRtn, LVals)
                    DRtn[set_key] = LVals

        return DRtn


    conv, _, before_after = s.partition(' when ')


    DConv = {
        'LInitial': None, 'LMedial': None,
        'LFinal': None, 'LSelf': None
    }
    #print 'FINDITER'
    for x, match in enumerate(conv_re.finditer(conv)):
        #print 'PROCESS DICT:', match
        DConv.update(
            _process_dict(DConv, match.groupdict())
        )
        #print 'OKK'
    assert 'x' in locals(), \
        'Error parsing conversions in line "%s"' % s
    #print 'OK!'


    DBeforeAfter = {
        'LBefore': [], 'LAfter': []
    }
    if before_after:
        for y, match in enumerate(before_after_re.finditer(before_after)):
            DBeforeAfter.update(
                _process_dict(DBeforeAfter, match.groupdict())
            )
        assert 'y' in locals(), \
            'Error parsing before/after conditions in line "%s"' % s


    return Side(
        Conditions(**DBeforeAfter),
        Conversions(**DConv)
    )


if __name__ == '__main__':
    print get_D('''blah or initial k,l or medial blah"blah{{SPACE}} when after s,u and before y,z''')
    print get_D('initial k final k')
