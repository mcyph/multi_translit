# Encoding of Korean: South Korean Translit 2000 
#                     (aka. Revised Translit of Korean)

# Id: SKR_2000.pm,v 1.5 2007/11/29 14:25:31 you Exp 

# == RULES ==
def init(coder):
    coder.consonants("g kk n d tt r m b pp s ss ng j jj ch k t p h".split());
    coder.vowels("a ae ya yae eo e yeo ye o wa wae oe yo u wo we wi yu eu ui i".split());
    coder.el('l');
    coder.ell('ll');
    coder.naught('-');
    coder.sep('-');
    coder.make();

    # == MODES ==
    coder.enmode('greedy');
    coder.demode('greedy');

r'''
=head1 NAME

Encode::Korean::SKR_2000 - Perl extension for Encoding of Korean: South Korean
Translit 2000.

=head1 SYNOPSIS

  use Encode::Korean::SKR_2000;

  string = decode 'skr-2000', octets;
  octets = encode 'skr-2000', string;

  while(line = <>) {
    print encode 'utf8', decode 'skr-2000', line;
  }

=head1 DESCRIPTION

L<Encode::Korean::SKR_2000|Encode::Korean::SKR_2000> implements an encoding system
of Korean based on the transliteration method of South Korean romanization system,
officially released on July 7, 2000 by South Korean Ministry of Culture and Tourism 
(aka. Revised Translit of Korean)

This module use Encode implementation base class L<Encode::Encoding|Encode::Encoding>.
The conversion is carried by a transliterator object of 
L<Encode::Korean::TransliteratorGenerator|Encode::Korean::TransliteratorGenerator>.


=head2 RULES
RR of Korean is basically similar to McCune-Reischaur, but uses only low ascii
characters. In case of ambiguity, orthographic syllable boundaries may be 
indicated with a hyphen.

	Unicode name		Transliteration

	kiyeok			g
	ssangkieok		kk
	nieun			n
	tikeut			d
	ssangtikeut		tt
	rieul			r
	mieum			m
	pieup			b
	ssangpieup		pp
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
	weo			wo
	we			we
	wi			wi
	yu			yu
	eu			eu
	yi			ui
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
