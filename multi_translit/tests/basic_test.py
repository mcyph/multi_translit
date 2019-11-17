from multi_translit.MultiTranslit import MultiTranslit
from multi_translit.translit.korean import SKoTypes

if __name__ == '__main__':
    multi_translit = MultiTranslit()

    from pprint import pprint
    pprint(multi_translit.DEngines)
    #raise

    #print 'BEST CONVERSION:', Translit.get_best_conversion('ja_Jpan-AU|VARIANT', 'ja_Latn')
    #print 'BEST CONVERSION:', Translit.get_best_conversion('ja_Jpan-AU', 'ja_Latn')

    #print Translit.translit('Latn', 'ja_Kana', 'nihongo')

    print(multi_translit.translit('ja', 'ja_Latn|FONIPA', 'aa'))

    txt = '私はボブ。日本語で書きますよ！どうしてそんなことを言うの？'
    print(multi_translit.translit('ja', 'ja_Kana', txt))
    print(multi_translit.translit('ja', 'ja_Hira', txt))
    print(multi_translit.translit('ja', 'Latn', txt))

    print([i for i in multi_translit.DEngines if 'ja' in i[0]])

    txt = '''(sŏ-ul=yŏn-hap-nyu-sŭ) i-chun-sŏ ki-cha = 4ㆍ11 ch'ong-sŏn kong-ch'ŏn tang-si'''
    txt_ko = '(서울=연합뉴스) 이준서 기자 = 4ㆍ11 총선 공천 당시'

    for system in SKoTypes:
        latin = multi_translit.translit('ko', 'ko_Latn|%s' % system, txt_ko)
        print(latin)
        print(multi_translit.translit('ko_Latn|%s' % system, 'ko_Hang', latin))
