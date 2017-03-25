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
#include "AlignTables.h"

bool alignmodel::insert(Vector<WordIndex>& aj, LogProb val)
{
  hash_map<Vector<WordIndex>, LogProb, hashmyalignment, equal_to_myalignment >::iterator i;
  i = a.find(aj);
  if(i != a.end() || val <= 0)
    return false ;
  a.insert(pair<const Vector<WordIndex>, LogProb>(aj, val));
  return true ;
}
 

LogProb alignmodel::getValue(Vector<WordIndex>& align) const
{
  const LogProb zero = 0.0 ;
  hash_map<Vector<WordIndex>, LogProb, hashmyalignment, equal_to_myalignment >::const_iterator i;
  i = a.find(align);
  if(i == a.end())
    return zero;
  else
    return (*i).second;
}
