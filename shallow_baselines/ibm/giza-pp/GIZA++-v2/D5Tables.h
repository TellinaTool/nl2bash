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
#ifndef _d5tables_h_define
#define _d5tables_h_define
#include <math.h>
#include "D4Tables.h"

extern float d5modelsmooth_countoffset;
extern float d5modelsmooth_factor;

#define UNSEENPROB (1.0/vacancies_total)

class d5model
{
 private:
  typedef Vector < pair < COUNT,PROB > >Vpff;
  map< m4_key,Vpff,compare1 > D1;
  map< m4_key,Vpff,compareb1 > Db1;
 public:
  d4model&d4m;
  WordClasses ewordclasses,fwordclasses;
  template<class MAPPER>
  void makeWordClasses(const MAPPER&m1,const MAPPER&m2,string efile,string ffile)
    {
      ifstream estrm(efile.c_str()),fstrm(ffile.c_str());
      if( !estrm )
	cerr << "ERROR: can not read classes from " << efile << endl;
      else
	ewordclasses.read(estrm,m1);
      if( !fstrm )
	cerr << "ERROR: can not read classes from " << ffile << endl;
      else
	fwordclasses.read(fstrm,m2);
    }
  d5model (d4model&_d4m)
    :D1 (compare1(M5_Dependencies)), Db1 (compareb1(M5_Dependencies)),d4m(_d4m)
    {}
  COUNT &getCountRef_first (PositionIndex vacancies_j,
			    PositionIndex vacancies_jp, int F,
			    PositionIndex l, PositionIndex m,
			    PositionIndex vacancies_total)
  {
    massert(vacancies_j>0);
    massert(vacancies_total>0);
    //massert(vacancies_jp<=vacancies_total);
    massert(vacancies_j <=vacancies_total);
    massert(vacancies_total<=m);
    m4_key key(M5_Dependencies,l,m,F,0,0,vacancies_jp,vacancies_total);
    map<m4_key,Vpff,compare1 >::iterator p=D1.find(key);
    if(p==D1.end())
      p=D1.insert(make_pair(key,Vpff(vacancies_total+1,make_pair(0,UNSEENPROB)))).first; // !!! constrain length
    massert(p!=D1.end());
    return (p->second)[vacancies_j].first;
  }
  COUNT &getCountRef_bigger (PositionIndex vacancies_j,
			     PositionIndex vacancies_jp, int F,
			     PositionIndex l, PositionIndex m,
			     PositionIndex vacancies_total)
  {
    massert(vacancies_j>0);
    massert(vacancies_total>0);
    massert (vacancies_jp <= vacancies_j);
    massert (vacancies_j-vacancies_jp <= vacancies_total);
    m4_key key(M5_Dependencies,l,m,F,0,0,-1,vacancies_total);
    map<m4_key,Vpff,compareb1 >::iterator p=Db1.find(key);
    if(p==Db1.end())
      p=Db1.insert(make_pair(key,Vpff(vacancies_total+1,make_pair(0,UNSEENPROB)))).first; // !!! constrain length
    massert(p!=Db1.end());
    return (p->second)[vacancies_j - vacancies_jp].first;
  }
  PROB getProb_first (PositionIndex vacancies_j, PositionIndex vacancies_jp,
		       int F, PositionIndex l, PositionIndex m,
		       PositionIndex vacancies_total) const
  {
    massert(vacancies_j>0);
    massert(vacancies_total>0);
    //massert(vacancies_jp<=vacancies_total);
    massert(vacancies_j <=vacancies_total);
    massert(vacancies_total<=m);
    m4_key key(M5_Dependencies,l,m,F,0,0,vacancies_jp,vacancies_total);
    map<m4_key,Vpff,compare1 >::const_iterator p=D1.find(key);
    if( p==D1.end() )
      return UNSEENPROB;
    else
      return max(PROB_SMOOTH,d5modelsmooth_factor/(vacancies_total)+(1-d5modelsmooth_factor)*(p->second)[vacancies_j].second);
  }
  PROB getProb_bigger (PositionIndex vacancies_j, PositionIndex vacancies_jp,
			int F, PositionIndex l, PositionIndex m,
			PositionIndex vacancies_total) const
  {
    massert(vacancies_j>0);
    massert(vacancies_total>0);
    massert (vacancies_jp <= vacancies_j);
    massert (vacancies_j-vacancies_jp <= vacancies_total);
    m4_key key(M5_Dependencies,l,m,F,0,0,-1,vacancies_total);
    map<m4_key,Vpff,compareb1 >::const_iterator p=Db1.find(key);
    if(p==Db1.end())
      return UNSEENPROB;
    else
      return max(PROB_SMOOTH,d5modelsmooth_factor/(vacancies_total)+(1-d5modelsmooth_factor)*(p->second)[vacancies_j - vacancies_jp].second);
  }
  void normalizeTable ()
    {
      int nParams=0;
      for(map<m4_key,Vpff,compare1 >::iterator i=D1.begin();i!=D1.end();++i)
	{
	  Vpff&d1=i->second;
	  COUNT sum=0.0;
	  for(PositionIndex i=0;i<d1.size();i++)
	    sum+=d1[i].first+d5modelsmooth_countoffset;
	  for(PositionIndex i=0;i<d1.size();i++)
	    {
	      d1[i].second=sum?((d1[i].first+d5modelsmooth_countoffset)/sum):(1.0/d1.size());
	      nParams++;
	    }
	}
      for(map<m4_key,Vpff,compareb1 >::iterator i=Db1.begin();i!=Db1.end();++i)
	{
	  Vpff&db1=i->second;
	  double sum=0.0;
	  for(PositionIndex i=0;i<db1.size();i++)
	    sum+=db1[i].first+d5modelsmooth_countoffset;
	  for(PositionIndex i=0;i<db1.size();i++)
	    {
	      db1[i].second=sum?((db1[i].first+d5modelsmooth_countoffset)/sum):(1.0/db1.size());
	      nParams++;
	    }
	}
      cout << "D5 table contains " << nParams << " parameters.\n";
    }
  
  friend ostream&operator<<(ostream&out,d5model&d5m)
    {
      out << "# Translation tables for Model 5 .\n";
      out << "# Table for head of cept.\n";
      for(map<m4_key,Vpff,compare1 >::const_iterator i=d5m.D1.begin();i!=d5m.D1.end();++i)
	{
	  const Vpff&d1=i->second;
	  COUNT sum=0.0;
	  for(PositionIndex ii=0;ii<d1.size();ii++)sum+=d1[ii].first;
	  if ( sum )
	    {
	      for(unsigned ii=0;ii<d1.size();ii++)
		{
		  print1_m5(out,i->first,d5m.ewordclasses,d5m.fwordclasses);
		  out << (int)(ii) << ' ' << d1[ii].second  << ' ' << d1[ii].first << '\n';
		}
	      out << endl;
	    }
	}
      out << "# Table for non-head of cept.\n";
      for(map<m4_key,Vpff,compareb1 >::const_iterator i=d5m.Db1.begin();i!=d5m.Db1.end();++i)
	{
	  const Vpff&db1=i->second;
	  double sum=0.0;
	  for(PositionIndex ii=0;ii<db1.size();++ii)sum+=db1[ii].first;
	  if( sum )
	    {
	      for(unsigned ii=0;ii<db1.size();ii++)
		{
		  printb1_m5(out,i->first,d5m.fwordclasses);
		  out << (int)(ii) << ' ' << db1[ii].second << ' ' << db1[ii].first << '\n';
		}
	      out << endl;
	    }
	}
      return out;
    }
  void readProbTable(const char*x)
    {
      ifstream f(x);
      string l;
      while(getline(f,l))
	{
	  if(l.length()&&l[0]=='#')
	    continue;
	  istringstream is(l.c_str());
	  string E,F;
	  int v1,v2,ii;
	  double prob,count;
	  if(is>>E>>F>>v1>>v2>>ii>>prob>>count)
	    {
	      //cerr << "Read: " << E << " " << F << " " << v1 << " " << v2 << " " << prob<< endl;
	      if( count>0 )
		if( E=="-1")
		  getCountRef_bigger(ii,0,fwordclasses(F),1000,1000,v2)+=count;
		else
		  getCountRef_first(ii,v1,fwordclasses(F),1000,1000,v2)+=count;
	    }
	}
      normalizeTable();
      ofstream of("M5FILE");
      of << (*this);
    }
  void clear()
    {
      for(map<m4_key,Vpff,compare1 >::iterator i=D1.begin();i!=D1.end();++i)
	{
	  Vpff&d1=i->second;
	  for(PositionIndex i=0;i<d1.size();i++)
	    d1[i].first=0.0;
	}
      for(map<m4_key,Vpff,compareb1 >::iterator i=Db1.begin();i!=Db1.end();++i)
	{
	  Vpff&db1=i->second;
	  for(PositionIndex i=0;i<db1.size();i++)
	    db1[i].first=0.0;
	}
    }
};

#endif



