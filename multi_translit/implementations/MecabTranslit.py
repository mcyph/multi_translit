from multi_translit.abstract_base_classes.TranslitEngineBase import TranslitEngineBase
from mecab.word_boundaries.WordBoundaries import WordBoundaries


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
        D['ja', 'ja-Hira'] = ('ja-Kana', 'ja-Hira', False)
        D['ja', 'ja-Kana'] = (None, None, False)  # Already Katakana!
        D['ja', 'Latn'] = ('ja-Kana', 'ja_Latn', True)
        return D

    def translit(self, from_, to, s):
        if not hasattr(self, 'word_boundaries'):
            self.word_boundaries = WordBoundaries(self.multi_translit)

        params = self.DEngines[from_, to]
        r = self.word_boundaries.to_katakana(s, wa_hack=params[2])
        if params[0]:
            r = self.multi_translit.translit(params[0], params[1], r)
        return str(r)
