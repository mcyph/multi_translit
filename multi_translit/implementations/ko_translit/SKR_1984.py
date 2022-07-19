# -*- coding: utf-8 -*-
# Encoding of Korean: South Korean Translit 1984 

# Id: SKR_1984.pm,v 1.4 2007/11/29 14:25:31 you Exp 

# == RULES ==
def init(skr):
    skr.consonants("k kk n t tt r m p pp s ss ng ch tch ch' k' t' p' h".split());
    skr.vowels([
        "a",
        "ae",
        "ya",
        "yae",
        "\u014F", # \x{014F} latin small letter o with breve (ŏ)
        "e",
        "y\u014F",
        "ye",
        "o",
        "wa",
        "wae",
        "oe",
        "yo",
        "u",
        "wo",
        "we",
        "wi",
        "yu",
        "\u016D", # \x{016D} latin small letter u with breve (ŭ)
        "\u016Dy",
        "i"
        ]);
    skr.el('l');
    skr.ell('ll');
    skr.naught('-');
    skr.sep('-');
    skr.make();
    
    # == MODES ==
    skr.enmode('greedy')
    skr.demode('greedy')

r'''
=head1 NAME

Encode::Korean::SKR_1984 - Perl extension for Encoding of Korean: South Korean
Translit 1984.

=head1 SYNOPSIS

  use Encode::Korean::SKR_1984;

  string = decode 'skr-1984', octets;
  octets = encode 'skr-1984', string;

  while(line = <>) {
    print encode 'utf8', decode 'skr-1984', line;
  }

=head1 DESCRIPTION

L<Encode::Korean::SKR_1984|Encode::Korean::SKR_1984> implements an encoding system
of Korean based on the transliteration method of South Korean romanization system,
officially released on January 1, 1984 by South Korean Ministry of Education.

This module use Encode implementation base class L<Encode::Encoding|Encode::Encoding>.
The conversion is carried by a transliterator object of 
L<Encode::Korean::TransliteratorGenerator|Encode::Korean::TransliteratorGenerator>.


=head2 RULES
RR of Korean is basically similar to McCune-Reischaur, but uses only low ascii
characters. In case of ambiguity, orthographic syllable boundaries may be 
indicated with a hyphen.

	Unicode name		Transliteration

	kiyeok			k (g)
	ssangkieok		kk
	nieun			n
	tikeut			t (d)
	ssangtikeut		tt
	rieul			r
	mieum			m
	pieup			p (b)
	ssangpieup		pp
	sios			s (sh)
	ssangsios		ss
	ieung			ng
	cieuc			ch (j)
	ssangcieuc		tch
	chieuch			ch'
	khieukh			k'
	thieuth			t'
	phieuph			p'
	hieuh			h

	a			a
	ae			ae
	ya			ya
	yae			yae
	eo			\x{014F}		(o with breve)
	e			e
	yeo			y\x{014F}
	ye			ye
	o			o
	wa			wa
	wae			wae
	oe			oe
	yo			yo
	u			u
	weo			wo
	we			we
	wi			wi
	yu			yu
	eu			\x{016D}		(u with breve)
	yi			\x{016D}i
	i			i


=head1 SEE ALSO

Visit 
L<http://en.wikipedia.org/wiki/Revised_Translit_of_Korean>, 
if you need information on Revised Translit of Korean.
Keep in mind that this module uses the transliteration method,
not the transcription method. 

Visit
L<http://www.alanwood.net/unicode/hangul_jamo.html>,
if you want a list of Hangul Jamo in Unicode.

See
L<Encode|Encode>, 
L<Encode::Encoding|Encode::Encoding>, 
L<Encode::Korean|Encode::Korean>, 
L<Encode::Korean::TransliteratorGenerator|Encode::Korean::TransliteratorGenerator>, 
if you want to know more about relevant modules.

See 
L<Encode::KR|Encode::KR>, 
L<Lingua::KO::MacKorean|Lingua::KO::MacKorean>, 
if you need common encodings.

See
L<Lingua::KO::Romanize::Hangul|Lingua::KO::Romanize::Hangul>, 
if you need a common romanization (transcription method used in public).

=head1 AUTHOR

You Hyun Jo, E<lt>you at cpan dot orgE<gt>

=head1 COPYRIGHT AND LICENSE

Copyright (C) 2007 by You Hyun Jo

This library is free software; you can redistribute it and/or modify
it under the same terms as Perl itself, either Perl version 5.8.8 or,
at your option, any later version of Perl 5 you may have available.


'''
