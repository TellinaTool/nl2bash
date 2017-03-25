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




#ifndef FIXARRAY_H_DEFINED
#define FIXARRAY_H_DEFINED
#include <iostream>
#include <string>
#include <functional>

template<class T>
bool writeOb(ostream&out,const T&f)
{ 
  out << f << " "; 
  return 1;
}

template<class T>
bool readOb(istream&in,T&f)
{ 
  in >> f;
  char c;
  in.get(c);
  massert(c==' ');
  return 1;
}

template<class T>
bool writeOb(ostream&out,const string &s,const T&f)
{ 
  out << s << " " << f << " "; 
  return 1;
}
template<class T>
bool readOb(istream&in,const string&s,T&f)
{ 
  string ss;
  in >> ss;
  if( s!=ss )
    {
      cerr << "ERROR: readOb should be '" << s << "' and is '" << ss << "'" << endl;
      return 0;
    }
  in >> f; 
  char c;
  in.get(c);
  massert(c==' ');
  return 1;
}

template<class T> class FixedArray
{
 private:  
  void copy(T *aa,const T *bb,int nnn)
    {for(int iii=0;iii<nnn;iii++)aa[iii]=bb[iii];}
  
 public:
  T *p;                       	
  int realSize;
  FixedArray() 
    : p(0),realSize(0){}
  FixedArray(const FixedArray<T> &x)
    : p(new T[x.realSize]),realSize(x.realSize) {copy(p,x.p,realSize);}
  explicit FixedArray(int n)
    : p(new T[n]),realSize(n){}
  FixedArray(int n,const T&_init)
    : p(new T[n]),realSize(n){for(int z=0;z<n;z++)p[z]=_init;}
  FixedArray(const FixedArray&f,const T&t)
    : p(new T[f.size()+1]),realSize(f.size()+1){for(int z=0;z<f.size();z++)p[z]=f[z];p[f.size()]=t;}
  ~FixedArray() 
    { delete [] p;p=0;realSize=-1;}
  
  FixedArray<T>& operator=(const FixedArray<T>&x)
    {
      if( this!= &x )
	{
	  delete [] p;
	  realSize = x.realSize;
	  p = new T[x.realSize]; 
	  copy(p,x.p,realSize);
	}
      return *this;
    }
  void resize(int n)
    {
      if( n<=realSize )
	shrink(n);
      else
	{
	  T*np=new T[n];
	  copy(np,p,realSize);
	  delete []p;
	  p=np;
	  realSize=n;
	}
    }
  void shrink(int n)
    {
      assert(n<=realSize);
      realSize=n;
    }
  void init(int n,const T&_init)
    {
      delete []p;
      p=new T[n];
      realSize=n;
      for(int l=0;l<n;l++)p[l]=_init;
    }
  inline const T&top(int n=0) const
    {return (*this)[realSize-1-n];}
  inline int size() const 
    {return realSize;}

  inline T*begin(){ return p; }
  inline T*end(){ return p+realSize; }

  inline const T*begin()const{ return p; }
  inline const T*end()const{return p+realSize;}

  inline int low() const 
    {return 0;}
  inline int high() const 
    {return realSize-1;}
  const void errorAccess(int n) const;
  
  inline T& operator[](int n)
    { 
      return p[n];
    }
  inline const T& operator[](int n) const 
    { 
      return p[n]; 
    }
  bool writeTo(ostream&out) const
    {
      out << "FixedArray ";
      out << size() << " ";
      for(int a=0;a<size();a++)
	{
	  writeOb(out,(*this)[a]);
	  out << " ";
	}
      out << endl;
      return 1;
    }
  bool readFrom(istream&in)
    {
      string s;
      if( !in )
	{
	  cerr << "ERROR(FixedArray): file cannot be opened.\n";
	  return 0;
	}
      in >> s;
      if( !(s=="FixedArray") )
	{
	  cerr << "ERROR(FixedArray): FixedArray!='"<<s<<"'\n";
	  return 0;
	}
      int biggest;
      in >> biggest;
      resize(biggest);
      for(int a=0;a<size();a++)
	readOb(in,(*this)[a]);
      return 1;
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
  int binary_locate(const T&t)
    {
      T*ppos=std::lower_bound(p,p+size(),t);
      int pos=ppos-p;
      if( pos>=-1&&pos<size() )
	return pos;
      else
	return -1;
    }
  int binary_search(const T&t)
    {
      T*ppos=std::lower_bound(p,p+size(),t);
      int pos=ppos-p;
      if( pos>=0&&pos<size()&& *ppos==t )
	return pos;
      else
	return -1;
    }
  typedef T* iterator;
  typedef const T* const_iterator;
};

template<class T> bool operator<(const FixedArray<T> &x, const FixedArray<T> &y)
{
  return lexicographical_compare(x.begin(),x.end(),y.begin(),y.end());
  
}


template<class T>  bool operator==(const FixedArray<T> &x, const FixedArray<T> &y)
{
  if( &x == &y )return 1;
  const int s = x.size();
  if( s !=y.size() )return 0;
  for(int iii=0;iii<s;iii++)
    if( !(x.p[iii]==y.p[iii]) )
      return 0;
  return 1;
}

template<class T> int Hash(const FixedArray<T>&a)
{
  int n=0;
  const int s=a.size();
  for(int iii=0;iii<s;iii++)
    n=13*n+Hash(a.p[iii]);
  return n;
}

template<class T> const void FixedArray<T>:: errorAccess(int n) const
{
  massert(0);
  cerr 	<< "ERROR: Access to array element " << n 
	<< " (" << realSize << "," << (void*)p << ")\n";
}
	
template<class T> ostream& operator<<(ostream&o,const FixedArray<T>&a)
{
  o << "FixedArray(" << a.size() << "){ ";
  for(int iii=0;iii<a.size();iii++)
    o << " " << iii<< ":" << a[iii]<<";";
  return o << "}\n";
}

template<class T> istream& operator>>(istream&in, FixedArray<T>&)
{ return in;}

template<class T> FixedArray<T> operator+(const FixedArray<T>&a,const FixedArray<T>&b)
{
  massert(a.size()==b.size());
  FixedArray<T> x(a.size());
  for(int iii=0;iii<a.size();iii++)
    x[iii]=a[iii]+b[iii];
  return x;
}
template<class T> FixedArray<T> operator|(const FixedArray<T>&aaa,const FixedArray<T>&bbb)
{
  iassert(aaa.size()==bbb.size());

  FixedArray<T> xxx(aaa.size());
  for(int iii=0;iii<aaa.size();iii++)
    xxx.p[iii]=aaa.p[iii]||bbb.p[iii];
  return xxx;
}

#endif



