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



#ifndef STATVAR_H
#define STATVAR_H

#include <stdlib.h>
#include <iostream>
#include "Array.h"
#include "mystl.h"
#include "myleda.h"
#include <cmath>


extern double compareStatVarQuantil;
int compareStatVar(const void *p,const void *j);

class StatV
  
{
 protected:
  int n;                    
  double sum;               
  double squareSum;         
  double smallest,biggest;  

 public:
  const char *title;     
  StatV() : n(0),sum(0),squareSum(0),smallest(1e100),biggest(-1e100),title("") {}
  virtual ~StatV();
  

  virtual void addValue(double a)
    {
      n++;
      sum+=a;
      squareSum+=a*a;
      if(smallest>a)
	smallest=a;
      if(biggest<a)
	biggest=a;
      
    }
  

  double getMean()
    { return sum/n; }
  

  double getSigma()
    {
      if(squareSum/n - getMean()*getMean()<=0)
	return 0.0;
      else
	return sqrt(squareSum/n - getMean()*getMean());
    }

  

  double getBiggest()
    { return biggest; }
  

  double getSmallest()
    { return smallest; }
  

  int getNum()
    { return n; }
  

  void dumpOn(ostream &strm);
  

};

class StatVar : public StatV
{
 private:
  Array<double> values;    
  short sortedFlag;       
 public:
  StatVar() 
    : values(10,0.0,1),sortedFlag(0) {}
  virtual ~StatVar(){}
  double quantil(double percent=0.5);
  
  
  inline double value(int i)
    {return values[i];}
  

  void printValues(ostream &strm);
  

  virtual void addValue(double a)
    {  
      sortedFlag=0;
      values[n]=a;
      StatV::addValue(a);
    }
  
  double getSigmaSmaller();
  

  double getSigmaBigger();
  

};


#endif
