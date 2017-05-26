/*

Copyright (C) 1997,1998,1999,2000,2001  Franz Josef Och

mkcls - a program for making word classes .

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




#include "HCOptimization.h"

HCOptimization::HCOptimization(Problem &p,int m) 
: IterOptimization(p,m) 
{
  if( maxStep<=0 )
    maxStep=(int)(problem.expectedNumberOfIterations());
}
HCOptimization::HCOptimization(HCOptimization &o)
: IterOptimization(o)
{
}


short HCOptimization::accept(double delta)
{
  if( delta < 0 )
    return 1;
  else
    return 0;
}
short HCOptimization::end() 
{ 
  return endFlag>0; 
}
void HCOptimization::abkuehlen()
{
}



