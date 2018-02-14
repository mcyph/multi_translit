# Encoding of Korean: Yale Translit System for Korean Language

# Id: Yale.pm,v 1.6 2007/11/29 14:25:31 you Exp 

def init(yale):
    yale.consonants('k kk n t tt l m p pp s ss ng c cc ch kh th ph h'.split())
    yale.vowels('a ay ya yay e ey ye yey o wa way oy yo wu we wey wi yu u uy i'.split())
    #yale.el('l')
    #yale.ell('ll')
    yale.naught('.')
    yale.sep('.')
    yale.make()

    # == MODES ==
    yale.enmode('greedy')
    yale.demode('greedy')

r'''
=head1 NAME

Encode::Korean::Yale - Perl extension for Encoding of Korean: Yale Translit 
System for Koran Language

=head1 SYNOPSIS

  use Encode::Korean::Yale;

  string = decode 'yale', octets;
  octets = encode 'yale', string;

  while(line = <>) {
    print encode 'utf8', decode 'yale', line;
  }

=head1 DESCRIPTION

L<Encode::Korean::Yale|Encode::Korean::Yale> implements an encoding system 
based on the transliteration method of Yale Translit for 
Korean Language, developed by S. Martin and his colleagues at Yale University. 
It is used mainly and only in academic litterature.

This module use Encode implementation base class L<Encode::Encoding|Encode::Encoding>.
The conversion is carried by a transliterator object of 
L<Encode::Korean::TransliteratorGenerator|Encode::Korean::TransliteratorGenerator>.


=head2 RULES

	Unicode name		Transliteration

	kiyeok			k
	ssangkieok		kk
	nieun			n
	tikeut			t
	ssangtikeut		tt
	rieul			l
	mieum			m
	pieup			p
	ssangpieup		pp
	sios			s
	ssangsios		ss
	ieung			ng
	cieuc			c
	ssangcieuc		cc
	chieuch			ch
	khieukh			kh
	thieuth			th
	phieuph			ph
	hieuh			h

	a			a
	ae			ay
	ya			ya
	yae			yay
	eo			e
	e			ey
	yeo			ye
	ye			yey
	o			o
	wa			wa
	wae			way
	oe			oy
	yo			yo
	u			wu
	weo			we
	we			wey
	wi			wi
	yu			yu
	eu			u
	yi			uy
	i			i


=head1 SEE ALSO

Visit 
 L<http://en.wikipedia.org/wiki/Yale_Translit>, 
 for more information about Yale Translit.

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
