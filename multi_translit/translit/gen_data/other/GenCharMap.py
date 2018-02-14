import os
import codecs
os.chdir('../../')
import File # Surrogate pair HACK!
from char_data.CharData import CharData, DISO2Lang, DISO2LFullText
from toolkit.surrogates import w_unichr

DFreq = {'cmn': ('Chinese Frequency', 
                 'Hong Kong Grade', 
                 'Japanese Frequency'),
         'jpn': ('Japanese Grade', 
                 'Japanese Frequency')}
DFreq['ltc'] = DFreq['kor'] = DFreq['vie'] = DFreq['hak'] = DFreq['yue'] = DFreq['cmn']

DMap = {} # {ISO: {Prop: [[LSort, CodePoint], ...], ...}, ..}
DISOs = {} # {Key: ISO, ...}
for ISO in DISO2LFullText:
    for k in DISO2LFullText[ISO][0]:
        DISOs[k] = ISO

for x in xrange(300000):
    for ISO in DISO2LFullText:
        for k in DISO2LFullText[ISO][0]: # DUPE WARNING!
            Prop = CharData.raw_data(k, x)
            if Prop:
                print x, ISO, k, Prop

                # Create the keys if they don't exist yet
                Prop = Prop[0].split()[0].strip(';,')
                if not k in DMap: DMap[k] = {}
                if not Prop in DMap[k]: DMap[k][Prop] = []

                # Append [LFreq, Value]
                LFreq = []
                for kFreq in DFreq[ISO]:
                    Freq = CharData.raw_data(kFreq, x)
                    if type(Freq) == int: LFreq.append(Freq)
                    elif type(Freq) in (list, tuple): LFreq.append(Freq[0])
                    else: LFreq.append(200000)
                L = [LFreq, x]
                DMap[k][Prop].append(L)

#=======================================================================#
#                      Output with tranlit maps                         #
#=======================================================================#

Template = '''
{{
FormatString: "%(Format)s"
LFonts: ["%(ToFont)s", "%(FromFont)s"]
LProvides: [
    ["%(ISO)s", "%(ProvidesTo)s"],
    ["%(ISO)s", "%(ProvidesFrom)s"]]
LCreate: [true, false]
LTypes = [["disp", "high"]]
BothWays: false
IgnoreCase: true
}}

'''.lstrip()

DMaps = {}
# COLLISION!
DMaps['Cantonese Readings'] = {'Format': 'Cantonese %s', 'FromFont': 'Latin', 'ToFont': 'Chinese (Unified)', 
                               'ProvidesFrom': 'Jyutping', 'ProvidesTo': 'Chinese (Unified)'}
DMaps['Cantonese'] = {'Format': 'Cantonese %s', 'FromFont': 'Latin', 'ToFont': 'Chinese (Unified)', 
                      'ProvidesFrom': 'Jyutping', 'ProvidesTo': 'Chinese (Unified)'}
# "From" MAY BE WRONG!
DMaps['Hakka'] = {'Format': 'Hakka %s', 'FromFont': 'Latin', 'ToFont': 'Chinese (Unified)', 
                  'ProvidesFrom': 'Guangdong', 'ProvidesTo': 'Chinese (Unified)'}

# COLLISION!
DMaps['Hangul Readings'] = {'Format': 'Korean %s', 'FromFont': 'Hangul', 'ToFont': 'Chinese (Unified)', 
                            'ProvidesFrom': 'Hangul', 'ProvidesTo': 'Hanja'}
DMaps['Korean Hangul'] = {'Format': 'Korean %s', 'FromFont': 'Hangul', 'ToFont': 'Chinese (Unified)', 
                          'ProvidesFrom': 'Hangul', 'ProvidesTo': 'Hanja'}
DMaps['Korean'] = {'Format': 'Korean %s', 'FromFont': 'Latin', 'ToFont': 'Chinese (Unified)', 
                   'ProvidesFrom': 'Yale', 'ProvidesTo': 'Hanja'}

DMaps['Japanese Kun'] = {'Format': 'Japanese %s (EXPERIMENTAL)', 'FromFont': 'Japanese', 'ToFont': 'Japanese', 
                         'ProvidesFrom': 'Kun', 'ProvidesTo': 'Japanese'}
DMaps['Japanese Nanori'] = {'Format': 'Japanese %s (EXPERIMENTAL)', 'FromFont': 'Japanese', 'ToFont': 'Japanese', 
                            'ProvidesFrom': 'Nanori', 'ProvidesTo': 'Japanese'}
DMaps['Japanese On'] = {'Format': 'Japanese %s (EXPERIMENTAL)', 'FromFont': 'Japanese', 'ToFont': 'Japanese', 
                        'ProvidesFrom': 'On', 'ProvidesTo': 'Japanese'}

DMaps['Mandarin'] = {'Format': 'Chinese %s', 'FromFont': 'Latin', 'ToFont': 'Chinese (Unified)', 
                     'ProvidesFrom': 'PinYin', 'ProvidesTo': 'Chinese (Unified)'}
# "From" MAY BE WRONG!
DMaps['Tang'] = {'Format': 'Tang %s', 'FromFont': 'Latin', 'ToFont': 'Chinese (Unified)', 
                 'ProvidesFrom': 'Latin', 'ProvidesTo': 'Chinese (Unified)'}
# Ditto!
DMaps['Vietnamese'] = {'Format': 'Vietnamese %s', 'FromFont': 'Latin', 'ToFont': 'Chinese (Unified)', 
                       'ProvidesFrom': 'Latin', 'ProvidesTo': 'Chinese (Unified)'}

DFiles = {}
for k in DISOs:
    DFiles[k] = codecs.open('Translit/BySound/Chars/%s.trn' % k, 'wb', 'utf-8')
    D = DMaps[k] 
    D['ISO'] = DISOs[k]
    t = Template % D
    DFiles[k].write(t)

for k in DMap:
    for Prop in DMap[k]:
        DMap[k][Prop].sort()
        Vals = '||'.join([w_unichr(i[1]) for i in DMap[k][Prop]])
        Prop = Prop.lower() # HACK!
        DFiles[k].write('%s = %s\n' % (Vals, Prop))

for k in DFiles:
    DFiles[k].close()
