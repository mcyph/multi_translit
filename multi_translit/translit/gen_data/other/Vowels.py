﻿D = {}
D['$LATINVOWELS'] = u'''À  à  Ȁ  ȁ  Á  á  Â  â  Ǎ  ǎ  Ă  ă  Ȃ  ȃ  ẚ  Ã  ã  Ā  ā  Ȧ  ȧ  Ä  ä  Å  å  
Ả  ả  Ạ  ạ  Ḁ  ḁ  Ą  ą  Ǟ  ǟ  Ǡ  ǡ  Ǻ  ǻ  Ấ  ấ  Ầ  ầ  Ẩ  ẩ  Ẫ  ẫ  Ậ  ậ  Ắ  ắ  Ằ  ằ  Ẳ  ẳ  Ẵ  ẵ  Ặ  
ặ  Æ æ  Ǽ  ǽ  Ǣ  ǣ È  è  Ȅ  ȅ  Éé Ê  ê  Ě  ě  Ĕ  ĕ  Ȇ  ȇ  Ẽ  ẽ  Ē  ē  Ė  ė  Ë  ë  Ẻ  ẻ  Ḙ  ḙ  Ḛ  ḛ  
Ẹ  ẹ  Ȩ  ȩ  Ę  ę  Ḕ  ḕ  Ḗ  ḗ  Ḝ  ḝ  Ế  ế  Ề  ề  Ể  ể  Ễ  ễ  Ệ  ệ  Ǝ Ə ǝ  Ɛ ı  Ì  ì  Ȉ ȉ Í í Î î Ǐ 
ǐ Ĭ ĭ Ȋ ȋ Ĩ ĩ Ī ī İ Ï ï Ỉ ỉ Ḭ ḭ Ị ị Į į Ḯ ḯ Ɩ Ɨ Ĳ ĳ Ò ò Ȍ ȍ Ó ó Ő ő Ô ô Ǒ ǒ Ŏ ŏ Ȏ ȏ Ō ō Õ õ Ȯ ȯ Ö 
ö Ỏ ỏ Ơ ơ Ọ ọ Ǫ ǫ Ṍ ṍ Ṏ ṏ Ṑ ṑ Ṓ ṓ Ố ố Ồ ồ Ổ ổ Ỗ ỗ Ộ ộ Ớ ớ Ờ ờ Ở ở Ỡ ỡ Ợ ợ Ȫ ȫ Ȭ ȭ Ȱ ȱ Ǭ ǭ Ø ø Ǿ ǿ 
Œ œ Ɵ Ƣ ƣ Ù ù Ȕ ȕ Ú ú Ű ű Û û Ǔ ǔ Ŭ ŭ Ȗ ȗ Ũ ũ Ū ū Ü ü Ů ů Ủ ủ Ṷ ṷ Ṵ ṵ Ụ ụ Ṳ ṳ Ų ų Ư ư Ǖ ǖ Ǘ ǘ Ǚ ǚ 
Ǜ ǜ Ṹ ṹ Ṻ ṻ Ứ ứ Ừ ừ Ử ử Ữ ữ Ự ự Ʊ'''
D['$LATINCONSONANTS'] = u'''Ḃ ḃ Ḇ ḇ Ḅ ḅ ƀ ƅ Ƅ Ɓ Ƃ ƃ Ć ć Ĉ ĉ Č č Ċ ċ Ç ç Ḉ ḉ Ɔ Ƈ ƈ Ď ď Ḋ ḋ Ḓ ḓ Ḏ ḏ 
Ḍ ḍ Ḑ ḑ ȡ Ð ð Đ đ Ɖ Ɗ Ƌ ƌ ƍ Ǳ ǲ ǳ Ǆ ǅ ǆ Ḟ ḟ Ƒ ƒ Ǵ ǵ Ĝ ĝ Ǧ ǧ Ğ ğ Ḡ ḡ Ġ ġ Ģ ģ Ɠ Ɣ Ǥ ǥ Ĥ ĥ Ḣ ḣ Ḧ ḧ Ȟ ȟ 
Ḫ ḫ ẖ Ḥ ḥ Ḩ ḩ Ħ ħ Ƕ ƕ Ĵ ĵ ǰ Ḱ ḱ Ǩ ǩ Ḵ ḵ Ḳ ḳ Ķ ķ ĸ Ƙ ƙ Ĺ ĺ Ľ ľ Ḽ ḽ Ḻ ḻ Ḷ ḷ Ļ ļ ȴ Ŀ ŀ Ł ł Ḹ ḹ ƚ ƛ Ǉ ǈ 
ǉ Ḿ ḿ Ṁ ṁ Ṃ ṃ Ɯ Ǹ ǹ Ń ń Ň ň Ñ ñ Ṅ ṅ ŉ Ṋ ṋ Ṉ ṉ Ṇ ṇ Ņ ņ Ŋ ŋ Ɲ ƞ Ƞ ȵ Ǌ ǋ ǌ Ṕ ṕ Ṗ ṗ Ƥ ƥ Ƿ ƿ Ȑ ȑ Ŕ ŕ Ř ř 
Ȓ ȓ Ṙ ṙ Ṟ ṟ Ṛ ṛ Ŗ ŗ Ṝ ṝ Ʀ Ś ś Ŝ ŝ Š š Ṡ ṡ Ṣ ṣ Ș ș Ş ş Ṥ ṥ Ṧ ṧ Ṩ ṩ Ƨ ƨ Ʃ ƪ ẛ Ť ť Ṫ ṫ ẗ Ṱ ṱ Ṯ ṯ Ṭ ṭ Ț ț ȶ ƫ Ʈ 
Ţ ţ Ŧ ŧ Ƭ ƭ Ṽ ṽ Ʋ Ṿ ṿ Ẁ ẁ Ẃ ẃ Ŵ ŵ Ẇ ẇ Ẅ ẅ ẘ Ẉ ẉ Ẋ ẋ Ẍ ẍ Ṽ ṽ Ʋ Ṿ ṿ Ẁ ẁ Ẃ ẃ Ŵ ŵ Ẇ ẇ Ẅ ẅ ẘ Ẉ ẉ Ẋ ẋ Ẍ ẍ Ź
 ź Ẑ ẑ Ž ž Ż ż Ẕ ẕ Ẓ ẓ Ȥ ȥ Ƶ ƶ Ʒ Ƹ ƹ ƺ Ǯ ǯ Ȝ ȝ Þ þ ß Ȣ ȣ'''
 
D['$CYRILLICIOTATED'] = u'''Ї ї Ю ю Я я Є є Ѥ ѥ Ѩ ѩ Ѭ ѭ'''
D['$CYRILLICVOWELS'] = D['$CYRILLICIOTATED']+u''' А а Ӑ ӑ Ӓ ӓ Ӕ ӕ Е е Ё ё І і Ӧ ӧ Ө ө Ӫ ӫ О о Ӯ ӯ Ӱ ӱ Ӳ ӳ 
Ѹ ѹ Ѻ ѻ Ӗ ӗ Ү ү Ұ ұ Ў ў Ә ә Ӛ ӛ И и Э э У у Ы ы Ь ь ѐ Ѡ ѡ Ѣ ѣ Ѧ ѧ Ѫ ѫ Ѯ ѯ Ѵ ѵ Ѷ ѷ Ѽ ѽ Ѿ ѿ Ҩ ҩ Ӣ ӣ Ӥ ӥ Й й'''
D['$CYRILLICCONSONANTS'] = u'''Б б В в Г г Д д Ж ж З з К к Л л М м Н н П п Р р С с Т т Ф ф Х х Ц ц Ч 
ч Ш ш Щ щ Ђ ђ Ѓ ѓ Ѕ ѕ Ј ј Љ љ Њ њ Ћ ћ Ќ ќ Џ џ Ѱ ѱ Ҏ ҏ Ґ ґ Ғ ғ Ҕ ҕ Җ җ Ҙ ҙ Қ қ Ҝ ҝ Ҟ ҟ Ҡ ҡ Ң ң Ҥ ҥ Ҧ 
ҧ Ҫ ҫ Ҭ ҭ Ҳ ҳ Ҵ ҵ Ҷ ҷ Ҹ ҹ Һ һ Ӂ ӂ Ӄ ӄ Ӆ ӆ Ӈ ӈ Ӊ ӊ Ӌ ӌ Ӎ ӎ Ӝ ӝ Ӟ ӟ Ӡ ӡ Ӹ ӹ Ӵ ӵ Ѳ ѳ Ҽ ҽ Ҿ ҿ'''
# Some of these characters modifier the next/previous character, are numeric, or are extremely rare
D['$CYRILLICCONTROVERSIAL'] = u'''Ъ ъ Ѝ ѝ Ҁ ҁ ҂ Ӏ ӏ Ӷ ӷ Ӻ ӻ Ӽ ӽ ӿ Ҋ ҋ Ҍ ҍ Ӭ ӭ'''

for k in D:
    D[k] = [i for i in D[k].split(' ') if i]
    D[k] = '||'.join(D[k])

# Arabic consonants/vowels in progress
'''
؋؍؎؏ؐؑؒؓؔؕ؞ءآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهوىيٖٜٗ٘ٙٚٛٝٞ٪٫٬٭ٮٯٱٲٳٴٵٶٷٸٹٺٻټٽپٿڀځڂڃڄڅچڇڈډڊڋڌڍڎڏڐڑڒړڔڕږ	ڗژ

VOWELS: ا‎ 
CONSONANTS: ب‎ ت‎ ث‎ ج‎ ح‎ خ‎ د‎ ذ‎ ر‎ ز‎ س‎ ش‎ ص‎ ض‎ ط‎ ظ‎ ع‎ غ‎ ف‎ ق‎ ك‎ ل‎ م‎ ن‎ ه‎ 
CONTROVERSIAL: و‎ (usually w but sometimes u: in arabic medial and final) ي‎ (usually consonant in initial and vowel i: in medial and final)
'''
