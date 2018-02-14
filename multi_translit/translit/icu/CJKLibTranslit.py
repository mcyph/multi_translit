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
    ('cmn_Latn|Gwoyeu Romatzyh', 'cmn_Latn|x-Pinyin'): lambda s: f.convert(s, 'GR', 'Pinyin'),
    ('cmn_Latn|Gwoyeu Romatzyh', 'cmn_Latn|Wade-Giles'): lambda s: f.convert(s, 'GR', 'WadeGiles'),
    ('cmn_Latn|Gwoyeu Romatzyh', 'cmn_Latn|Braille'): lambda s: f.convert(s, 'GR', 'MandarinBraille'),
    ('cmn_Latn|Gwoyeu Romatzyh', 'cmn_Latn|Alternative IPA'): lambda s: f.convert(s, 'GR', 'MandarinIPA'),


    ('cmn_Latn|Numeric Pinyin', 'cmn_Latn|x-Pinyin'): lambda s: f.convert(s, 'Pinyin', 'Pinyin', sourceOptions={
        'toneMarkType': 'numbers'
    }),
    ('cmn_Latn|Numeric Pinyin', 'cmn_Latn|Gwoyeu Romatzyh'): lambda s: f.convert(s, 'Pinyin', 'GR', sourceOptions={
        'toneMarkType': 'numbers'
    }),
    ('cmn_Latn|Numeric Pinyin', 'cmn_Latn|Wade-Giles'): lambda s: f.convert(s, 'Pinyin', 'WadeGiles', sourceOptions={
        'toneMarkType': 'numbers'
    }),
    ('cmn_Latn|Numeric Pinyin', 'cmn_Latn|Braille'): lambda s: f.convert(s, 'Pinyin', 'MandarinBraille', sourceOptions={
        'toneMarkType': 'numbers'
    }),
    ('cmn_Latn|Numeric Pinyin', 'cmn_Latn|Alternative IPA'): lambda s: f.convert(s, 'Pinyin', 'MandarinIPA', sourceOptions={
        'toneMarkType': 'numbers'
    }),


    ('cmn_Latn|x-Pinyin', 'cmn_Latn|Gwoyeu Romatzyh'): lambda s: f.convert(s, 'Pinyin', 'GR'),
    ('cmn_Latn|x-Pinyin', 'cmn_Latn|Wade-Giles'): lambda s: f.convert(s, 'Pinyin', 'WadeGiles'),
    ('cmn_Latn|x-Pinyin', 'cmn_Latn|Braille'): lambda s: f.convert(s, 'Pinyin', 'MandarinBraille'),
    ('cmn_Latn|x-Pinyin', 'cmn_Latn|Alternative IPA'): lambda s: f.convert(s, 'Pinyin', 'MandarinIPA'),


    ('cmn_Latn|Wade-Giles', 'cmn_Latn|Gwoyeu Romatzyh'): lambda s: f.convert(s, 'WadeGiles', 'GR'),
    ('cmn_Latn|Wade-Giles', 'cmn_Latn|x-Pinyin'): lambda s: f.convert(s, 'WadeGiles', 'Pinyin'),
    ('cmn_Latn|Wade-Giles', 'cmn_Latn|Braille'): lambda s: f.convert(s, 'WadeGiles', 'MandarinBraille'),
    ('cmn_Latn|Wade-Giles', 'cmn_Latn|Alternative IPA'): lambda s: f.convert(s, 'WadeGiles', 'MandarinIPA'),


    #('cmn_Latn|Braille', 'cmn_Latn|Gwoyeu Romatzyh'): lambda s: f.convert(s, 'MandarinBraille', 'GR'),
    #('cmn_Latn|Braille', 'cmn_Latn|x-Pinyin'): lambda s: f.convert(s, 'MandarinBraille', 'Pinyin'),
    #('cmn_Latn|Braille', 'cmn_Latn|Wade-Giles'): lambda s: f.convert(s, 'MandarinBraille', 'WadeGiles'),
    #('cmn_Latn|Braille', 'cmn_Latn|Alternative IPA'): lambda s: f.convert(s, 'MandarinBraille', 'MandarinIPA'),


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
            if from_iso != 'cmn_Latn|Numeric Pinyin':
                s = DConv['cmn_Latn|Numeric Pinyin', from_iso]('tou1')
            else:
                s = 'tou1'
        else:
            s = 'jiang5'

        print from_iso, to_iso, s
        print DConv[from_iso, to_iso](s)
        print
