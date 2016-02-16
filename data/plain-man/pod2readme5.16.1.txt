POD2README(1)         User Contributed Perl Documentation        POD2README(1)



NAME
       pod2readme - script to convert POD to README file

SYNOPSIS
         pod2readme lib/Some/Module.pm

DESCRIPTIONS
       Converts POD in the specified file to a README text file. If a second
       argument is given, it will use that as the output file and assume that
       is the type of file to export:

         pod2readme Module.pm COPYING

       If need be, this can be overridden in cases where the output file is
       not the same as the type, using a third argument:

         pod2readme Module.pm Module-Install.HOWTO install

SEE ALSO
       Pod::Readme

AUTHOR
       Robert Rothenberg <rrwo at cpan.org>

LICENSE
       Copyright (c) 2005 Robert Rothenberg. All rights reserved.  This
       program is free software; you can redistribute it and/or modify it
       under the same terms as Perl itself.



perl v5.16.3                      2010-04-14                     POD2README(1)
