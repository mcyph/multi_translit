# -*- coding: utf-8 -*-
# See "Appendix N: Transform Rules" of 
# http://unicode.org/reports/tr35/ for more information
from multi_translit.translit.my_engine.TranslitFunctions import CODEPOINTS_TO_HEX_DICT

# Basic define types
from iso_tools.chardata.unicodeset.tokenizer.ProcessRangeBase import ProcessRangeBase
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

inverse_dict = {}
for _from, _to in [
    ('Any-Null', 'Any-Null'),
    ('Any-NFD', 'Any-NFC'),
    ('Any-NFKD', 'Any-NFKC'),
    ('Any-Lower', 'Any-Upper')
]:
    inverse_dict[_from] = _to
    inverse_dict[_to] = _from

# NOTE: Any-Accents/Any-Publishing/Fullwidth-Halfwidth 
# are supplied in other files.
fns_dict = {
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

for key in CODEPOINTS_TO_HEX_DICT:
    fns_dict['Hex/%s-Any' % key] = "hex_to_codepoints('%s')" % key
    fns_dict['Any-Hex/%s' % key] = "codepoints_to_hex('%s')" % key


def get_icu_transform_list(path):
    inst = ParseICUTransform(path)
    return post_process(inst.out_list)


class ParseICUTransform(ProcessRangeBase):
    direction_chars_dict = {
        '→': '=>',
        '↔': '<=>',
        '←': '<='
    }
    
    tokens_dict = {
        '{': BEFORE_TOKEN,
        '}': AFTER_TOKEN,
        '|': CURSOR_TOKEN
    }
    
    repetition_dict = {
        '*': ZERO_OR_MORE,
        '+': ONE_OR_MORE,
        '?': ZERO_OR_ONE
    }
    
    def __init__(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            s = f.read()
        
        self.vars_dict = {}
        self.out_list = self.process_normal(s)
        
    def process_normal(self, s, x=0, group_mode=False):
        """
        item_dict -> {'mode': ASSIGN_VARIABLE/CONVERSION/TRANSFORM_RULE,
                  'data': (...),
                  'comments_list': [comment, ...]}
        """
        item_dict = {}
        
        """
        Information about the current conversion:
        
        current_list -> The tokens for the current conversion 
                    (either from or to depending on the current state)
        conversion_list -> LBefore, direction, LAfter
        """
        return_list = []
        current_list = []
        conversion_list = [None, None, None]
        
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
            
            print('MAIN:', x, c, ord(c), start_of_statement, backslash_mode, current_list, conversion_list)
            
            #========================================================#
            #                   Variable Handling                    #
            #========================================================#
            
            # Variable handling
            if c=='$' and not backslash_mode:
                x, var_name, var_list, comments_list = self.get_variable(x+1, s)
                
                if var_list != None:
                    # make sure there are no previous comments etc
                    assert not item_dict
                    item_dict['mode'] = VARIABLE
                    item_dict['data'] = (var_name, var_list)
                    item_dict['comments_list'] = comments_list
                    return_list.append(item_dict)
                    
                    assert not var_name in self.vars_dict # WARNING! =============
                    self.vars_dict[var_name] = var_list
                else:
                    assert not comments_list # Just to make sure...
                    x -= 1 # HACK! ===========================================================================
                    current_list.append((VARIABLE, var_name))
            
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
                    item_dict.setdefault('comments_list', []).append(comment)
                
                # Continue to make sure `start_of_statement` isn't set to `False`!
                #x += 1
                continue
            
            elif start_of_statement and not group_mode \
                and s[x:x+2]=='::':
                
                # Transform rules
                x, rule_dict = self.add_transform_rule(x+2, s)
                return_list.append({'mode': TRANSFORM_RULE,
                                    'data': rule_dict})
                continue
                
            elif c in self.direction_chars_dict and \
                not backslash_mode and not group_mode:
                
                # Conversion direction characters
                assert not conversion_list[1]
                conversion_list[1] = self.direction_chars_dict[c]
                
                # Change to the right hand side direction
                conversion_list[0] = current_list
                current_list = []
                
                # Set the mode to CONVERSION
                item_dict['mode'] = CONVERSION
                item_dict['data'] = conversion_list
            
            elif c==';' and not backslash_mode and not group_mode:
                # End of the line
                # TODO: Add more sophisticated checking!
                
                if item_dict.get('mode') == CONVERSION:
                    # Append the last item if in CONVERSION mode
                    assert conversion_list == item_dict['data']
                    conversion_list[2] = current_list
                    current_list = []
                    conversion_list = [None, None, None]
                else:
                    # Make sure that current_list is 
                    # blank if not in conversion mode!
                    assert not current_list, current_list
                
                if item_dict:
                    return_list.append(item_dict)
                item_dict = {}
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
                x, append_list = self.process_normal(s, x+1, group_mode=True)
                current_list.append((GROUP, [None, append_list]))
                repetition_idx = len(current_list) # CHECK ME! ==================
            
            elif c==')' and not backslash_mode and group_mode:
                # End a group (if in group mode)
                break
            
            elif c in self.repetition_dict and not backslash_mode:
                flag = self.repetition_dict[c]
                
                if current_list and current_list[-1][0]==GROUP:
                    # If the previous item is 
                    # a group, set the repetition flag
                    assert current_list[-1][1][0] is None
                    current_list[-1][1][0] = flag
                else:
                    # Otherwise, create an artificial group
                    # with a given repetition flag
                    group_list = current_list[repetition_idx:]
                    del current_list[repetition_idx:]
                    current_list.append((GROUP, [flag, group_list]))
                
                repetition_idx = len(current_list)

            #========================================================#
            #        Conversion Character/Range Processing           #
            #========================================================#
            
            else:
                extend_list, backslash_mode, x = \
                    self.get_conversion_tokens(backslash_mode, x, s)
                current_list.extend(extend_list)
            
            if start_of_statement and c.strip():
                # COMMENT IN THE MIDDLE OF A STATEMENT WARNING! ===========================
                start_of_statement = False
            x += 1
        
        if group_mode:
            return x, current_list
        else:
            return return_list
    
    def get_conversion_tokens(self, backslash_mode, x, s):
        """
        Conversion Character/Range Processing
        """
        c = s[x]
        out_list = []
        
        if c == '[':
            # Start of UnicodeSet mode
            x, range_ = self.process_range(x, s)
            #if True:
            #    from iso_tools.chardata.unicodeset.unicodeset import get_unicode_set_ranges
                
            #    print('RANGE TOKENS:', get_unicode_set_ranges(range_, self.vars_dict, char_indexes=None))
            out_list.append((UNICODE_SET, range_))
        
        elif c == '&':
            # Start of function call mode
            x, fn_name, fn_args_list = self.process_function_call(x, s)
            out_list.append((FUNCTION_CALL, (fn_name, fn_args_list)))
        
        elif backslash_mode:
            # Backslash mode
            # CHECK ME! ==========================================================
            if c == 'u':
                # Unicode backslash
                out_list.append((CHARS, chr(int(s[x+1:x+5], 16))))
                x += 4
            else:
                out_list.append((CHARS, c))
            
            backslash_mode = False
            
        elif c == '\\':
            backslash_mode = True
        
        elif c == "'":
            # Quotes mode
            print("QUOTES!")
            x, extend_list = self.process_quotes(x, s)
            out_list.extend(extend_list)
        
        elif c in self.tokens_dict:
            # Before/after/cursor tokens
            print('TOKEN:', self.tokens_dict[c])
            out_list.append(self.tokens_dict[c])
        
        elif c.strip():
            out_list.append((CHARS, c))
        
        return out_list, backslash_mode, x
    
    def get_comment(self, x, s):
        """
        "# comment"'s go until the end of the line
        """
        out_list = []
        while 1:
            # Get the next character
            try: c = s[x]
            except IndexError: break
            
            if c == '\n':
                break
            
            out_list.append(c)
            x += 1
        return x, ''.join(out_list)
    
    def get_variable(self, x, s):
        """
        Get the variable name and tokens
        """
        x, name = self.get_variable_name(x, s)
        
        out_list = []
        found_equals = False
        backslash_mode = False
        comments_list = []
        
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
                    out_list = None
                    break
                
                #assert not c.strip(), \
                #    '"%s" should be "=" after specifying variable name' % c
            
            elif c == '#':
                # Process comments
                x, comment = self.get_comment(x, s)
                comments_list.append(comment)
                
            elif c == ';':
                # Reprocess semicolons again
                x -= 1
                break
            
            else:
                # TODO: How to process the logic?
                # Seems a bit repetitive to copy-paste the above code...
                extend_list, backslash_mode, x = \
                    self.get_conversion_tokens(backslash_mode, x, s)
                out_list.extend(extend_list)
            x += 1
        
        return x, name, out_list, comments_list
    
    def get_variable_name(self, x, s):
        """
        Get the name of the variable
        
        FIXME: Make it work with numbers etc after the variable! ===========================
        """
        out_list = []
        allowed = 'abcdefghijklmnopqrstuvwxyz_'
        allowed_set_1 = set(allowed+allowed.upper())
        allowed_set_2 = allowed_set_1.union(set('1234567890_'))
        
        first_time = False
        while 1:
            # Get the next character
            try: c = s[x]
            except IndexError: break
            
            if first_time and c in allowed_set_1 and False:
                out_list.append(c)
            elif c in allowed_set_2:
                out_list.append(c)
            else:
                break
            
            x += 1
            first_time = False
        
        assert out_list
        return x, ''.join(out_list)
    
    def process_quotes(self, x, s):
        """
        Extract 'the quoted text\'s contents' :D
        """
        out_list = []
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
                    out_list.append((CHARS, chr(int(s[x+1:x+5], 16))))
                    x += 4
                elif c == "'":
                    # '\' -> an actual backslash!
                    out_list.append((CHARS, '\\'))
                    break
                else:
                    out_list.append((CHARS, c))
                
                backslash_mode = False
            elif c == '\\':
                backslash_mode = True
            elif first_char and c=="'":
                # `''` means a single escaped `'`
                out_list.append((CHARS, "'"))
                break
            elif c == "'":
                break
            else:
                out_list.append((CHARS, c))
            
            first_char = False
            x += 1
        
        return x, out_list
    
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
        brackets_list = []
        # Chars outside the brackets
        out_list = []
        
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
                    brackets_list.append(c) # OPEN ISSUE: Are spaces ignored? =======
            
            elif c == '[':
                # Start of a range (normal mode)
                x, normal_range = self.process_range(x, s)
            
            elif c == ';':
                # End of the rule
                break
            
            elif c == '(':
                # Start of the brackets
                assert not brackets_list
                brackets_mode = True
                found_brackets = True
            
            else:
                out_list.append(c)
            
            x += 1
        
        normal = ''.join(out_list).strip()
        inverse = ''.join(brackets_list).strip()
        
        if normal:
            normal = 'Any-%s'%normal \
                if not '-' in normal else normal
        
        if inverse:
            inverse = 'Any-%s'%inverse \
                if not '-' in inverse else inverse
        
        if normal and not found_brackets:
            # If no brackets found, then use for the inverse too!
            # Note that it sometimes makes Lower->Upper etc!
            inverse = inverse_dict[normal] \
                if normal in inverse_dict else normal
        
        if not found_brackets:
            # CHECK ME! =======================================================
            inverse_range = normal_range
        
        rule_dict = {
            'normal_range': normal_range,
            'inverse_range': inverse_range,
            'normal': normal or None,
            'inverse': inverse or None
        }
        
        return x, rule_dict
    
    def process_function_call(self, x, s):
        """
        Parse the `&function(args);` syntax
        """
        name_list = []
        args_list = []
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
                    name_list.append(c)
                
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
                    extend_list, backslash_mode, x = \
                        self.get_conversion_tokens(backslash_mode, x, s)
                    args_list.extend(extend_list)
            x += 1
        return x, ''.join(name_list).strip(), args_list


if __name__ == '__main__':
    from pprint import pprint
    from os import listdir
    
    root = data_path('icu_translit', 'conversions')
    for path in listdir(root):
        if not path.endswith('.txt'):
            continue
        elif not '_' in path:
            print('IGNORING:', path)
            continue
        
        print('PROCESSING:', path)
        # 'Arabic_Latin.txt'
        out_list = get_icu_transform_list('%s/%s' % (root, path))
        pprint(out_list)
