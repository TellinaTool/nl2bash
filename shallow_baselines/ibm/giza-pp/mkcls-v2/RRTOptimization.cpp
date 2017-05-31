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




#include "RRTOptimization.h"
#include "ProblemTest.h"

double RRTOptimization::defaultAnnRate=0.6;
double RRTOptimization::defaultMultiple=2.0;


     
RRTOptimization::RRTOptimization(Problem &p,double t,double dt,int m) 
: IterOptimization(p,m),deviation(t),deltaDeviation(dt)
{  
  assert(deviation>=0);
}


     
RRTOptimization:: RRTOptimization(Problem &p,int m) 
: IterOptimization(p,m),deviation(-1),deltaDeviation(0)
{
}


     
RRTOptimization::RRTOptimization(RRTOptimization &o)
: IterOptimization(o)
{
  deviation     = o.deviation;
  deltaDeviation= o.deltaDeviation;
  record        = o.record;
}


     
void RRTOptimization::zInitialize()
{
  IterOptimization::zInitialize();
  if( deviation<0 )
    { 
      

      int n;
      
      StatVar &v=problem.deviationStatVar(*this,ANZ_VERSCHLECHTERUNGEN); 

      if( maxStep>0 ) 
	n=(int)(maxStep*4.0/5.0);    
      else            
	maxStep=n=(int)(problem.expectedNumberOfIterations()*defaultMultiple);
 
      deviation      = v.quantil(defaultAnnRate);
      deltaDeviation = deviation/(float)n;

      if( verboseMode>0 )
	cout << "#Algorithm: Record-To-Record-Travel: (anfAnnRate="
	  << defaultAnnRate << ",T=" << deviation << ",deltaT=" 
	  << deltaDeviation << ")\n";

      curStep=0;
      endFlag=0;
      delete &v;
      problem.initialize();
      IterOptimization::zInitialize();
    }
  record=problem.value();
  assert(deviation>=0);
}

short RRTOptimization::end()
{
  return ( endFlag>0 && deviation==0.0 );
}
void  RRTOptimization::abkuehlen()
{
  if( deviation>=0 )
    {
      deviation -= deltaDeviation;
      if(deviation<0)
	deviation=0;
    }
}
short RRTOptimization::accept(double delta)
{
  if( deviation<0 )
    return 1;
  else
    {
      if(  delta + curValue - deviation < record )
	{
	  if( delta + curValue < record )
	    record = delta+curValue;
	  return 1;
	}
      else
	return 0;
    }
}

void RRTOptimization::makeGraphOutput()
{
  IterOptimization::makeGraphOutput();
  *GraphOutput << deviation;
}



     
double RRTOptimization::optimizeValue(Problem &p,int proParameter,int numParameter,int typ,
			 int optimierungsschritte,int print)
{
  switch(typ)
    {
    case 1: 
      {
	double bestPar=-1,best=1e100;
	if( print )
	  cout << "#RRT-optimizeValues: Quantil: " << numParameter << endl;
	for(int i=0;i<=numParameter;i++)
	  {
	    StatVar end,laufzeit,init;
	    double now;
	    if(i==0) defaultAnnRate=0.2;
	    else defaultAnnRate = 0.3+(float)(0.6*i)/numParameter;
	    solveProblem(0,p,proParameter,optimierungsschritte,RRT_OPT,now,
			 end,laufzeit,init);
	    if( best>now )
	      {
		best=now;
		bestPar=defaultAnnRate;
	      }
	    if( print )
	      {
		cout << defaultAnnRate << " ";
		cout << end.getMean() << " " << end.quantil(0.2) << " " 
		  << end.quantil(0.79) << "  " << laufzeit.getMean() << " " 
		  << end.quantil(0.0) << " " << end.getSigma() << " " 
		  << end.getSigmaSmaller() << " " << end.getSigmaBigger() 
		  << " " << now << endl;
	      }
	  }
	if( print )
	  cout << "#Parameter Mittelwert 0.2-Quantil 0.8-Quantil Laufzeit "
	          "Bester Sigma SigmaSmaller SigmaBigger\n";
	defaultAnnRate=0.8;
	return bestPar;
      }
      break;
    case 10: 
      {
	double i;
	double bestPar=-1,best=1e100;
	StatVar end,laufzeit,init;
	
	if( print )
	  cout << "#RRT-optimizeValues: defaultMultiple" << 8 << endl;    
	for(i=0.5;i<=10;i+=1.5)
	  {
	    double now;
	    defaultMultiple = i;
	    solveProblem(0,p,proParameter,optimierungsschritte,RRT_OPT,now,
			 end,laufzeit,init);
	    if( best>now )
	      {
		best=now;
		bestPar=defaultMultiple;
	      }
	    if( print )
	      {
		cout << defaultMultiple << " ";
		cout << end.getMean() << " " << end.quantil(0.2) << " " 
		  << end.quantil(0.79) << "  " << laufzeit.getMean() << " " 
		  << end.quantil(0.0) << " " << end.getSigma() << " " 
		  << end.getSigmaSmaller() << " " << end.getSigmaBigger() 
		  << " " << now << endl;
	      }
	  }
	if( print )
	  cout << "#Parameter Mittelwert 0.2-Quantil 0.8-Quantil Laufzeit "
	          "Bester Sigma SigmaSmaller SigmaBigger\n";
	defaultMultiple=2.0;
	return bestPar;
      }
      break;
    default:
      cerr << "Error: wrong parameter-type in RRTOptimization::optimizeValue ("
	<< typ << ")\n";
      exit(1);
    }
	return 1e100;
}


