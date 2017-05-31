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



#include "StatVar.h"
#include <iostream>
#include <stdlib.h>

double compareStatVarQuantil=-1; 

StatV::~StatV() {}
                               

int doublecompare(const void *p,const void *j)
{
  if( *(double *)p == *(double *)j)
    return 0;
  if( *(double *)p- *(double *)j<0 )
    return -1;
  else
    return 1;
}

int compareStatVar(const void *p,const void *j)
{
  double a;
  double b;
  if(compareStatVarQuantil>=0)
    {
      a=((StatVar *)p)->quantil(compareStatVarQuantil);
      b=((StatVar *)j)->quantil(compareStatVarQuantil);
    }
  else
    {
      a=((StatVar *)p)->getMean();
      b=((StatVar *)j)->getMean();
    }
  if(a==b)
    return 0;
  if(a<b)
    return -1;
  else
    return +1;
}


double StatVar::getSigmaSmaller()
{
  double ss=0;
  int ns=0;
  for(int i=0;i<n;i++)
    {
      if( values[i]<getMean() )
	{
	  ss+=(values[i]-getMean())*(values[i]-getMean());
	  ns++;
	}
    }
  if( ss/ns>0 )
    return sqrt(ss/ns);
  else
    return 0;
}
double StatVar::getSigmaBigger()
{
  double ss=0;
  int ns=0;
  for(int i=0;i<n;i++)
    if( values[i]>getMean() )
      {
	ss+=(values[i]-getMean())*(values[i]-getMean());
	ns++;
      }
  if( ss/ns>0 )
    return sqrt(ss/ns);
  else
    return 0;
}


  
void StatV::dumpOn(ostream &strm)
{
  strm << "MEAN: " << getMean() << " (" << smallest << "-" << biggest 
    << ")  SIGMA:" << getSigma()<< "   ";
}


  
double StatVar::quantil(double percent)
{
  int index=(int)(n*percent);
  if(index==n)
    index=n-1;
  assert(index>=0&&index<n);
  if(sortedFlag==0)
    {
      qsort(values.getPointerToData(),n,sizeof(double),doublecompare);
      assert(n<=values.size());
      sortedFlag=1;
    }
  if(index<0)
    {
      cerr << "WARNING: StatVar.cc\n";
      return 0.0;
    }
  else
    return values[index];
}

  
void StatVar::printValues(ostream &strm)
{
  qsort(values.getPointerToData(),n,sizeof(double),doublecompare);
  assert(n<=values.size());
  for(int i=0;i<n;i++)
    strm << i/(double)n << " " << values[i] << endl;
  return;
}
