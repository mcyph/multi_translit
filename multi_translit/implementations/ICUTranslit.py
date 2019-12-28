from multi_translit.toolkit.json_tools import load
from multi_translit.data_paths import data_path
from multi_translit.abstract_base_classes.TranslitEngineBase import TranslitEngineBase
from iso_tools.ISOTools import ISOTools


class ICUTranslit(TranslitEngineBase):
    def __init__(self):
        """
        Create an International Components for Unicode (ICU)
        transliteration engine
        """
        TranslitEngineBase.__init__(self)
        self.DICU = {}  # CHECK ME - IS THIS THREADSAFE? =================================================

    def _mapping_to_iso(self, part3, script=None, variant=None, other=None):
        if other:
            if not part3 and other[0] and other[0] != 'ben':
                part3 = other[0]

        r = ISOTools.join(part3, script, variant=variant)

        DMap = {
          'zh_Hani': 'zh',
          'Hani': 'zh',
          'ja_Zyyy': 'ja_Hrkt',
          'zh_Bopo|Zhuyin': 'zh_Bopo',
          'Bopo': 'zh_Bopo',
          'zh_Latn': 'zh_Latn|x-Pinyin'
        }

        if r in DMap:
            r = DMap[r]
        return r

    def _remove_invalid(self):
        from PyICU import ICUError

        for from_key, to_key in list(self.DEngines.keys()):
            # Remove invalid engines (somewhat hackish, but oh well...)
            try:
                self.translit(from_key, to_key, 'a')
            except ICUError:
                del self.DEngines[from_key, to_key]

    def get_D_engines(self):
        from PyICU import Transliterator, UTransDirection, ICUError
        D = {}

        DMappings = load(data_path('translit', 'script_mappings.json'))
        LUnknownScripts = []

        for engine in Transliterator.getAvailableIDs():
            # print engine
            from_, _, to = engine.partition('-')
            to = to.replace('/', '-')

            try:
                from_key = self._mapping_to_iso(*DMappings[from_], other=DMappings[to])
            except KeyError as e:
                LUnknownScripts.append('%s-%s' % (from_, to))
                continue

            try:
                to_key = self._mapping_to_iso(*DMappings[to], other=DMappings[from_])
            except KeyError as e:
                LUnknownScripts.append('%s-%s' % (to, from_))
                continue

            SIgnore = {
                'ko_Zyyy',
                'th_Zyyy',
                'el_Zyyy',
                'cs_Zyyy',
                'es_Zyyy',
                'ko_Zyyy',
                'zh_Zyyy',
                'ar_Zyyy',
                'he_Zyyy',
                'syr_Zyyy',
                'hy_Zyyy',
                'ka_Zyyy',
                'pl_Zyyy',
                'ro_Zyyy',
                'ru_Zyyy',
                'am_Zyyy',  # TODO: Add latin -> amharic
                'sk_Zyyy'
            }

            if from_key in SIgnore or to_key in SIgnore:
                continue

            D[from_key, to_key] = (
                engine, UTransDirection.FORWARD
            )

            if not (to_key, from_key) in D:
                if 'Zyyy' in from_key and not 'Zyyy' in str(to_key):
                    # print('IGNORED:', from_key, to_key)
                    # HACK: Disable "to common"
                    continue

                D[to_key, from_key] = (
                    engine, UTransDirection.REVERSE
                )

        if LUnknownScripts:
            from warnings import warn
            warn(
                "Scripts in ICU not recognised by multi_translit engine: %s"
                % ', '.join(LUnknownScripts)
            )
        return D

    def translit(self, from_, to, s):
        params = self.DEngines[from_, to]
        if not params in self.DICU:
            from PyICU import Transliterator
            self.DICU[params] = Transliterator.createInstance(*params)

        return self.DICU[params].transliterate(s)
