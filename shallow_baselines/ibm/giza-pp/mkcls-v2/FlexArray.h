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



#ifndef CLASS_FlexArray_defined
#define CLASS_FlexArray_defined
#include "FixedArray.h"

template<class T>
class FlexArray
{
private:
  FixedArray<T> p;
  int start,end;
public:
  FlexArray(int _start=0,int _end=-1)
    : p(_end-_start+1),start(_start),end(_end) {}
  T&operator[](int i)
    {return p[i-start];}
  const T&operator[](int i)const
    {returnp[i-start];}
  int low()const{return start;}
  int high()const{return end;}
};


#endif
