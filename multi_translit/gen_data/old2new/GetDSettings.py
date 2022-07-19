import re
from multi_translit.toolkit.json_tools import loads

# Possible settings keys: FormatString[REQ], LFonts[REQ], LProvides[REQ], 
# LCreate[true, true], LTypes[REQ], BothWays[true], IgnoreCase[false], 
# IgnoreMe[false], MatchCase[false]
DPossibleSet = {
    'FormatString': '%s',
    'LFonts': 'REQ',
    'LProvides': 'REQ',
    'LTypes': [],
    'LCreate': [True, True],
    'BothWays': True,
    'IgnoreCase': False,
    'IgnoreMe': False,
    'MatchCase': False,
    'FromSep': '',
    'ToSep': ''
}

def get_D_settings(txt):
    if not '{{' in txt or not '}}' in txt:
        #print "TAT:", txt
        raise Exception("Settings section not found")
    elif txt.count('{{') > 1 or txt.count('}}') > 1:
        raise Exception("Multiple settings sections not allowed")
    
    DSettings = {}
    cfg = txt.split('{{')[1].split('}}')[0]
    txt = '%s\n%s' % (txt.split('{{')[0], txt.split('}}')[1])
    
    curKey = None
    LCurItem = []
    for line in cfg.split('\n'):
        line = line.replace(' = ', ': ') # HACK!
        
        # TODO: What about settings that pass onto multiple lines?
        # {{
        # blah = ['',
        #     '']
        # }}
        if line.strip() and line.strip()[0] == '#': 
            continue
        elif '#' in line:
            # Filter out comments
            line = line[:line.index('#')]
        
        if not line.strip(): 
            continue
        
        if line[0] in ('\t', ' '):
            # Append any tabbed items to continue on from last time
            assert curKey
            assert LCurItem
            LCurItem.append(line.strip())
            continue
        
        if LCurItem:
            json = '\n'.join(LCurItem).replace("'", '"') # HACK!
            assert not curKey in DSettings, "%s already in DSettings" % curKey
            try: DSettings[curKey] = loads(json)
            except: raise Exception('JSON Error: %s' % json)
            LCurItem = []
        line = line.strip()
        
        # Grab Keys/Values and decode using JSON
        LSplit = line.split(':')
        curKey = LSplit[0].strip()
        LCurItem.append(':'.join(LSplit[1:]).strip())
        
    # Add the last item (if there is one :-)
    if LCurItem:
        DSettings[curKey] = loads('\n'.join(LCurItem))
    
    # Add default keys/check no invalid keys/check required keys exist
    for k in DPossibleSet:
        if not k in DSettings and DPossibleSet[k] == 'REQ':
            raise Exception("Required key %s not found in DSettings" % k)
        elif not k in DSettings:
            DSettings[k] = DPossibleSet[k]
    
    for k in DSettings:
        if not k in DPossibleSet:
            raise Exception("Invalid key %s in DSettings" % k)
    
    return txt, DSettings
