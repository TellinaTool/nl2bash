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




#include "ProblemTest.h"
#include "HCOptimization.h"
#include "RRTOptimization.h"
#include "SAOptimization.h"
#include "TAOptimization.h"
#include "GDAOptimization.h"
#include "MYOptimization.h"
#include <stdio.h>
#include "general.h"
#include <stdlib.h>

short ProblemTestVerboseMode=1;
ofstream *PrintBestTo=0,*PrintBestTo2=0;


int compareProblem(const void *p,const void *j)
{
  double a=(*(Problem **)p)->value();
  double b=(*(Problem **)j)->value();
  if(a==b)
    return 0;
  if(a<b)
    return -1;
  else
    return +1;
}


IterOptimization *genIterOptimizer(int verfahren,Problem &problem,int maxIter)
{
  IterOptimization *opt;
  switch(verfahren)
    {
    case HC_OPT:
      opt = new HCOptimization(problem,maxIter);
      break;
    case GDA_OPT:
      opt = new GDAOptimization(problem,maxIter);
      break;
    case SA_OPT:
      opt = new SAOptimization(problem,maxIter);
      break;
    case TA_OPT:
      opt = new TAOptimization(problem,maxIter);
      break;
    case RRT_OPT:
      opt = new RRTOptimization(problem,maxIter);
      break;
    case MY_OPT:
      opt = new MYOptimization(problem,maxIter);
      break;
    default:
      return 0;
    }
  problem.initialize(); 
  return opt;
}


double solveProblem(int verbose,Problem &problem,int versuche,
		  int optimierungsschritte,int verfahren,double &mean,
		  StatVar &endNice,StatVar &auswertungen,StatVar &startNice,
		  double maxClock,int *iterationsschritte)
{
  double smallestV=1e100;
  Problem *bestP=0;
  StatVar start,end;
  StatVar dauer;
  StatVar iterschritte;

  for(int i=0;i<versuche;i++)
    {
      if(verbose>2)
	{
	  cout << "                  " << i << " of " << versuche << ".\n";
	  cout.flush();
	}
      double vorher=clockSec();

      IterOptimization *opt=genIterOptimizer(verfahren,problem,
					     optimierungsschritte);
      problem.numberOfPartEvaluations=0;

      startNice.addValue(problem.nicevalue());
      start.addValue(problem.value());
      
      double v=opt->minimize(optimierungsschritte);

	if( problem.numberOfPartEvaluations==0)
      auswertungen.addValue(opt->getCurStep());
	else
      auswertungen.addValue(problem.numberOfPartEvaluations);
      iterschritte.addValue(opt->getCurStep());

      endNice.addValue(problem.nicevalue());
      end.addValue(problem.value());
      dauer.addValue(clockSec()-vorher);
      if( verbose>2 )
	{
	  cout << i << ". " << v << ": ";
	  problem.dumpOn(cout);
	}
      delete opt;
      if( v<smallestV && verbose>1 )
	{
	  bestP=problem.makeEqualProblem();
	  smallestV=v;
	}
      if( verbose>2 )
	cout << "  time: " << clockSec() << " best:" << endNice.quantil(0) 
	  << " this:" << problem.nicevalue() << endl;
      if( maxClock && clockSec()>maxClock )
	{
	  if(verbose)
	    cout << "Stop because of time limit ( " << (clockSec()-maxClock) 
	      << " Sekunden)\n";
	  break;
	}
    }
  
  if(verbose)
    {
      cout << "\n***** " << start.getNum() << " runs. (algorithm:";
      switch(verfahren)
	{
	case HC_OPT:
	  cout << "HC";
	  break;
	case RRT_OPT:
	  cout << "RRT";
	  break;
	case GDA_OPT:
	  cout << "GDA";
	  break;
	case TA_OPT:
	  cout << "TA";
	  break;
	case SA_OPT:
	  cout << "SA";
	  break;
	case MY_OPT:
	  cout << "MY";
	  break;
	default:
	  cout << "!unknown!";
	}
      cout << ")*****\n";
      problem.dumpInfos(cout);
      cout << endl;
      cout << "start-costs: "; start.dumpOn(cout); cout << endl;
      cout << "  end-costs: "; end.dumpOn(cout); cout << endl;
      cout << "   start-pp: "; startNice.dumpOn(cout); cout << endl;
      cout << "     end-pp: "; endNice.dumpOn(cout); cout << endl;
      cout << " iterations: "; auswertungen.dumpOn(cout); cout << endl;
      cout << "       time: "; dauer.dumpOn(cout);
      cout << endl;
    }
  if( bestP )
    {
      if(PrintBestTo)
	bestP->dumpOn(*PrintBestTo);
      else
	bestP->dumpOn(cout);
      delete bestP;
    }
  mean = end.getMean();
  if( iterationsschritte )
    *iterationsschritte=(int)(iterschritte.getMean());
  return end.getSmallest();
}



void multiSolveProblem(Problem &problem,int versuche,int maxSeconds)
{
	int i;
  int maxLaeufe;
  double rDummy;
  StatVar end[MAX_OPT_NR],auswertungen[MAX_OPT_NR],start[MAX_OPT_NR];
  double maxClock=clockSec()+maxSeconds;
  if(maxSeconds<=0)maxClock=0;
  solveProblem(ProblemTestVerboseMode,problem,versuche,-1,HC_OPT,rDummy,
	       end[HC_OPT],auswertungen[HC_OPT],start[HC_OPT],maxClock);
  maxLaeufe=(int)(auswertungen[HC_OPT].getMean()*5);
  for(i=0;i<MAX_OPT_NR;i++)
    {
      if( i==HC_OPT )
	continue;
      double maxClock=clockSec()+maxSeconds;
      if(maxSeconds<=0)maxClock=0;
      solveProblem(ProblemTestVerboseMode,problem,versuche, -1,i,rDummy,end[i],
		   auswertungen[i],start[i],maxClock);
    }
  end[HC_OPT].title = "  HC";
  end[SA_OPT].title =   "  SA";
  end[GDA_OPT].title =  " GDA";
  end[RRT_OPT].title =  " RRT";
  end[TA_OPT].title =   "  TA";
  end[MY_OPT].title =   "  MY";

    for(i=0;i<MAX_OPT_NR;i++) 
    end[i].quantil(0.5);

  cout << "mean: \n";
  compareStatVarQuantil=-1;
  qsort(end,MAX_OPT_NR,sizeof(StatVar),compareStatVar);
  for(i=0;i<MAX_OPT_NR;i++)
    cout << end[i].title << " " << end[i].getMean() << endl;

  cout << "\nbest: \n";
  compareStatVarQuantil=0;
  qsort(end,MAX_OPT_NR,sizeof(StatVar),compareStatVar);
  for(i=0;i<MAX_OPT_NR;i++)
    cout << end[i].title << " " << end[i].quantil(compareStatVarQuantil) 
      << endl;

  cout << "\n20%-quantil: \n";
  compareStatVarQuantil=0.2;
  qsort(end,MAX_OPT_NR,sizeof(StatVar),compareStatVar);
  for(i=0;i<MAX_OPT_NR;i++)
    cout << end[i].title << " " << end[i].quantil(compareStatVarQuantil) 
      << endl;
}


void metaOptimization(Problem &tp,int nLaeufe,int nPars)
{
  double bestPar,bestValue;

  bestPar=IterOptimizationOptimizeParameter(tp,TAOptimization::defaultAnnRate,0.0,1.0,nLaeufe,nPars,TA_OPT,bestValue);
  cout << "#TA(defaultAnnRate) BEST-PAR: " << bestPar << "   BEST-VAL: " << bestValue << endl;
  bestPar=IterOptimizationOptimizeParameter(tp,RRTOptimization::defaultAnnRate,0.0,1.0,nLaeufe,nPars,RRT_OPT,bestValue);
  cout << "#RRT(defaultAnnRate) BEST-PAR: " << bestPar << "   BEST-VAL: " << bestValue << endl;
  bestPar=IterOptimizationOptimizeParameter(tp,GDAOptimization::defaultAlpha,0.0,0.01,nLaeufe,nPars,GDA_OPT,bestValue);
  cout << "#GDA(defaultAlpha) BEST-PAR: " << bestPar << "   BEST-VAL: " << bestValue << endl;
  bestPar=IterOptimizationOptimizeParameter(tp,SAOptimization::defaultEndAnnRate,0.0,1.0,nLaeufe,nPars,SA_OPT,bestValue);
  cout << "#SA(defaultEndAnnRate) BEST-PAR: " << bestPar << "   BEST-VAL: " << bestValue << endl;
}
