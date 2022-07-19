# -*- coding: utf-8 -*-

DATA = '''ゟ	ゟ	ゟ	
぀	぀	぀	
ゕ	ゕ	ゕ	
ゖ	ゖ	ゖ	
゗	゗	゗	
゘	゘	゘	
゙	゙	゙	
゛	゛	ﾞ	
゚	゚	゚	
゜	゜	ﾟ	
ぁ	ァ	ｧ	
あ	ア	ｱ	㋐
ぃ	ィ	ｨ	
い	イ	ｲ	㋑
ぅ	ゥ	ｩ	
う	ウ	ｳ	㋒
ゔ	ヴ	ｳﾞ	
ぇ	ェ	ｪ	
え	エ	ｴ	㋓
ぉ	ォ	ｫ	
お	オ	ｵ	㋔
か	カ	ｶ	㋕
が	ガ	ｶﾞ	
き	キ	ｷ	㋖
ぎ	ギ	ｷﾞ	
く	ク	ｸ	㋗
ぐ	グ	ｸﾞ	
け	ケ	ｹ	㋘
げ	ゲ	ｹﾞ	
こ	コ	ｺ	㋙
ご	ゴ	ｺﾞ	
さ	サ	ｻ	㋚
ざ	ザ	ｻﾞ	
し	シ	ｼ	㋛
じ	ジ	ｼﾞ	
す	ス	ｽ	㋜
ず	ズ	ｽﾞ	
せ	セ	ｾ	㋝
ぜ	ゼ	ｾﾞ	
そ	ソ	ｿ	㋞
ぞ	ゾ	ｿﾞ	
た	タ	ﾀ	㋟
だ	ダ	ﾀﾞ	
ち	チ	ﾁ	㋠
ぢ	ヂ	ﾁﾞ	
っ	ッ	ｯ	
つ	ツ	ﾂ	㋡
づ	ヅ	ﾂﾞ	
て	テ	ﾃ	㋢
で	デ	ﾃﾞ	
と	ト	ﾄ	㋣
ど	ド	ﾄﾞ	
な	ナ	ﾅ	㋤
に	ニ	ﾆ	㋥
ぬ	ヌ	ﾇ	㋦
ね	ネ	ﾈ	㋧
の	ノ	ﾉ	㋨
は	ハ	ﾊ	㋩
ば	バ	ﾊﾞ	
ぱ	パ	ﾊﾟ	
ひ	ヒ	ﾋ	㋪
び	ビ	ﾋﾞ	
ぴ	ピ	ﾋﾟ	
ふ	フ	ﾌ	㋫
ぶ	ブ	ﾌﾞ	
ぷ	プ	ﾌﾟ	
へ	ヘ	ﾍ	㋬
べ	ベ	ﾍﾞ	
ぺ	ペ	ﾍﾟ	
ほ	ホ	ﾎ	㋭
ぼ	ボ	ﾎﾞ	
ぽ	ポ	ﾎﾟ	
ま	マ	ﾏ	㋮
み	ミ	ﾐ	㋯
む	ム	ﾑ	㋰
め	メ	ﾒ	㋱
も	モ	ﾓ	㋲
ゃ	ャ	ｬ	
や	ヤ	ﾔ	㋳
ゅ	ュ	ｭ	
ゆ	ユ	ﾕ	㋴
ょ	ョ	ｮ	
よ	ヨ	ﾖ	㋵
ら	ラ	ﾗ	㋶
り	リ	ﾘ	㋷
る	ル	ﾙ	㋸
れ	レ	ﾚ	㋹
ろ	ロ	ﾛ	㋺
わ	ワ	ﾜ	㋻
ゎ	ヮ	ヮ	
ゐ	ヰ	ヰ	㋼
ゑ	ヱ	ヱ	㋽
を	ヲ	ｦ	㋾
ん	ン	ﾝ	
ゝ	ヽ	ヽ	
ゞ	ヾ	ヾ	'''


DHiraToKata = {}
DKataToHira = {}
DKataToHalfwidth = {}
DKataToFullwidth = {}
DCKataToKata = {}

for Line in DATA.split('\n'):
    Hira, fKata, hKata, cKata = Line.split('\t')
    DHiraToKata[Hira] = fKata # Fullwidth->Kata
    DKataToHira[fKata] = Hira # Fullwidth->Hira
    DKataToHalfwidth[fKata] = hKata # Half->Full
    DKataToFullwidth[hKata] = fKata # Full->Half
    DCKataToKata[cKata] = fKata


def hira_to_kata(S):
    """
    Converts Hiragana to fullwidth Katakana
    """
    L = []
    for c in S:
        if c in DHiraToKata: 
            c = DHiraToKata[c]
        L.append(c)
    return ''.join(L)


def kata_to_hira(S):
    """
    Converts Katakana to Hiragana, converting Katakana to 
    fullwidth and converting circled characters to normal
    """
    L = []
    for c in S:
        if c in DKataToFullwidth: 
            c = DKataToFullwidth[c]
        
        if c in DCKataToKata: 
            c = DCKataToKata[c]
        
        if c in DKataToHira: 
            c = DKataToHira[c]
        L.append(c)
    return ''.join(L)


def round_kata_to_hira(S):
    """
    Converts Katakana characters enclosed in circles to normal characters
    """
    L = []
    for c in S:
        if c in DCKataToKata: 
            c = DCKataToKata[c]
        L.append(c)
    return ''.join(L)


def full_kata_to_half(S):
    """
    Converts Katakana to halfwidth from fullwidth
    """
    L = []
    for c in S:
        if c in DKataToHalfwidth: 
            c = DKataToHalfwidth[c]
        L.append(c)
    return ''.join(L)
