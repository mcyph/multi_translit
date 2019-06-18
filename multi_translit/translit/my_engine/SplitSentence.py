import unicodedata


DCats = {
    'Cc': 'L', # Other, control
    'Cf': 'L', # Other, format
    'Cn': 'L', # Other, not assigned
    'Co': 'L', # Other, private use
    'Cs': 'L', # Other, surrogate
    'Ll': 'L', # Letter, lowercase
    'Lm': 'L', # Letter, modifier
    'Lo': 'L', # Letter, other
    'Lt': 'L', # Letter, titlecase
    'Lu': 'L', # Letter, uppercase
    'Mc': 'L', # Mark, spacing combining
    'Me': 'L', # Mark, enclosing
    'Mn': 'L', # Mark, non-spacing
    'Nd': 'L', # Number, decimal digit (changed N->L because of PinYin)
    'Nl': 'L', # Number, letter (N)
    'No': 'L', # Number other (N)
    'Pc': 'P', # Punctuation, connector
    'Pd': 'P', # Punctuation, dash
    'Pe': 'P', # Punctuation, close
    'Pf': 'P', # Punctuation, final quote
    'Pi': 'P', # Puntuation, initial quote
    'Po': 'P', # Punctuation, other
    'Ps': 'P', # Punctuation, open
    'Sc': 'S', # Symbol, currency
    'Sk': None, # Symbol, modifier (e.g. combining tilde)
    'Sm': 'S', # Symbol, math
    'So': 'S', # Symbol, other
    'Zl': 'Z', # Separator, line
    'Zp': 'Z', # Separator, paragraph
    'Zs': 'Z', # Separator, space
    'L': 'L' # All L group
}


def split_sentence(S):
    """
    Split a sentence by character categories
    e.g. "Word!?&$ [END]" would split into
    ['Word', '!?&', '$', ' ', '[', 'END', ']']
    to allow proper processing of initials/finals etc
    """
    LRtn = []
    LWord = []
    
    current_mode = None
    for char in S:
        try: 
            new_mode = DCats.get(
                unicodedata.category(unicode(char)),
                'Z'
            )
        except: 
            new_mode = 'Z' # HACK!
        
        if char == ':': 
            new_mode = 'L' # PINYIN HACK!
        
        if new_mode and new_mode!=current_mode:
            current_mode = new_mode
            LRtn.append(''.join(LWord))
            LWord = [char]
        else:
            LWord.append(char)
    
    LRtn.append(''.join(LWord))
    return LRtn
