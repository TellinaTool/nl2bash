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




#include "PopOptimization.h"
#include "ProblemTest.h"


int compareProbAndOpt(const void *p,const void *j)
{
  double a=((ProbAndOpt *)p)->prob->value();
  double b=((ProbAndOpt *)j)->prob->value();
  if(a==b)
    return 0;
  if(a<b)
    return -1;
  else
    return +1;
}
bool operator<(const ProbAndOpt&a, const ProbAndOpt&b)
	{
	return a.prob->value()<b.prob->value();
	}
bool operator==(const ProbAndOpt&a, const ProbAndOpt&b)
	{
	return a.prob->value()==b.prob->value();
	}

ostream& operator<<(ostream&o , const ProbAndOpt&){return o;}
istream& operator>>(istream&i , ProbAndOpt&){return i;}


      
PopOptimization::PopOptimization(Problem &p,int verf,int anz) 
: probandopt(anz),initialisiert(0),verfahren(verf)
{
  originalProblem = &p;
}

     
int PopOptimization::size()
{
  return probandopt.size();
}

Problem *PopOptimization::problem(int i)
{
  assert(initialisiert);
  return probandopt[i].prob;
}

Optimization *PopOptimization::optimization(int i)
{
  assert(initialisiert);
  return probandopt[i].opt;
}

void PopOptimization::zInitialize()
{
	int i;
  zufallSeed();
  for(i=0;i<size();i++)
    {
      probandopt[i].prob=originalProblem->makeEqualProblem();
      probandopt[i].prob->initialize();
    }

  zufallSeed();
  for(i=0;i<size();i++)
    probandopt[i].opt=(Optimization *)genIterOptimizer(verfahren,
						    *(probandopt[i].prob),-1);

  initialisiert=1;
}

    
void PopOptimization::sort()
{
  assert(initialisiert);
  
  probandopt.sort(size());
}

