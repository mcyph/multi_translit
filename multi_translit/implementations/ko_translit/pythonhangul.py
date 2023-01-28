#
# This file is part of KoreanCodecs.
#
# Copyright(C) Hye-Shik Chang <perky@FreeBSD.org>, 2002.
#
# KoreanCodecs is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# KoreanCodecs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with KoreanCodecs; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# $Id: hangul.py,v 1.14 2002/07/19 00:01:53 perky Exp $
#

class UnicodeHangulError(Exception):
    
    def __init__ (self, msg):
        self.msg = msg
        Exception.__init__(self, msg)
    
    def __repr__ (self):
        return self.msg
    
    __str__ = __repr__

Null = ''

class Jaeum:

    Codes = ('\u3131', '\u3132', '\u3133', '\u3134', '\u3135', '\u3136',
            #    G         GG          GS         N          NJ         NH
             '\u3137', '\u3138', '\u3139', '\u313a', '\u313b', '\u313c',
            #    D         DD          L          LG         LM         LB
             '\u313d', '\u313e', '\u313f', '\u3140', '\u3141', '\u3142',
            #    LS        LT          LP         LH         M          B
             '\u3143', '\u3144', '\u3145', '\u3146', '\u3147', '\u3148',
            #    BB        BS          S          SS         NG         J
             '\u3149', '\u314a', '\u314b', '\u314c', '\u314d', '\u314e')
            #    JJ        C           K          T          P          H
    Width = len(Codes)
    G, GG, GS, N, NJ, NH, D, DD, L, LG, LM, LB, LS, LT, LP, LH, M, B, \
    BB, BS, S, SS, NG, J, JJ, C, K, T, P, H = Codes
    Chosung = [G, GG, N, D, DD, L, M, B, BB, S, SS, NG, J, JJ, C, K, T, P, H]
    Jongsung = [Null, G, GG, GS, N, NJ, NH, D, L, LG, LM, LB, LS, LT, \
                LP, LH, M, B, BS, S, SS, NG, J, C, K, T, P, H]
    MultiElement = {
        GG: (G, G),  GS: (G, S),  NJ: (N, J),  NH: (N, H),  DD: (D, D),
        LG: (L, G),  LM: (L, M),  LB: (L, B),  LS: (L, S),  LT: (L, T),
        LP: (L, P),  LH: (L, H),  BB: (B, B),  BS: (B, S),  SS: (S, S),
        JJ: (J, J)
    }


class Moeum:

    Codes = ('\u314f', '\u3150', '\u3151', '\u3152', '\u3153', '\u3154',
            #    A          AE        YA         YAE         EO         E
             '\u3155', '\u3156', '\u3157', '\u3158', '\u3159', '\u315a',
            #    YEO        YE        O          WA          WAE        OE
             '\u315b', '\u315c', '\u315d', '\u315e', '\u315f', '\u3160',
            #    YO         U         WEO        WE          WI         YU
             '\u3161', '\u3162', '\u3163')
            #    EU         YI        I
    Width = len(Codes)
    A, AE, YA, YAE, EO, E, YEO, YE, O, WA, WAE, OE, YO, \
    U, WEO, WE, WI, YU, EU, YI, I = Codes
    Jungsung = list(Codes)
    MultiElement = {
        AE: (A, I),  YAE: (YA, I),  YE: (YEO, I), WA: (O, A),  WAE: (O, A, I),
        OE: (O, I),  WEO: (U, EO),  WE: (U, E),   WI: (U, I),  YI: (EU, I)
    }

# Aliases for your convinience
Chosung = Jaeum.Chosung
Jungsung = Moeum.Jungsung
Jongsung = Jaeum.Jongsung

for name, code in list(Jaeum.__dict__.items()) + list(Moeum.__dict__.items()):
    if name.isupper() and len(name) <= 3:
        exec("%s = %s" % (name, repr(code)))
del name, code

# Unicode Hangul Syllables Characteristics
ZONE = ('\uAC00', '\uD7A3')
NCHOSUNG  = len(Chosung)
NJUNGSUNG = len(Jungsung)
NJONGSUNG = len(Jongsung)
JBASE_CHOSUNG  = '\u1100'
JBASE_JUNGSUNG = '\u1161'
JBASE_JONGSUNG = '\u11A8'
CHOSUNG_FILLER = '\u115F'
JUNGSUNG_FILLER = '\u1160'

_ishangul = (
    lambda code:
        ZONE[0] <= code <= ZONE[1] or
        code in Jaeum.Codes or
        code in Moeum.Codes
)

# Alternative Suffixes : do not use outside
ALT_SUFFIXES = {
    '\uc744': ('\ub97c', '\uc744'), # reul, eul
    '\ub97c': ('\ub97c', '\uc744'), # reul, eul
    '\uc740': ('\ub294', '\uc740'), # neun, eun
    '\ub294': ('\ub294', '\uc740'), # neun, eun
    '\uc774': ('\uac00', '\uc774'), # yi, ga
    '\uac00': ('\uac00', '\uc774'), # yi, ga
    '\uc640': ('\uc640', '\uacfc'), # wa, gwa
    '\uacfc': ('\uc640', '\uacfc'), # wa, gwa
}

# Ida-Varitaion Suffixes : do not use outside
IDA_SUFFIXES = {
    '(\uc774)': ('', '\uc774'),     # (yi)da
    '(\uc785)': (17, '\uc785'),      # (ip)nida
    '(\uc778)': (4, '\uc778'),       # (in)-
}

def is_jaeum(u):
    if u:
        for c in u:
            if c not in Jaeum.Codes:
                break
        else:
            return True
    return False

def is_moeum(u):
    if u:
        for c in u:
            if c not in Moeum.Codes:
                break
        else:
            return True
    return False

def ishangul(u):
    if u:
        for c in u:
            if not _ishangul(c):
                break
        else:
            return True
    return False

def join(codes):
    """ Join function which makes hangul syllable from jamos """
    if len(codes) is not 3:
        raise UnicodeHangulError("needs 3-element tuple")
    if not codes[0] or not codes[1]: # single jamo
        return codes[0] or codes[1]

    return chr(
        0xac00 + (
            Chosung.index(codes[0])*NJUNGSUNG +
            Jungsung.index(codes[1])
        )*NJONGSUNG + Jongsung.index(codes[2])
    )

def split(code):
    """ Split function which splits hangul syllable into jamos """
    if len(code) != 1 or not _ishangul(code):
        raise UnicodeHangulError("needs 1 hangul letter")
    if code in Jaeum.Codes:
        return (code, Null, Null)
    if code in Moeum.Codes:
        return (Null, code, Null)

    code = ord(code) - 0xac00
    return (
        Chosung[int(code / (NJUNGSUNG*NJONGSUNG))], # Python3000 safe
        Jungsung[int(code / NJONGSUNG) % NJUNGSUNG],
        Jongsung[code % NJONGSUNG]
    )

def conjoin(s):
    obuff = []
    ncur = 0

    while ncur < len(s):
        c = s[ncur]
        if JBASE_CHOSUNG <= c <= '\u1112' or c == CHOSUNG_FILLER: # starts with chosung
            if len(s) > ncur+1 and JUNGSUNG_FILLER <= s[ncur+1] <= '\u1175':
                cho = Chosung[ord(c) - ord(JBASE_CHOSUNG)]
                jung = Jungsung[ord(s[ncur+1]) - ord(JBASE_JUNGSUNG)]
                if len(s) > ncur+2 and JBASE_JONGSUNG <= s[ncur+2] <= '\u11C2':
                    jong = Jongsung[ord(s[ncur+2]) - ord(JBASE_JONGSUNG) + 1]
                    ncur += 2
                else:
                    jong = Null
                    ncur += 1
                obuff.append(join([cho, jung, jong]))
            else:
                obuff.append(join([Chosung[ord(c) - ord(JBASE_CHOSUNG)], Null, Null]))
        elif JBASE_JUNGSUNG <= c <= '\u1175':
            obuff.append(join([Null, Jungsung[ord(c) - ord(JBASE_JUNGSUNG)], Null]))
        else:
            obuff.append(c)
        ncur += 1
    
    return ''.join(obuff)

def disjoint(s):
    obuff = []
    for c in s:
        if _ishangul(c):
            cho, jung, jong = split(c)
            if cho:
                obuff.append( chr(ord(JBASE_CHOSUNG) + Chosung.index(cho)) )
            else:
                obuff.append( CHOSUNG_FILLER )

            if jung:
                obuff.append( chr(ord(JBASE_JUNGSUNG) + Jungsung.index(jung)) )
            else:
                obuff.append( JUNGSUNG_FILLER )

            if jong:
                obuff.append( chr(ord(JBASE_JONGSUNG) + Jongsung.index(jong) - 1) )
        else:
            obuff.append(c)
    return ''.join(obuff)

def _has_final(c):
    # for internal use only
    if '\uac00' <= c <= '\ud7a3': # hangul
        return 1, (ord(c) - 0xac00) % 28 > 0
    else:
        return 0, c in '013678.bklmnptLMNRZ'

# Iterator Emulator for ancient versions before 2.1
try:
    iter
except:
    class iter:
        def __init__(self, obj):
            self.obj = obj
            self.ptr = 0
        def __next__(self):
            try:
                return self.obj[self.ptr]
            finally:
                self.ptr += 1

# Nested scope lambda emulation for versions before 2.2
import sys
if sys.hexversion < '0x2020000':
    class plambda:
        def __init__(self, obj):
            self.obj = obj
        def __call__(self):
            return self.obj
else:
    plambda = None
del sys

def format(fmtstr, *args, **kwargs):
    if kwargs:
        argget = lambda:kwargs
        if plambda:
            argget = plambda(kwargs)
    else:
        argget = iter(args).__next__

    obuff = []
    ncur = escape = fmtinpth = 0
    ofmt = fmt = ''

    while ncur < len(fmtstr):
        c = fmtstr[ncur]

        if escape:
            obuff.append(c)
            escape = 0
            ofmt   = ''
        elif c == '\\':
            escape = 1
        elif fmt:
            fmt += c
            if not fmtinpth and c.isalpha():
                ofmt = fmt % argget()
                obuff.append(ofmt)
                fmt = ''
            elif fmtinpth and c == ')':
                fmtinpth = 0
            elif c == '(':
                fmtinpth = 1
            elif c == '%':
                obuff.append('%')
        elif c == '%':
            fmt  += c
            ofmt = ''
        else:
            if ofmt and c in ALT_SUFFIXES:
                obuff.append(ALT_SUFFIXES[c][
                    _has_final(ofmt[-1])[1] and 1 or 0
                ])
            elif ofmt and fmtstr[ncur:ncur+3] in IDA_SUFFIXES:
                sel = IDA_SUFFIXES[fmtstr[ncur:ncur+3]]
                ishan, hasfinal = _has_final(ofmt[-1])

                if hasfinal:
                    obuff.append(sel[1])
                elif ishan:
                    if sel[0]:
                        obuff[-1] = obuff[-1][:-1] + chr(ord(ofmt[-1]) + sel[0])
                else:
                    obuff.append(sel[0] and sel[1])
                ncur += 2
            else:
                obuff.append(c)
    
            ofmt = ''

        ncur += 1
    
    return ''.join(obuff)

