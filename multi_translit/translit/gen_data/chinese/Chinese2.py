import codecs

# First line: the PinYin consonant map
PinYinKeys = u'''b	ch	c	d	f	g	h	j	k	l	m	n	p	q	r	sh	s	t	x	zh	z'''

# Following lines: vowel/consonants as final, self form (ignored if -*), and the PinYin using the above map
PinYinCombs = u'''a	a	ba	tʂʰa	tsʰa	da	fa	ga	xa		kʰa	la	ma	na	pʰa			ʂa	sa	tʰa		tʂa	dzɑ
ai	ai	bai	tʂʰai	tsʰai	dai		gai	xai		kʰai	lai	mai	nai	pʰai			ʂai	sai	tʰai		tʂai	dzai
an	ɑn	bɑn	tʂʰɑn	tsʰɑn	dɑn	fɑn	gɑn	xɑn		kʰɑn	lɑn	mɑn	nɑn	pʰɑn		ɹɑn	ʂɑn	sɑn	tʰɑn		tʂɑn	dzɑn
ang	ɑŋ	bɑŋ	tʂʰɑŋ	tsʰɑŋ	dɑŋ	fɑŋ	gɑŋ	xɑŋ		kʰɑŋ	lɑŋ	mɑŋ	nɑŋ	pʰɑŋ		ɹɑŋ	ʂɑŋ	sɑŋ	tʰɑŋ		tʂɑŋ	dzɑŋ
ao	au|ɑʊ	bɑʊ	tʂʰɑʊ	tsʰɑʊ	dɑʊ		gɑʊ	xɑʊ		kʰɑʊ	lɑʊ	mɑʊ	nɑʊ	pʰɑʊ		ɹɑʊ	ʂɑʊ	sɑʊ	tʰɑʊ		tʂɑʊ	dzɑʊ
e	ɜ | ə		tʂʰə		də		gə	xə		kʰə	lə	mə	nə			ɹə	ʂə	sə	tʰə		tʂə	dzə
ê	ε												nε									
ei	ei	bei			dei	fei	gei	xei		kʰei	lei	mei	nei	pʰei			ʂei	sei			tʂei	dzei
en	ən 	bən	tʂʰən		dən	fən	gən	xən		kʰən		mən	nən	pʰən		ɹən	ʂən	sən			tʂən	dzən
eng	ʌŋ	bʌŋ	tʂʰʌŋ	tsʰʌŋ	dʌŋ	fʌŋ	gʌŋ	xʌŋ		kʰʌŋ	lʌŋ	mʌŋ	nʌŋ	pʰʌŋ		ɹʌŋ	ʂʌŋ	sʌŋ	tʰʌŋ		tʂʌŋ	dzʌŋ
o	o			tsʰo		fo					lo	mo		pʰo								
-i	i	bi			di				tɕi		li	mi	ni	pʰi	tɕʰi				tʰi	ɕi		
-a	ia | iɑ								tɕia		lia		nia		tɕʰia					ɕia		
-in	in | ɪn								tɕɪn		lɪn	mɪn	nɪn	pʰɪn	tɕʰɪn					ɕɪn		
-ing	i ŋ | ɪŋ	bɪŋ			dɪŋ				tɕɪŋ		lɪŋ	mɪŋ	nɪŋ	pʰɪŋ	tɕʰɪŋ				tʰɪŋ	ɕɪŋ		
-u	y								tɕy		ly		ny		tɕʰy					ɕy		
-er	ɚ																					
-ou	ou		tʂʰou	tsʰou	dou	fou	gou	xou		kʰou	lou	mou	nou	pʰou		ɹou	ʂou	sou	tʰou		tʂou	dzou
-ian	iɛn	biɛn			diɛn				tɕiɛn		liɛn	miɛn	niɛn	pʰiɛn	tɕʰiɛn				tʰiɛn	ɕiɛn		
-iang	iaŋ				diaŋ				tɕiaŋ		liaŋ		niaŋ		tɕʰiaŋ					ɕiaŋ		
-iao	iau | iao	biau			diau	fiau			tɕiau		liau	miau	niau	pʰiau	tɕʰiau				tʰiau	ɕiau		
-ie	iɛ	biɛ			diɛ				tɕiɛ		liɛ	miɛ	niɛ	pʰiɛ	tɕʰiɛ				tʰiɛ	ɕiɛ		
-iu	iou | iu				diou				tɕiou		liou	miou	niou		tɕʰiou					ɕiou		
-ua	uɑ | uɑ		tʂʰua				gua	xua		kʰua							ʂua				tʂua	
-ong	ʊŋ		tʂʰʊŋ	tsʰʊŋ	dʊŋ		gʊŋ	xʊŋ		kʰʊŋ	lʊŋ		nʊŋ				ʂʊŋ	sʊŋ	tʰʊŋ		tʂʊŋ	dzʊŋ
-u	u	bu	tʂʰu	tsʰu	du	fu	gu	xu		kʰu	lu	mu	nu	pʰu		ɹu	ʂu	su	tʰu		tʂu	dzu
-uai	uai		tʂʰuai				guai	xuai		kʰuai							ʂuai				tʂuai	
-uan	uan		tʂʰuan	tsʰuan	duan		guan	xuan		kʰuan	luan		nuan			ɹuan	ʂuan	suan	tʰuan		tʂuan	dzuan
-uang	uaŋ		tʂʰuaŋ				guaŋ	xuaŋ		kʰuaŋ							ʂuaŋ				tʂuaŋ	
-ui	uei		tʂʰuei	tsʰuei	duei		guei	xuei		kʰuei						ɹuei	ʂuei	suei	tʰuei		tʂuei	dzuei
-uei	uei		tʂʰuei	tsʰuei	duei		guei	xuei		kʰuei						ɹuei	ʂuei	suei	tʰuei		tʂuei	dzuei
-un	ʊn		tʂʰʊn	tsʰʊn	dʊn		gʊn	xʊn		kʰʊn	lʊn		nʊn			ɹʊn	ʂʊn	sʊn	tʰʊn		tʂʊn	dzʊn
-uo	uɔ|uo		tʂʰuɔ	tsʰuɔ	duɔ		guɔ	xuɔ		kʰuɔ	luɔ		nuɔ			ɹuɔ	ʂuɔ	suɔ	tʰuɔ		tʂuɔ	dzuɔ
-iong	 iʊŋ								tɕiyŋ						tɕʰiyŋ					ɕiyŋ		
-uan	yan | yɛn								tɕyɛn		lyɛn				tɕʰyɛn					ɕyɛn		
-ue	yɛ								tɕyɛ		lyɛ		nyɛ		tɕʰyɛ					ɕyɛ		
-un	yn								tɕyn		lyn				tɕʰyn					ɕyn		'''

PinYinSelf = u'''Yan	jɛn
Yang	jaŋ
Yao	jɑu
Ye	jɛ
You	jou
Wa	wɑ
Weng	wʌŋ
Wu	wu
Wai	wai
Wan	wan
Wang	waŋ
Wei	wei
Wen	wən
Wo	wɔ|wo
Yong	jʊŋ
Yuan	ɥan | ɥɛn
Yue	ɥɛ
Yun	ɥn
Yi	i
Ya	ia | iɑ
Yin	in | ɪn
Ying	i ŋ | ɪŋ
Yu	y'''

Tones = u'''IPA 	˥˥ 	˧˥ 	˨˩˦ 	˥˩	
IPA Tongyong	˥˥ 	˧˥ 	˨˩˦ 	˥˩	
Pinyin 	1 	2 	3 	4	
Tongyong Pinyin 	ma 	maˊ 	maˇ 	maˋ	ma
Wade-Giles 	1 	2 	3 	4	
Zhuyin 	ㄇㄚ 	ㄇㄚˊ 	ㄇㄚˇ 	ㄇㄚˋ	ㄇㄚ˙'''

def generate():
    L = []
    
    # Load the 'Self' PinYin conversions
    for Line in PinYinSelf.split('\n'):
        Line = Line.strip()
        Line = Line.replace(' | ', '||')
        PinYin, IPA = Line.split('\t')
        L.append((PinYin.strip().lower(), IPA.strip()))
    
    # Load the tone conversions
    # TODO: Make this on the vowels?
    Tones = (('1', u'˥˥'), ('2', u'˧˥ '), ('3', u'˨˩˦'), ('4', u'˥˩'), ('5', 'ignore()'))
    for PinYin, IPA in Tones:
        L.append((PinYin, IPA))
    
    # Load the base PinYin combinations
    LPinYinKeys = [i.strip() for i in PinYinKeys.split('\t') if i.strip()]
    LPinYinCombs = [[x.strip().replace(' | ', '|').replace('|', '||') for x in i.split('\t')]
                    for i in PinYinCombs.split('\n')]
    
    for Line in LPinYinCombs:
        i = 0
        VowelEtc = Line[0]
        
        # Add the self form if not prefixed with '-'
        SelfForm = Line[1]
        if not VowelEtc.startswith('-'):
            L.append((VowelEtc, SelfForm))
        
        LPinYin = Line[2:]
        for i in range(len(LPinYin)):
            IPA = LPinYin[i]
            if not IPA: continue
            PinYin = '%s%s' % (LPinYinKeys[i].strip(), VowelEtc.lstrip('-'))
            L.append((PinYin, IPA))
    
    # Write the combinations out to file
    File = codecs.open("BySound/Asian/Chinese/Chinese PinYin-IPA2.trn", 'wb', 'utf-8')
    L.sort(reverse=True)
    for PinYin, IPA in L:
        File.write("%s = %s\n" % (PinYin, IPA))
    File.close()
    print 'PINYIN-IPA OUTPUT OK!'
generate()
