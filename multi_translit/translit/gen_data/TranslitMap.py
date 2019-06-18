# TODO: write a parser to add maps for e.g. conversions 
# between the many chinese transliteration systems!

import os
import glob
import codecs
import random

from toolkit import json_tools
from GetDSettings import get_D_settings

Format = '''
{{
FormatString: %(FormatString)s
LFonts: %(LFonts)s
LProvides: %(LProvides)s
LCreate: [true, false]
LTypes = %(LTypes)s
BothWays: false
IgnoreCase: %(IgnoreCase)s
MatchCase: %(MatchCase)s
}}

BEGIN Modifiers(Source)
%(Modifiers)s
END Modifiers
'''

def parse_map(DTranslitPaths, D, Path):
    fFont = None
    LTranslit = None
    LangName = None
    fScript = None
    tScript = None
    
    def write(LTranslit):
        # Reset any existing maps and output to file
        print(LTranslit)
        LTranslit = json_tools.loads(''.join(LTranslit).replace("'", '"'))
        DFrom = D[LTranslit[0]]
        DTo = D[LTranslit[-1]]
        ISO = DFrom['LProvides'][0][0] # HACK!
        
        # Create a new "include" plugin for each system in LTranslit
        LModifiers = []
        for System in LTranslit:
            S = '    from include(%s)' % (json_tools.dumps(System))
            LModifiers.append(S)
        Modifiers = '\n'.join(LModifiers)
        
        DFormat = {'FormatString': '%s %%s' % (LangName),
                   'LFonts': [fFont or DFrom['LFonts'][0], 
                              DTo['LFonts'][1]], # CHECK ME!
                   'LProvides': [[ISO, fScript], 
                                 [ISO, tScript]],
                   'LTypes': DFrom['LTypes'],
                   'IgnoreCase': DFrom.get('IgnoreCase', False),
                   'MatchCase': DFrom.get('MatchCase', False),
                   'Modifiers': Modifiers}
        
        for k in DFormat: 
            if k != 'Modifiers':
                DFormat[k] = json_tools.dumps(DFormat[k])
        
        Path = 'Translit/BySound/AutoGen/AutoGen%s.trn'\
                % (random.randint(1, 1000000))
        nFile = codecs.open(Path, 'wb', 'utf-8')
        nFile.write(Format % DFormat)
        DTranslitPaths[os.path.split(Path)[-1]] = Path # HACK!
        nFile.close()
    
    File = codecs.open(Path, 'rb', 'utf-8')
    for Line in File:
        Line = Line.split('#')[0].rstrip()
        if not Line.strip():
            continue
        print(Line.encode('utf-8'))
        
        if Line[0] not in '\t ':
            if LTranslit: write(LTranslit)
            LSplit = Line.split('[')
            if len(LSplit) == 3:
                # "From font" supplied
                LangName = LSplit[0].strip()
                fScript, tScript = LSplit[1].strip(' ]:').split(':')
                fFont = LSplit[2].strip(' ]:')
                LTranslit = []
                
            elif len(LSplit) == 2:
                # "From font" not supplied - default to the 
                # font used by the first transliteration system
                LangName = LSplit[0].strip()
                fScript, tScript = LSplit[1].strip(' ]:').split(':')
                fFont = None
                LTranslit = []
                
            else: raise Exception("Invalid line: %s" % Line)
        else:
            LTranslit.append(Line.strip())
    
    if LTranslit: write(LTranslit)
    File.close()

def write_maps(DTranslitPaths):
    #  Delete the previous auto-generated files!
    for Path in glob.glob('Translit/BySound/AutoGen/*.trn'):
        os.remove(Path)
    
    D = {}
    for k in DTranslitPaths:
        Key = os.path.split(k)[-1].split('.')[0]
        print 'ADDING MAP FOR:', Key
        try: 
            File = open(DTranslitPaths[k], 'rb')
            Text = File.read().decode('utf-8', 'replace')
            File.close()
            
            Ignore, DSettings = get_D_settings(Text)
            k = DSettings['FormatString'] % '%s-%s' % (DSettings['LProvides'][0][1],
                                                       DSettings['LProvides'][1][1])
            D[k] = DSettings
            
            if DSettings['BothWays']:
                k = DSettings['FormatString'] % '%s-%s' % (DSettings['LProvides'][1][1],
                                                           DSettings['LProvides'][0][1])
                D[k] = DSettings
            
        except Exception, exc: 
            print('MAP ERROR:', DTranslitPaths[k])
            import traceback
            traceback.print_exc()
    
    for Dir, LDirs, LFiles in os.walk('Translit/BySound'):
        for File in LFiles:
            if File.endswith('.map'):
                print('PARSING MAP:', File.encode('utf-8'))
                parse_map(DTranslitPaths, D, '%s/%s' % (Dir, File))
