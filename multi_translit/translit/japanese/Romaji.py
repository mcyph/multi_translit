# -*- coding: UTF-8 -*-

from types import ListType

def get_rom_hira():
    LRomHira = [['1', '１'],
                ['2', '２'],
                ['3', '３'],
                ['4', '４'],
                ['5', '５'],
                ['6', '６'],
                ['7', '７'],
                ['8', '８'],
                ['9', '９'],
                ['0', '０'],
                
                ['a', 'あ'],
                ['i', 'い'],
                ['u', 'う'],
                ['e', 'え'],
                ['o', 'お'],
                ['ka', 'か'],
                ['ki', 'き'],
                ['ku', 'く'],
                ['ke', 'け'],
                ['ko', 'こ'],
                ['sa', 'さ'],
                ['si', 'し'],
                ['su', 'す'],
                ['se', 'せ'],
                ['so', 'そ'],
                ['ta', 'た'],
                ['ti', 'ち'],
                ['tu', 'つ'],
                
                ['te', 'て'],
                ['to', 'と'],
                ['na', 'な'],
                ['ni', 'に'],
                ['nu', 'ぬ'],
                ['ne', 'ね'],
                ['no', 'の'],
                ['ha', 'は'],
                ['hi', 'ひ'],
                ['hu', 'ふ'],
                ['he', 'へ'],
                ['ho', 'ほ'],
                ['ma', 'ま'],
                ['mi', 'み'],
                ['mu', 'む'],
                ['me', 'め'],
                ['mo', 'も'],
                ['ya', 'や'],
                
                ['yi', 'い'],
                
                ['yu', 'ゆ'],
                ['ye', 'いぇ'],
                ['yo', 'よ'],
                ['ra', 'ら'],
                ['ri', 'り'],
                ['ru', 'る'],
                ['re', 'れ'],
                ['ro', 'ろ'],
                ['wa', 'わ'],
                
                ['wi', 'ゐ'],
                
                ['wu', 'う'],
                
                ['we', 'ゑ'],
                
                ['wo', 'を'],
                ['ga', 'が'],
                ['gi', 'ぎ'],
                ['gu', 'ぐ'],
                ['ge', 'げ'],
                ['go', 'ご'],
                ['za', 'ざ'],
                ['zi', 'じ'],
                ['zu', 'ず'],
                ['ze', 'ぜ'],
                ['zo', 'ぞ'],
                ['da', 'だ'],
                ['di', 'ぢ'],
                ['du', 'づ'],
                ['de', 'で'],
                ['do', 'ど'],
                ['ba', 'ば'],
                ['bi', 'び'],
                ['bu', 'ぶ'],
                ['be', 'べ'],
                ['bo', 'ぼ'],
                ['pa', 'ぱ'],
                ['pi', 'ぴ'],
                ['pu', 'ぷ'],
                ['pe', 'ぺ'],
                ['po', 'ぽ'],
                ['fa', 'ふぁ'],
                ['fi', 'ふぃ'],
                ['fu', 'ふ'],
                ['fe', 'ふぇ'],
                ['fo', 'ふぉ'],
                ['ja', 'じゃ'],
                ['ji', 'じ'],
                ['ju', 'じゅ'],
                ['je', 'じぇ'],
                ['jo', 'じょ'],
                
                ['ca', 'か'],
                ['cu', 'く'],
                ['co', 'こ'],
                
                ['la', 'ら'],
                ['li', 'り'],
                ['lu', 'る'],
                ['le', 'れ'],
                ['lo', 'ろ'],
                
                ['va', 'う゛ぁ'],
                ['vi', 'う゛ぃ'],
                ['vu', 'う゛'],
                ['ve', 'う゛ぇ'],
                ['vo', 'う゛ぉ'],
                
                ['kya', 'きゃ'],
                ['kyi', 'きぃ'],
                ['kyu', 'きゅ'],
                ['kye', 'きぇ'],
                ['kyo', 'きょ'],
                ['gya', 'ぎゃ'],
                ['gyi', 'ぎぃ'],
                ['gyu', 'ぎゅ'],
                ['gye', 'ぎぇ'],
                ['gyo', 'ぎょ'],
                ['sya', 'しゃ'],
                ['syi', 'しぃ'],
                ['syu', 'しゅ'],
                ['sye', 'しぇ'],
                ['syo', 'しょ'],
                ['zya', 'じゃ'],
                ['zyi', 'じぃ'],
                ['zyu', 'じゅ'],
                ['zye', 'じぇ'],
                ['zyo', 'じょ'],
                
                ['jya', 'じゃ'],
                ['jyi', 'じぃ'],
                ['jyu', 'じゅ'],
                ['jye', 'じぇ'],
                ['jyo', 'じょ'],
                
                ['tya', 'ちゃ'],
                ['tyi', 'ちぃ'],
                ['tyu', 'ちゅ'],
                ['tye', 'ちぇ'],
                ['tyo', 'ちょ'],
                
                ['cya', 'ちゃ'],
                ['cyi', 'ちぃ'],
                ['cyu', 'ちゅ'],
                ['cye', 'ちぇ'],
                ['cyo', 'ちょ'],
                
                ['dya', 'ぢゃ'],
                ['dyi', 'ぢぃ'],
                ['dyu', 'ぢゅ'],
                ['dye', 'ぢぇ'],
                ['dyo', 'ぢょ'],
                ['nya', 'にゃ'],
                ['nyi', 'にぃ'],
                ['nyu', 'にゅ'],
                ['nye', 'にぇ'],
                ['nyo', 'にょ'],
                ['hya', 'ひゃ'],
                ['hyi', 'ひぃ'],
                ['hyu', 'ひゅ'],
                ['hye', 'ひぇ'],
                ['hyo', 'ひょ'],
                
                ['bya', 'びゃ'],
                ['byi', 'びぃ'],
                ['byu', 'びゅ'],
                ['bye', 'びぇ'],
                ['byo', 'びょ'],
                ['pya', 'ぴゃ'],
                ['pyi', 'ぴぃ'],
                ['pyu', 'ぴゅ'],
                ['pye', 'ぴぇ'],
                ['pyo', 'ぴょ'],
                ['mya', 'みゃ'],
                ['myi', 'みぃ'],
                ['myu', 'みゅ'],
                ['mye', 'みぇ'],
                ['myo', 'みょ'],
                ['rya', 'りゃ'],
                ['ryi', 'りぃ'],
                ['ryu', 'りゅ'],
                ['rye', 'りぇ'],
                ['ryo', 'りょ'],
                ['tsa', 'つぁ '],
                ['tsi', 'つぃ'],
                ['tsu', 'つ'],
                ['tse', 'つぇ'],
                ['tso', 'つぉ'],
                
                ['lya', 'りゃ'],
                ['lyi', 'りぃ'],
                ['lyu', 'りゅ'],
                ['lye', 'りぇ'],
                ['lyo', 'りょ'],
                
                ['sha', 'しゃ'],
                ['shi', 'し'],
                ['shu', 'しゅ'],
                ['she', 'しぇ'],
                ['sho', 'しょ'],
                
                ['tha', 'てゃ'],
                ['thi', 'てぃ'],
                ['thu', 'てゅ'],
                ['the', 'てぇ'],
                ['tho', 'てょ'],
                
                
                ['dha', 'でゃ'],
                ['dhi', 'でぃ'],
                ['dhu', 'でゅ'],
                ['dhe', 'でぇ'],
                ['dho', 'でょ'],
                
                ['cha', 'ちゃ'],
                ['chi', 'ち'],
                ['chu', 'ちゅ'],
                ['che', 'ちぇ'],
                ['cho', 'ちょ'],
                
                ['gwa', 'ぐぁ'],
                ['gwi', 'ぐぃ'],
                ['gwu', 'ぐぅ'],
                ['gwe', 'ぐぇ'],
                ['gwo', 'ぐぉ'],
                
                ['xa', 'ぁ'],
                ['xi', 'ぃ'],
                ['xu', 'ぅ'],
                ['xe', 'ぇ'],
                ['xo', 'ぉ'],
                ['xwa', 'ゎ'],
                ['xtu', 'っ'],
                ['xtsu', 'っ'],
                ['xya', 'ゃ'],
                ['xyu', 'ゅ'],
                ['xyo', 'ょ'],
                
                ['n', 'ん'],
                ['n\\x27', 'ん'],
                ['mn', 'ん'],
                ['nn', 'ん'],
                
                ['kk', ['っ', 'k']],
                ['ss', ['っ', 's']],
                ['tt', ['っ', 't']],
                ['hh', ['っ', 'h']],
                ['mm', ['っ', 'm']],
                ['yy', ['っ', 'y']],
                ['rr', ['っ', 'r']],
                ['ww', ['っ', 'w']],
                ['gg', ['っ', 'g']],
                ['zz', ['っ', 'z']],
                ['dd', ['っ', 'd']],
                ['bb', ['っ', 'b']],
                ['pp', ['っ', 'p']],
                ['cc', ['っ', 'c']],
                ['ff', ['っ', 'f']],
                ['jj', ['っ', 'j']],
                ['qq', ['っ', 'q']],
                ['vv', ['っ', 'v']],
                ['tch', ['っ', 'ch']],
                
                [" ", "　"],
                [",", "、"],
                [".", "。"],
                ["!", "！"],
                ["\"", "\\u201d"],
                ["#", "＃"],
                ["$", "＄"],
                ["%", "％"],
                ["&", "＆"],
                ["'", "\\u2019"],
                ["(", "（"],
                [")", "）"],
                ["~", "\\uff5e"],
                ["-", "ー"],
                ["=", "＝"],
                ["^", "＾"],
                ["\\", "＼"],
                ["|", "｜"],
                ["`", "\\u2018"],
                ["@", "＠"],
                ["{", "｛"],
                ["[", "「"],
                ["+", "＋"],
                [";", "；"],
                ["*", "＊"],
                [":", "："],
                ["}", "｝"],
                ["]", "」"],
                ["<", "＜"],
                [">", "＞"],
                ["?", "？"],
                ["/", "／"],
                ["_", "＿"],
                ["¥", "￥"],
                
                ['0', '０'],
                ['1', '１'],
                ['2', '２'],
                ['3', '３'],
                ['4', '４'],
                ['5', '５'],
                ['6', '６'],
                ['7', '７'],
                ['8', '８'],
                ['9', '９']]
    
    DRomaji = {}
    DHira = {}
    for romaji, hira in LRomHira:
        do_subst = False
        if type(hira) == ListType:
            do_subst = True
            hira, subst = hira
            subst = subst.decode('utf-8')
        
        hira = hira.decode('utf-8')
        romaji = romaji.decode('utf-8')
        if hira not in DHira:
            #if do_subst: DHira[hira] = {'romaji': romaji, 'subst': subst}
            #else: DHira[hira] = {'romaji': romaji}
            DHira[hira] = romaji
        
        if do_subst: 
            DRomaji[romaji] = {'hira': hira, 
                               'subst': subst}
        else: 
            DRomaji[romaji] = {'hira': hira}
    return DHira, DRomaji

def get_okuri_ari(lHira):
    hira, romaji = get_rom_hira()
    LRtn = [hira[i]['romaji'][0] for i in hira if i[0] == lHira]
    return LRtn

class RomajiConv:
    def __init__(self): 
        self.DHira, self.DRomaji = get_rom_hira()
        
    def len(self, s):
        '''
        If greater than three, reduce as the maximum 
        length for Kana conversions is 3 to improve speed :-)
        '''
        len_conv_this = len(s)
        if len_conv_this > 3: 
            len_conv_this = 3
        return len_conv_this
        
    def romaji_to_hiragana(self, s):
        l_s = self.len(s)
        
        LRtn = []
        while s:
            while l_s:
                search_for_rom = s[0:l_s]
                if search_for_rom in self.DRomaji:
                    LRtn.append([search_for_rom, self.DRomaji[search_for_rom]['hira']])
                    
                    do_subst = False
                    if 'subst' in self.DRomaji[search_for_rom]:
                        do_subst = True
                        subst = self.DRomaji[search_for_rom]['subst']
                    
                    s = s[l_s:]
                    if do_subst: 
                        s = subst+s 
                    l_s = self.len(s)
                else:
                    l_s -= 1
            
            if self.len(s) > 0:
                LRtn.append([s[0], s[0]])
                s = s[1:]
                l_s = self.len(s)
        
        return LRtn

# Init Japanese Hiragana
inst = RomajiConv()
romaji_to_hira = inst.romaji_to_hiragana

if __name__ == '__main__':
    print((hira_to_romaji('ひらがな').encode('utf-8')))
    print((kata_to_romaji('カタカナ').encode('utf-8')))
    
    from toolkit.misc.Timer import Timer
    t = Timer()
    for i in range(1000000):
        kana_to_latin('gfgㄴひらがなカタカナ')
    print(("Time:", t))
