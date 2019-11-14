from network_tools.posix_shm_sockets.SHMServer import SHMServer, json_method
from multi_translit.MultiTranslit import MultiTranslit


class MultiTranslitServer(SHMServer):
    def __init__(self):
        SHMServer.__init__(self, DCmds={
            'get_D_scripts': self.get_D_scripts,
            'get_L_possible_conversions': self.get_L_possible_conversions,
            'get_best_conversion': self.get_best_conversion,
            'get_L_best_conversions': self.get_L_best_conversions,
            'get_L_all_conversions': self.get_L_all_conversions,
            'translit': self.translit,
            'get_D_script_headings': self.get_D_script_headings
        }, port=40552)

    @json_method
    def get_D_scripts(self):
        return MultiTranslit.get_D_scripts()

    @json_method
    def get_L_possible_conversions(self, from_, remove_variant=False):
        return MultiTranslit.get_D_scripts(from_, remove_variant)

    @json_method
    def get_best_conversion(self, from_iso, to_iso, default=KeyError):
        if default == '$ERROR$':
            default = KeyError
        return MultiTranslit.get_best_conversion(
            from_iso, to_iso, default
        )

    @json_method
    def get_L_best_conversions(self, from_iso, to_iso):
        return MultiTranslit.get_L_best_conversions(from_iso, to_iso)

    @json_method
    def get_L_all_conversions(self, from_, s):
        return MultiTranslit.get_L_all_conversions(from_, s)

    @json_method
    def translit(self, from_, to, s):
        return MultiTranslit.translit(from_, to, s)

    @json_method
    def get_D_script_headings(self):
        from multi_translit.translit.get_D_script_headings import get_D_script_headings
        return get_D_script_headings()

