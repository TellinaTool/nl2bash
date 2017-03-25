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



#ifndef MY_STL_H_DEFINED
#define MY_STL_H_DEFINED
#include <string>
#include <utility>
#if __GNUC__>2 
#include <ext/hash_map>
using __gnu_cxx::hash_map;
using __gnu_cxx::hash;
#else
#include <hash_map>
#endif
#include <cmath>

using namespace std;

#define over_string(a,i) for(unsigned int i=0;i<a.length();i++)

inline int Hash(const string& s)
{
  int sum=0;
  string::const_iterator i=s.begin(),end=s.end();
  for(;i!=end;i++)sum=5*sum+(*i);
  return sum;
}

template<class V> int Hash(const pair<V,V>&a) 
{ return Hash(a.first)+4*Hash(a.second); }

template<class T1,class T2>
istream& operator>>(istream &in,pair<T1,T2> &ir)
{
 char c;
 
 do in.get(c); while (in && isspace(c));
 
 if (!in) return in;
 
 if (c != '(') in.putback(c);
 
 in >> ir.first;
 
 do in.get(c); while (isspace(c));
 if (c != ',') in.putback(c);
 
 in >> ir.second; 
 
 do in.get(c); while (c == ' ');
 if (c != ')') in.putback(c);
 
 return in; 
}

template<class T1,class T2>
ostream& operator<<(ostream &out,const pair<T1,T2> &ir)
{ 
  out << "(" << ir.first << "," << ir.second << ")";
  return out;
} 

void printSpaces(ostream&out,int n);
void mysplit(const string &s,string &s1,string &s2);
string untilChar(const string&s,char c);

template<class A,class B,class C>
class tri
{
public:
  A a;
  B b;
  C c;
  tri(){};
  tri(const A&_a,const B&_b,const C&_c)
    : a(_a),b(_b),c(_c) {}
};
template<class A,class B,class C>
bool operator==(const tri<A,B,C>&x,const tri<A,B,C>&y)
{ return x.a==y.a&&x.b==y.b&&x.c==y.c;}

template<class A,class B,class C>
bool operator<(const tri<A,B,C>&x,const tri<A,B,C>&y)
{
  if(x.a<y.a)
    return 1;
  if(y.a<x.a)
    return 0;

  if(x.b<y.b)
    return 1;
  if(y.b<x.b)
    return 0;

  if(x.c<y.c)
    return 1;
  if(y.c<x.c)
    return 0;
  return 0;
}

#endif
