/*

Copyright (C) 1999,2000,2001  Franz Josef Och (RWTH Aachen - Lehrstuhl fuer Informatik VI)

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
#ifndef HMM_TABLES_H_ASDF_DEFINED
#define HMM_TABLES_H_ASDF_DEFINED
#include "FlexArray.h"

#include "Array.h"
#include <map>
#include "mymath.h"

template<class T>
T normalize_if_possible(T*a,T*b)
{
  T sum=0;
  for(T*i=a;i!=b;++i)
    sum+=*i;
  if( sum )
    for(T*i=a;i!=b;++i)
      *i/=sum;
  else
    fill(a,b,1.0/(b-a));
  return sum;
}

extern short CompareAlDeps;
template<class CLS>
class AlDeps
{
 public:
  int englishSentenceLength;
  CLS classPrevious;
  int previous;
  int j;
  CLS Cj;
  AlDeps(int l,int p=0,int _j=0,CLS s1=0,CLS _Cj=0)
    : englishSentenceLength(l),classPrevious(s1),previous(p),j(_j),Cj(_Cj)
    {}
  friend bool operator<(const AlDeps&x,const AlDeps&y)
  {
    if( (CompareAlDeps&1) && x.englishSentenceLength<y.englishSentenceLength ) return 1;
    if( (CompareAlDeps&1) && y.englishSentenceLength<x.englishSentenceLength ) return 0;
    if( (CompareAlDeps&2) && x.classPrevious<y.classPrevious ) return 1;
    if( (CompareAlDeps&2) && y.classPrevious<x.classPrevious ) return 0;
    if( (CompareAlDeps&4) && x.previous<y.previous ) return 1;
    if( (CompareAlDeps&4) && y.previous<x.previous ) return 0;
    if( (CompareAlDeps&8) && x.j<y.j ) return 1;
    if( (CompareAlDeps&8) && y.j<x.j ) return 0;
    if( (CompareAlDeps&16) && x.Cj<y.Cj ) return 1;
    if( (CompareAlDeps&16) && y.Cj<x.Cj ) return 0;
    return 0;
  }
  friend bool operator==(const AlDeps&x,const AlDeps&y)
  { return !( x<y || y<x );  }
};

template<class CLS>
class Hash_AlDeps
{
 public:
  unsigned 
    int 
    operator()
    (const AlDeps<CLS>&x)
    const
    {
      unsigned int hash=0;
      if( (CompareAlDeps&1) ) { hash=hash+x.englishSentenceLength;hash*=31;}
      if( (CompareAlDeps&2) ) { hash=hash+x.classPrevious;hash*=31;}
      if( (CompareAlDeps&4) ) { hash=hash+x.previous;hash*=31;}
      if( (CompareAlDeps&8) ) { hash=hash+x.j;hash*=31;}
      if( (CompareAlDeps&16) ) { hash=hash+x.Cj;hash*=31;}
      return hash;
      
    }
};

template<class CLS,class MAPPERCLASSTOSTRING>
class HMMTables
{
 protected:
  double probabilityForEmpty;
  bool updateProbabilityForEmpty;
  hash_map<int,Array<double> > init_alpha;
  hash_map<int,Array<double> > init_beta;
  map<AlDeps<CLS>,FlexArray<double> > alProb;
  map<AlDeps<CLS>,FlexArray<double> > alProbPredicted;
  int globalCounter;
  double divSum;
  double p0_count,np0_count;
  const MAPPERCLASSTOSTRING*mapper1;
  const MAPPERCLASSTOSTRING*mapper2;
 public:
  const HMMTables<CLS,MAPPERCLASSTOSTRING>*getThis()const {return this;}
  HMMTables(double _probForEmpty,const MAPPERCLASSTOSTRING&m1,const MAPPERCLASSTOSTRING&m2);
  virtual ~HMMTables();
  virtual double getAlProb(int i,int k,int sentLength,int J,CLS w1,CLS w2,int j,int iter=0) const;
  virtual void writeJumps(ostream&) const;
  void addAlCount(int i,int k,int sentLength,int J,CLS w1,CLS w2,int j,double value,double valuePredicted);
  virtual void readJumps(istream&);
  virtual bool getAlphaInit(int I,Array<double>&x)const;
  virtual bool getBetaInit(int I,Array<double>&x)const;
  Array<double>&doGetAlphaInit(int I);
  Array<double>&doGetBetaInit(int I);
  virtual double getProbabilityForEmpty()const
    {return probabilityForEmpty;}  
  void performGISIteration(const HMMTables<CLS,MAPPERCLASSTOSTRING>*old)
    {
      cout << "OLDSIZE: " << (old?(old->alProb.size()):0) << " NEWSIZE:"<< alProb.size()<< endl;
      for(typename map<AlDeps<CLS>,FlexArray<double> >::iterator i=alProb.begin();i!=alProb.end();++i)
	{
	  if( alProbPredicted.count(i->first))
	    {
	      normalize_if_possible(i->second.begin(),i->second.end());
	      normalize_if_possible(alProbPredicted[i->first].begin(),alProbPredicted[i->first].end());
	      for(int j=i->second.low();j<=i->second.high();++j)
		{
		  if( i->second[j] )
		    if(alProbPredicted[i->first][j]>0.0 )
		      {
			double op=1.0;
			if( old && old->alProb.count(i->first) )
			  op=(old->alProb.find(i->first)->second)[j];
			//cerr << "GIS: " << j << ' ' << " OLD:"
			//     << op << "*true:" 
			//     << i->second[j] << "/pred:" << alProbPredicted[i->first][j] << " -> ";
			i->second[j]= op*(i->second[j]/alProbPredicted[i->first][j]);
			//cerr << i->second[j] << endl;
		      }
		    else
		      {
			cerr << "ERROR2 in performGISiteration: " << i->second[j] << endl;
		      }
		}
	    }
	  else
	    cerr << "ERROR in performGISIteration: " << alProbPredicted.count(i->first) << endl;
	}
    }
};

template<class CLS,class MAPPERCLASSTOSTRING>
inline void printAlDeps(ostream&out,const AlDeps<CLS>&x,const MAPPERCLASSTOSTRING&mapper1,const MAPPERCLASSTOSTRING&mapper2)
{
  if( (CompareAlDeps&1) ) out << "sentenceLength: " << x.englishSentenceLength<< ' ';
  if( (CompareAlDeps&2) ) out << "previousClass: " << mapper1.classString(x.classPrevious) << ' ';
  if( (CompareAlDeps&4) ) out << "previousPosition: " << x.previous << ' ';
  if( (CompareAlDeps&8) ) out << "FrenchPosition: " << x.j << ' ';
  if( (CompareAlDeps&16) ) out << "FrenchClass: " << mapper2.classString(x.Cj) << ' ';
  //out << '\n';
}

#endif
