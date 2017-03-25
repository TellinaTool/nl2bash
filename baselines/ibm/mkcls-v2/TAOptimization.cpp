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




#include "TAOptimization.h"
#include "ProblemTest.h"


double TAOptimization::defaultAnnRate=0.4;
double TAOptimization::defaultMultiple=2.0;

     
TAOptimization::TAOptimization(Problem &p,double t,double d,int m) 
: IterOptimization(p,m) , temperatur(t) , deltaTemperatur(d)
{
  assert(t>0 && d>0);
}


     
TAOptimization::TAOptimization(Problem&p,int m)
: IterOptimization(p,m), temperatur(-1)
{
}


     
TAOptimization::TAOptimization(TAOptimization &o)
: IterOptimization(o)
{
  temperatur= o.temperatur;
  deltaTemperatur= o.deltaTemperatur;
}



     
void TAOptimization::zInitialize()
{
  IterOptimization::zInitialize();
  if( temperatur<0)
    { 
      
      
      int n;
      
      StatVar &v=problem.deviationStatVar(*this,ANZ_VERSCHLECHTERUNGEN); 

      if(maxStep>0) 
	n=(int)(maxStep*4.0/5.0);    
      else            
	maxStep=n=(int)(problem.expectedNumberOfIterations()*defaultMultiple);
      
      temperatur      = v.quantil(defaultAnnRate);
      deltaTemperatur = temperatur/n;
  
      if( verboseMode>0 )
	cout << "#TA: (anfAnnRate=" 
	  << defaultAnnRate << ",T=" << temperatur << ",deltaT=" 
	  << deltaTemperatur << ")\n";
      curStep=0;
      endFlag=0;
      delete &v;
    }
}


short TAOptimization::end()
{
  
  
  if( temperatur>0 )
    {
      endFlag=0;
      bestStep=curStep;
    }
  return endFlag>0;
}

short TAOptimization::accept(double delta)
{
  if( temperatur<0 ) 
    return 1;
  else
      if( delta < temperatur )
	return 1;
      else
	return 0;
}

void TAOptimization::abkuehlen()
{
  if( temperatur>=0 )
    temperatur=(temperatur-deltaTemperatur>0)?(temperatur-deltaTemperatur):0;
}

void TAOptimization::makeGraphOutput()
{
  IterOptimization::makeGraphOutput();
  *GraphOutput << temperatur;
}



     
double TAOptimization::optimizeValue(Problem &p,int proParameter,int numParameter,int typ,
			 int optimierungsschritte,int print)
{
  switch(typ)
    {
    case 1: 
      {
	double bestPar=-1,best=1e100;
	if(print)cout << "#TA-optimizeValues: " << numParameter << endl;
	for(int i=0;i<=numParameter;i++)
	  {
	    StatVar end,laufzeit,init;
	    double now;
	    defaultAnnRate = (float)(i)/numParameter;
	    solveProblem(0,p,proParameter,optimierungsschritte,TA_OPT,now,end,
			 laufzeit,init);
	    if( best>now )
	      {
		best=now;
		bestPar=defaultAnnRate;
	      }
	    if( print)
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
	  cout << "#Mittelwert 0.2-Quantil 0.8-Quantil Laufzeit Bester"
	          " Sigma SigmaSmaller SigmaBigger\n";
	defaultAnnRate=0.5;
	return bestPar;
      }
      break;
    case 10: 
      {
	double bestPar=-1,best=1e100;
	if( print )
	  cout << "#TA-optimizeValues: defaultMultiple " << 10 << endl;  
	for(int i=1;i<=6;i++)
	  {
	    StatVar end,laufzeit,init;
	    double now;
	    defaultMultiple = i;
	    solveProblem(0,p,proParameter,optimierungsschritte,TA_OPT,now,
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
	  cout << "#Mittelwert 0.2-Quantil 0.8-Quantil Laufzeit Bester Sigma "
                  " SigmaSmaller SigmaBigger\n";
	defaultMultiple=2.0;
	return bestPar;
      }
      break;
    default:
      cerr << "Error: wrong parameter-type in TAOptimization::optimizeValue ("
	   << typ << ")\n";
      exit(1);
    }
  return 1e100;
}


