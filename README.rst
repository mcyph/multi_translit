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
    from multi_translit import MultiTranslit, translit, get_D_scripts

    MultiTranslit.mapping_to_iso
    MultiTranslit.get_D_engines
    MultiTranslit.get_D_scripts
    MultiTranslit.get_L_possible_conversions
    MultiTranslit.get_best_conversion
    MultiTranslit.get_L_best_conversions
    MultiTranslit.get_L_all_conversions
    MultiTranslit.translit

