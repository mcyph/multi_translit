# -*- coding: utf-8 -*-
# Korean Transliterator Generator
# Id: TransliteratorGenerator.pm,v 1.7 2007/11/29 14:25:31 you Exp 

#  == CONSTANTS ==
import re
NotFound = '-1' # CHECK ME!
CamelCase = 0
GREEDY_SEP =1
SMART_SEP =  2

MODE = {
    'CamelCase': CamelCase, # NOT YET IMPLEMENTED!
    'camel': CamelCase,     # "!

    'greedy_sep': GREEDY_SEP,
    'greedy': GREEDY_SEP,
    
    'smart_sep': SMART_SEP,
    'smart': SMART_SEP}

class Class:
    def __init__(self):
        self.CONSONANTS = []
        self.VOWELS = []
        self.EL = None
        self.ELL = None
        self.NAUGHT = None
        self.SEP = None
        self.ENMODE = []
        self.DEMODE = []
        self.HEAD = []
        self.BODY = []
        self.FOOT = []
        self.HEADMAP = {}
        self.BODYMAP = {}
        self.FOOTMAP = {}
    
    # == METHODS ==
    
    # accessor
    
    def consonants(self, L=None):
        if L:
            self.CONSONANTS = L
            self.head(L)
            self.FOOT = [
                '',                                                                        # NULL
                self.CONSONANTS[0],                                          # kiyeok (ㄱ)
                self.CONSONANTS[1],                                          # ssangkiyeok (ㄲ)
                self.CONSONANTS[0] + self.CONSONANTS[9],      # kiyeok sios (ㄳ)
                self.CONSONANTS[2],                                          # nieun (ㄴ)
                self.CONSONANTS[2] + self.CONSONANTS[12],     # nieun cieuc (ㄵ)
                self.CONSONANTS[2] + self.CONSONANTS[18],     # nieun hieuh (ㄶ)
                self.CONSONANTS[3],                                          # tikeut (ㄷ)
                self.CONSONANTS[5],                                          # rieul (ㄹ)
                self.CONSONANTS[5] + self.CONSONANTS[0],      # rieul kiyeok (ㄺ)
                self.CONSONANTS[5] + self.CONSONANTS[6],      # rieul mieum (ㄻ)
                self.CONSONANTS[5] + self.CONSONANTS[7],      # rieul pieup (ㄼ)
                self.CONSONANTS[5] + self.CONSONANTS[9],      # rieul sios (ㄽ)
                self.CONSONANTS[5] + self.CONSONANTS[16],     # rieul thieuth (ㄾ)
                self.CONSONANTS[5] + self.CONSONANTS[17],     # rieul phieuph (ㄿ)
                self.CONSONANTS[5] + self.CONSONANTS[18],     # rieul hieuh (ㅀ)
                self.CONSONANTS[6],                                          # mieum (ㅁ)
                self.CONSONANTS[7],                                          # pieup (ㅂ)
                self.CONSONANTS[7] + self.CONSONANTS[9],      # pieup sios (ㅄ)
                self.CONSONANTS[9],                                          # sios (ㅅ)
                self.CONSONANTS[10],                                         # ssangsios (ㅆ)
                self.CONSONANTS[11],                                         # ieung (ㅇ)
                self.CONSONANTS[12],                                         # cieuc (ㅈ)
                self.CONSONANTS[14],                                         # chieuch (ㅊ)
                self.CONSONANTS[15],                                         # khieukh (ㅋ)
                self.CONSONANTS[16],                                         # thieuth (ㅌ)
                self.CONSONANTS[17],                                         # phieuph (ㅍ)
                self.CONSONANTS[18]                                          # hieuh (ㅎ)
            ]
        return self.CONSONANTS
    
    def head(self, Val=None):
        if Val != None: self.HEAD = Val
        return self.HEAD

    def foot(self, Val=None):
        if Val != None: self.FOOT = Val
        return self.FOOT

    # accessor
    def vowels(self, Val=None):
        if Val != None:
            self.VOWELS = Val
            self.body(Val) # CHECK ME! -----------------------------------
        return self.VOWELS

    def body(self, Val=None):
        if Val != None: self.BODY = Val
        return self.BODY

    # accessor
    def el(self, Val=None):
        if Val != None: 
            self.EL = Val

            # Sets jongseongs with rieul
            self.foot()[8] =    self.EL                                    # rieul (ㄹ)
            self.foot()[9] =    self.EL + self.consonants()[0]  # rieul kiyeok (ㄺ)
            self.foot()[10] =  self.EL + self.consonants()[6]  # rieul mieum (ㄻ)
            self.foot()[11] =  self.EL + self.consonants()[7]  # rieul pieup (ㄼ)
            self.foot()[12] =  self.EL + self.consonants()[9]  # rieul sios (ㄽ)
            self.foot()[13] =  self.EL + self.consonants()[16] # rieul thieuth (ㄾ)
            self.foot()[14] =  self.EL + self.consonants()[17] # rieul phieuph (ㄿ)
            self.foot()[15] =  self.EL + self.consonants()[18] # rieul hieuh (ㅀ)
        return self.EL

    # accessor
    def ell(self, Val=None):
        if Val != None: self.ELL = Val
        return self.ELL

    # accessor
    def naught(self, Val=None):
        if Val != None:
            self.NAUGHT = Val
            self.HEAD[11] = self.NAUGHT
        return self.NAUGHT

    # accessor
    def sep(self, Sep=None):
        if Sep != None: self.SEP = Sep
        return self.SEP

    # accessor
    def enmode(self, Mode=None):
        if (Mode != None): self.ENMODE = Mode
        return self.ENMODE

    def demode(self, Mode=None):
        if (Mode != None): self.DEMODE = Mode
        return self.DEMODE



    def make(self):
        for i in xrange(len(self.head())):
            if (self.head()[i] == "" and i != 11):
                pass
                #printf "error: empty slot. fill the transliteration for /%s/!<br />", 
                #          encode::encode("utf8", han_consonant[i]) exit(1)
            if self.head()[i] in self.HEADMAP: 
                #print_mapping_error(self::head[i], self::head{self::head[i]}, i) 
                raise Exception()
            else:
                self.HEADMAP[self.head()[i]] = i # CHECK ME!

        for i in xrange(len(self.body())):
            if (self.body()[i] == ""):
                #printf "error: empty slot. fill the transliteration for /%s/!<br />", 
                #          Encode::encode("utf8", HAN_VOWEL[i]) 
                            exit(1)
            if self.body()[i] in self.BODYMAP: 
                #print_mapping_error(self::BODY[i], self::BODY{self::BODY[i]}, i) 
                raise Exception()
            else: self.BODYMAP[self.body()[i]] = i
            self.BODYMAP[self.body()[i]] = i
         
        for i in xrange(len(self.foot())):
            self.FOOTMAP[self.foot()[i]] = i
        return self

    # encode(string [,check])
    # = transliteration (romanization)
    def encode(self, str, chk=False):
        tr = self.transliterate(str)
        #_[1] = '' if chk # WTF?! ------------------------------------------------
        return tr

    # decode(octets [,check])
    def decode(self, str, chk=False):
        han = self.hangulize(str)
        #_[1] = '' if chk # WTF?! ------------------------------------------------
        return han

    # to work with encoding pragma
    # cat_decode(destination, octets, offset, terminator [,check])






    # = HAN TRANSLITERATOR = 
    # romanizer and hangulizer

    # == hangul composer and decomposer ==
    #
    # Unicode : 0xAC00 (가) -- 0xD7A3 (힣)
    #
    # foot (28 types) : 가각갂갃간갅갆갇갈갉갊갋갌갍갎갏감갑값갓갔강갖갗갘같갚갛
    # body (21 types) : 가개갸걔거게겨계고과괘괴교구궈궤귀규그긔기
    # head (19 types) : 가까나다따라마바빠사싸아자짜차카타파하
    #


    # === decompose  ===
    # decomposes an unicode hangul chr into a hancode (head, body, foot)
    # for example, decompose('한') returns (18, 0, 4)
    def decompose(self, chr):
        unicode = ord(chr)
        head = int((unicode - 0xAC00) / (28*21))
        body = int((unicode - 0xAC00 - head*28*21) /28)
        foot = unicode - 0xAC00 - head*28*21 - body*28
        return (head, body, foot)

    # === compose ===
    # composes an unicode hangul chr from a hancode (head, body, foot)
    # for example, compose((18,0,4)) returns '한'
    def compose(self, head, body, foot):
        unicode = 0xAC00 + head*28*21 + body*28 + foot
        return unichr(unicode)

    # == ROMANIZE (TRANSLITERATE) ==

    # === transliterates a hangul chr (unicode hangul syllable) ===
    # for example, transliterate('한') returns ('h', 'a', 'n')
    def transliterate_chr(self, chr):
        head, body, foot = self.decompose(chr)
        #return (self->head[head], self->body[body], self->foot[foot])
        if (self.enmode() == 'greedy' and head == 11):
            return self.body()[body] + self.foot()[foot]
        else:
            return self.head()[head] + self.body()[body] + self.foot()[foot]
    
    def transliterate_first_chr_of_word(self, chr):
        head, body, foot = self.decompose(chr)
        if (head == 11):
            return self.body()[body] + self.foot()[foot]
        else:
            return self.head()[head] + self.body()[body] + self.foot()[foot]

    # === transliterate a hangul word ===
    # Transliterates a hangul word (a string containing
    # only hangul syllables)
    def transliterate_hangul_word(self, word):
        char = list(word) # FIXME! ---------------------------------------------
        tr = self.transliterate_first_chr_of_word(char[0])
        for i in xrange(1, len(char)): # CHECK ME! ---------------------------------
            if MODE[self.enmode()] == GREEDY_SEP:
                tr = tr + self.sep() + self.transliterate_chr(char[i])
            else:
                tr = tr + self.transliterate_chr(char[i])
        return tr

    # === transliterate a string ===
    # The input string may contain any character.
    # Transliterates only unicode hangul syllables (AC00-D7A3),
    # returns other characters including hangul jamo (1100-11F9)
    # and hangul compatibility jamo.
    def transliterate_line(self, str):
        char = list(str)
        for c in char:
            if (ord(c)>=0xAC00 and ord(c)<=0xD7A3):
                tr = tr + self.transliterate_chr(c)
            else:
                tr = tr + c
        return tr

    # === transliterate ===
    # Transliterates word by word
    def transliterate(self, str):
        tr = ''
        word = re.split(u'([^\uAC00-\uD7A3]+)', str) # CHECK ME! ----------------------------
        for w in word:
            if re.match(u'^[\uAC00-\uD7A3]+$', w): # m?
                tr = tr + self.transliterate_hangul_word(w)
            else:
                tr = tr + w
        return tr 


    #
    # == HANGULIZE (REVERSE TRANSLITERATION) ==
    #
    # H: head, B: body, F: foot
    #  H?BF?(HBF?)*

    # === hangulize ===
    # reverse transliteration : hangulizes a transliterated strings
    # for example: hangulize('hangugmal') returns '한국말'
    def hangulize(self, str):
        h = ''
        sep = self.sep()
        #print 'SEP:', sep
        
        if (sep != ''):
            word = str.split(sep) #re.split('\Q%s\E' % sep, str)
            for _ in word: 
                h = h + self.get_han(_)
        else:
            h = h + self.get_han(str)
        return h

    #------------------------------
    # hangulizes an array of alphabets into one hangul chr
    # for example, hangulize_code(('h', 'a', 'n')) returns '한'
    def hangulize_code(self, head, body, foot):
        #print self.head(), self.body(), self.foot()
        hancode = (self.HEADMAP[head], 
                      self.BODYMAP[body], 
                      self.FOOTMAP[foot])
        return self.compose(*hancode)


    #-------------------------------
    # lookup str, @list_of_jamo_transliteration
    # eg. lookup('ssan', @CONSONANT) returns ('ss', 'an')
    #      where @CONSONANT has an item 'ss' 
    def lookup(self, str, where):
        found = NotFound
        rest = str
        
        for _ in where:
            if (_ == str[0:len(_)]):
                if (found == NotFound):
                    found = _
                    rest = str[len(_):]
                elif (len(found) < len(_)):
                    found = _
                    rest = str[len(_):]
    #  if(found == NotFound) {
    #      if(@where == @HEAD) {found = HEAD[11]}
    #      elsif (@where == @BODY) {found = NotFound}
    #      elsif (@where == @FOOT) {found = FOOT[0]}
    #      rest = str
    #  }
        return (found, rest)

    #-------------------------------
    #      SEP = "/" NAUGHT = "'"
    #      isse      = 이써
    #      iss'e     = 있어        :      is/se      = 잇서
    #      ibsi    =  입시
    #      ibs'i  =  잆이 
    #      ibsse     = 입써      :      ibs/se    = 잆서
    #      ibssse  = 잆써

    #-------------------------------
    # get_head(str)
    # eg. get_head("ssan") retunrs ("ss", "an")
    def get_head(self, str):
        head, rest = self.lookup(str, self.head()) # FIXmE! ------------------------------------------
        return head, rest

    #-------------------------------
    # get_body(str) 
    # eg. get_body("wan") returns ("wa", "n")
    def get_body(self, str):
        body, rest = self.lookup(str, self.body())
        return body, rest
    
    #-------------------------------
    # get_foot(str) 
    # eg. get_foot("bssan") returns ("bs", "san")
    def get_foot(self, str):
        foot, rest = self.lookup(str, self.foot())
        return foot, rest

    #-------------------------------
    # look_ahead for the next head - body sequence
    # case :
    #  normal :     look_ahead("mal") == "m"
    #  no_head: look_ahead("an") == ""
    #  no_body: look_ahead("kkkkk") == NotFound
    def look_ahead(self, right):
        head, right = self.get_head(right)
        body, right = self.get_body(right)
         
        if body == NotFound: return NotFound
        elif head == NotFound: return ""
        else: return head

    #-------------------------------
    # get a hangul string from a transliteration :
    # Makes the first hangul syllable from a transliterated string
    # and recursively processes the rest.  
    # for example: get_han('hangugmal') returns unicode string '한국말'
    def get_han(self, right):
        NAUGHT = self.naught()
        FILL = ""      # jongseong filler

        head = None
        body = None
        foot = None
        look_ahead_token = None
        h = ''
        
        show_process(0, "begin", h, head, body, foot, look_ahead_token, right)

        head, right = self.get_head(right)
        show_process(1, "get_head", h, head, body, foot, look_ahead_token, right)
        
        body, right = self.get_body(right)
        show_process(2, "get_body", h, head, body, foot, look_ahead_token, right)

        if head == NotFound and body == NotFound:
            h = h + right[0:1]
            show_process(21, "no head", h, head, body, foot, look_ahead_token, right)
            if right != "": h = h + self.get_han(right[1:])
        elif head != NotFound and body == NotFound:
            h = h + head
            show_process(22, "no body", h, head, body, foot, look_ahead_token, right)
            if right != "": h = h + right[0:1] + self.get_han(right[1:])
        else:
            if head == NotFound: head = NAUGHT
            foot, right = self.get_foot(right)
            show_process(3, "get_foot", h, head, body, foot, look_ahead_token, right)
            
            if foot == NotFound or foot == FILL:
                h = h + self.hangulize_code(head, body, FILL)
                show_process(31, "no foot", h, head, body, foot, look_ahead_token, right)
                if right != "": h = h + self.get_han(right)
            elif right == "":
                h = h + self.hangulize_code(head, body, foot)
                show_process(32, "eof", h, head, body, foot, look_ahead_token, right)
            else:
                look_ahead_token = self.look_ahead(right)
                show_process(4, "look_ahead", h, head, body, foot, look_ahead_token, right)
                if look_ahead_token == NotFound or look_ahead_token == NAUGHT:
                    h = h + self.hangulize_code(head, body, foot)
                    show_process(41, "no look", h, head, body, foot, look_ahead_token, right)
                    if right != "": h = h + self.get_han(right)
                else:
                    foot, right = self.get_correct_foot(foot, look_ahead_token, right)
                    h = h + self.hangulize_code(head, body, foot)
                    show_process(42, "get_correct_foot", h, head, body, foot, look_ahead_token, right)
                    if right != "": h = h + self.get_han(right)
        return h
    
    #-------------------------------
    # correct foot
    # <n:a:nh>(NAUGHT)a  -->     <n:a:n>ha
    # <n:a:bs>(s)sa                  -->     <n:a:b>ssa
    # <n:a:nh>(t)ta                    -->     <n:a:nh>ta
    #my foot_p, my look_ahead_token, my right_p
    #my foot, my right
    def get_correct_foot(self, foot_p, look_ahead_token, right_p):
        foot = None
        right = None
        foot_p = foot_p + look_ahead_token
        right_p = right_p[len(look_ahead_token):]
        foot = foot_p
        right = right_p
        found = NotFound
        
        for _ in self.head():
            if (_ == foot_p[len(foot_p)-len(_):]):
                if found == NotFound:
                    found = _
                    foot = foot_p[0:len(foot)-len(found)]
                    right = found + right_p
                elif len(found) < len(_):
                    found = _
                    foot = foot_p[0:len(foot_p)-len(found)]
                    right = found + right_p
        return foot, right

#, = "\t" # FIXME1
def show_process(id, desc, h, head, body, foot, look_ahead_token, right):
    if False:
      print id , desc, h, head, body, foot, look_ahead_token, right, "\n"

'''
=encoding utf8

=head1 NAME

Encode::Korean - Perl extension for Encoding of Korean: Transliterator Generator 

=head1 SYNOPSIS

  use Encode::Korean::TransliteratorGenerator

  my coder = Encode::Korean::TransliteratorGenerator->new()

  coder->consonants(@CONSONANTS)
  coder->vowels(@VOWELS)
  coder->sep(SEP)
  coder->make()

  while(utf_input = <>) {
	print coder->encode(decode 'utf8', utf_input)
  }

=head1 DESCRIPTION

This module provide a generic Korean transliterator class. You can define your
own rules and create your own transliterator object. 

The transliteration based encoding modules uses this class.
See L<Encode::Korean>.



=head2 How to define a custom transliteration set

 @CONSONANT  : array of 19 consonant letters
 @VOWEL        : array of 21 vowel letters
 EL            : jongseong l
 ELL          : consecutive l's 
 NAUGHT      : soundless choseong ieung
 SEP          : syllable separator
 MODE         : CamelCase, greedy_sep, smart_sep 
 

eg. South Korean Standard

 @CONSONANT = qw(g kk n d tt r m b pp s ss ng j jj ch k t p h)
 @VOWEL = qw(a ae ya yae eo e yeo ye o wa wae oe yo u wo we wi yu eu ui i)
 EL = "l"
 ELL = "ll"
 NAUGHT = "'"
 SEP = "-"

=head2 TRANSLITERATION MODES

Transliteration modes for ambiguous syllable boundary resolution. 


=head3 1. Use CamelCase

Makes syllables capitalized. Ignores NAUGHT and SEP. Not yet implemented at all.

 eg. 하나 -> HaNa, 한아 -> HanA

=head3 2. Greedy Separator

Insert SEP between syllables. Implemented. The object can produces (when encode)
transliteration with greedy separator mode and recognize (decode) it.

 eg. 하나 -> ha.na, 한아 -> han'a, where SEP = '.' NAUGHT = "'"
 eg. 하나 -> ha.na, 한아 -> han.a, where SEP = '.' NAUGHT = undef

=head3 3. Smart Separator

Insert SEP when syllable boundaries are ambiguous in transliteration.
Partially implemented. The object can recognize (decode) it but does not
produce it.

 If NAUGHT is defined and is not null:

    insert NAUGHT for the soundless head (choseong ieung)
    insert SEP between consonant groups.

    eg. 하나 -> hana, 한아 -> han'a
    eg. 앉자 -> anc.ca, 안짜 -> an.cca

 else :

    insert SEP for the soundless head and between consonant groups.

    eg. 하나 -> hana,     한아 -> han.a
    eg. 앉자 -> anc.ca,  안짜 -> an.cca 
        앉하 -> anc.ha,  안차 -> an.cha
    eg. 갂아 -> kakk.a,  각가 -> kak.ka, 가까 -> kakka
        각까 -> kak.kka, 갂가 -> kakk.ka
        갂까 -> kakk.kka

=head1 SEE ALSO


=head1 AUTHOR

You Hyun Jo, E<lt>you at cpan dot orgE<gt>

=head1 COPYRIGHT AND LICENSE

Copyright (C) 2007 by You Hyun Jo

This library is free software you can redistribute it and/or modify
it under the same terms as Perl itself, either Perl version 5.8.8 or,
at your option, any later version of Perl 5 you may have available.


'''
# vim: set ts=3 sts=3 sw=3 et:
