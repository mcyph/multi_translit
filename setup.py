"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from codecs import open
from os import path
from os.path import join

from os import walk


def get_L_data_dir(folder):
    LData = []
    for root, directories, filenames in walk(folder):
        LData.append([
            root,
            [join(root, filename) for filename in filenames]
        ])
    return LData

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='multi_translit',
    version='0.1.0',
    description='',
    long_description=long_description,
    url='https://github.com/mcyph/multi_translit',
    author='Dave Morrissey',
    author_email='20507948+mcyph@users.noreply.github.com',

    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Software Development :: Localization',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Text Processing :: General',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        # 'Programming Language :: Python :: 3.6',
    ],

    keywords='unicode keyboards hanzi kanji transliteration',
    packages=find_packages(),

    install_requires=[
        'Cython',
        'PyStemmer',
        'PyICU',
    ],

    data_files=get_L_data_dir('multi_translit/data'),
    zip_safe=False
)
