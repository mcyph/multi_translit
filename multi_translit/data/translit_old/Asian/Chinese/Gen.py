# -*- coding: utf-8 -*-
import codecs
if False:
    File = codecs.open("Han-Latin.xml", 'rb', 'utf-8')
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
        Key, Value = Line.split(u'→')
        Key = '||'.join([i for i in Key])
        print ('%s = %s' % (Key, Value)).encode('utf-8')
    File.close()
else:
    File = codecs.open("Simplified-Traditional.xml", 'rb', 'utf-8')
    for Line in File:
        if '<comment>' in Line:
            Comment = Line.split('<comment>')[1].split('</comment>')[0]
            if Comment.strip('#'): print Comment.encode('utf-8')
            else: print
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
            elif Line[0] == u'＃': continue
            elif not Line.strip(): continue
            try:
                if u'←' in Line:
                    Key, Value = Line.split(u'←')
                    print ('%s <= %s' % (Key, Value)).encode('utf-8')
                elif u'→' in Line:
                    Key, Value = Line.split(u'→')
                    print ('%s => %s' % (Key, Value)).encode('utf-8')
                else:
                    Key, Value = Line.split(u'↔')
                    print ('%s = %s' % (Key, Value)).encode('utf-8')
            except:
                if '$' in Line: print Line.encode('utf-8')
                else: raise
