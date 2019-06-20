# http://rescomp.stanford.edu/~domingo2/Chinese.html

def read(s):
    f = open(s, 'r', encoding='utf-16')
    t = f.readlines()
    f.close()
    return t

def assign(L):
    D = {} # {Reading: LChars}
    Started = False
    for Line in L:
        Line = Line.strip()
        print((Line.encode('utf-8')))
        if Line == 'BEGINCHARACTER':
            Started = True
            continue
        elif not Started:
            continue
        elif Line == 'ENDCHARACTER':
            continue
        
        k, chars = Line.split('\t')
        chars = chars.split(',')
        iL = D.setdefault(k, [])
        iL.extend(chars)
    return D

def write(Path, D):
    # write a Hanzi-Yale/Jyutping translit file
    # MAY HAVE ISSUES FOR CHARS WITH MULTIPLE READINGS!
    f = open(Path, 'w', encoding='utf-8')
    LKeys = list(D.keys())
    LKeys.sort()
    for k in LKeys:
        L = D[k]
        f.write('%s = %s\n' % (k, '||'.join(L)))
    f.close()

def has_nums(s):
    return [i for i in s if i in '1234567890']

def rem_tones(s):
    return ''.join([i for i in s if i not in '1234567890'])

def Write2(Path, D1, D2, Format):
    def rev(D):
        # Returns {Char: [Reading1, Reading2], ...}
        DRtn = {}
        for k, v in list(D.items()):
            for i in v:
                if not has_nums(k): continue # TONES HACK!
                L = DRtn.setdefault(i, [])
                L.append(k)
        return DRtn
    
    D1 = rev(D1)
    D2 = rev(D2)
    
    # Look for the most common readings for the various readings,
    # taking into account there might be multiple readings per Hanzi
    DSort = {} # {Reading1: {Reading2: Num, ...}, ...}
    LChars = list(D1.keys())
    LChars.sort()
    for c in LChars:
        for Reading1 in D1[c]:
            for Reading2 in D2[c]:
                D = DSort.setdefault(Reading1, {})
                if not Reading2 in D:
                    D[Reading2] = 0
                D[Reading2] += 1
    
    # write to file
    #print DSort
    
    LOut = []
    for Reading1 in DSort:
        D = DSort[Reading1]
        LSort = [(D[Reading2], Reading2) for Reading2 in D]
        LSort.sort(reverse=True)
        print(LSort)
        LOut.append((Reading1, LSort[0][1]))
    
    f = codecs.open(Path, 'wb', 'utf-8')
    f.write(Format.strip())
    f.write('\n\n')
    LOut.sort(key=lambda x: (-len(x[0]), x)) # SORT WARNING!
    for i1, i2 in LOut:
        f.write('%s = %s\n' % (i1, i2))
    
    DUsed = {}
    f.write('\n')
    for i1, i2 in LOut:
        if i1 in DUsed: continue
        DUsed[i1] = i1
        f.write('%s = %s\n' % (rem_tones(i1), rem_tones(i2)))
    f.close()

Format = '''
{{
FormatString: "Cantonese %%s"
LFonts: ["Latin", "Latin"]
LProvides: [
    ["yue", "%s"],
    ["yue", "%s"]]
LCreate: [true, false]
LTypes = [["input", "low"], ["disp", "low"]]
BothWays: 0
IgnoreCase: 1
}}
'''

DJP = assign(read('yale-10.inputplugin'))
DYale = assign(read('jp112.inputplugin'))

write('BySound/Asian/Chinese/Cantonese/Hanzi-Yale.trn', DYale)
write('BySound/Asian/Chinese/Cantonese/Hanzi-Jyutping.trn', DJP)
Write2('BySound/Asian/Chinese/Cantonese/Yale-Jyutping.trn', DJP, DYale, 
       Format % ('Yale', 'Jyutping'))
Write2('BySound/Asian/Chinese/Cantonese/Jyutping-Yale.trn', DYale, DJP,
       Format % ('Jyutping', 'Yale'))
