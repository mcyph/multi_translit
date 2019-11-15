from multi_translit.abstract_base_classes.TranslitEngineBase import TranslitEngineBase


class MecabTranslit(TranslitEngineBase):
    def __init__(self, multi_translit):
        """
        A Japanese transliterator using the
        Mecab morphological analyser.

        :param multi_translit: the MultiTranslit instance
        """
        self.multi_translit = multi_translit
        TranslitEngineBase.__init__(self)

    def get_D_engines(self):
        # Add Japanese internal conversions
        D = {}
        D['ja', 'ja_Hira'] = ('ja_Kana', 'ja_Hira', False)
        D['ja', 'ja_Kana'] = (None, None, False)  # Already Katakana!
        D['ja', 'Latn'] = ('ja_Kana', 'ja_Latn', True)
        return D

    def translit(self, from_, to, s):
        try:
            global to_katakana
            to_katakana
        except:
            from mecab.word_boundaries import to_katakana

        params = self.DEngines[from_, to]
        r = to_katakana(s, wa_hack=params[2])
        if params[0]:
            r = self.multi_translit.translit(params[0], params[1], r)
        return str(r)
