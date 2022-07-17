from speedysvc.service_method import service_method
from speedysvc.client_server.base_classes.ServerMethodsBase import ServerMethodsBase

from multi_translit.MultiTranslit import MultiTranslit


class MultiTranslitServer:
    def __init__(self):
        self.multi_translit = MultiTranslit()

    @service_method()
    def get_scripts_dict(self):
        return self.multi_translit.get_scripts_dict()

    @service_method()
    def get_possible_conversions_list(self, from_, remove_variant=False):
        return self.multi_translit.get_possible_conversions_list(from_, remove_variant)

    @service_method()
    def get_best_conversion(self, from_iso, to_iso, default='$ERROR$'):
        if default == '$ERROR$':
            default = KeyError
        return self.multi_translit.get_best_conversion(from_iso, to_iso, default)

    @service_method()
    def get_best_conversions_list(self, from_iso, to_iso):
        return self.multi_translit.get_best_conversions_list(from_iso, to_iso)

    @service_method()
    def get_all_transliterations(self, from_, s):
        return self.multi_translit.get_all_transliterations(from_, s)

    @service_method()
    def translit(self, from_, to, s):
        return self.multi_translit.translit(from_, to, s)

    @service_method()
    def get_script_headings_dict(self):
        from multi_translit.translit.get_script_headings_dict import get_script_headings_dict
        return get_script_headings_dict()


if __name__ == '__main__':
    import time
    s = MultiTranslitServer()
    while True:
        time.sleep(1)
