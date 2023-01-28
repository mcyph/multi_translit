from cjklib.reading import ReadingFactory

f = ReadingFactory()


[
    'GR', 'Pinyin', 'WadeGiles', 'MandarinBraille', 'MandarinIPA',
    'ShanghaineseIPA',
    #'Hangul',
    #'Kana', 'Hiragana', 'Katakana',
    'CantoneseYale', 'CantoneseIPA', 'Jyutping'
]


DConv = {
    # Mandarin conversions
    ('zh-Latn|x-GwoyeuRomatzyh', 'zh-Latn-x-Pinyin'): lambda s: f.convert(s, 'GR', 'Pinyin'),
    ('zh-Latn|x-GwoyeuRomatzyh', 'zh-Latn|Wade-Giles'): lambda s: f.convert(s, 'GR', 'WadeGiles'),
    ('zh-Latn|x-GwoyeuRomatzyh', 'zh-Latn|Braille'): lambda s: f.convert(s, 'GR', 'MandarinBraille'),
    ('zh-Latn|x-GwoyeuRomatzyh', 'zh-Latn|Alternative IPA'): lambda s: f.convert(s, 'GR', 'MandarinIPA'),


    ('zh-Latn-x-NumericPinyin', 'zh-Latn-x-Pinyin'): lambda s: f.convert(s, 'Pinyin', 'Pinyin', sourceOptions={
        'toneMarkType': 'numbers'
    }),
    ('zh-Latn-x-NumericPinyin', 'zh-Latn|x-GwoyeuRomatzyh'): lambda s: f.convert(s, 'Pinyin', 'GR', sourceOptions={
        'toneMarkType': 'numbers'
    }),
    ('zh-Latn-x-NumericPinyin', 'zh-Latn|Wade-Giles'): lambda s: f.convert(s, 'Pinyin', 'WadeGiles', sourceOptions={
        'toneMarkType': 'numbers'
    }),
    ('zh-Latn-x-NumericPinyin', 'zh-Latn|Braille'): lambda s: f.convert(s, 'Pinyin', 'MandarinBraille', sourceOptions={
        'toneMarkType': 'numbers'
    }),
    ('zh-Latn-x-NumericPinyin', 'zh-Latn|Alternative IPA'): lambda s: f.convert(s, 'Pinyin', 'MandarinIPA', sourceOptions={
        'toneMarkType': 'numbers'
    }),


    ('zh-Latn-x-Pinyin', 'zh-Latn|x-GwoyeuRomatzyh'): lambda s: f.convert(s, 'Pinyin', 'GR'),
    ('zh-Latn-x-Pinyin', 'zh-Latn|Wade-Giles'): lambda s: f.convert(s, 'Pinyin', 'WadeGiles'),
    ('zh-Latn-x-Pinyin', 'zh-Latn|Braille'): lambda s: f.convert(s, 'Pinyin', 'MandarinBraille'),
    ('zh-Latn-x-Pinyin', 'zh-Latn|Alternative IPA'): lambda s: f.convert(s, 'Pinyin', 'MandarinIPA'),


    ('zh-Latn|Wade-Giles', 'zh-Latn|x-GwoyeuRomatzyh'): lambda s: f.convert(s, 'WadeGiles', 'GR'),
    ('zh-Latn|Wade-Giles', 'zh-Latn-x-Pinyin'): lambda s: f.convert(s, 'WadeGiles', 'Pinyin'),
    ('zh-Latn|Wade-Giles', 'zh-Latn|Braille'): lambda s: f.convert(s, 'WadeGiles', 'MandarinBraille'),
    ('zh-Latn|Wade-Giles', 'zh-Latn|Alternative IPA'): lambda s: f.convert(s, 'WadeGiles', 'MandarinIPA'),


    #('zh-Latn|Braille', 'zh-Latn|x-GwoyeuRomatzyh'): lambda s: f.convert(s, 'MandarinBraille', 'GR'),
    #('zh-Latn|Braille', 'zh-Latn-x-Pinyin'): lambda s: f.convert(s, 'MandarinBraille', 'Pinyin'),
    #('zh-Latn|Braille', 'zh-Latn|Wade-Giles'): lambda s: f.convert(s, 'MandarinBraille', 'WadeGiles'),
    #('zh-Latn|Braille', 'zh-Latn|Alternative IPA'): lambda s: f.convert(s, 'MandarinBraille', 'MandarinIPA'),


    # Cantonese conversions
    ('yue_Latn|Yale', 'yue_Latn|CantoneseIPA'): lambda s: f.convert(s, 'CantoneseIPA', 'CantoneseIPA'),
    ('yue_Latn|Yale', 'yue_Latn|Jyutping'): lambda s: f.convert(s, 'CantoneseYale', 'Jyutping'),

    ('yue_Latn|Jyutping', 'yue_Latn|CantoneseIPA'): lambda s: f.convert(s, 'CantoneseIPA', 'CantoneseIPA'),
    ('yue_Latn|Jyutping', 'yue_Latn|Yale'): lambda s: f.convert(s, 'Jyutping', 'CantoneseYale'),


    # Shanghainese conversions
    ('wuu_Latn', 'wuu_Latn|x-IPA'): lambda s: f.convert(s, 'Jyutping', 'CantoneseYale')
}



if __name__ == '__main__':
    for (from_iso, to_iso) in sorted(DConv):

        if from_iso.startswith('cmn'):
            if from_iso != 'zh-Latn-x-NumericPinyin':
                s = DConv['zh-Latn-x-NumericPinyin', from_iso]('tou1')
            else:
                s = 'tou1'
        else:
            s = 'jiang5'

        print(from_iso, to_iso, s)
        print(DConv[from_iso, to_iso](s))
        print()
