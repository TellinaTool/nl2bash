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



#ifndef myleda_HEADER_defined
#define myleda_HEADER_defined
using namespace std;
#include "myassert.h"


#if defined(USE_LEDA_array)||defined(USE_LEDA)
#include <LEDA/array.h>
#else

#include "FixedArray.h"

template<class T>
class leda_array : public FixedArray<T>
{
public:
  leda_array() {}
  leda_array(int n) : FixedArray<T>(n) {}
};
#endif


#if defined(USE_LEDA_set)||defined(USE_LEDA)
#include <LEDA/set.h>
#define forall_set(a,b,c) forall(b,c)
#else
#include <set>
template<class T>
class leda_set : public set<T>
{
public:
  bool member(const T&m) const
    { return this->count(m)!=0; }
  void del(const T&m)
    { this->erase(m); }
};
#define forall_set(a,b,c) for(a::iterator __i__=c.begin();__i__!=c.end()&&((b=*__i__),1);++__i__)
template<class T>
leda_set<T> operator&(const leda_set<T>&a,const leda_set<T>&b)
{
  leda_set<T>c;
  insert_iterator<set<T> > iter(c,c.begin());
  set_intersection(a.begin(),a.end(),b.begin(),b.end(),iter);
  return c;
}
template<class T>
leda_set<T> operator-(const leda_set<T>&a,const leda_set<T>&b)
{
  leda_set<T>c;
  insert_iterator<set<T> > iter(c,c.begin());
  set_difference(a.begin(),a.end(),b.begin(),b.end(),iter);
  return c;
}

#endif


#if defined(USE_LEDA_d_array)||defined(USE_LEDA)
#include <LEDA/d_array.h>
#define forall_defined_d(a,b,c,d) forall_defined(c,d)
#define forall_d(a,b,c,d) forall(c,d)
#else
#include <map>
template<class A,class B>
class leda_d_array : public map<A,B>
{
private:
  B init;
public:
  bool defined(const A&a) const
    { return find(a)!=this->end(); }
  const B&operator[](const A&a)const
    { 
      typename map<A,B>::const_iterator pos=find(a);
      iassert(pos!=this->end());
      if( pos==this->end() )
	return init;
      else
	return pos->second;
    }
  B&operator[](const A&a)
    { 
      typename map<A,B>::iterator pos=find(a);
      if( pos==this->end() )
	{
	  insert(map<A,B>::value_type(a,init));
	  pos=find(a);
	  iassert(pos!=this->end());
	}
      return pos->second;
    }
};

#define forall_defined_d(a,b,c,d) for(typename leda_d_array<a,b>::const_iterator __ii__=(d).begin();__ii__!=(d).end()&&((c=__ii__->first),1) ;++__ii__)
#define forall_d(a,b,c,d)         for(typename leda_d_array<a,b>::const_iterator __ii__=(d).begin();__ii__!=(d).end()&&((c=__ii__->second),1);++__ii__)
#endif


#if defined(USE_LEDA_h_array)||defined(USE_LEDA)
#include <LEDA/h_array.h>
#define forall_defined_h(a,b,c,d) forall_defined(c,d)
#define forall_h(a,b,c,d) forall(c,d)
#else

double used_time();
#if 0

#include "my_hashmap.h"
#define leda_h_array my_hashmap

#else

template<class T>
class my_hash
{
public:
  int operator()(const T&t)const {return Hash(t);}
};

inline int Hash(int value) { return value; }
#define MY_HASH_BASE hash_map<A,B,my_hash<A> >

#if __GNUC__>2 
#include <ext/hash_map>
using __gnu_cxx::hash_map;
using __gnu_cxx::hash;
#else
#include <hash_map>
#endif
template<class A,class B>
class leda_h_array : public MY_HASH_BASE
{
private:
  B init;
public:
  leda_h_array() {}
  leda_h_array(const B&_init)
    : MY_HASH_BASE(),init(_init) {}
  bool defined(const A&a) const
    { return find(a)!=this->end(); }
  const B&operator[](const A&a)const
    { 
      typename MY_HASH_BASE::const_iterator pos=this->find(a);
      
      if( pos==this->end() )
	return init;
      else
	return pos->second;
    }
  B&operator[](const A&a)
    { 
      typename MY_HASH_BASE::iterator pos=this->find(a);
      if( pos==this->end() )
	{
	  insert(typename MY_HASH_BASE::value_type(a,init));
	  pos=this->find(a);
	  iassert(pos!=this->end());
	}
      return pos->second;
    }
};

#define forall_defined_h(a,b,c,d) for(typename leda_h_array<a,b>::const_iterator __jj__=(d).begin();__jj__!=(d).end()&&((c=__jj__->first),1); ++__jj__)
#define forall_defined_h2(a,b,c,d) for(leda_h_array<a,b>::const_iterator __jj__=(d).begin();__jj__!=(d).end()&&((c=__jj__->first),1); ++__jj__)
#define forall_h(a,b,c,d)         for(typename leda_h_array<a,b>::const_iterator __jjj__=(d).begin();__jjj__!=(d).end()&&((c=__jjj__->second),1);++__jjj__)

#endif

#endif



template<class T> int compare(const T&a,const T&b)
{if(a==b)return 0; else if(a<b) return -1; else return 1;}

template<class T,class U>
ostream & operator<<(ostream&out,const leda_h_array<T,U>&w)
{
  T t;
  bool makeNl=0;
  out << "h_array{";
  forall_defined_h(T,U,t,w)
    {
      if( makeNl )
	out << "\n       ";
      out << "EL:" << t << " INH:" << w[t] << ".";
      makeNl=1;
    }
  return out << "}\n";
}
template<class T,class U>
ostream & operator<<(ostream&out,const leda_d_array<T,U>&w)
{
  T t;
  bool makeNl=0;
  out << "h_array{";
  forall_defined_h(T,U,t,w)
    {
      if( makeNl )
	out << "\n       ";
      out << "EL:" << t << " INH:" << w[t] << ".";
      makeNl=1;
    }
  return out << "}\n";
}

template<class T>
ostream&printSet(ostream&out,const leda_set<T>&s)
{
  bool first=1;
  T t;
  out << "{";
  forall_set(typename set<T>,t,s)
    {
      if( first==0 )
	out << ", ";
      out << t;
      first=0;
    }
  return out << "}\n";
}

template<class T,class U>
istream & operator>>(istream&in,leda_h_array<T,U>&)
{
  return in;
}

template<class A,class B>
bool operator==(const leda_h_array<A,B>&p1,const leda_h_array<A,B>&p2)
{
  A v;
  forall_defined_h(A,B,v,p1)
    if( !( p1[v]==p2[v]) ) return 0;
  forall_defined_h(A,B,v,p2)
    if( !( p1[v]==p2[v]) ) return 0;
  return 1; 
}
template<class A,class B>
bool operator==(const leda_d_array<A,B>&p1,const leda_d_array<A,B>&p2)
{
  A v;
  forall_defined_d(A,B,v,p1)
    if( !( p1[v]==p2[v]) ) return 0;
  forall_defined_d(A,B,v,p2)
    if( !( p1[v]==p2[v]) ) return 0;
  return 1; 
}




#endif
