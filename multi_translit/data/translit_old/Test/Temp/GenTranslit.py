import re
import codecs
import glob
import sys, os
from BOMFile import EncFile

def Max(x, y):
    if x > y: return x
    else: return y

def Min(x, y):
    if x < y: return x
    else: return y

for FileName in glob.glob('%s/*.txt' % os.getcwdu()):
    print FileName
    iFile = codecs.open(FileName, 'rb', 'utf-8')
    DOFiles = {}
    DWPending = {}
    DIPAPending = {}
    i = 0
    for Line in iFile:
        Line = Line.strip()
        if i == 0:
            LTransNames = Line.split('  ')
        elif i == 1:
            LTransYears = Line.split('  ')
            assert len(LTransYears) == len(LTransNames), "%s has wrong TransNames/TransYears!" % FileName
            # Open all the different translit output files
            x = 0
            for LTransName in LTransNames+['IPA']:
                Path = 'Output\\%s %s.txt' % (FileName.split('\\')[-1].split('.')[0], LTransName.strip().strip(u'\ufeff').replace('/', '_').replace('\\', '_'))
                DOFiles[LTransName] = EncFile(Path)
                DWPending[LTransName] = []
                #DOFiles[LTransName] = codecs.open(Path, 'wb', 'utf-8', 'replace')
                #DOFiles[LTransName].write(codecs.BOM_UTF8)
                if LTransName != 'IPA':
                    DOFiles[LTransName].write("# Translit auto-generated from %s version/date %s\n\n" % (FileName, LTransYears[x].strip()))
                    DOFiles[LTransName].write("usematchcase()\n")
                x += 1
        else:
            try:
                #Line = Line.replace(u'\xee', '')
                Line = Line.replace('  ', ' ')
                Line = Line.replace(' (', '(')
                Line = Line.replace(' [', '[')
                Line = re.sub(r'(?<=\S), (?=\S)', ',', Line)
                
                #Line = Line.replace(', ', ',')
                Line = Line.replace(' ~ ', '~')
                LTrans = Line.split(' ')
                LTrans = [xx.strip(' ') for xx in LTrans if xx.strip() and xx != u'\ue000']
                try: int(LTrans[0])
                except: LTrans = ['-1']+LTrans
                
                # Fix cursive/roman dupes
                if len(LTrans) > 5 and LTrans[1][0] == LTrans[3][0] and LTrans[2][0] == LTrans[4][0]:
                    #print 'LTrans Delete:', LTrans
                    import unicodedata
                    Cat = unicodedata.category(LTrans[1][0])[0]
                    if Cat == 'L':
                        del LTrans[3]
                        del LTrans[3]
                
                try:
                    try: 
                        int(LTrans[0])
                        Lower, Upper, LLine = LTrans[1], LTrans[2], LTrans[3:]
                    except: 
                        # No line numbers?
                        Lower, Upper, LLine = LTrans[0], LTrans[1], LTrans[2:]
                        assert len(LLine) == len(LTrans)
                except:
                    Lower, LLine = LTrans[0], LTrans[1:]
                Lower = Lower.lower()
                Upper = Upper.upper()
                if not Lower in DIPAPending: 
                    DIPAPending[Lower] = None
                
                x = 0
                for LTransName in LTransNames:
                    # Get [IPA] guides
                    # TODO: Separate into a separate file!
                    Comment = ''
                    RE = re.compile(r'\[.*?\]', re.UNICODE)
                    Match = RE.search(LLine[x])
                    if Match: 
                        #Comment = Match.group()
                        DIPAPending[Lower] = Match.group().strip('[]')
                        LLine[x] = RE.sub('', LLine[x])
                    
                    # Get (1.1) comment pointers
                    RE = re.compile(r'\(.*?\)', re.UNICODE)
                    Match = RE.search(LLine[x])
                    if Match: 
                        Comment += ' '+Match.group()
                        LLine[x] = RE.sub('', LLine[x])
                    
                    # Get (1.1) comment pointers for Cyrillic/etc left
                    RE = re.compile(r'\(.*?\)', re.UNICODE)
                    Match = RE.search(Lower)
                    if Match: 
                        Comment += ' '+Match.group()
                        Lower = RE.sub('', Lower).strip(' ')
                    
                    # SortKey, WriteVal
                    #if LLine[x].strip() != ',':
                    #LLine[x] = LLine[x].replace(', ', ',')
                    LLine[x] = re.sub(r'(?<=\S),(?=\S)', '||', LLine[x])
                    #LLine[x].replace(',', '||')
                    LLine[x] = LLine[x].strip(' ')
                    
                    if Comment: Comment = ' # %s' % Comment.strip()
                    else: Comment = ''
                    Write = "%s = allforms(%s)%s" % (Lower.lower(), LLine[x].lower(), Comment)
                    DWPending[LTransName].append((((-Max(len(Lower), len(LLine[x])), 
                                                    -Min(len(Lower), len(LLine[x]))), 
                                                       Lower.lower()), 
                                                    Write))
                    x += 1
                if len(LLine)>x+1:
                    print 'LINE WARNING:', Line.encode('utf-8'), '\n\t', LLine
            except IndexError: print 'INDEXERROR:', Line.encode('utf-8'), LLine
        i += 1
    
    for k in DOFiles: 
        if k == 'IPA': continue
        DWPending[k].sort()
        DOFiles[k].write('\n'.join([i[1] for i in DWPending[k]]))
        DOFiles[k].close()
    
    L = []
    for k in DIPAPending: 
        if not DIPAPending[k]: 
            L.append((-len(k), 0, '%s = ignore()' % k))
        else: 
            DIPAPending[k] = DIPAPending[k].replace(', ', ',')
            DIPAPending[k] = DIPAPending[k].replace(',', '||')
            L.append((-len(k), -len(DIPAPending[k]), '%s = %s' % (k, DIPAPending[k])))
    L.sort()
    L = [i[2] for i in L]
    DOFiles['IPA'].write('\n'.join(L))
    DOFiles['IPA'].close()
    iFile.close()
    
    #break
    