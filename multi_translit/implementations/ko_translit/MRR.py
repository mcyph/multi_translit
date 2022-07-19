# -*- coding: utf-8 -*-
# Encoding of Korean: McCune-Reischauer Translit

# Id: MRR.pm,v 1.5 2007/11/29 14:25:31 you Exp 

def init(mrr):
    mrr.consonants("k kk n t tt r m p pp s ss ng ch tch ch' k' t' p' h".split());
    mrr.vowels([
        "a",
        "ae",
        "ya",
        "yae",
        "\u014F", # \x{014F} latin small letter with breve (ŏ)
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
        "\u016D", # \x{016D} latin small letter u with breve (ŭ)
        "\u016Dy",
        "i"
        ]);
    mrr.el('l');
    mrr.ell('ll');
    mrr.naught('.');
    mrr.sep('.');
    mrr.make();

    # == MODES ==
    mrr.enmode('greedy');
    mrr.demode('greedy');

r'''

=head1 NAME

Encode::Korean::MRR - Perl extension for Encoding of Korean: McCune-Reishauer Translit 

=head1 SYNOPSIS

   use Encode::Korean::MRR;

   string = decode 'mrr', octets;
   octets = encode 'mrr', string;

   while(line = <>) {
     print decode 'mrr', line;
   }

=head1 DESCRIPTION

L<Encode::Korean::MMR> implements an encoding system based on McCune-Reischauer
Translit, created in 1937 by George M. McCune and Edwin O. Reischauer. It
is one of the most widely used methods.  

=head1 SEE ALSO

See
 L<http://en.wikipedia.org/wiki/McCune-Reischauer>
 for McCune-Reischauer Translit 


=head1 AUTHOR

You Hyun Jo, E<lt>you at cpan dot orgE<gt>

=head1 COPYRIGHT AND LICENSE

Copyright (C) 2007 by You Hyun Jo

This library is free software; you can redistribute it and/or modify
it under the same terms as Perl itself, either Perl version 5.8.8 or,
at your option, any later version of Perl 5 you may have available.


'''
# vim: set ts=4 sts=4 sw=4 et
