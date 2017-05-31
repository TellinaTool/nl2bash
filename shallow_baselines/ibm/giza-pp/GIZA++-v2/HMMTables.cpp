/*

Copyright (C) 1998,1999,2000,2001  Franz Josef Och (RWTH Aachen - Lehrstuhl fuer Informatik VI)

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
#include "HMMTables.h"
#include <fstream>
#include "Globals.h"
#include "Parameter.h"

template<class CLS,class MAPPERCLASSTOSTRING>
void HMMTables<CLS,MAPPERCLASSTOSTRING>::writeJumps(ostream&out) const
{
  double ssum=0.0;
  for(typename map<AlDeps<CLS>,FlexArray<double> >::const_iterator i=alProb.begin();i!=alProb.end();++i)
    {
      double sum=0.0;
      out << "\n\nDistribution for: ";
      printAlDeps(out,i->first,*mapper1,*mapper2);
      out << ' ';
      for(int a=i->second.low();a<=i->second.high();++a)
	if( i->second[a] )
	  {
	    out << a << ':' << i->second[a] << ';' << ' ';
	    sum+=i->second[a];
	  }
      out << '\n' << '\n';
      out << "SUM: " << sum << '\n';
      ssum+=sum;
    }
  out << "FULL-SUM: " << ssum << '\n';
}
template<class CLS,class MAPPERCLASSTOSTRING>
void HMMTables<CLS,MAPPERCLASSTOSTRING>::readJumps(istream&)
{
}
template<class CLS,class MAPPERCLASSTOSTRING>
double HMMTables<CLS,MAPPERCLASSTOSTRING>::getAlProb(int istrich,int k,int sentLength,int J,CLS w1,CLS w2,int j,int iter) const
{
  massert(k<sentLength&&k>=0);
  massert(istrich<sentLength&&istrich>=-1);
  int pos=istrich-k;
  switch(PredictionInAlignments)
    {
    case 0: pos=istrich-k; break;
    case 1: pos=k; break;
    case 2: 
      pos=(k*J-j*sentLength);
      if( pos>0 ) pos+=J/2; else pos-=J/2;
      pos/=J;
      break;
    default:abort();
    }
  typename map<AlDeps<CLS>,FlexArray<double> >::const_iterator p=alProb.find(AlDeps<CLS>(sentLength,istrich,j,w1,w2));
  if( p!=alProb.end() )
    {
      return (p->second)[pos];
    }
  else
    {
      if( iter>0&&iter<5000 )
      	cout << "WARNING: Not found: " << ' ' << J << ' ' << sentLength << '\n';;
     return 1.0/(2*sentLength-1); 
    }
}

template<class CLS,class MAPPERCLASSTOSTRING>
void HMMTables<CLS,MAPPERCLASSTOSTRING>::addAlCount(int istrich,int k,int sentLength,int J,CLS w1,CLS w2,int j,double value,double valuePredicted)
{
  int pos=istrich-k;
  switch(PredictionInAlignments)
    {
    case 0: pos=istrich-k; break;
    case 1: pos=k; break;
    case 2:
      pos=(k*J-j*sentLength);
      if( pos>0 ) pos+=J/2; else pos-=J/2;
      pos/=J;
      break;
    default:abort();
    }
  AlDeps<CLS> deps(AlDeps<CLS>(sentLength,istrich,j,w1,w2));

  {
    typename map<AlDeps<CLS>,FlexArray<double> >::iterator p=alProb.find(deps);
    if( p==alProb.end() ) 
      {
	if( (CompareAlDeps&1)==0 )
	  p=alProb.insert(make_pair(deps,FlexArray<double> (-MAX_SENTENCE_LENGTH,MAX_SENTENCE_LENGTH,0.0))).first;
	else
	  p=alProb.insert(make_pair(deps,FlexArray<double> (-sentLength,sentLength,0.0))).first;
      }
    p->second[pos]+=value;
  }

  if( valuePredicted )
    {
      typename map<AlDeps<CLS>,FlexArray<double> >::iterator p=alProbPredicted.find(deps);
      if( p==alProbPredicted.end() ) 
	{
	  if( (CompareAlDeps&1)==0 )
	    p=alProbPredicted.insert(make_pair(deps,FlexArray<double> (-MAX_SENTENCE_LENGTH,MAX_SENTENCE_LENGTH,0.0))).first;
	  else
	    p=alProbPredicted.insert(make_pair(deps,FlexArray<double> (-sentLength,sentLength,0.0))).first;
	}
      p->second[pos]+=valuePredicted;
    }
}

template<class CLS,class MAPPERCLASSTOSTRING>
Array<double>&HMMTables<CLS,MAPPERCLASSTOSTRING>::doGetAlphaInit(int I)
{
  if( !init_alpha.count(I) )
    init_alpha[I]=Array<double>(I,0);
  return init_alpha[I];
}
template<class CLS,class MAPPERCLASSTOSTRING>
Array<double>&HMMTables<CLS,MAPPERCLASSTOSTRING>::doGetBetaInit(int I)
{
  if( !init_beta.count(I) )
    init_beta[I]=Array<double>(I,0);
  return init_beta[I];
}

template<class CLS,class MAPPERCLASSTOSTRING>
bool HMMTables<CLS,MAPPERCLASSTOSTRING>::getAlphaInit(int I,Array<double>&x)const
{
  hash_map<int,Array<double> >::const_iterator i=init_alpha.find(I);
  if( i==init_alpha.end() )
    return 0;
  else
    {
      x=i->second;
      for(unsigned int j=x.size()/2+1;j<x.size();++j) // only first empty word can be chosen
	x[j]=0;
      return 1;
    }
}
template<class CLS,class MAPPERCLASSTOSTRING>
bool HMMTables<CLS,MAPPERCLASSTOSTRING>::getBetaInit(int I,Array<double>&x)const
{
  hash_map<int,Array<double> >::const_iterator i=init_beta.find(I);
  if( i==init_beta.end() )
    return 0;
  else
    {
      x=i->second;
      return 1;
    }
}

template<class CLS,class MAPPERCLASSTOSTRING>
HMMTables<CLS,MAPPERCLASSTOSTRING>::  HMMTables(double _probForEmpty,const MAPPERCLASSTOSTRING&m1,const MAPPERCLASSTOSTRING&m2): 
  probabilityForEmpty(mfabs(_probForEmpty)),
  updateProbabilityForEmpty(_probForEmpty<0.0),
  mapper1(&m1),
  mapper2(&m2)
{}
template<class CLS,class MAPPERCLASSTOSTRING>
HMMTables<CLS,MAPPERCLASSTOSTRING>::~HMMTables() {}
