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
#include "Parameter.h"
#include <fstream>
#include <unistd.h>
#include <sstream>


bool absolutePathNames=0;
string ParameterPathPrefix;
bool ParameterChangedFlag=0;

bool writeParameters(ofstream&of,const ParSet&parset,int level)
{
  if(!of)return 0;
  for(ParSet::const_iterator i=parset.begin();i!=parset.end();++i)
    {
      if(((*i)->getLevel()==level||level==-1)&&(*i)->onlyCopy==0)
	{
	  ostringstream os;
	  (*i)->printValue(os);
	  os << ends;
	  string s(os.str());
	  of << (*i)->getString() << " ";
	  if( absolutePathNames&&(*i)->isFilename()&&s.length()&&s[0]!='/' )
	    {
	      char path[1024];
	      getcwd(path,1024);
	      of << path << '/';
	    }
	  if( ParameterPathPrefix.length()&&(*i)->isFilename()&&s.length()&&s[0]!='/' )
	    of << ParameterPathPrefix << '/'; 
	  (*i)->printValue(of);
	  of << endl;
	}
    }
  return 1;
}

bool readParameters(ifstream&f,const ParSet&parset,int verb,int level)
{
  string s;
  if(!f)return 0;
  while(getline(f,s))
    {
      istringstream eingabe(s);
      string s1,s2;
      eingabe>>s1>>s2;
      if(makeSetCommand(s1,s2,parset,verb,level)==0)
	cerr << "ERROR: could not set: (C) " << s1 << " " << s2 << endl;
    }
  return 1;
}

 
bool makeSetCommand(string _s1,string s2,const ParSet&parset,int verb,int level)
{
  ParPtr anf;
  int anfset=0;
  string s1=simpleString(_s1);
  for(ParSet::const_iterator i=parset.begin();i!=parset.end();++i)
    {
      if( *(*i)==s1 )
	{
	  if( level==-1 || level==(*i)->getLevel() )
	    (*i)->setParameter(s2,verb);
	  else if(verb>1)
	    cerr << "ERROR: Could not set: (A) " << s1 << " " << s2 << " " << level << " " << (*i)->getLevel() << endl;
	  return 1;
	}
      else if( (*i)->getString().substr(0,s1.length())==s1 )
	{
	  anf=(*i);anfset++;
	}
    }
  if(anfset==1)
    {
      if( level==-1 || level==anf->getLevel() )
	anf->setParameter(s2,verb);
      else if( verb>1 )
	cerr << "ERROR: Could not set: (B) " << s1 << " " << s2 << " " << level << " " << anf->getLevel() << endl;
      return 1;
    }
  if( anfset>1 )
    cerr << "ERROR: ambiguous parameter '" << s1 << "'.\n";
  if( anfset==0 )
    cerr << "ERROR: parameter '" << s1 << "' does not exist.\n";
  return 0;
}

ostream& printPars(ostream&of,const ParSet&parset,int level)
{
  if(!of)return of;
  for(ParSet::const_iterator i=parset.begin();i!=parset.end();++i)
    {
      if(((*i)->getLevel()==level||level==-1)&&(*i)->onlyCopy==0)
	{
	  (*i)->printAt(of);
	  of << endl;
	}
    }
  return of;
}

string simpleString(const string s)
{
  string k;
  for(unsigned int i=0;i<s.length();++i)
    {
      char c[2];
      c[0]=tolower(s[i]);
      c[1]=0;
      if( (c[0]>='a'&&c[0]<='z')||(c[0]>='0'&&c[0]<='9') )
	k += c;
    }
  return k;
}


ParSet&getGlobalParSet()
{
  static ParSet x;
  return x;
}
