from multi_translit.data_paths import data_path
from multi_translit.utils.get_translit_mappings_dict import get_D_translit_mappings
from multi_translit.implementations.my_translit.TranslitEngine import TranslitEngine
from multi_translit.implementations.TranslitEngineBase import TranslitEngineBase

from iso_tools.bcp47.get_tag_details import get_tag_details


class MyTranslit(TranslitEngineBase):
    def __init__(self):
        """
        The (simple, naive) transliteration engine made by me
        it has basic lookahead/lookbehind assertions, but unlike
        the ICU engine has little internal state.

        This should make the files easy to read
        (the syntax resembles python's), but it's hard to add
        complex exceptions in many scripts.
        """
        self.DTranslitMappings = get_D_translit_mappings()
        TranslitEngineBase.__init__(self)

    def get_D_engines(self):
        # Add internal python transliterators
        # print DTranslitMappings
        D = {}
        with open(data_path('translit', 'ignored_isos.txt'), 'r') as f:
            # HACK: Ignore these (mostly fairly uncommonly used) transliteration systems
            # as they probably have errors/I don't have much time to maintain them
            SIgnoredISOs = set(i for i in f.read().split('\n'))

        for from_iso, L in list(self.DTranslitMappings.items()):
            for path, to_iso, direction in L:
                print(path, to_iso, direction)
                if get_tag_details(from_iso).language in SIgnoredISOs:
                    continue
                elif get_tag_details(to_iso).language in SIgnoredISOs:
                    continue

                D[from_iso, to_iso] = (path, direction)
        return D

    def translit(self, from_: str, to: str, s: str):
        params = self.DEngines[from_, to]
        te = TranslitEngine(data_path('translit_new', params[0]), params[1])
        return te.convert(s)
