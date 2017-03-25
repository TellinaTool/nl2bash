/*

Copyright (C) 2000,2001  Franz Josef Och (RWTH Aachen - Lehrstuhl fuer Informatik VI)

This file is part of GIZA++ ( extension of GIZA ).

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
#ifndef transpair_model2_defined_h
#define transpair_model2_defined_h

#include "defs.h"
#include "Vector.h"
#include "NTables.h"
#include "ATables.h"
#include "TTables.h"
#include "alignment.h"
#include <cmath>
#include "transpair_model1.h"


class transpair_model2 : public transpair_model1
{
 protected:
  Array2<PROB, Vector<PROB> > a;
 public:
  transpair_model2(const Vector<WordIndex>&es, const Vector<WordIndex>&fs, const tmodel<COUNT, PROB>&tTable, 
		   const amodel<PROB>&aTable)
    : transpair_model1(es,fs,tTable),a(es.size(),fs.size())
    {
      for(WordIndex i=0;i<=l;i++)
	for(WordIndex j=1;j<=m;j++)
	  a(i, j)=aTable.getValue(i, j, l, m);
    }
  const PROB&get_a(WordIndex i, WordIndex j)const
    {return a(i, j);}
};
#endif
