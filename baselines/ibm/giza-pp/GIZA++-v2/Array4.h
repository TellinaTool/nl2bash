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
#ifndef AlignmentArray4_h_DEFINED
#define AlignmentArray4_h_DEFINED

#include "Array2.h"
template<class T> class Array4
{
 private:
  Array2< Array2<T>* > A;
  int M;
  T init;
 public:
  Array4(int m,const T&_init)
    : A(m,m,0),M(m),init(_init) {}
  ~Array4()
    {
      for(int l=0;l<M;++l)
	for(int m=0;m<M;++m)
	  delete A(l,m);
    }
  const T&operator()(int i, int j, int l, int m)const
    {
      if( A(l,m)==0 )
	return init;
      else
	return (*A(l,m))(i,j);
    }
  const T&get(int i, int j, int l, int m)const
    {
      if( A(l,m)==0 )
	return init;
      else
	return (*A(l,m))(i,j);
    }
  T&operator()(int i, int j, int l, int m)
    {
      if( A(l,m)==0 )
	{
	  A(l,m)=new Array2<T>(max(l+1,m+1),max(l+1,m+1),init);
	}
      return (*A(l,m))(i,j);
    }
  void clear()
    {
      for(int l=0;l<M;++l)
	for(int m=0;m<M;++m)
	  if( A(l,m) )
	    {
	      Array2<T>&a=*A(l,m);
	      for(int i=0;i<=l;++i)
		for(int j=0;j<=m;++j)
		  a(i,j)=0.0;
	    }
    }
};

#endif
