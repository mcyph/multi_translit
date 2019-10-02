import os
#from langlynx.db.misc.RemDupes import FastRemDupes
#from langlynx.db.misc.FastCopy import Copy
DCurID = {None: 0}

# DStrToISO: 
#     String (e.g. Japanese Hiragana-Latin) -> (iso, script, iso, script)

# DIdToStr:
#     Id -> String for DTranslitChars compression

# DIdToDSet:
#     (iso, script, iso, script) -> settings dict with paths added
#     NOTE: See also TranslitGen's DPossibleSet for settings dict info

# DISOToAlpha:
#     (iso, script) -> alphabet for language data mappings

# DTranslitChars: 
#     char -> Translit Id -> to allow seeing possible transliterations of 
#           a character in the character palette, e.g:
#     [[System, FromChar, ToChar, Before, After], ...]
#     Note: Latin will need to be removed as there'd be too many of them :-)

# DSingleISOToISO: 
#     (fromiso, fromscript) -> (toiso, toscript) to allow finding mappings
#     Note: if there's no variant in the language profile it defaults 
#     to the font type and the variant is never blank

DStrToISO = {}
DIDToStr = {}
DISOToDSet = {}
DISOToAlpha = {}
DTranslitChars = {}
DSingleISOToISO = {}

def AddToMaps(Inst, D):
    LProvides = D['LProvides']
    FormatString = D['FormatString']
    
    # Get the ISOCode/Variants in combination and by themselves
    LFromISO = tuple(D['LProvides'][0])
    LToISO = tuple(D['LProvides'][1])
    LISOCodes = tuple(list(D['LProvides'][0])+list(D['LProvides'][1]))
    LRevISOCodes = tuple(list(D['LProvides'][1])+list(D['LProvides'][0]))
    
    #===============================================================#
    #                    Add to DStrToISO/DIDToStr                  #
    #===============================================================#
    
    FromFormat = '%s-%s' % (D['LProvides'][0][1], D['LProvides'][1][1])
    LTry = [['From-To', FromFormat, LFromISO, LToISO, LISOCodes, Inst.LFromAlphabet]]
    
    if Inst.DSet['BothWays']:
        ToFormat = '%s-%s' % (D['LProvides'][1][1], D['LProvides'][0][1])
        LTry.append(['To-From', ToFormat, LToISO, LFromISO, LRevISOCodes, Inst.LToAlphabet])
    
    for Direction, Format, LFrom, LTo, LISO, LAllAlpha in LTry:
        # Add to the string map
        ID = DCurID[None]; DCurID[None] += 1
        assert LProvides, "Provides information not provided for %s" % Inst.Path # FIXME!
        FileName = '.'.join(os.path.split(Inst.Path)[-1].split('.')[:-1])
        
        # add DStrToISO/DIDToStr mappings
        StrAssign = FormatString % Format # DEPRECATE ME!
        assert not StrAssign in DStrToISO, "Duplicate string map entry %s" % StrAssign
        assert not LISO in DISOToDSet, "LISO Duplicate: %s" % LISO
        assert not ID in DIDToStr
        DStrToISO[StrAssign] = (Direction, LISO)
        DIDToStr[ID] = StrAssign
        
        # Add possible mappings to get auto-conversions
        if not LFrom in DSingleISOToISO:
            DSingleISOToISO[LFrom] = []
        DSingleISOToISO[LFrom].append(LTo)
        
        # Add the settings with paths to DISOToDSet
        DSet = Copy(Inst.DSet)
        DSet['Path'] = (Direction, FileName)
        DISOToDSet[LISO] = DSet
        
        #===============================================================#
        #                      Alphabet Mappings                        #
        #===============================================================#
        
        # Add to the alphabet map (rough)
        # Better than typing them out for each language though :-)
        LAlpha = []
        [LAlpha.extend([x.lower() for x in i]) for i in LAllAlpha]
        [LAlpha.extend([x.upper() for x in i]) for i in LAllAlpha]
        
        # TODO: Shouldn't this be by (ISO, Variant)?
        # TODO: Remove "' and other punctuation marks?
        if not LFrom in DISOToAlpha: DISOToAlpha[LFrom] = []
        DISOToAlpha[LFrom].extend(LAlpha)
        DISOToAlpha[LFrom] = FastRemDupes(DISOToAlpha[LFrom])
        DISOToAlpha[LFrom].sort()
        
        # HACK: If more than 1000 characters, don't 
        # list to save space (e.g. Chinese characters)
        if len(DISOToAlpha[LFrom]) > 1000: del DISOToAlpha[LFrom]
