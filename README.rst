=====
About
=====

Provides transliteration functions between different scripts in use by different languages.

For example, this can provide conversions between Cyrillic and Latin.

It uses tables and engines from multiple sources:

* ICU: ...
* Korean: ...
* Internal: My own engine

===============
Install
===============

===============
Usage
===============

.. code-block:: python

    # TODO: PLEASE MOVE ME!!!
    from multi_translit.translit.ICUTranslit import Translit

    Translit.mapping_to_iso
    Translit.get_D_engines
    Translit.get_D_scripts
    Translit.get_L_possible_conversions
    Translit.get_best_conversion
    Translit.get_L_best_conversions
    Translit.get_L_all_conversions
    Translit.translit

