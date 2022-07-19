# Encoding of Korean: South Korean Translit 1959 

# Id: SKR_1959.pm,v 1.5 2007/11/29 14:25:31 you Exp 

# == RULES ==
def init(skr):
    skr.consonants('g gg n d dd r m b bb s ss ng j jj ch k t p h'.split());
    skr.vowels('a ae ya yae eo e yeo ye o wa wae oe yo u weo we wi yu eu eui i'.split());
    skr.el('l');
    skr.ell('ll');
    skr.naught('.');
    skr.sep(';');
    skr.make();

    # == MODES ==
    skr.enmode('greedy');
    skr.demode('greedy');

r'''
=head1 NAME

Encode::Korean::SKR_1959 - Perl extension for Encoding of Korean: South Korean
Translit 1959.

=head1 SYNOPSIS

  use Encode::Korean::SKR_1959;

  string = decode 'skr-1959', octets;
  octets = encode 'skr-1959', string;

  while(line = <>) {
		print encode 'utf8', decode 'skr-1959', line;
  }

=head1 DESCRIPTION

L<Encode::Korean::SKR_1959|Encode::Korean::SKR_1959> implements an encoding system
of Korean based on the transliteration method of South Korean romanization system,
officially released in 1959 by South Korean Ministry of Education.

This module use Encode implementation base class L<Encode::Encoding|Encode::Encoding>.
The conversion is carried by a transliterator object of 
L<Encode::Korean::TransliteratorGenerator|Encode::Korean::TransliteratorGenerator>.


=head2 RULES

RR of Korean is basically similar to McCune-Reischaur, but uses only low ascii
characters. In case of ambiguity, orthographic syllable boundaries may be 
indicated with a hyphen.

	Unicode name		Transliteration

	kiyeok			g
	ssangkieok		gg
	nieun			n
	tikeut			d
	ssangtikeut		dd
	rieul			r
	mieum			m
	pieup			b
	ssangpieup		bb
	sios			s
	ssangsios		ss
	ieung			ng
	cieuc			j
	ssangcieuc		jj
	chieuch			ch
	khieukh			k
	thieuth			t
	phieuph			p
	hieuh			h

	a			a
	ae			ae
	ya			ya
	yae			yae
	eo			eo
	e			e
	yeo			yeo
	ye			ye
	o			o
	wa			wa
	wae			wae
	oe			oe
	yo			yo
	u			u
	weo			weo
	we			we
	wi			wi
	yu			yu
	eu			eu
	yi			eui
	i			i


=head1 SEE ALSO

Visit 
L<en.wikipedia.org/wiki/Korean_romanization>, 
if you need information on romanization systems of Korean language.

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
