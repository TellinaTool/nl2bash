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
Vector: checked vector implementation

Franz Josef Och (30/07/99)
--*/
#ifndef ARRAY_H_DEFINED
#define ARRAY_H_DEFINED
#include "mystl.h"
#include <algorithm>
#include <string>
#include <utility>
#include <functional>
#include <cassert>


#ifdef NDEBUG

#include <vector>
#define Vector vector
template<class T> ostream& operator<<(ostream&o, const Vector<T>&a)
{
  o << "Vector(" << a.size() << "){ ";
  for(unsigned int iii=0;iii<a.size();iii++)
    o << " " << iii<< ": " << a[iii]<<" ;";
  return o << "}\n";
}

#else

#define ARRAY_DEBUG
#define memo_del(a, b)
#define memo_new(a)

template<class T> class Vector
{
 private:
  T *p;                  	
  int realSize;
  int maxWritten;

  void copy(T *a, const T *b, int n);
  void copy(T *a, T *b, int n);
  void _expand();
		
 public:
  Vector() 
    : p(0), realSize(0), maxWritten(-1)
    {
#ifdef VERY_ARRAY_DEBUG
      cout << "MAKE ARRAY: " << this<<" "<<(void*)p << '\n';
#endif
    }
  Vector(const Vector<T> &x)
    : p(new T[x.maxWritten+1]), realSize(x.maxWritten+1), maxWritten(x.maxWritten)
    {
      memo_new(p);
      copy(p, x.p, realSize);
#ifdef VERY_ARRAY_DEBUG
      cout << "MAKE ARRAY copy: " << this << " " << realSize <<" "<<(void*)p<< '\n';
#endif
    }
  explicit Vector(int n)
    : p(new T[n]), realSize(n), maxWritten(n-1)
    {
      memo_new(p);
#ifdef VERY_ARRAY_DEBUG
      cout << "MAKE ARRAY with parameter n: " << this << " " << realSize<<" "<<(void*)p << '\n';
#endif			
    }
  Vector(int n, const T&_init)
    : p(new T[n]), realSize(n), maxWritten(n-1)
    {
      memo_new(p);
      for(int iii=0;iii<n;iii++)p[iii]=_init;
#ifdef VERY_ARRAY_DEBUG
      cout << "MAKE ARRAY with parameter n and init: " << this << " " << realSize<<" "<<(void*)p << '\n';
#endif			
    }
  
  ~Vector() 
    { 
#ifdef VERY_ARRAY_DEBUG
      cout << "FREE ARRAY: " << this << " " << realSize<<" "<<(void*)p << '\n';
#endif			
      delete [] p;
      memo_del(p, 1);
#ifndef NDEBUG
      p=0;realSize=-1;maxWritten=-1;
#endif
    }
  
  Vector<T>& operator=(const Vector<T>&x)
    {
      if( this!= &x )
	{
#ifdef VERY_ARRAY_DEBUG
	  cout << "FREE ARRAY because of operator=: " << this << " " << realSize<<" "<<(void*)p << '\n';
#endif	
	  delete [] p;
	  memo_del(p, 1);
	  realSize = x.maxWritten+1;
	  maxWritten = x.maxWritten;
	  p = new T[realSize]; 
	  memo_new(p);
	  copy(p, x.p, realSize);
#ifdef VERY_ARRAY_DEBUG
	  cout << "NEW ARRAY because of operator=: " << this << " " << realSize<<" "<<(void*)p << '\n';
#endif			
	}
      return *this;
    }
  
  Vector<T>& operator=(Vector<T>&x)
    {
      if( this!= &x )
	{
#ifdef VERY_ARRAY_DEBUG
	  cout << "FREE ARRAY because of operator=: " << this << " " << realSize<<" "<<(void*)p << '\n';
#endif			
	  delete [] p;
	  memo_del(p, 1);
	  realSize = x.maxWritten+1;
	  maxWritten = x.maxWritten;
	  p = new T[realSize]; 
	  memo_new(p);
	  copy(p, x.p, realSize);
#ifdef VERY_ARRAY_DEBUG
	  cout << "NEW ARRAY because of operator=: " << this << " " << realSize<<" "<<(void*)p << '\n';
#endif			
	}
      return *this;
    }
  
  void allowAccess(int n) 
    { 
      while( realSize<=n )
	_expand(); 
      maxWritten=max(maxWritten, n);
      assert( maxWritten<realSize );
    }
  void resize(int n)
    {
      while( realSize<n ) 
	_expand(); 
      maxWritten=n-1;
    }
  void clear()
    {
      resize(0);
    }
  void reserve(int n)
    {
      int maxOld=maxWritten;
      resize(n);
      maxWritten=maxOld;
    }
  void sort(int until=-1)
    {
      if( until== -1 ) until=size();
      std::sort(p, p+until);
    }
  void invsort(int until=-1)
    {
      if( until== -1 ) until=size();
      std::sort(p, p+until, greater<T>());      
    }
  void init(int n, const T&_init)
    {
#ifdef VERY_ARRAY_DEBUG
      cout << "FREE ARRAY because of init: " << this << " " << realSize<<" "<<(void*)p << '\n';
#endif			
      delete []p;
      memo_del(p, 1);
      p=new T[n];
      memo_new(p);
      realSize=n;
      maxWritten=n-1;
      for(int iii=0;iii<n;iii++)p[iii]=_init;
#ifdef VERY_ARRAY_DEBUG
      cout << "NEW ARRAY because of init: " << this << " " << realSize<<" "<<(void*)p << '\n';
#endif			
    }
  inline unsigned int size() const
    {assert( maxWritten<realSize );
    return maxWritten+1;}
  inline int low() const
    { return 0; }
  inline int high() const
    { return maxWritten; }
  int findMax() const;
  int findMin() const;
  void errorAccess(int n) const;
  inline T*getPointerToData(){return p;}
  inline T*begin(){return p;}
  inline T*end(){return p+maxWritten+1;}
  inline T& operator[](int n)
    { 
#ifndef NDEBUG
      if( n<0 || n>maxWritten )
	errorAccess(n);
#endif
      return p[n];
    }
  inline const T& operator[](int n) const 
    { 
#ifndef NDEBUG
      if(n<0 || n>maxWritten )
	errorAccess(n);
#endif
      return p[n]; 
    }
  inline const T& get(int n) const 
    { 
#ifndef NDEBUG
      if(n<0 || n>maxWritten )
	errorAccess(n);
#endif      
      return p[n]; 
    }
  const T&top(int n=0) const
    {return (*this)[maxWritten-n];}
  T&top(int n=0)
    {return (*this)[maxWritten-n];}
  const T&back(int n=0) const
    {return (*this)[maxWritten-n];}
  T&back(int n=0)
    {return (*this)[maxWritten-n];}
  T&push_back(const T&x)
    {     
      allowAccess(maxWritten+1);
      (*this)[maxWritten]=x;
      return top();
    }
    /*
  bool writeTo(ostream&out) const
    {
      out << "Vector ";
      out << size() << " ";
      out << a << '\n';
      for(int iv=0;iv<=maxWritten;iv++)
	{
	  writeOb(out, (*this)[iv]);
	  out << '\n';
	}
      return 1;
    }
    */
    
  bool readFrom(istream&in)
    {
      string s;
      if( !in )
	{
	  cerr << "ERROR(Vector): file cannot be opened.\n";
	  return 0;
	}
      in >> s;
      if( !(s=="Vector") )
	{
	  cerr << "ERROR(Vector): Vector!='"<<s<<"'\n";
	  return 0;
	}
      int biggest;
      in >> biggest;
      in >> a;
      resize(biggest);
      for(int iv=0;iv<size();iv++)
	{
	  readOb(in, (*this)[iv]);
	}
      return 1;
    }
};

template<class T> bool operator==(const Vector<T> &x, const Vector<T> &y)
{
  if( &x == &y )
    return 1;
  else
    {
      if( y.size()!=x.size() )
	return 0;
      else
	{
	  for(unsigned int iii=0;iii<x.size();iii++)
	    if( !(x[iii]==y[iii]) )
	      return 0;
	  return 1;
	}
    }
}
template<class T> bool operator!=(const Vector<T> &x, const Vector<T> &y)
{
  return !(x==y);
}

template<class T> bool operator<(const Vector<T> &x, const Vector<T> &y)
{
  if( &x == &y )
    return 0;
  else
    {
      if( y.size()<x.size() )
	return !(y<x);
      for(int iii=0;iii<x.size();iii++)
	{
	  assert( iii!=y.size() );
	  if( x[iii]<y[iii] )
	    return 1;
	  else if( y[iii]<x[iii] )
	    return 0;
	}
      return x.size()!=y.size();//??
    }
}


template<class T> void Vector<T>:: errorAccess(int n) const
{
  cerr 	<< "ERROR: Access to array element " << n 
	<< " (" << maxWritten << ", " << realSize << ", " << (void*)p << ")\n";
  cout <<  "ERROR: Access to array element " << n 
       << " (" << maxWritten << ", " << realSize << ", " << (void*)p << ")\n";
  assert(0);
#ifndef DEBUG
  abort();
#endif
}

template<class T> ostream& operator<<(ostream&o, const Vector<T>&a)
{
  o << "Vector(" << a.size() << "){ ";
  for(unsigned int iii=0;iii<a.size();iii++)
    o << " " << iii<< ": " << a[iii]<<" ;";
  return o << "}\n";
}

template<class T> istream& operator>>(istream&in, Vector<T>&)
{return in;}

template<class T> int Hash(const Vector<T>&a)
{
  int n=0;
  for(int iii=0;iii<a.size();iii++)
    n+=Hash(a[iii])*(iii+1);
  return n+a.size()*47;
}
template<class T> void Vector<T>::copy(T *aa, const T *bb, int n)
{
  for(int iii=0;iii<n;iii++)
    aa[iii]=bb[iii];
}
template<class T> void Vector<T>::copy(T *aa, T *bb, int n)
{
  for(int iii=0;iii<n;iii++)
    aa[iii]=bb[iii];
}

template<class T> void Vector<T>::_expand()
{
#ifdef VERY_ARRAY_DEBUG
  cout << "FREE ARRAY because of _expand: " << this << " " << realSize<<" "<<(void*)p << '\n';
#endif			
  T *oldp=p;
  int oldsize=realSize;
  realSize=realSize*2+1;
  p=new T[realSize];
  memo_new(p);
  copy(p, oldp, oldsize);
  delete [] oldp;
  memo_del(oldp, 1);
#ifdef VERY_ARRAY_DEBUG
  cout << "NEW ARRAY because of _expand: " << this << " " << realSize<<" "<<(void*)p << '\n';
#endif			
}

template<class T> int Vector<T>::findMax() const
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
template<class T> int Vector<T>::findMin() const
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

#endif
