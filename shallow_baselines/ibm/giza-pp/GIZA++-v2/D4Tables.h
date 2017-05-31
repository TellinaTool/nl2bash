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
#ifndef _d4tables_h_define
#define _d4tables_h_define
#include <math.h>
#include "WordClasses.h"
#include "Globals.h"
#include "myassert.h"

extern float d4modelsmooth_factor;

class m4_key
{
 public:
  int deps;
  int l;
  int m;
  int F;
  int E;
  int prevj;
  int vacancies1,vacancies2;
  m4_key(int _deps,int _l,int _m,int _F,int _E,int _prevj,int _v1,int _v2)
    : deps(_deps),l(_l),m(_m),F(_F),E(_E),prevj(_prevj),vacancies1(_v1),vacancies2(_v2) {}
  friend ostream&print1(ostream&out,const m4_key&x,const WordClasses&wce,const WordClasses&wcf)
    {
      if(x.deps&DEP_MODEL_l)out << "l: " << x.l<<' ';
      if(x.deps&DEP_MODEL_m)out << "m: " << x.m<<' ';
      if(x.deps&DEP_MODEL_F)out << "F: " << wcf.classString(x.F)<< ' ';
      if(x.deps&DEP_MODEL_E)out << "E: " << wce.classString(x.E)<< ' ';
      //      if(x.deps&DEP_MODEL_pj)out << "j-1: " << x.prevj<<' ';
      if(x.vacancies1!=-1)out << "v1: " << x.vacancies1 << ' ';
      if(x.vacancies2!=-1)out << "v2: " << x.vacancies2 << ' ';
      return out << '\n';
    }
  friend ostream&print1_m5(ostream&out,const m4_key&x,const WordClasses&wce,const WordClasses&wcf)
    {
      out << ((x.deps&DEP_MODEL_E)?wce.classString(x.E):string("0"))<< ' ';
      out << ((x.deps&DEP_MODEL_F)?wcf.classString(x.F):string("0"))<< ' ';
      out << x.vacancies1 << ' ';
      out << x.vacancies2 << ' ';
      return out;
    }
  friend ostream&printb1(ostream&out,const m4_key&x,const WordClasses&wce,const WordClasses&wcf)
    {
      if(x.deps&DEP_MODELb_l)out << "l: " << x.l<<' ';
      if(x.deps&DEP_MODELb_m)out << "m: " << x.m<<' ';
      if(x.deps&DEP_MODELb_F)out << "F: " << wcf.classString(x.F) << ' ';
      if(x.deps&DEP_MODELb_E)out << "E: " << wce.classString(x.E) << ' ';
      if(x.vacancies1!=-1)out << "v1: " << x.vacancies1 << ' ';
      if(x.vacancies2!=-1)out << "v2: " << x.vacancies2 << ' ';
      return out << '\n';
    }
  friend ostream&printb1_m5(ostream&out,const m4_key&x,const WordClasses&wcf)
    {
      out << "-1 " << ((x.deps&DEP_MODEL_F)?wcf.classString(x.F):string("0"))<< ' ';
      out << x.vacancies1 << ' ';
      out << x.vacancies2 << ' ';
      return out;
    }
};

class compare1
{
 private:
  int deps;
 public:
  compare1(int _deps) : deps(_deps) {}
  bool operator()(const m4_key&a,const m4_key&b)const
    {
      if(deps&DEP_MODEL_l){if( a.l<b.l )return 1;if( b.l<a.l )return 0;}
      if(deps&DEP_MODEL_m){if( a.m<b.m )return 1;if( b.m<a.m )return 0;}
      if(deps&DEP_MODEL_F){if( a.F<b.F )return 1;if( b.F<a.F )return 0;}
      if(deps&DEP_MODEL_E){if( a.E<b.E )return 1;if( b.E<a.E )return 0;}
      //if(deps&DEP_MODEL_pj){if( a.prevj<b.prevj )return 1;if( b.prevj<a.prevj )return 0;}
      if(a.vacancies1<b.vacancies1)return 1;if(b.vacancies1<a.vacancies1)return 0;
      if(a.vacancies2<b.vacancies2)return 1;if(b.vacancies2<a.vacancies2)return 0;
      return 0;
    }
};

class compareb1
{
 private:
  int deps;
 public:
  compareb1(int _deps) : deps(_deps) {}
  bool operator()(const m4_key&a,const m4_key&b)const
    {
      if(deps&DEP_MODELb_l){if( a.l<b.l )return 1;if( b.l<a.l )return 0;}
      if(deps&DEP_MODELb_m){if( a.m<b.m )return 1;if( b.m<a.m )return 0;}
      if(deps&DEP_MODELb_F){if( a.F<b.F )return 1;if( b.F<a.F )return 0;}
      if(deps&DEP_MODELb_E){if( a.E<b.E )return 1;if( b.E<a.E )return 0;}
      //if(deps&DEP_MODELb_pj){if( a.prevJ<b.prevJ )return 1;if( b.prevJ<a.prevJ )return 0;}
      if(a.vacancies1<b.vacancies1)return 1;if(b.vacancies1<a.vacancies1)return 0;
      if(a.vacancies2<b.vacancies2)return 1;if(b.vacancies2<a.vacancies2)return 0;
      return 0;
    }
};

inline void tokenize(const string&in,Vector<string>&out)
{
  string s;
  istringstream l(in);
  while(l>>s)
    out.push_back(s);
}

class d4model
{
 public:
  typedef Vector<pair<COUNT,PROB> > Vpff;
  map<m4_key,Vpff,compare1 > D1;
  map<m4_key,Vpff,compareb1> Db1;
  PositionIndex msl;
  WordClasses ewordclasses;
  WordClasses fwordclasses;
  template<class MAPPER>
  void makeWordClasses(const MAPPER&m1,const MAPPER&m2,string efile,string ffile)
    {
      ifstream estrm(efile.c_str()),fstrm(ffile.c_str());
      if( !estrm )
	{
	  cerr << "ERROR: can not read " << efile << endl;
	}
      else
	ewordclasses.read(estrm,m1);
      if( !fstrm )
	cerr << "ERROR: can not read " << ffile << endl;
      else
	fwordclasses.read(fstrm,m2);
    }
  d4model(PositionIndex _msl)
    : D1(compare1(M4_Dependencies)),Db1(compareb1(M4_Dependencies)),msl(_msl)
    {}
  COUNT&getCountRef_first(WordIndex j,WordIndex j_cp,int E,int F,int l,int m)
    {
      assert(j>=1);
      m4_key key(M4_Dependencies,l,m,F,E,j_cp,-1,-1);
      map<m4_key,Vpff,compare1 >::iterator p=D1.find(key);
      if(p==D1.end())p=D1.insert(make_pair(key,Vpff(msl*2+1,pair<COUNT,PROB>(0.0,0.0)))).first;
      assert(p!=D1.end());
      return (p->second)[j-j_cp+msl].first;
    }
  COUNT&getCountRef_bigger(WordIndex j,WordIndex j_prev,int E,int F,int l,int m)
    {
      assert(j>=1);
      assert(j_prev>=1);
      m4_key key(M4_Dependencies,l,m,F,E,j_prev,-1,-1);
      map<m4_key,Vpff,compareb1 >::iterator p=Db1.find(key);
      if(p==Db1.end())p=Db1.insert(make_pair(key,Vpff(msl*2+1,pair<COUNT,PROB>(0.0,0.0)))).first;
      assert(p!=Db1.end());
      return (p->second)[j-j_prev+msl].first;
    }
  map<m4_key,Vpff,compare1 >::const_iterator getProb_first_iterator(int E,int F,int l,int m)const
    {return D1.find(m4_key(M4_Dependencies,l,m,F,E,0,-1,-1));}
  PROB getProb_first_withiterator(WordIndex j,WordIndex j_cp,int m,const map<m4_key,Vpff,compare1 >::const_iterator& p)const
    {
      assert(j>=1);//assert(j_cp>=0);
      assert(j<=msl);assert(j_cp<=msl);
      if(p==D1.end())
	{
	return PROB_SMOOTH;
	}
      else
	{
	  massert((p->second)[j-j_cp+msl].second<=1.0);
	  return max(PROB_SMOOTH,d4modelsmooth_factor/(2*m-1)+(1-d4modelsmooth_factor)*(p->second)[j-j_cp+msl].second);
	}
    }
  PROB getProb_first(WordIndex j,WordIndex j_cp,int E,int F,int l,int m)const
    {
      assert(j>=1);//assert(j_cp>=0);
      assert(j<=msl);assert(j_cp<=msl);
      m4_key key(M4_Dependencies,l,m,F,E,j_cp,-1,-1);
      map<m4_key,Vpff,compare1 >::const_iterator p=D1.find(key);
      if(p==D1.end())
	{
	return PROB_SMOOTH;
	}
      else
	{
	  massert((p->second)[j-j_cp+msl].second<=1.0);
	  return max(PROB_SMOOTH,d4modelsmooth_factor/(2*m-1)+(1-d4modelsmooth_factor)*(p->second)[j-j_cp+msl].second);
	}
    }
  map<m4_key,Vpff,compareb1 >::const_iterator getProb_bigger_iterator(int E,int F,int l,int m)const
    {
      return Db1.find(m4_key(M4_Dependencies,l,m,F,E,0,-1,-1));
    }
  PROB getProb_bigger_withiterator(WordIndex j,WordIndex j_prev,int m,const map<m4_key,Vpff,compareb1 >::const_iterator&p)const
    {
      massert(j>=1);massert(j_prev>=1);
      massert(j>j_prev);
      massert(j<=msl);massert(j_prev<=msl);
      if(p==Db1.end())
	{
	  return PROB_SMOOTH;
	}
      else
	{
	  massert((p->second)[j-j_prev+msl].second<=1.0 );
	  return max(PROB_SMOOTH,d4modelsmooth_factor/(m-1)+(1-d4modelsmooth_factor)*(p->second)[j-j_prev+msl].second);
	}
    }
    
  PROB getProb_bigger(WordIndex j,WordIndex j_prev,int E,int F,int l,int m)const
    {
      massert(j>=1);massert(j_prev>=1);
      massert(j>j_prev);
      massert(j<=msl);massert(j_prev<=msl);
      m4_key key(M4_Dependencies,l,m,F,E,j_prev,-1,-1);
      map<m4_key,Vpff,compareb1 >::const_iterator p=Db1.find(key);
      if(p==Db1.end())
	{
	  return PROB_SMOOTH;
	}
      else
	{
	  massert((p->second)[j-j_prev+msl].second<=1.0 );
	  return max(PROB_SMOOTH,d4modelsmooth_factor/(m-1)+(1-d4modelsmooth_factor)*(p->second)[j-j_prev+msl].second);
	}
    }
  void normalizeTable()
    {
      int nParams=0;
      for(map<m4_key,Vpff,compare1 >::iterator i=D1.begin();i!=D1.end();++i)
	{
	  Vpff&d1=i->second;
	  double sum=0.0;
	  for(PositionIndex i=0;i<d1.size();i++)
	    sum+=d1[i].first;
	  for(PositionIndex i=0;i<d1.size();i++)
	    {
	      d1[i].second=sum?(d1[i].first/sum):(1.0/d1.size());
	      nParams++;
	    }
	}
      for(map<m4_key,Vpff,compareb1 >::iterator i=Db1.begin();i!=Db1.end();++i)
	{
	  Vpff&db1=i->second;
	  double sum=0.0;
	  for(PositionIndex i=0;i<db1.size();i++)
	    sum+=db1[i].first;
	  for(PositionIndex i=0;i<db1.size();i++)
	    {
	      db1[i].second=sum?(db1[i].first/sum):(1.0/db1.size());
	      nParams++;
	    }
	}
      cout << "D4 table contains " << nParams << " parameters.\n";      
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
 
  void printProbTable(const char*fname1,const char*fname2)
    {
      ofstream out(fname1);
      double ssum=0.0;
      out << "# Translation tables for Model 4 .\n";
      out << "# Table for head of cept.\n";
      for(map<m4_key,Vpff,compare1 >::const_iterator i=D1.begin();i!=D1.end();++i)
	{
	  const Vpff&d1=i->second;
	  double sum=0.0;
	  for(PositionIndex ii=0;ii<d1.size();ii++)sum+=d1[ii].first;
	  if ( sum )
	    {
	      print1(out,i->first,ewordclasses,fwordclasses);
	      out << "SUM: " << sum << ' '<< '\n';
	      for(unsigned ii=0;ii<d1.size();ii++)
		if( d1[ii].first )
		  out << (int)(ii)-(int)(msl) << ' ' << d1[ii].first << '\n';
	      out << endl;
	    }
	  ssum+=sum;
	}
      out << "# Table for non-head of cept.\n";
      for(map<m4_key,Vpff,compareb1 >::const_iterator i=Db1.begin();i!=Db1.end();++i)
	{
	  const Vpff&db1=i->second;
	  double sum=0.0;
	  for(PositionIndex ii=0;ii<db1.size();++ii)sum+=db1[ii].first;
	  if( sum )
	    {
	      printb1(out,i->first,ewordclasses,fwordclasses);
	      out << "SUM: " << sum << ' '<<'\n';
	      for(unsigned ii=0;ii<db1.size();ii++)
		if( db1[ii].first )
		  {
		    out << (int)(ii)-(int)(msl) << ' ' << db1[ii].first << '\n';
		  }
	      out << endl;
	    }
	  ssum+=sum;
	}
      out << endl << "FULL-SUM: " << ssum << endl;
      if( M4_Dependencies==76 )
	{
	  ofstream out2(fname2);
	  for(map<m4_key,Vpff,compare1 >::const_iterator i=D1.begin();i!=D1.end();++i)
	    {
	      const Vpff&d1=i->second;
	      for(unsigned ii=0;ii<d1.size();ii++)
		if( d1[ii].first )
		  out2 << ewordclasses.classString(i->first.E) << ' ' << fwordclasses.classString(i->first.F) << ' ' << (int)(ii)-(int)(msl) << ' ' << d1[ii].second << '\n';
	    }
	  for(map<m4_key,Vpff,compareb1 >::const_iterator i=Db1.begin();i!=Db1.end();++i)
	    {
	      const Vpff&db1=i->second;
	      for(unsigned ii=0;ii<db1.size();ii++)
		if( db1[ii].first )
		  out2 << -1 << ' ' << fwordclasses.classString(i->first.F) << ' ' << (int)(ii)-(int)(msl) << ' ' << db1[ii].second << '\n';
	    }
	}
    }
  bool readProbTable(const char *fname)
    {
      cerr << "Reading D4Tables from " << fname << endl;
      ifstream file(fname);
      string line;
      do
	{
	  getline(file,line);
	} while(line.length()&&line[0]=='#');
      
      do
	{
	  while(line.length()==0)
	    getline(file,line);
	  if( line[0]=='#')
	    break;
	  Vector<string> linestr;
	  tokenize(line,linestr);
	  m4_key k(M4_Dependencies,0,0,0,0,0,-1,-1);
	  for(unsigned int i=0;i<linestr.size();i+=2)
	    {
	      if( linestr[i]=="l:" ){k.l=atoi(linestr[i+1].c_str());iassert(M4_Dependencies&DEP_MODEL_l);}
	      if( linestr[i]=="m:" ){k.m=atoi(linestr[i+1].c_str());iassert(M4_Dependencies&DEP_MODEL_m);}
	      if( linestr[i]=="F:" ){k.F=fwordclasses(linestr[i+1]);iassert(M4_Dependencies&DEP_MODEL_F);}
	      if( linestr[i]=="E:" ){k.E=ewordclasses(linestr[i+1]);iassert(M4_Dependencies&DEP_MODEL_E);}
	      //if( linestr[i]=="j-1:" ){k.prevj=atoi(linestr[i+1].c_str());iassert(M4_Dependencies&DEP_MODEL_pj);}
	    }
	  string str;
	  double sum;
	  file >> str >> sum;
	  iassert(str=="SUM:");
	  if( str!="SUM:")
	    cerr << "ERROR: string is " << str << " and not sum " << endl;
	  
	  do
	    {
	      int value;
	      double count;
	      getline(file,line);
	      istringstream twonumbers(line);
	      if(twonumbers >> value >> count)
		{
		  if( D1.count(k)==0 )
		    D1.insert(make_pair(k,Vpff(msl*2+1,pair<COUNT,PROB>(0.0,0.0))));
		  D1[k][value+msl]=make_pair(count,count/sum);
		}
	    }while(line.length());
	}while(file);
      do
	{
	  getline(file,line);
	} while(line.length()&&line[0]=='#');
      do
	{
	  while(line.length()==0)
	    getline(file,line);
	  if( line[0]=='#')
	    break;
	  Vector<string> linestr;
	  tokenize(line,linestr);
	  m4_key k(M4_Dependencies,0,0,0,0,0,-1,-1);
	  bool sumRead=0;
	  for(unsigned int i=0;i<linestr.size();i+=2)
	    {
	      if( linestr[i]=="l:" ){k.l=atoi(linestr[i+1].c_str());iassert(M4_Dependencies&DEP_MODELb_l);}
	      else if( linestr[i]=="m:" ){k.m=atoi(linestr[i+1].c_str());iassert(M4_Dependencies&DEP_MODELb_m);}
	      else if( linestr[i]=="F:" ){k.F=fwordclasses(linestr[i+1]);iassert(M4_Dependencies&DEP_MODELb_F);}
	      else if( linestr[i]=="E:" ){k.E=ewordclasses(linestr[i+1]);iassert(M4_Dependencies&DEP_MODELb_E);}
	      else if( linestr[i]=="SUM:" )
		{
		  cerr << "Warning: obviously no dependency.\n";
		  sumRead=1;
		}
	      else if( linestr[i]=="FULL-SUM:" )
		{
		  break;
		}
	      else
		{
		  cerr << "ERROR: error in reading d4 tables: " << linestr[i] << ' ' << linestr[i+1] << endl;
		}
	    }
	  string str;
	  double sum;
	  if( sumRead==0 )
	    file >> str >> sum;
	  else
	    {
	      str=linestr[0];
	      sum=atof(linestr[1].c_str());
	    }
	  if( str!="SUM:" )
	    cerr << "ERROR: should read SUM but read " << str << endl;
	  do
	    {
	      int value;
	      double count;
	      getline(file,line);
	      istringstream twonumbers(line);
	      if(twonumbers >> value >> count)
		{
		  if( Db1.count(k)==0 )
		    Db1.insert(make_pair(k,Vpff(msl*2+1,pair<COUNT,PROB>(0.0,0.0))));
		  Db1[k][value+msl]=make_pair(count,count/sum);
		}
	    }while(file&&line.length());
	}while(file);
      return 1;
    }
};

#endif
