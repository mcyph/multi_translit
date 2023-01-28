import os
from multi_translit.data_paths import data_path


def iter_translit_files(old_ver=False):
    folder = data_path('translit_old' if old_ver else 'translit_new')

    for root, dirs, files in os.walk(folder):
        if '.svn' in root:
            continue
        
        for fnam in files:
            if fnam.endswith('.trn'):
                #if not 'Yi.' in fnam:
                #    continue
                yield '%s/%s' % (root, fnam)


if __name__ == '__main__':
    import json
    from traceback import print_exc
    from multi_translit.implementations.my_translit.TranslitEngine import TranslitEngine
    from iso_tools.bcp47.make_preferred_form import make_preferred_form

    DTranslit = {}

    for path in iter_translit_files():
        for direction in ('=>', '<='):
            try:
                t = TranslitEngine(path, direction)
                print('OK:', t.from_iso, t.to_iso, t.direction)
                DTranslit.setdefault(make_preferred_form(t.from_iso), []).append((
                    path.replace(
                        data_path('translit_new').strip('/\\'),
                        ''
                    ).strip('/\\'),

                    make_preferred_form(t.to_iso),
                    t.direction
                ))
            except:
                print('ERROR:', direction, path)
                print_exc()

    with open(
        data_path('translit_new', 'translit-mappings.json'),
        'w', encoding='utf-8'
    ) as f:
        d = json.dumps(
            DTranslit, indent=4, ensure_ascii=False
        )

        print(d)
        f.write(d)
