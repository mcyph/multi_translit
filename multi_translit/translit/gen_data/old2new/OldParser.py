# -*- coding: utf-8 -*-
from re import sub, compile, UNICODE, DOTALL
from toolkit.io.file_tools import file_read
from multi_translit.translit.gen_data.old2new.GetDSettings import get_D_settings, DPossibleSet

REIFAFTER = compile(r'^if after\((?P<after>.*?)\):(?P<expression>.*)$', UNICODE)
REIFBEFORE = compile(r'^if before\((?P<before>.*?)\):(?P<expression>.*)$', UNICODE)
REIFELSE = compile(r'^else:(?P<expression>.*?)$', UNICODE)
BEGINIGNORECOMB = compile(r'BEGIN IgnoreComb\((?P<ignorechar>.*)\)$', UNICODE)
BEGINMODIFIERS = compile(r'BEGIN Modifiers\((?P<modmode>.*)\)$', UNICODE)
RECOMMENT = compile(r"'''.*?'''", DOTALL|UNICODE)
REVARIABLE = compile(r'^\$(?P<name>.*?) = (?P<value>.*?)$')


def get_D_re(regex, s):
    match = regex.match(s)
    if match:
        return match.groupdict()


"""
In modifier mode check the command ok
both/from/to include/lower/upper/title/replace/swapcase/capitalize/
strip/rstrip/lstrip/format/normalize/splithangul/joinhangul/splitaccents/joinaccents
"""
CMDMODRECOGNIZED = compile(r' *?(both|from|to) *? (include|lower|upper|title|replace|swapcase'+
'|capitalize|strip|rstrip|lstrip|format|normalize|splithangul|joinhangul|splitaccents|joinaccents'+
'|koreanenc|koreandec)\(.*\) *?')

DREs = {
    'self': r'.*?\sself\((?P<char>.*?)\).*?',
    'initial': r'.*?\sinitial\((?P<char>.*?)\).*?',
    'medial': r'.*?\smedial\((?P<char>.*?)\).*?',
    'final': r'.*?\sfinal\((?P<char>.*?)\).*?',
    'allforms': r'.*?\sallforms\((?P<char>.*?)\).*?',
    'sylinitial': r'.*?\ssylinitial\((?P<char>.*?)\).*?',
    'sylfinal': r'.*?\ssylfinal\((?P<char>.*?)\).*?',
    'others': r'.*?\sothers\((?P<char>.*?)\).*?'
}

LOrder = [
    'self',
    'initial',
    'medial',
    'final',
    'allforms',
    'sylinitial',
    'sylfinal',
    'others'
]

for k, v in DREs.items():
    DREs[k] = compile(v, UNICODE)


CONTINUE = True
KEEP_PROCESSING = False


class OldParser:
    def __init__(self, path):
        D = self.D = {}
        self.txt = file_read(path, encoding='utf-8')
        self.txt = self.txt.replace(u'﻿', '').replace('\r', '') # HACK! ====================================
        
        D['comment'], D['initial_comments'] = self.pop_comment()
        
        try: 
            D['DSettings'] = self.pop_D_settings()
        except:
            from traceback import print_exc
            print('settings not found for:', path)
            print_exc()
        
        # Now go through and process the file one line at a time
        ignore_comb = None
        mods = None
        
        LModComments = []
        LLines = D['LLines'] = []
        
        for line in self.txt.split('\n'):
            #print line
            DVariable = get_D_re(REVARIABLE, line)
            if DVariable:
                LLines.append({'variable': (DVariable['name'].strip(),
                                            DVariable['value'].strip().split('||'))})
                continue
            
            # Process the modifiers
            LModComments, mods, continue_ = self.process_modifiers(LModComments, mods, line)
            if continue_==CONTINUE:
                continue
            
            # Process the ignore combinations
            ignore_comb, continue_ = self.process_ignore_comb(ignore_comb, line)
            if continue_==CONTINUE:
                continue
            
            # Get any comments
            DLine = {}
            #print line
            DLine['comment'], line = self.extract_comments(line)
            if not line.strip():
                LLines.append(DLine)
                continue
            
            # (Note adding ignore_comb AFTERWARDS!)
            if ignore_comb:
                DLine['ignore_comb'] = ignore_comb
            
            # Get the before/after conditions
            line, DLine['LBefore'] = self.extract_L_before(line)
            line, DLine['LAfter'] = self.extract_L_after(line)
            line = self.remove_else(line)
            
            # Extract the direction
            line, direction = self.extract_direction(line)
            
            # Get the conversions
            from_, _, to = line.partition('=')
            LFrom = self.get_L_from(from_)
            LTo = self.get_L_to(to)
            
            # Make things a little more convenient for processing
            DLine['LConv'] = [(i[0],)+(direction,)+(i[1],) 
                              for i in zip(LFrom, LTo)]
            LLines.append(DLine)
        
        for DLine in LLines:
            # Delete keys if they're blank
            for key in ('comment', 'LBefore', 'LAfter'):
                if key in DLine and DLine[key] is None:
                    del DLine[key]
        
        for key in ('comment',):
            if D[key] is None:
                del D[key]


    #============================================================#
    #                        Pop Comments                        #
    #============================================================#


    def pop_comment(self):
        """
        Extract the comment (if there is one)
        """
        initial_comments = self.pop_initial_comments()
        
        if "'''" in self.txt:
            comment = self.txt.split("'''")[1].split("'''")[0]
            self.txt = RECOMMENT.sub('', self.txt)
        
        elif initial_comments and True:
            comment = '\n'.join(i.strip('# \t')
                                for i in initial_comments.split('\n'))
            initial_comments = ''
        
        else:
            comment = None
        
        return comment, initial_comments


    def pop_initial_comments(self):
        """
        Get/remove the initial comments at the top of the file
        """
        LComments = []
        LOut = []
        
        for line in self.txt.split('\n'):
            if LOut:
                LOut.append(line)
            elif line.strip().startswith('#') or not line.strip():
                LComments.append(line)
            elif "'''" in line or '{{' in line:
                LOut.append(line)
            elif line.strip():
                LOut.append(line) # MALFORMED FILE HACK!
                #print line # WARNING! =======================================================
        
        self.txt = '\n'.join(LOut)
        return '\n'.join(LComments)


    #============================================================#
    #                        Pop Settings                        #
    #============================================================#


    def pop_D_settings(self):
        """
        Get the {{{...}}} settings
        """
        #print txt, LComments, LOut
        self.txt, self.D['DSettings'] = get_D_settings(self.txt)
        return self.dict_keys_underscored(self.D['DSettings'])


    def pop_D_legacy_settings(self):
        LOut = []
        D = self.dict_keys_underscored(DPossibleSet)
        del D['LFonts']
        iso = None
        from_script = None
        to_script = None
        
        for line in self.txt.split('\n'):
            o_line = line
            line = line.split('#')[0].strip()
            
            'provides(',
            'addISO(',
            'addType(',
            'addType(',
            'useMatchCase()',
            'useIgnoreCase()' # CHECK ME!
            
            if line.startswith('provides('):
                L = eval(line.partition('(')[2][:-1]
                         .replace('true', 'True')
                         .replace('false', 'False'))
                
                print(line)
                if len(L) == 2:
                    from_script = L[0]
                    to_script = L[1]
                    D['both_ways'] = True # CHECK ME! ===================================
                else:
                    D['format_string'] = L[0]
                    from_script = L[1]
                    to_script = L[2]
                    D['both_ways'] = L[3] if len(L)==4 else False
                
            elif line.startswith('addISO('):
                iso = eval(line.partition('(')[2][:-1]) # MULTIPLE ISO CODES WARNING!
            
            elif line.startswith('fonts('):
                from_font, to_font = eval(line.partition('(')[2][:-1])
                D['LFonts'] = [from_font, to_font]
                
            elif line.startswith('addType'):
                pass
            elif line == 'useMatchCase()':
                D['match_case'] = True
            elif line == 'useIgnoreCase()':
                D['ignore_case'] = True
            
            else:
                LOut.append(o_line)
        
        D['LProvides'] = [
            [iso, from_script],
            [iso, to_script]
        ]
        
        if None in (iso, from_script, to_script):
            D['ignore_me'] = True
        
        if not 'LFonts' in D:
            D['LFonts'] = [
                D['LProvides'][0][1],
                D['LProvides'][1][1]
            ]
        
        self.txt = '\n'.join(LOut)
        return D


    #============================================================#
    #                  Modifier mode processing                  #
    #============================================================#


    def process_modifiers(self, LComments, mods, line):
        """
        Modifier mode processing
        
        Returns (the new modifiers, True/False)
        * True -> continue
        * False -> keep processing
        """
        if mods and line.strip()=='END Modifiers':
            LComments = [] # WARNING! ====================================================
            return LComments, None, CONTINUE
            
        elif mods:
            if line.strip().startswith('#') or not line.strip():
                LComments.append(line.strip())
            else:
                direction, _, cmd = line.strip().partition(' ')
                
                DMods = {
                    'source': 'before_conversions',
                    'output': 'after_conversions'
                }
                DDir = {
                    'from': 'from_direction',
                    'to': 'to_direction'
                }
                L = self.D.setdefault('%s:%s' % (DMods[mods.lower()], 
                                                 DDir[direction]), 
                                      [])
                L.extend(LComments) # NOTE ME!
                LComments = []
                L.append(cmd)

            return LComments, mods, CONTINUE
            
        else:
            DBeginMods = get_D_re(BEGINMODIFIERS, line)
            if DBeginMods:
                return LComments, DBeginMods['modmode'], CONTINUE
        
        return LComments, mods, KEEP_PROCESSING


    #============================================================#
    #               Ignore combinations processing               #
    #============================================================#


    def process_ignore_comb(self, ignore_comb, line):
        """
        Ignore combinations processing
        
        returns (the new ignore_comb, True->continue/False->keep processing)
        """
        if ignore_comb and line.strip()=='END IgnoreComb':
            return None, CONTINUE
        
        elif not ignore_comb:
            DBegin = get_D_re(BEGINIGNORECOMB, line)
            if DBegin:
                return DBegin['ignorechar'], CONTINUE
        
        return ignore_comb, KEEP_PROCESSING


    #============================================================#
    #                      Extract comments                      #
    #============================================================#


    def extract_comments(self, line):
        if '#' in line:
            comment = '#'.join(line.split('#')[1:])
            line = line.split('#')[0]
            return comment, line
        
        return None, line


    #============================================================#
    #                Extract conditional statements              #
    #============================================================#


    def extract_L_after(self, line):
        DIfAfter = get_D_re(REIFAFTER, line)
        
        if DIfAfter:
            line = DIfAfter['expression']
            LAfter = DIfAfter['after'].split('||')
            return line, LAfter
        
        return line, None


    def extract_L_before(self, line):
        DIfBefore = get_D_re(REIFBEFORE, line)
        
        if DIfBefore:
            line = DIfBefore['expression']
            LBefore = DIfBefore['before'].split('||')
            return line, LBefore
        
        return line, None


    def remove_else(self, line):
        """
        (I'll just ignore "else" as it's unnecessary)
        """
        DIfElse = get_D_re(REIFELSE, line)
        if DIfElse:
            line = DIfElse['expression']
        return line


    #============================================================#
    #                   Extract the direction                    #
    #============================================================#


    def extract_direction(self, line):
        if '=>' in line:
            dir_ = '=>'
        elif '<=' in line:
            dir_ = '<='
        else:
            dir_ = '<=>'
        
        line = line.replace('=>', '=')
        line = line.replace('<=', '=')
        return line, dir_


    #============================================================#
    #                  Extract the conversions                   #
    #============================================================#


    def get_L_from(self, from_):
        def split(s):
            return [i.strip() for i in s.split('||')]
        
        return [split(i) for i in from_.split(';')]


    def get_L_to(self, to):
        """
        TODO: Convert {'allforms': [['abc', ...], ...]}
        to [{'allforms': ['abc', ...], ...}, ...]
        """
        LRtn = []
        D = self.get_D_to(to)
        if not D: 
            return []
        num_items = len(D[list(D.keys())[0]])
        
        for x in xrange(num_items):
            i_D = {}
            for key in D:
                i_D[key] = D[key][x]
            LRtn.append(i_D)
        return LRtn


    def get_D_to(self, to):
        def split(s):
            LRtn = []
            for x in s.split(';'):
                LItem = []
                for y in x.split('||'):
                    LItem.append(y.strip())
                LRtn.append(LItem)
            return LRtn
        
        DTo = {}
        for key, regex in DREs.items():
            DMatch = get_D_re(regex, to)
            if DMatch:
                DTo[key] = split(DMatch['char']\
                    .replace('ignore()', '')\
                    .replace('ignore(', ''))
                to = regex.sub('', to).strip()
        
        if to.strip():
            DTo['allforms'] = split(to.strip().replace('ignore()', ''))
        
        return DTo


    #============================================================#
    #                       Miscellaneous                        #
    #============================================================#


    def dict_keys_underscored(self, D):
        n_D = {}
        for k, v in D.items():
            if k.startswith('D') or k.startswith('L'):
                n_D[k] = v
            else:
                n_D[self.underscored(k)] = v
        return n_D


    def underscored(self, name):
        s1 = sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def get_D_old(path):
    parser = OldParser(path)
    return parser.D


if __name__ == '__main__':
    from pprint import pprint
    #PATH = 'Translit/BySound/Asian/Korean/HSR.trn'
    PATH = 'Translit/BySound/Asian/Japanese/Latin/Japanese Hiragana-Latin.trn'
    pprint(get_D_old(PATH))
