# -*- coding: utf-8 -*-

if False:
    File = open("Han-Latin.xml", 'r', encoding='utf-8')

    for Line in File:
        if not '<tRule>' in Line: continue
        Line = Line.replace('			<tRule>', '')
        Line = Line.replace(';</tRule>', '')
        Line = Line.replace('[', '')
        Line = Line.replace(']', '')
        Line = Line.strip('\r\n')
        #print Line.encode('utf-8')
        if Line[0] == ':': continue
        elif not Line.strip(): continue
        Key, Value = Line.split('→')
        Key = '||'.join([i for i in Key])
        print(('%s = %s' % (Key, Value)).encode('utf-8'))
    File.close()

else:
    File = open("Simplified-Traditional.xml", 'r', encoding='utf-8')

    for Line in File:
        if '<comment>' in Line:
            Comment = Line.split('<comment>')[1].split('</comment>')[0]
            if Comment.strip('#'): print(Comment.encode('utf-8'))
            else: print()
        else:
            if not '<tRule>' in Line: continue
            Line = Line.replace('\t\t\t<tRule>', '')
            Line = Line.replace(';</tRule>', '')
            Line = Line.replace('</tRule>', '')
            Line = Line.replace(';', '')
            Line = Line.strip('\r\n')
            #print Line.encode('utf-8')
            if Line[0] == ':': continue
            #elif Line[0] == '$': continue
            elif Line[0] == '＃': continue
            elif not Line.strip(): continue
            try:
                if '←' in Line:
                    Key, Value = Line.split('←')
                    print(('%s <= %s' % (Key, Value)).encode('utf-8'))
                elif '→' in Line:
                    Key, Value = Line.split('→')
                    print(('%s => %s' % (Key, Value)).encode('utf-8'))
                else:
                    Key, Value = Line.split('↔')
                    print(('%s = %s' % (Key, Value)).encode('utf-8'))
            except:
                if '$' in Line: print(Line.encode('utf-8'))
                else: raise
