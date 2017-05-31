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








#ifndef GENERAL_HEADER
#define GENERAL_HEADER

#include <iostream>
#ifdef NeXT
#include <minmax.h>
#endif
#include <string.h>



#define NULLFLOAT(x)	( fabs(x)<=0.0000001 )
#define EQUALFLOAT(x,y)	( fabs(x-y)<(fabs(x)+fabs(y))/10000000.0 )




#define TEST_RANDOM_SEED 532567487 

double zufall01();                   
                                   

double zufall(double min,double max);    
                                   

int randomInt(int exclusive);      
                                   

void zufallSeed(int z =TEST_RANDOM_SEED);                 
                                   



#include "myassert.h"
#include <cassert>
#include "Array.h"






double clockSec(); 

extern int verboseMode;



inline string operator&(const string&a,const string&b)
{
  string c(a);
  c+=b;
  return c;
}



#endif

