import unicodedata
from multi_translit.translit.korean import pythonhangul as hangul

try: 
    import hangul
except ImportError:

def limited_len(s): 
    len_ = len(s)
    if len_ > 3: 
        len_ = 3
    return len_

def get_three_parts(L):
    LRtn = []
    for i in xrange(3):
        if len(L) < (i+1): 
            LRtn.append('')
        else: 
            LRtn.append(L[i])
    return LRtn

def jamo_to_hangul(s):
    'Split into three parts each'
    LRtn = []
    len_ = limited_len(s)
    
    while s:
        if not len_:
            # No results, so chop the leftmost char off
            LRtn.append(s[0])
            s = s[1:]
            len_ = limited_len(s)
        
        if 'HANGUL' in unicodedata.name(s[0]):
            try: 
                '''
                hangul.join requires the arguments to be of length three as there 
                are three jamo characters in a Jamo. Blank strings need to be used 
                if not a character in a specific position
                '''
                joined = hangul.join(get_three_parts(s[:len_]))
                
                if joined: 
                    LRtn.extend(joined)
                    s = s[len_:]
                    len_ = limited_len(s)
            except: 
                len_ -= 1
        else: 
            LRtn.append(s[0])
            s = s[1:]
            len_ = limited_len(s)
    
    return ''.join(LRtn)

def hangul_to_jamo(s):
    '''
    Convert Korean to Jamo (the smaller parts that 
    make up a Hangul letter) This is useful in 
    similar matches to improve accuracy :-)
    '''
    LRtn = []
    for char in s:
        if 'HANGUL' in unicodedata.name(char):
            try: 
                LRtn.extend(hangul.split(char))
            except: 
                LRtn.append(char)
        else: 
            LRtn.append(char)
    
    return ''.join(LRtn)

if __name__ == '__main__':
    Test1 = hangul_to_jamo(u'g민fdsaf')
    Test2 = hangul_to_jamo(u'gfgㄴ')
    
    print Test1.encode('utf-8'), ';', Test2.encode('utf-8')
    print jamo_to_hangul(Test1).encode('utf-8'), jamo_to_hangul(Test2).encode('utf-8')
