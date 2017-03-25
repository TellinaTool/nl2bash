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
Array2: Implementation of a twodimensional checked array allowing for
a specified underlieing one-dimensional data-structure.

Franz Josef Och (30/07/99)
--*/
#ifndef CLASS_Array2_DEFINED
#define CLASS_Array2_DEFINED

#include "mystl.h"
#include <string>
#include <vector>

template<class T, class Y=vector<T> > class Array2
{
private:
  Y p;
  //  short h1, h2;
  unsigned int h1, h2;
public:
  Array2(unsigned int _h1, unsigned int _h2) 
    : p(_h1*_h2), h1(_h1), h2(_h2) {}
  Array2(unsigned int _h1, unsigned int _h2, const T&_init) 
    : p(_h1*_h2, _init), h1(_h1), h2(_h2) {}
  Array2() 
    : h1(0), h2(0) {}
  inline T &operator()(unsigned int i, unsigned int j)
    { assert(i<h1);assert(j<h2);return p[i*h2+j]; }
  inline const T&operator()(unsigned int i, unsigned int j) const
    { assert(i<h1);assert(j<h2);return p[i*h2+j]; }
  inline T get(unsigned int i, unsigned int j)
    { assert(i<h1);assert(j<h2);return p[i*h2+j]; }
  inline void set(unsigned int i, unsigned int j, T x)
    { assert(i<h1);assert(j<h2);p[i*h2+j]=x; }
  inline const T get(unsigned int i, unsigned int j) const
    { assert(i<h1);assert(j<h2);return p[i*h2+j]; }
  inline unsigned int getLen1() const
    { return h1; }
  inline unsigned int getLen2() const
    { return h2; }

inline T*begin(){ 
  if( h1==0||h2==0)return 0;
  return &(p[0]); 
}
inline T*end(){ 
  if( h1==0||h2==0)return 0;
  return &(p[0])+p.size(); 
}

  inline const T*begin()const{ return p.begin(); }
  inline const T*end()const{return p.end();}

  friend ostream&operator<<(ostream&out, const Array2<T, Y>&ar)
    {
      for(unsigned int i=0;i<ar.getLen1();i++)
	{
	  //out << i << ": ";
	  for(unsigned int j=0;j<ar.getLen2();j++)
	    out << ar(i, j) << ' ';
	  out << '\n';
	}
      return out << endl;
    }
  inline void resize(unsigned int a,unsigned int b)
    {
      if( !(a==h1&&b==h2))
	{
	  h1=a;
	  h2=b;
	  p.resize(h1*h2);
	}
    }
  inline void resize(unsigned int a,unsigned int b,const T&t)
    {
      if( !(a==h1&&b==h2))
	{
	  h1=a;
	  h2=b;
	  p.resize(h1*h2);
	  fill(p.begin(),p.end(),t);
	}
    }
};

#endif
