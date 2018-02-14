import platform

try:
    from ICUTranslit import translit, get_D_scripts, Translit
except ImportError:
    from network_tools.remote_objects.client import import_
    translit = import_('from multi_translit.translit.icu.ICUTranslit import translit')
    get_D_scripts = import_('from multi_translit.translit.icu.ICUTranslit import get_D_scripts')
    Translit = import_('from multi_translit.translit.icu.ICUTranslit import Translit')
