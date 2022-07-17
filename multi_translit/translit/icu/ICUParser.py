# -*- coding: utf-8 -*-
# See "Appendix N: Transform Rules" of 
# http://unicode.org/reports/tr35/ for more information
from multi_translit.translit.my_engine.TranslitFunctions import DCodepoints2Hex

# Basic define types
from char_data.unicodeset.tokenizer.ProcessRangeBase import ProcessRangeBase
from multi_translit.data_paths import data_path

from .post_process import post_process

ASSIGN_VARIABLE = 0
CONVERSION = 1
TRANSFORM_RULE = 2
COMMENT = 3

# CONVERSION mode defines
BEFORE_TOKEN = 0  # { (?)
AFTER_TOKEN = 1   # } (?)
CURSOR_TOKEN = 2  # |
CHARS = 3
VARIABLE = 4      # $x = blah;
UNICODE_SET = 5   # [...]
FUNCTION_CALL = 6 # &fn(arg, ...)
GROUP = 7         # (...)

# Repetition modes for GROUP
ZERO_OR_MORE = 0  # X*
ONE_OR_MORE = 1   # X+
ZERO_OR_ONE = 2   # X?

# (forward, reverse): (langlynx forward function, langlynx reverse function)
# (Any-)X

DInverse = {}
for _from, _to in [
    ('Any-Null', 'Any-Null'),
    ('Any-NFD', 'Any-NFC'),
    ('Any-NFKD', 'Any-NFKC'),
    ('Any-Lower', 'Any-Upper')
]:
    DInverse[_from] = _to
    DInverse[_to] = _from

# NOTE: Any-Accents/Any-Publishing/Fullwidth-Halfwidth 
# are supplied in other files.
DFns = {
    'Any-Null': 'null()',
    'Any-NFD': "normalize('nfd')",
    'Any-NFC': "normalize('nfc')",
    'Any-NFKD': "normalize('nfkd')", 
    'Any-NFKC': "normalize('nfkc')",
    'Any-Lower': "lower()", # Looks like this can be case-insensitive... ==========
    'Any-Upper': "upper()",
    'Any-Remove': 'remove()',
    
    'Any-Hex': "codepoints_to_hex()",
    'Hex-Any': "hex_to_codepoints()",
    
    'Any-Name': 'codepoints_to_names()',
    'Name-Any': 'names_to_codepoints()'
}

for key in DCodepoints2Hex:
    DFns['Hex/%s-Any' % key] = "hex_to_codepoints('%s')" % key
    DFns['Any-Hex/%s' % key] = "codepoints_to_hex('%s')" % key


def get_L_icu_transform(path):
    inst = ParseICUTransform(path)
    return post_process(inst.L)

class ParseICUTransform(ProcessRangeBase):
    DDirectionChars = {
        '→': '=>',
        '↔': '<=>',
        '←': '<='
    }
    
    DTokens = {
        '{': BEFORE_TOKEN,
        '}': AFTER_TOKEN,
        '|': CURSOR_TOKEN
    }
    
    DRepetition = {
        '*': ZERO_OR_MORE,
        '+': ONE_OR_MORE,
        '?': ZERO_OR_ONE
    }
    
    def __init__(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            s = f.read()
        
        self.DVars = {}
        self.L = self.process_normal(s)
        
    def process_normal(self, s, x=0, group_mode=False):
        """
        DItem -> {'mode': ASSIGN_VARIABLE/CONVERSION/TRANSFORM_RULE,
                  'data': (...),
                  'LComments': [comment, ...]}
        """
        DItem = {}
        
        """
        Information about the current conversion:
        
        LCurrent -> The tokens for the current conversion 
                    (either from or to depending on the current state)
        LConv -> LBefore, direction, LAfter
        """
        return_list = []
        LCurrent = []
        LConv = [None, None, None]
        
        # Misc
        start_of_statement = True
        backslash_mode = False
        repetition_idx = 0
        
        while 1:
            # Get the next character
            try: c = s[x]
            except IndexError: break
            
            if not backslash_mode and c=='@':
                # HACK: For the time being, "dummy" characters which change 
                # the position of the cursor, e.g. "blah|@@blah", aren't 
                # implemented
                raise NotImplementedError
            
            if ord(c) == 65279:
                # utf-8 BOM HACK!
                x += 1
                continue
            
            print('MAIN:', x, c, ord(c), start_of_statement, backslash_mode, LCurrent, LConv)
            
            #========================================================#
            #                   Variable Handling                    #
            #========================================================#
            
            # Variable handling
            if c=='$' and not backslash_mode:
                x, var_name, LVar, LComments = self.get_variable(x+1, s)
                
                if LVar != None:
                    # make sure there are no previous comments etc
                    assert not DItem
                    DItem['mode'] = VARIABLE
                    DItem['data'] = (var_name, LVar)
                    DItem['LComments'] = LComments
                    return_list.append(DItem)
                    
                    assert not var_name in self.DVars # WARNING! =============
                    self.DVars[var_name] = LVar
                else:
                    assert not LComments # Just to make sure...
                    x -= 1 # HACK! ===========================================================================
                    LCurrent.append((VARIABLE, var_name))
            
            #========================================================#
            #         Comments/Transform Rules/UnicodeSets           #
            #========================================================#
            
            elif c=='#' and not backslash_mode:
                # Comment handling
                x, comment = self.get_comment(x, s)
                
                if start_of_statement:
                    # A full line comment
                    return_list.append({'mode': COMMENT,
                                'data': comment})
                else:
                    # A comment for this rule only
                    DItem.setdefault('LComments', []).append(comment)
                
                # Continue to make sure `start_of_statement` isn't set to `False`!
                #x += 1
                continue
            
            elif start_of_statement and not group_mode \
                and s[x:x+2]=='::':
                
                # Transform rules
                x, DRule = self.add_transform_rule(x+2, s)
                return_list.append({'mode': TRANSFORM_RULE,
                             'data': DRule})
                continue
                
            elif c in self.DDirectionChars and \
                not backslash_mode and not group_mode:
                
                # Conversion direction characters
                assert not LConv[1]
                LConv[1] = self.DDirectionChars[c]
                
                # Change to the right hand side direction
                LConv[0] = LCurrent
                LCurrent = []
                
                # Set the mode to CONVERSION
                DItem['mode'] = CONVERSION
                DItem['data'] = LConv
            
            elif c==';' and not backslash_mode and not group_mode:
                # End of the line
                # TODO: Add more sophisticated checking!
                
                if DItem.get('mode') == CONVERSION:
                    # Append the last item if in CONVERSION mode
                    assert LConv == DItem['data']
                    LConv[2] = LCurrent
                    LCurrent = []
                    LConv = [None, None, None]
                else:
                    # Make sure that LCurrent is 
                    # blank if not in conversion mode!
                    assert not LCurrent, LCurrent
                
                if DItem:
                    return_list.append(DItem)
                DItem = {}
                start_of_statement = True
                repetition_idx = 0
                
                # Don't reset `start_of_statement` below!
                x += 1
                continue
            
            #========================================================#
            #             Groups and Repetition Tokens               #
            #========================================================#
            
            elif c=='(' and not backslash_mode:
                # Process a group
                x, LAppend = self.process_normal(s, x+1, 
                                                 group_mode=True)
                LCurrent.append((GROUP, [None, LAppend]))
                repetition_idx = len(LCurrent) # CHECK ME! ==================
            
            elif c==')' and not backslash_mode and group_mode:
                # End a group (if in group mode)
                break
            
            elif c in self.DRepetition and not backslash_mode:
                flag = self.DRepetition[c]
                
                if LCurrent and LCurrent[-1][0]==GROUP:
                    # If the previous item is 
                    # a group, set the repetition flag
                    assert LCurrent[-1][1][0] is None
                    LCurrent[-1][1][0] = flag
                else:
                    # Otherwise, create an artificial group
                    # with a given repetition flag
                    LGroup = LCurrent[repetition_idx:]
                    del LCurrent[repetition_idx:]
                    LCurrent.append((GROUP, [flag, LGroup]))
                
                repetition_idx = len(LCurrent)

            #========================================================#
            #        Conversion Character/Range Processing           #
            #========================================================#
            
            else:
                LExtend, backslash_mode, x = \
                    self.get_conversion_tokens(backslash_mode, x, s)
                LCurrent.extend(LExtend)
            
            if start_of_statement and c.strip():
                # COMMENT IN THE MIDDLE OF A STATEMENT WARNING! ===========================
                start_of_statement = False
            x += 1
        
        if group_mode:
            return x, LCurrent
        else:
            return return_list
    
    def get_conversion_tokens(self, backslash_mode, x, s):
        """
        Conversion Character/Range Processing
        """
        c = s[x]
        L = []
        
        if c == '[':
            # Start of UnicodeSet mode
            x, range_ = self.process_range(x, s)
            #if True:
            #    from char_data.unicodeset.unicodeset import get_unicode_set_ranges
                
            #    print('RANGE TOKENS:', get_unicode_set_ranges(range_, self.DVars, char_indexes=None))
            L.append((UNICODE_SET, range_))
        
        elif c == '&':
            # Start of function call mode
            x, fn_name, LFnArgs = self.process_function_call(x, s)
            L.append((FUNCTION_CALL, (fn_name, LFnArgs)))
        
        elif backslash_mode:
            # Backslash mode
            # CHECK ME! ==========================================================
            if c == 'u':
                # Unicode backslash
                L.append((CHARS, chr(int(s[x+1:x+5], 16))))
                x += 4
            else:
                L.append((CHARS, c))
            
            backslash_mode = False
            
        elif c == '\\':
            backslash_mode = True
        
        elif c == "'":
            # Quotes mode
            print("QUOTES!")
            x, LExtend = self.process_quotes(x, s)
            L.extend(LExtend)
        
        elif c in self.DTokens:
            # Before/after/cursor tokens
            print('TOKEN:', self.DTokens[c])
            L.append(self.DTokens[c])
        
        elif c.strip():
            L.append((CHARS, c))
        
        return L, backslash_mode, x
    
    def get_comment(self, x, s):
        """
        "# comment"'s go until the end of the line
        """
        L = []
        while 1:
            # Get the next character
            try: c = s[x]
            except IndexError: break
            
            if c == '\n':
                break
            
            L.append(c)
            x += 1
        return x, ''.join(L)
    
    def get_variable(self, x, s):
        """
        Get the variable name and tokens
        """
        x, name = self.get_variable_name(x, s)
        
        L = []
        found_equals = False
        backslash_mode = False
        LComments = []
        
        while 1:
            # Get the next character
            try: c = s[x]
            except IndexError: break
            print('VARIABLE:', x, c)
            
            # Search for the "=" character
            if not found_equals and c=='=':
                found_equals = True
            elif not found_equals:
                if c.strip():
                    # Using a variable in a statement instead of assigning!
                    L = None
                    break
                
                #assert not c.strip(), \
                #    '"%s" should be "=" after specifying variable name' % c
            
            elif c == '#':
                # Process comments
                x, comment = self.get_comment(x, s)
                LComments.append(comment)
                
            elif c == ';':
                # Reprocess semicolons again
                x -= 1
                break
            
            else:
                # TODO: How to process the logic?
                # Seems a bit repetitive to copy-paste the above code...
                LExtend, backslash_mode, x = \
                    self.get_conversion_tokens(backslash_mode, x, s)
                L.extend(LExtend)
            x += 1
        
        return x, name, L, LComments
    
    def get_variable_name(self, x, s):
        """
        Get the name of the variable
        
        FIXME: Make it work with numbers etc after the variable! ===========================
        """
        L = []
        allowed = 'abcdefghijklmnopqrstuvwxyz_'
        SAllowed1 = set(allowed+allowed.upper())
        SAllowed2 = SAllowed1.union(set('1234567890_'))
        
        first_time = False
        while 1:
            # Get the next character
            try: c = s[x]
            except IndexError: break
            
            if first_time and c in SAllowed1 and False:
                L.append(c)
            elif c in SAllowed2:
                L.append(c)
            else:
                break
            
            x += 1
            first_time = False
        
        assert L
        return x, ''.join(L)
    
    def process_quotes(self, x, s):
        """
        Extract 'the quoted text\'s contents' :D
        """
        L = []
        backslash_mode = False
        first_char = True
        x += 1 # HACK!
        
        while 1:
            # Get the next character
            try: c = s[x]
            except IndexError: break
            print("QUOTES:", x, c)
            
            if backslash_mode:
                # Backslash mode
                # CHECK ME! ==========================================================
                if c == 'u':
                    # Unicode backslash
                    L.append((CHARS, chr(int(s[x+1:x+5], 16))))
                    x += 4
                elif c == "'":
                    # '\' -> an actual backslash!
                    L.append((CHARS, '\\'))
                    break
                else:
                    L.append((CHARS, c))
                
                backslash_mode = False
            elif c == '\\':
                backslash_mode = True
            elif first_char and c=="'":
                # `''` means a single escaped `'`
                L.append((CHARS, "'"))
                break
            elif c == "'":
                break
            else:
                L.append((CHARS, c))
            
            first_char = False
            x += 1
        
        return x, L
    
    def add_transform_rule(self, x, s):
        """
        Add 
        :: [:^Katakana:] ; # do not touch any katakana that was in the text!
        :: Hiragana-Katakana;
        :: Katakana-Latin;
        :: ([:^Katakana:]) ; # do not touch any katakana that was in the text
                             # for the inverse either!
        
        :: lower () ; # only executed for the normal
        :: (lower) ; # only executed for the inverse
        :: lower ; # executed for both the normal and the inverse
        
        ID    Inverse of ID
        A-B    B-A
        A-B ( )    (A-B)
        (A-B)    A-B ( )
        
        (Any-)Null/(Any-)Null
        (Any-)NFD/(Any-)NFC
        (Any-)NFKD/(Any-)NFKC
        (Any-)Lower/(Any-)Upper
        
        Title
        
        * If there's a range and a function, then the 
          function is executed for that range only.
        
        * If there's a range, then it applies to this pass.
        
        * If there's a function, then it applies to this pass.
        """
        brackets_mode = False
        found_brackets = False
        
        inverse_range = None
        normal_range = None
        
        # Chars inside the brackets
        LBrackets = []
        # Chars outside the brackets
        L = []
        
        while 1:
            # Get the next character
            try: c = s[x]
            except IndexError: break
            print('TRANSFORM RULE:', x, c)
            
            if brackets_mode:
                # Brackets ("inverse") mode processing
                if c == ')':
                    brackets_mode = False
                elif c == '[':
                    # Start of a range (inverse mode)
                    x, inverse_range = self.process_range(x, s)
                else:
                    LBrackets.append(c) # OPEN ISSUE: Are spaces ignored? =======
            
            elif c == '[':
                # Start of a range (normal mode)
                x, normal_range = self.process_range(x, s)
            
            elif c == ';':
                # End of the rule
                break
            
            elif c == '(':
                # Start of the brackets
                assert not LBrackets
                brackets_mode = True
                found_brackets = True
            
            else:
                L.append(c)
            
            x += 1
        
        normal = ''.join(L).strip()
        inverse = ''.join(LBrackets).strip()
        
        if normal:
            normal = 'Any-%s'%normal \
                if not '-' in normal else normal
        
        if inverse:
            inverse = 'Any-%s'%inverse \
                if not '-' in inverse else inverse
        
        if normal and not found_brackets:
            # If no brackets found, then use for the inverse too!
            # Note that it sometimes makes Lower->Upper etc!
            inverse = DInverse[normal] \
                if normal in DInverse else normal
        
        if not found_brackets:
            # CHECK ME! =======================================================
            inverse_range = normal_range
        
        DRule = {
            'normal_range': normal_range,
            'inverse_range': inverse_range,
            'normal': normal or None,
            'inverse': inverse or None
        }
        
        return x, DRule
    
    def process_function_call(self, x, s):
        """
        Parse the `&function(args);` syntax
        """
        LName = []
        LArgs = []
        backslash_mode = False
        
        FN_NAME = 0
        FN_ARGS = 1
        
        mode = FN_NAME
        # Level of "()" characters for recursive processing
        level = 1
        x += 1 # Skip the "&"
        
        while 1:
            # Get the next character
            try: c = s[x]
            except IndexError: break
            
            if mode == FN_NAME:
                if c == '(':
                    # The start of the arguments found
                    mode = FN_ARGS
                else:
                    LName.append(c)
                
            elif mode == FN_ARGS:
                if not backslash_mode and c=='(':
                    # If a "(" then descend into a new processing level
                    level += 1
                elif not backslash_mode and c==')':
                    # Stop processing if no more brackets
                    level -= 1
                    if not level:
                        break
                else:
                    # Otherwise process as normal
                    # (Note that
                    LExtend, backslash_mode, x = \
                        self.get_conversion_tokens(backslash_mode, x, s)
                    LArgs.extend(LExtend)
            x += 1
        return x, ''.join(LName).strip(), LArgs

if __name__ == '__main__':
    from pprint import pprint
    from os import listdir
    
    root = data_path('icu_translit')
    for path in listdir(root):
        if not path.endswith('.txt'):
            continue
        elif not '_' in path:
            print('IGNORING:', path)
            continue
        
        print('PROCESSING:', path)
        # 'Arabic_Latin.txt'
        L = get_L_icu_transform('%s/%s' % (root, path))
        pprint(L)
