import os
os.chdir('../../')
from multi_translit.translit.TranslitLoad import convert_script

CMU_PATH = r'E:\Dev\Dictionaries\Thesaurus, Pronunciation and  Frequencies\CMU Pronunciation\fgdata\SF\cmudict.0.7a'

f = open(CMU_PATH, 'rb')
fout = open('Translit/Tests/out.txt', 'w', encoding='utf-8')

for line in f:
    line = line.strip()
    if not line or line.startswith(';;;'):
        continue
    
    word, pron = line.split(' ', 1)
    word = word.strip()
    pron = pron.strip().replace('0', '') # HACK!
    
    # Convert to IPA from the CMU data
    _, _, ipa = convert_script(pron, 'eng', 'CMU Pron', 'eng', 'IPA')
    ipa = ipa.replace(' ', '')
    
    # Convert to Katakana from the IPA
    _, _, kata = convert_script(ipa, 'eng', 'IPA', 'jpn', 'Katakana')
    
    fout.write('%s %s %s\n' % (word, ipa.encode('utf-8'), kata.encode('utf-8')))

f.close()
fout.close()
