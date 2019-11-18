from toolkit.patterns.Singleton import Singleton
from multi_translit.abstract_base_classes.MultiTranslitBase import MultiTranslitBase
from network_tools.posix_shm_sockets.SHMClient import SHMClient
from network_tools.mmap_sockets.MMapClient import MMapClient


class MultiTranslitClient(MultiTranslitBase,
                          Singleton,
                          ):
    def __init__(self):
        self.client = SHMClient(port=40552)

    def get_D_scripts(self):
        return self.client.send_json('get_D_scripts', [])

    def get_L_possible_conversions(self, from_, remove_variant=False):
        return self.client.send_json(
            'get_L_possible_conversions',
            [from_, remove_variant]
        )

    def get_best_conversion(self, from_iso, to_iso, default=KeyError):
        return self.client.send_json(
            'get_best_conversion',
            [
                from_iso,
                to_iso,
                (
                    '$ERROR$'
                    if default == KeyError
                    else default
                )
            ]
        )

    def get_L_best_conversions(self, from_iso, to_iso):
        return self.client.send_json(
            'get_L_best_conversions',
            [from_iso, to_iso]
        )

    def get_all_transliterations(self, from_, s):
        return self.client.send_json(
            'get_all_transliterations',
            [from_, s]
        )

    def translit(self, from_, to, s):
        #print("TRANSLIT", from_, to, s, self.client.send_json(
        #    'translit',
        #    [from_, to, s]
        #))
        #raise Exception()
        return self.client.send_json(
            'translit',
            [from_, to, s]
        )

    def get_D_script_headings(self):
        return self.client.send_json(
            'get_D_script_headings', []
        )


#MultiTranslit = MultiTranslitClient()
#translit = MultiTranslit.translit
#get_D_scripts = MultiTranslit.get_D_scripts
#get_D_script_headings = MultiTranslit.get_D_script_headings
#get_L_possible_conversions = MultiTranslit.get_L_possible_conversions


if __name__ == '__main__':
    import time
    from toolkit.benchmarking.benchmark import benchmark

    if True:
        c = MultiTranslitClient()
    else:
        from multi_translit.MultiTranslit import MultiTranslit
        c = MultiTranslit()

    #@benchmark(restrictions=(30,))
    def run():
        _c = c
        t_from = time.time()
        for x in range(10000):
            _c.translit('ja', 'ja_Hira', '政府、結論ありきの大嘗祭　憲法論争避け前例踏襲〔深層探訪〕'*5)
        print(time.time()-t_from)
    run()
