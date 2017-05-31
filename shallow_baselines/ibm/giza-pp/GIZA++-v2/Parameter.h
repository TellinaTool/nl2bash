/*

Copyright (C) 1997,1998,1999,2000,2001  Franz Josef Och (RWTH Aachen - Lehrstuhl fuer Informatik VI)

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
#ifndef PARAMETER_H_DEFINED
#define PARAMETER_H_DEFINED

#include "mystl.h"
#include <set>
#include "Pointer.h"
#include <string>
#include "Globals.h"
#include <fstream>
#include <cstring>

inline unsigned int mConvert(const string&s,unsigned int &i)
{ 
  if( strcasecmp(s.c_str(),"yes")==0 || strcasecmp(s.c_str(),"y")==0 || strcasecmp(s.c_str(),"true")==0 || strcasecmp(s.c_str(),"t")==0 ) { cerr << "TRUE\n";return i=1; }
  if( strcasecmp(s.c_str(),"no")==0 ||  strcasecmp(s.c_str(),"n")==0 ||  strcasecmp(s.c_str(),"false")==0 ||  strcasecmp(s.c_str(),"f")==0 ) { cerr << "FALSE\n";return i=0;}
  return i=atoi(s.c_str()); 
}
inline int mConvert(const string&s,int &i){ 
  if( strcasecmp(s.c_str(),"yes")==0 ||  strcasecmp(s.c_str(),"y")==0 ||  strcasecmp(s.c_str(),"true")==0 ||  strcasecmp(s.c_str(),"t")==0 ) { cerr << "TRUE\n";return i=1;}
  if( strcasecmp(s.c_str(),"no")==0 ||  strcasecmp(s.c_str(),"n")==0 ||  strcasecmp(s.c_str(),"false")==0 ||  strcasecmp(s.c_str(),"f")==0 ) { cerr << "FALSE\n";return i=0;}
  return i=atoi(s.c_str()); 
}
inline double mConvert(const string&s,double &d) { return d=atof(s.c_str()); }
inline double mConvert(const string&s,float &d) { return d=atof(s.c_str()); }
inline string mConvert(const string&s,string&n) { return n=s; }
inline bool mConvert(const string&s,bool&n) { 
  if( strcasecmp(s.c_str(),"yes")==0 ||  strcasecmp(s.c_str(),"y")==0 ||  strcasecmp(s.c_str(),"true")==0 ||  strcasecmp(s.c_str(),"t")==0 ) { cerr << "TRUE\n";return n=1;}
  if( strcasecmp(s.c_str(),"no")==0 ||  strcasecmp(s.c_str(),"n")==0 ||  strcasecmp(s.c_str(),"false")==0 ||  strcasecmp(s.c_str(),"f")==0 ) { cerr << "FALSE\n";return n=0;}
  return n=atoi(s.c_str()); 
}
inline short mConvert(const string&s,short&n) { 
  if( strcasecmp(s.c_str(),"yes")==0 ||  strcasecmp(s.c_str(),"y")==0 ||  strcasecmp(s.c_str(),"true")==0 ||  strcasecmp(s.c_str(),"t")==0 ) { cerr << "TRUE\n";return n=1;}
  if( strcasecmp(s.c_str(),"no")==0 ||  strcasecmp(s.c_str(),"n")==0 ||  strcasecmp(s.c_str(),"false")==0 ||  strcasecmp(s.c_str(),"f")==0 ) { cerr << "FALSE\n";return n=0;}
  return n=atoi(s.c_str()); 
}
inline unsigned short mConvert(const string&s,unsigned short&n) { 
  if( strcasecmp(s.c_str(),"yes")==0 ||  strcasecmp(s.c_str(),"y")==0 ||  strcasecmp(s.c_str(),"true")==0 ||  strcasecmp(s.c_str(),"t")==0 ) { cerr << "TRUE\n";return n=1;}
  if( strcasecmp(s.c_str(),"no")==0 ||  strcasecmp(s.c_str(),"n")==0 ||  strcasecmp(s.c_str(),"false")==0 ||  strcasecmp(s.c_str(),"f")==0 ) { cerr << "FALSE\n";return n=0;}
  return n=atoi(s.c_str()); 
}

string simpleString(const string s);

inline int Hashstring(const string& s)
{
  int sum=0;
  string::const_iterator i=s.begin(),end=s.end();
  for(;i!=end;i++)sum=5*sum+(*i);
  return sum;
}

class _Parameter
{
 protected:
  string name;
  bool *ifChanged;
  string description;
  int level;
  bool filename;
 public:
  int onlyCopy;
  _Parameter(string n,bool&b,string desc,int _level,bool _onlyCopy)
    : name(simpleString(n)),ifChanged(&b),description(desc),level(_level),filename(0),onlyCopy(_onlyCopy) {}
  virtual ~_Parameter(){};
  bool operator==(const string&s)const
    { return name== simpleString(s); }
  void setChanged() 
    { *ifChanged=true; }
  virtual bool setParameter(string s2,int)=0;
  virtual ostream&printAt(ostream&out)=0;
  virtual ostream&printValue(ostream&out)=0;
  const string&getString() const { return name; }
  int getLevel() const { return level;}
  bool isFilename() { return filename;}
  void setFilename(bool x=1) { filename=x;}
  friend bool operator==(const _Parameter&a,const _Parameter&b)
    { return a.name==b.name; }
  friend bool operator<(const _Parameter&a,const _Parameter&b)
    { return a.name<b.name; }
  friend int Hash(const _Parameter&aaa)
    { return Hashstring(aaa.name); }
  friend ostream&operator<<(ostream&out,const _Parameter&p)
    { return out<<"Parameter: "<<p.name <<endl;}
};

template<class T>
class Parameter : public _Parameter
{
 private:
  T*t;
 public:
  Parameter(string n,bool&b,string desc,T&_t,int level=0,bool onlyCopy=0)
    : _Parameter(n,b,desc,level,onlyCopy),t(&_t) {}
  virtual ~Parameter(){}
  virtual bool setParameter(string s2,int verb)
    { 
      T x;  
      if( !(*t==mConvert(s2,x)))
	{
	  bool printedFirst=0;
	  if( verb>1 ) 
	    {
	      cout << "Parameter '"<<name <<"' changed from '"<<*t<<"' to '";
	      printedFirst=1;
	    }
	  mConvert(s2,*t);
	  if( printedFirst ) 
	    cout << *t <<"'\n";
	  setChanged();
	  return 1;
	} 
      return 0;
    }
  virtual ostream&printAt(ostream&out)
    {return out << name << " = " << *t << "  (" << description << ")";}
  virtual ostream&printValue(ostream&out)
    {return out << *t;}
};

typedef MP<_Parameter> ParPtr;

class ParSet : public set<ParPtr>
{
 public:
  void insert(const ParPtr&x)
    {
      if( count(x)!=0 )
	cerr << "ERROR: element " << x->getString() << " already inserted.\n";
      set<ParPtr>::insert(x);
    }
};

bool makeSetCommand(string s1,string s2,const ParSet&pars,int verb=1,int level= -1);
ostream&printPars(ostream&out,const ParSet&pars,int level=-1);
bool writeParameters(ofstream&of,const ParSet&parset,int level=0);
bool readParameters(ifstream&f,const ParSet&parset,int verb=2,int level=0);
ParSet&getGlobalParSet();
extern bool ParameterChangedFlag;
template<class T>const T&addGlobalParameter(const char *name,const char *description,int level,T*adr,const T&init)
{
  *adr=init;
  getGlobalParSet().insert(new Parameter<T>(name,ParameterChangedFlag,description,*adr,level));
  return init;
}
template<class T>const T&addGlobalParameter(const char *name,const char *name2,const char *description,int level,T*adr,const T&init)
{
  *adr=init;
  getGlobalParSet().insert(new Parameter<T>(name,ParameterChangedFlag,description,*adr,level));
  getGlobalParSet().insert(new Parameter<T>(name2,ParameterChangedFlag,description,*adr,-1));
  return init;
}
template<class T>const T&addGlobalParameter(const char *name,const char *name2,const char *name3,const char *description,int level,T*adr,const T&init)
{
  *adr=init;
  getGlobalParSet().insert(new Parameter<T>(name,ParameterChangedFlag,description,*adr,level));
  getGlobalParSet().insert(new Parameter<T>(name2,ParameterChangedFlag,description,*adr,-1));
  getGlobalParSet().insert(new Parameter<T>(name3,ParameterChangedFlag,description,*adr,-1));
  return init;
}
template<class T>const T&addGlobalParameter(const char *name,const char *name2,const char *name3,const char *name4,const char *description,int level,T*adr,const T&init)
{
  *adr=init;
  getGlobalParSet().insert(new Parameter<T>(name,ParameterChangedFlag,description,*adr,level));
  getGlobalParSet().insert(new Parameter<T>(name2,ParameterChangedFlag,description,*adr,-1));
  getGlobalParSet().insert(new Parameter<T>(name3,ParameterChangedFlag,description,*adr,-1));
  getGlobalParSet().insert(new Parameter<T>(name4,ParameterChangedFlag,description,*adr,-1));
  return init;
}
void MakeParameterOptimizing(istream&file,string resultingParameters);

#define GLOBAL_PARAMETER(TYP,VARNAME,NAME,DESCRIPTION,LEVEL,INIT) TYP VARNAME=addGlobalParameter< TYP >(NAME,DESCRIPTION,LEVEL,&VARNAME,INIT);
#define GLOBAL_PARAMETER2(TYP,VARNAME,NAME,NAME2,DESCRIPTION,LEVEL,INIT) TYP VARNAME=addGlobalParameter< TYP >(NAME,NAME2,DESCRIPTION,LEVEL,&VARNAME,INIT);
#define GLOBAL_PARAMETER3(TYP,VARNAME,NAME,NAME2,NAME3,DESCRIPTION,LEVEL,INIT) TYP VARNAME=addGlobalParameter< TYP >(NAME,NAME2,NAME3,DESCRIPTION,LEVEL,&VARNAME,INIT);
#define GLOBAL_PARAMETER4(TYP,VARNAME,NAME,NAME2,NAME3,NAME4,DESCRIPTION,LEVEL,INIT) TYP VARNAME=addGlobalParameter< TYP >(NAME,NAME2,NAME3,NAME4,DESCRIPTION,LEVEL,&VARNAME,INIT);

void setParameterLevelName(unsigned int i,string x);

#endif
