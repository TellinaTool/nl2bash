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




#include "MSBOptimization.h"
#include <stdlib.h>
#include "ProblemTest.h"

#ifdef __GNUC__
template class Array<double>;
template class Array<ProbAndOpt>;
#endif

struct doubleInt { double a; int i; };
static int doubleintcompare(const void *p,const void *j)
{
  if(((struct doubleInt *)p)->a < ((doubleInt *)j)->a)
    return -1;
  else if(((struct doubleInt *)p)->a == ((doubleInt *)j)->a)
    return 0;
  else
    return 1;
}

     
MSBOptimization::MSBOptimization(Problem &p,int verf,int anz,Array<double> &pos,Array<double> &por) 
: PopOptimization(p,verf,anz),
percentOfSteps(pos),percentOfRun(por),nachMinimierung(0)
{
}

     
void MSBOptimization::zInitialize()
{
  PopOptimization::zInitialize();

  int iterationsschritte;
  double mean;
  StatVar end,laufzeit,start;  
  zufallSeed(); 

  
  
  
  solveProblem(ProblemTestVerboseMode,*originalProblem,2,-1,verfahren,mean,
	       end,laufzeit,start,0,&iterationsschritte);
  expectedSteps=(int)(iterationsschritte);

  if(verboseMode)
    cout << "MSB:mean number of steps for one run: " << expectedSteps << endl;
}
	
     
double MSBOptimization::minimize(int)
{
  if( initialisiert==0 )
    zInitialize();

  int i;
  int anz=size();
  int numproblems=anz;

  if( verboseMode )
    { 
      double usedSteps=0;
      for(i=0;i<percentOfSteps.size();i++)
	{
	  usedSteps+=expectedSteps*(percentOfSteps[i]-
				    (i==0?0:percentOfSteps[i-1]))*numproblems;
	  numproblems=(int)(ceil(anz*(1.0-percentOfRun[i])));
	  if( numproblems<1 )numproblems=1;
	}
      usedSteps+=expectedSteps*
	(1.0-percentOfSteps[percentOfSteps.size()-1])*numproblems;
      cout << "MSB: speed factor: " 
	   << (double)usedSteps/(expectedSteps*size()) << endl;
      numproblems=anz=size();
    }

  for(i=0;i<percentOfSteps.size();i++)
    {
      
      int steps=(int)(expectedSteps*(percentOfSteps[i]-
				     (i==0?0:percentOfSteps[i-1])));

      
      for(int a=0;a<numproblems;a++)
	{
	  
	  double v;
	  v= optimization(a)->minimize(steps);
	  if(verboseMode)cout << "MSB:" << i << " " << a << ":" << v << endl;
	}

      sort(); 

      if(verboseMode)
	cout << "MSB: best:" << problem(0)->value() 
	     << "    worst:" << problem(numproblems-1)->value() << endl;

      
      numproblems=(int)(anz*(1.0-percentOfRun[i]));
      if( numproblems<1 )
	numproblems=1;
      if(verboseMode)
	cout << "MSB: now i have : " << numproblems << " Problem's." << endl;
      if(numproblems==1)
	break;
    }
  assert( numproblems>0 );

  
  for(int a=0;a<numproblems;a++)
    optimization(a)->minimize(-1);
  sort();

  double ergebnisWert = problem(0)->value();
  cout << "MSB: value:" << ergebnisWert << " (nicevalue:" 
    << problem(0)->nicevalue() << ")\n";
  nachMinimierung=1;
  return ergebnisWert;
}


     
void MSBOptimization::optimizeValues(Problem &p,int verfahren)
{
	int i;
  struct doubleInt ri[20];
  double mean;
  StatVar end,laufzeit,start;  
  solveProblem(ProblemTestVerboseMode,p,5,-1,verfahren,mean,end,laufzeit,start);
  double fivePercentSteps=(int)(laufzeit.getMean()/20.0);
  double qualitaet[20][20];
  for(i=0;i<20;i++)
    {
      Optimization *o=(Optimization *)genIterOptimizer(verfahren,p,-1);
      for(int a=0;a<20;a++)
	{
	  qualitaet[i][a]=o->minimize((int)fivePercentSteps);
	  cout << qualitaet[i][a] << " ";
	}
      ri[i].a=o->minimize(-1);
      ri[i].i=i;
      cout << ri[i].a << endl;
      delete o;
    }
  qsort(ri,20,sizeof(struct doubleInt),doubleintcompare);

  cout << "#Beschneidungsmatrix, welche die drei besten Laeufe erhaelt: ";
  for(i=0;i<20;i++)
    {
		int a;
      struct doubleInt v[20];
      for(a=0;a<20;a++)
	{ v[a].i=a;v[a].a=qualitaet[a][i];}
      qsort(v,20,sizeof(struct doubleInt),doubleintcompare);
      int nr=0;
      for(a=0;a<20;a++)
	if( v[a].i==ri[0].i || v[a].i==ri[1].i || v[a].i==ri[2].i )
	  nr=a;
      float percent=(1.0-nr/20.0)*100.0;
      if(nr==2)
	percent=100.0;
      cout << "# " << i << " " << (i/20.0)*100 << "%    " << percent << "%\n";
    }
  cout << "#Beschneidungsmatrix, welche die zwei besten Laeufe erhaelt: ";
  for(i=0;i<20;i++)
    {
		int a;
      struct doubleInt v[20];
      for(a=0;a<20;a++)
	{ v[a].i=a;v[a].a=qualitaet[a][i];}
      qsort(v,20,sizeof(struct doubleInt),doubleintcompare);
      int nr=0;
      for(a=0;a<20;a++)
	if( v[a].i==ri[0].i || v[a].i==ri[1].i )
	  nr=a;
      float percent=(1.0-nr/20.0)*100.0;
      if(nr==1)
	percent=100.0;
      cout << "# " << i << " " << (i/20.0)*100 << "%    " << percent << "%\n";
    }
  cout << "#Beschneidungsmatrix, welche den besten Lauf erhaelt: ";
  for(i=0;i<20;i++)
    {int a;
      struct doubleInt v[20];
      for(a=0;a<20;a++)
	{ v[a].i=a;v[a].a=qualitaet[a][i];}
      qsort(v,20,sizeof(struct doubleInt),doubleintcompare);
      int nr=0;
      for(a=0;a<20;a++)
	if( v[a].i==ri[0].i )
	  nr=a;
      float percent=(1.0-nr/20.0)*100.0;
      if(nr==0)
	percent=100.0;
      cout << "# " << i << " " << (i/20.0)*100 << "%    " << percent << "%\n";
    }
}

     
Problem& MSBOptimization::bestProblem()
{
  assert(nachMinimierung==1);
  return *(problem(0));
}
