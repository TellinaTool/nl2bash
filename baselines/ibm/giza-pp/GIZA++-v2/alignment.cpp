/*

EGYPT Toolkit for Statistical Machine Translation
Written by Yaser Al-Onaizan, Jan Curin, Michael Jahr, Kevin Knight, John Lafferty, Dan Melamed, David Purdy, Franz Och, Noah Smith, and David Yarowsky.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, 
USA.

*/
/*--
alignment: 'checked' alignment representation with automatic calculation
           of fertilities
Franz Josef Och (30/07/99)
--*/
#include "alignment.h"

ostream&operator<<(ostream&out, const alignment&a)
{
  int m=a.a.size()-1,l=a.f.size()-1;
  out << "AL(l:"<<l<<",m:"<<m<<")(a: ";
  for(int j=1;j<=m;j++)out << a(j) << ' ';
  out << ")(fert: ";
  for(int i=0;i<=l;i++)out << a.fert(i) << ' ';
  return out << ")  c:"<<"\n";
}

