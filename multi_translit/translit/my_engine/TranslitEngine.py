# -*- coding: utf-8 -*-
from multi_translit.translit.my_engine.ProcessWord import process_word
from multi_translit.translit.my_engine.SplitSentence import split_sentence

from multi_translit.translit.my_engine.TranslitParse import TranslitParse


cache_dict = {}
def TranslitEngine(path, direction='=>', sep=''):
    key = (path, direction, sep)
    if not key in cache_dict:
        cache_dict[key] = _TranslitEngine(path, direction, sep)
    return cache_dict[key]


class _TranslitEngine(TranslitParse):
    def __init__(self, path, direction='=>', sep=' '):
        #print 'TRANSLIT PARSE!'
        TranslitParse.__init__(self, path, direction)
        #print 'PARSE OK!'
        self.sep = sep


    #======================================================#
    #                   Basic Conversion                   #
    #======================================================#


    def convert(self, text):
        """
        Convert the script with a basic string input/output, 
        processing each word separately by splitting by spaces
        """
        return_list = []

        for word in split_sentence(text):
            LOut = []
            word = process_word(word, self.direction, self.LFromModifiers)
            
            def fn(source, output):
                LOut.append(output)
            
            self.convert_word(word, fn)
            word = process_word(self.sep.join(LOut), self.direction, self.LToModifiers)
            return_list.append(word)

        return self.sep.join(return_list)


    #======================================================#
    #                  Actual Conversion                   #
    #======================================================#


    def convert_word(self, text, fn):
        before = '' # Previous text
        next = text # Next text
        LNotFound = [] # Not found results
        
        while 1: 
            if not next: 
                break
            
            #print 'NEXTCHAR:', next_char.encode('utf-8')
            LMatch = self.match(before, before, next) # FIXME: MAKE UNCONVERTED TEXT AVAILABLE(!) =======================


            if not LMatch:
                # Shift the text one forward, 
                # leaving the text unconverted
                before += next[0]
                LNotFound.append(next[0])
                next = next[1:]

            else:
                # Slice the word based on the end pos
                match_end, conv = LMatch
                end_pos = match_end

                if LNotFound:
                    fn(*[''.join(LNotFound)]*2)
                    LNotFound = []


                # convert to the correct case
                in_txt = next[:end_pos]
                if self.match_case:
                    conv = self._match_case(in_txt, conv)


                fn(in_txt, conv)
                before += next[:end_pos]
                next = next[end_pos:]


        if LNotFound: 
            fn(*[''.join(LNotFound)]*2)


    def _match_case(self, in_, out):
        if in_.islower():
            return out.lower()
        elif in_.isupper():
            return out.upper()
        elif in_.istitle():
            return out.title()
        else:
            return out.lower()


if __name__ == '__main__':
    te = TranslitEngine(
        '/home/david/Dev/git/uni_tools/translit/data-new/' +
            'Asian/Japanese/Latin/Japanese Hiragana-Latin.trn'
    )

    print(te.convert('にほんご'))
    print(te.convert('にんんに'))
