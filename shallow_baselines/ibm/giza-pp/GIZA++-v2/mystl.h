/* ---------------------------------------------------------------- */
/* Copyright 1998 (c) by RWTH Aachen - Lehrstuhl fuer Informatik VI */
/* Franz Josef Och                                                  */
/* ---------------------------------------------------------------- */
#ifndef MY_STL_H_DEFINED
#define MY_STL_H_DEFINED

#include <string>
using namespace std;
#ifdef USE_STLPORT
#ifdef __STL_DEBUG
using namespace _STLD;
#else
using namespace _STL;
#endif
#endif

#include "myassert.h"
#include <string>
#include <utility>

#if __GNUC__==2
#include <hash_map>
#elsif __GNUC__==3
#include <ext/hash_map>
using __gnu_cxx::hash_map;
#else
#include <tr1/unordered_map>
#define hash_map unordered_map
using namespace std::tr1;
#endif

#include <vector>
#include <iostream>
#include "mymath.h"
#include "Array2.h"

#define over_string(a,i) for(unsigned int i=0;i<a.length();i++)
#define over_array(a,i) for(i=(a).low();i<=(a).high();i++)
#define backwards_array(a,i) for(i=(a).high();i>=(a).low();i--)
#define over_arr(a,i) for(int i=(a).low();i<=(a).high();i++)
#define over_arrMAX(a,i,max) for(int i=(a).low();i<=min((a).high(),max-1);i++)
#define backwards_arr(a,i) for(int i=(a).high();i>=(a).low();i--)

extern double n1mult,n2mult,n3mult;

inline double realProb(int n1,int n2)
{
  massert(n1<=n2);
  iassert(n1>=0&&n2>0);
  if(n2==0)n2=1;
  return ((double)n1)/(double)n2;
}

inline double verfProb(int n1,int n2)
{
  double prob = realProb(n1,n2);
  if( n1==1 )return prob*n1mult;
  else if( n1==2 )return prob*n2mult;
  else if( n1==3 )return prob*n3mult;
  else 
  return prob;
}

inline bool prefix(const string&x,const string&y)
{
  if(y.size()>x.size() )
    return 0;
  for(unsigned int i=0;i<y.size();++i)
    if( y[i]!=x[i] )
      return 0;
  return 1;
}


/*template<class T>
int lev(const T&s1,const T&s2)
{
  Array2<int,vector<int> > a(s1.size()+1,s2.size()+1,1000);
  Array2<pair<int,int>,vector<pair<int,int> > > back(s1.size()+1,s2.size()+1,pair<int,int>(0,0));
  for(unsigned int i=0;i<=s1.size();i++)
    for(unsigned int j=0;j<=s2.size();j++)
      {
	if( i==0&&j==0 )
	  a(i,j)=0;
	else
	  {
	    int aDEL=100,aINS=100,aSUB=100;
	    if(i>0)
	      aDEL=a(i-1,j)+1;
	    if(j>0)
	      aINS=a(i,j-1)+1;
	    if(i>0&&j>0)
	      aSUB=a(i-1,j-1)+ !(s1[i-1]==s2[j-1]);
	    if( aSUB<=aDEL && aSUB<=aINS )
	      {
		a(i,j)=aSUB;
		back(i,j)=pair<int,int>(i-1,j-1);
	      }
	    else if( aDEL<=aSUB && aDEL<=aINS )
	      {
		a(i,j)=aDEL;
		back(i,j)=pair<int,int>(i-1,j);
	      }
	    else
	      {
		a(i,j)=aINS;
		back(i,j)=pair<int,int>(i,j-1);
	      }
	  }
      }
  return a(s1.size(),s2.size());
}

template<class T>
float rel_lev(const T&s1,const T&s2)
{
  if( s1.size()==0 )
    return s2.size()==0;
  else
    return min(1.0,lev(s1,s2)/(double)s1.size());
}*/

template<class V> int Hash(const pair<V,V>&a) 
{ return Hash(a.first)+13001*Hash(a.second); }

template<class T1,class T2>
ostream& operator<<(ostream &out,const pair<T1,T2> &ir)
{ 
  out << "(" << ir.first << "," << ir.second << ")";
  return out;
} 

inline int Hash(const string& s)
{
  int sum=0;
  string::const_iterator i=s.begin(),end=s.end();
  for(;i!=end;i++)sum=5*sum+(*i);
  return sum;
}
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
  if(x.a<y.a)return 1;
  if(y.a<x.a)return 0;
  if(x.b<y.b)return 1;
  if(y.b<x.b)return 0;
  if(x.c<y.c)return 1;
  if(y.c<x.c)return 0;
  return 0;
}

double used_time();

template<class T>
class my_hash
{
public:
  int operator()(const T&t)const {return Hash(t);}
};

inline int Hash(int value) { return value; }
#define MY_HASH_BASE hash_map<A,B,my_hash<A> >

template<class A,class B>
class leda_h_array : public MY_HASH_BASE
{
private:
  B init;
public:
  leda_h_array() : MY_HASH_BASE() {}
  leda_h_array(const B&_init)
    : MY_HASH_BASE(),init(_init) {}
  bool defined(const A&a) const
    { return find(a)!=this->end(); }
  const B&operator[](const A&a)const
    { 
      typename MY_HASH_BASE::const_iterator pos=find(a);
      if( pos==this->end() )
	return init;
      else
	return pos->second;
    }
  B&operator[](const A&a)
    { 
      typename MY_HASH_BASE::iterator pos=find(a);
      if( pos==this->end() )
	{
	  insert(MY_HASH_BASE::value_type(a,init));
	  pos=find(a);
	  iassert(pos!=this->end());
	}
      return pos->second;
    }
  const B&initValue()const
    {return init;}
};

#define forall_defined_h(a,b,c,d) for(typename leda_h_array<a,b>::const_iterator __jj__=(d).begin();__jj__!=(d).end()&&((c=__jj__->first),1); ++__jj__)
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

template<class T>
int count_elements(T a,T b)
{
  int c=0;
  while(a!=b)
    {
      a++;
      c++;
    }
  return c;
}

template<class T>
T normalize_if_possible_with_increment(T*a,T*b,int increment)
{
  T sum=0;
  for(T*i=a;i!=b;i+=increment)
    sum+=*i;
  if( sum )
    for(T*i=a;i!=b;i+=increment)
      *i/=sum;
  else
    {
      T factor=increment/(b-a);
      for(T*i=a;i!=b;i+=increment)
	*i=factor;
    }
  return sum;
}

template<class T>
inline int m_comp_3way(T a,T b,int n)
{
  int _n=0;
  while((_n++<n) && a && b)
    {
      const typename T::value_type &aa=*a;
      const typename T::value_type &bb=*b;
      if( aa<bb )return 1;
      if( bb<aa )return -1;
      ++a;
      ++b;
    }
  return 0;
}

template<class T>
void smooth_standard(T*a,T*b,double p)
{
  int n=b-a;
  if( n==0 ) 
    return;
  double pp=p/n;
  for(T*i=a;i!=b;++i)
    *i = (1.0-p)*(*i)+pp;
}

template<class T>
const T *conv(typename vector<T>::const_iterator i)
{
  return &(*i);
}
#if __GNUC__>2
template<class T>
T *conv(typename vector<T>::iterator i)
{
  return &(*i);
}
#endif

/*template<class T>
const T *conv(const T*x)
{
  return x;
}*/
template<class T>
T *conv(T*x)
{
  return x;
}

#endif
