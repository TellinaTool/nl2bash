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
#ifndef WordClasses_h_DEFINED
#define WordClasses_h_DEFINED
#include <map>
#include <string>
#include <set>

class WordClasses
{
 private:
  map<string,string> Sw2c;
  map<string,int> Sc2int;
  Vector<string> Sint2c;
  Vector<int> w2c;
  unsigned int classes;
 public:
  WordClasses() 
    : classes(1) 
    {
      Sint2c.push_back("0");
      Sc2int["0"]=0;
    }
  template<class MAPPER> bool read(istream&in,const MAPPER&m)
    {
      string sline;
      int maxword=0;
      while(getline(in,sline))
	{
	  string word,wclass;
	  //istringstream iline(sline.c_str());
	  istringstream iline(sline);
	  iline>>word>>wclass;
	  maxword=max(m(word),maxword);
	  assert(Sw2c.count(word)==0);
	  Sw2c[word]=wclass;
	  if( !Sc2int.count(wclass) )
	    {
	      Sc2int[wclass]=classes++;
	      Sint2c.push_back(wclass);
	      assert(classes==Sint2c.size());
	    }
	}
      w2c=Vector<int>(maxword+1,0);
      for(map<string,string>::const_iterator i=Sw2c.begin();i!=Sw2c.end();++i)
	w2c[m(i->first)]=Sc2int[i->second];
      cout << "Read classes: #words: " << maxword << " " << " #classes: "<< classes <<endl;
      return 1;
    }
  int getClass(int w)const
    {
      if(w>=0&&int(w)<int(w2c.size()) )
	return w2c[w];
      else
	return 0;
    }
  int operator()(const string&x)const
    {
      if( Sc2int.count(x) )
	return Sc2int.find(x)->second;
      else
	{
	  cerr << "WARNING:  class " << x << " not found.\n";
	  return 0;
	}
    }
  string classString(unsigned int cnr)const
    {
      if( cnr<Sint2c.size())
	return Sint2c[cnr];
      else
	return string("0");
    }
};

#endif
