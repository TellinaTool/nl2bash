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



#ifndef ARRAY_H_DEFINED
#define ARRAY_H_DEFINED
using namespace std;
#include "myassert.h"
#include <algorithm>
#include <string>
#include <utility>
#include <functional>
#include "my.h"

#define ARRAY_DEBUG


template<class T> class Array
{
 private:
  T *p;                  	
  int realSize;
  int maxWritten;
  char a;

  void copy(T *a,const T *b,int n);
  void copy(T *a,T *b,int n);
  void _expand();
		
 public:
  Array() 
    : p(0),realSize(0),maxWritten(-1) ,a(1)
    {
#ifdef VERY_ARRAY_DEBUG
      cout << "MAKE ARRAY: " << this<<" "<<(void*)p << endl;
#endif
    }
  Array(const Array<T> &x)
    : p(new T[x.maxWritten+1]),realSize(x.maxWritten+1),maxWritten(x.maxWritten),a(x.a)
    {
      copy(p,x.p,realSize);
#ifdef VERY_ARRAY_DEBUG
      cout << "MAKE ARRAY copy: " << this << " " << realSize <<" "<<(void*)p<< endl;
#endif
    }
  explicit Array(int n)
    : p(new T[n]),realSize(n),maxWritten(n-1),a(0)
    {
#ifdef VERY_ARRAY_DEBUG
      cout << "MAKE ARRAY with parameter n: " << this << " " << realSize<<" "<<(void*)p << endl;
#endif			
    }
  Array(int n,const T&_init,int _a=0)
    : p(new T[n]),realSize(n),maxWritten(n-1),a(_a)
    {
      for(int iii=0;iii<n;iii++)p[iii]=_init;
#ifdef VERY_ARRAY_DEBUG
      cout << "MAKE ARRAY with parameter n and init: " << this << " " << realSize<<" "<<(void*)p << endl;
#endif			
    }
  
  ~Array() 
    { 
#ifdef VERY_ARRAY_DEBUG
      cout << "FREE ARRAY: " << this << " " << realSize<<" "<<(void*)p << endl;
#endif			
      delete [] p;
    }
  
  Array<T>& operator=(const Array<T>&x)
    {
      if( this!= &x )
	{
#ifdef VERY_ARRAY_DEBUG
	  cout << "FREE ARRAY because of operator=: " << this << " " << realSize<<" "<<(void*)p << endl;
#endif			
	  
	  delete [] p;
	  realSize = x.maxWritten+1;
	  maxWritten = x.maxWritten;
	  a = x.a;
	  p = new T[realSize]; 
	  copy(p,x.p,realSize);
#ifdef VERY_ARRAY_DEBUG
	  cout << "NEW ARRAY because of operator=: " << this << " " << realSize<<" "<<(void*)p << endl;
#endif			
	}
      return *this;
    }
  
  Array<T>& operator=(Array<T>&x)
    {
      if( this!= &x )
	{
#ifdef VERY_ARRAY_DEBUG
	  cout << "FREE ARRAY because of operator=: " << this << " " << realSize<<" "<<(void*)p << endl;
#endif			
	  delete [] p;
	  realSize = x.maxWritten+1;
	  maxWritten = x.maxWritten;
	  a = x.a;
	  p = new T[realSize]; 
	  copy(p,x.p,realSize);
#ifdef VERY_ARRAY_DEBUG
	  cout << "NEW ARRAY because of operator=: " << this << " " << realSize<<" "<<(void*)p << endl;
#endif			
	}
      return *this;
    }
  
  void allowAccess(int n) 
    { 
      while( realSize<=n )
	_expand(); 
      maxWritten=max(maxWritten,n);
      massert( maxWritten<realSize );
    }
  void resize(int n)
    {
      while( realSize<n ) 
	_expand(); 
      maxWritten=n-1;
    }
  void sort(int until=-1)
    {
      if( until== -1 ) until=size();
      std::sort(p,p+until);
    }
  void invsort(int until=-1)
    {
      if( until== -1 ) until=size();
      std::sort(p,p+until,greater<T>());      
    }
  void init(int n,const T&_init,bool _a=0)
    {
#ifdef VERY_ARRAY_DEBUG
      cout << "FREE ARRAY because of init: " << this << " " << realSize<<" "<<(void*)p << endl;
#endif			
      delete []p;
      p=new T[n];
      realSize=n;
      a=_a;
      maxWritten=n-1;
      for(int iii=0;iii<n;iii++)p[iii]=_init;
#ifdef VERY_ARRAY_DEBUG
      cout << "NEW ARRAY because of init: " << this << " " << realSize<<" "<<(void*)p << endl;
#endif			
    }
  inline int size() const
    {massert( maxWritten<realSize );
    return maxWritten+1;}
  inline int low() const
    { return 0; }
  inline int high() const
    { return maxWritten; }
  inline bool autoexpand() const 
    {return a;}
  inline void autoexpand(bool autoExp) 
    {a=autoExp;}
  int findMax() const;
  int findMin() const;
  const void errorAccess(int n) const;
  inline T*getPointerToData(){return p;}
  
  inline T& operator[](int n)
    { 
      if( a && n==maxWritten+1 )
	allowAccess(n);
      if( n<0 || n>maxWritten )
	errorAccess(n);
      return p[n];
    }
  inline const T& operator[](int n) const 
    { 
      if(n<0 || n>maxWritten )
	errorAccess(n);
      return p[n]; 
    }
  const T&top(int n=0) const
    {return (*this)[maxWritten-n];}
  T&top(int n=0)
    {return (*this)[maxWritten-n];}
  T&push(const T&x)
    {
      (*this)[maxWritten+1]=x;
      return top();
    }
  bool writeTo(ostream&out) const
    {
      out << "Array ";
      out << size() << " ";
      out << a << endl;
      for(int iv=0;iv<=maxWritten;iv++)
	{
	  writeOb(out,(*this)[iv]);
	  out << endl;
	}
      return 1;
    }
  bool readFrom(istream&in)
    {
      string s;
      if( !in )
	{
	  cerr << "ERROR(Array): file cannot be opened.\n";
	  return 0;
	}
      in >> s;
      if( !(s=="Array") )
	{
	  cerr << "ERROR(Array): Array!='"<<s<<"'\n";
	  return 0;
	}
      int biggest;
      in >> biggest;
      in >> a;
      resize(biggest);
      for(int iv=0;iv<size();iv++)
	{
	  readOb(in,(*this)[iv]);
	}
      return 1;
    }
};

template<class T> bool operator==(const Array<T> &x, const Array<T> &y)
{
  if( &x == &y )
    return 1;
  else
    {
      if( y.size()!=x.size() )
	return 0;
      else
	{
	  for(int iii=0;iii<x.size();iii++)
	    if( !(x[iii]==y[iii]) )
	      return 0;
	  return 1;
	}
    }
}

template<class T> bool operator<(const Array<T> &x, const Array<T> &y)
{
  if( &x == &y )
    return 0;
  else
    {
      if( y.size()<x.size() )
	return !(y<x);
      for(int iii=0;iii<x.size();iii++)
	{
	  massert( iii!=y.size() );
	  if( x[iii]<y[iii] )
	    return 1;
	  else if( y[iii]<x[iii] )
	    return 0;
	}
      return x.size()!=y.size();
    }
}


template<class T> const void Array<T>:: errorAccess(int n) const
{
  cerr 	<< "ERROR: Access to array element " << n 
	<< " (" << maxWritten << "," << realSize << "," << (void*)p << " " << a << ")\n";
  cout <<  "ERROR: Access to array element " << n 
       << " (" << maxWritten << "," << realSize << "," << (void*)p << "  " << a << ")\n";
  massert(0);
#ifndef DEBUG
  abort();
#endif
}

template<class T> ostream& operator<<(ostream&o,const Array<T>&a)
{
  o << "Array(" << a.size() << "," << a.autoexpand() << "){ ";
  for(int iii=0;iii<a.size();iii++)
    o << " " << iii<< ":" << a[iii]<<";";
  return o << "}\n";
}

template<class T> istream& operator>>(istream&in, Array<T>&)
{return in;}

template<class T> int Hash(const Array<T>&a)
{
  int n=0;
  for(int iii=0;iii<a.size();iii++)
    n+=Hash(a[iii])*(iii+1);
  return n+a.size()*47;
}
template<class T> void Array<T>::copy(T *aa,const T *bb,int n)
{
  for(int iii=0;iii<n;iii++)
    aa[iii]=bb[iii];
}
template<class T> void Array<T>::copy(T *aa,T *bb,int n)
{
  for(int iii=0;iii<n;iii++)
    aa[iii]=bb[iii];
}

template<class T> void Array<T>::_expand()
{
#ifdef VERY_ARRAY_DEBUG
  cout << "FREE ARRAY because of _expand: " << this << " " << realSize<<" "<<(void*)p << endl;
#endif			
  T *oldp=p;
  int oldsize=realSize;
  realSize=realSize*2+1;
  p=new T[realSize];
  copy(p,oldp,oldsize);
  delete [] oldp;
#ifdef VERY_ARRAY_DEBUG
  cout << "NEW ARRAY because of _expand: " << this << " " << realSize<<" "<<(void*)p << endl;
#endif			
}

template<class T> int Array<T>::findMax() const
{
  if( size()==0 )
    return -1;
  else
    {
      int maxPos=0;
      for(int iii=1;iii<size();iii++)
	if( (*this)[maxPos]<(*this)[iii] )
	  maxPos=iii;
      return maxPos;
    }
}
template<class T> int Array<T>::findMin() const
{
  if( size()==0 )
    return -1;
  else
    {
      int minPos=0;
      for(int iii=1;iii<size();iii++)
	if( (*this)[iii]<(*this)[minPos] )
	  minPos=iii;
      return minPos;
    }
}

#endif
