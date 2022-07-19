# -*- coding: utf-8 -*-
# Encoding of Korean: North Korean Translit 1992

# Id: NKR_1992.pm,v 1.7 2007/11/29 14:25:31 you Exp 

def init(nkr):
    nkr.consonants('k kk n t tt r m p pp s ss ng ts tss tsh kh th ph h'.split());
    nkr.vowels([
        "a",
        "ae",
        "ya",
        "yae",
        "\u014F", # latin small letter with breve (ŏ)
        "e",
        "y\u014F",
        "ye",
        "o",
        "wa",
        "wae",
        "oe",
        "yo",
        "u",
        "w\u014F",
        "we",
        "wi",
        "yu",
        "\u016Du", # latin small letter u with breve (ŭ)
        "\u016Dy",
        "i"
        ]);
    nkr.el('l');
    nkr.ell('ll');
    nkr.naught('.');
    nkr.sep('.');
    nkr.make();

    # == MODES ==
    nkr.enmode('greedy');
    nkr.demode('greedy');

r'''
=encoding utf8
=head1 NAME

Encode::Korean::NKR_1992 - Perl extension for Encoding of Korean: North Korean 
Romanizaiton 

=head1 SYNOPSIS

  use Encode::Korean::NKR_1992;
  
  string = decode 'nkr', decode enc, octets;
  octets = encode enc, encode 'nkr', string;
  
  while(line = <>) {
    print encode 'utf8', decode 'nkr', line;
  }
  
=head1 DESCRIPTION

L<Encode::Korean::NKR_1992> implements an encoding system based on North Korean 
Romanizaiton (National system of DPKR), released in 1992 by Chosun Gwahagwon.

=head2 RULES

 nkr.consonants(qw(k kk n t tt r m p pp s ss ng ts tss tsh kh th ph h));
 nkr.vowels(
	"a",
	"ae",
	"ya",
	"yae",
	"\x{014F}", # latin small letter with breve (ŏ)
	"e",
	"y\x{014F}",
	"ye",
	"o",
	"wa",
	"wae",
	"oe",
	"yo",
	"u",
	"w\x{014F}",
	"we",
	"wi",
	"yu",
	"\x{016D}", # latin small letter u with breve (ŭ)
	"\x{016D}y",
	"i"

=head1 SEE ALSO

See
 L<http://en.wikipedia.org/wiki/Korean_romanization>,
 you can find a link to comparsion table of transliteration systems.

=head1 AUTHOR

You Hyun Jo, E<lt>you at cpan dot orgE<gt>

=head1 COPYRIGHT AND LICENSE

Copyright (C) 2007 by You Hyun Jo

This library is free software; you can redistribute it and/or modify
it under the same terms as Perl itself, either Perl version 5.8.8 or,
at your option, any later version of Perl 5 you may have available.

'''
