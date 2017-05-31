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




#include <stdlib.h>
#include <iostream>

#include "SAOptimization.h"

#include "ProblemTest.h"

#define ALPHA 0.95 

double SAOptimization::defaultAnfAnnRate=0.9;
double SAOptimization::defaultEndAnnRate=1e-9;
double SAOptimization::defaultMultiple=2.0;


     
SAOptimization::SAOptimization(Problem &p,int m)
: IterOptimization(p,m), temperatur(-1)
{
}



     
SAOptimization::SAOptimization(Problem &p,double t,double a,int s,int m) 
: IterOptimization(p,m),temperatur(t), alpha(a),schrittzahl(s)
{
  assert(alpha<1);
  assert(schrittzahl>0);
  assert(t>0);
}

     
SAOptimization::SAOptimization(SAOptimization &o)
: IterOptimization(o)
{
  temperatur = o.temperatur;
  endTemperatur = o.endTemperatur;
  alpha = o.alpha;
  schrittzahl = o.schrittzahl;
  stepsForAbkuehlung = o.stepsForAbkuehlung;
}

     
void SAOptimization::zInitialize()
{
  IterOptimization::zInitialize();
  if( temperatur<0)
    { 
      

      
      StatVar &v=problem.deviationStatVar(*this,ANZ_VERSCHLECHTERUNGEN); 

      if( maxStep>0 )
	stepsForAbkuehlung=(int)(maxStep*4.0/5.0); 
      else                          
	maxStep=stepsForAbkuehlung=(int)(problem.expectedNumberOfIterations()*
				 defaultMultiple);
      
      temperatur    = v.getMean()/log(1/defaultAnfAnnRate);
      endTemperatur = v.getMean()/log(1/defaultEndAnnRate);
      schrittzahl = (int)(stepsForAbkuehlung/(log(endTemperatur/temperatur)/
					      log(ALPHA)));
      if(schrittzahl==0)schrittzahl=1;
      alpha       = ALPHA;
      
      if( verboseMode )
	cout << "#Algorithm: Simulated Annealing(anfAnnRate=" 
	  << defaultAnfAnnRate <<",(endAnnRate=" << defaultEndAnnRate 
	  << ",T0=" << temperatur<< ",Te=" << endTemperatur<< ",schrittzahl=" 
          << schrittzahl<< ",stepsForAbkuehlung=" << stepsForAbkuehlung 
	  << ")\n";
      curStep=0;
      endFlag=0;
      delete &v;
      problem.initialize();
      IterOptimization::zInitialize();
    }
}

short SAOptimization::end()
{
  if( temperatur>endTemperatur )
    bestStep = curStep;
  if( endFlag>0 &&  temperatur<endTemperatur)
    return 1;
  else
    return 0;
}
void  SAOptimization::abkuehlen()
{
  if(temperatur>=0)
    {
      if( curStep%schrittzahl == 0 )
	temperatur=temperatur * alpha;
      if( curStep> stepsForAbkuehlung)
	temperatur = 0;
    }
}
short SAOptimization::accept(double delta)
{
  if( temperatur<0 )
    return 1;
  else
    {
      if( delta > 0 )
	{
	  if( temperatur==0 )
	    return 0;
	  else
	    {
	      double z=zufall01();
	      assert(z!=0.0);
		  if(z==0.0)
		  	z+=1e-20;
	      double e=exp(-delta/temperatur);
	      
	      
	      
	      return z+0.000000000001<=e; 
	    }
	}
      else
	return 1;
    }
}

void SAOptimization::makeGraphOutput()
{
  IterOptimization::makeGraphOutput();
  *GraphOutput << temperatur;
}



     
double SAOptimization::optimizeValue(Problem &p,int proParameter,int numParameter,
			 int typ,int optimierungsschritte,int print)
{
  switch(typ)
    {
    case 1: 
      {
	double bestPar=-1,best=1e100;
	double now;
	if( print )
	cout << "#SA-optimizeValues: defaultAnfAnnRate" << endl;
	for(int i=0;i<numParameter;i++)
	  {
	    StatVar end,laufzeit,init;
	    defaultAnfAnnRate=0.1 + (1.0/numParameter)*i;
	    solveProblem(0,p,proParameter,optimierungsschritte,SA_OPT,now,
			 end,laufzeit,init);
	    if( best>now )
	      {
		best=now;
		bestPar=defaultAnfAnnRate;
	      }
	    if( print )
	      {
		cout << defaultAnfAnnRate << " ";
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
	defaultAnfAnnRate=0.9;
	return bestPar;
      }
      break;
    case 2: 
      {
	double bestPar=-1,best=1e100;
	double now;
	if( print )
	  cout << "#Optimierung von SA: defaultEndAnnRate" << endl;
	for(int i=1;i<=numParameter;i++)
	  {
	    StatVar end,laufzeit,init;
	    defaultEndAnnRate=1/(pow(10.0,i));
	    solveProblem(0,p,proParameter,optimierungsschritte,SA_OPT,now,end,
			 laufzeit,init);
	    if( best>now )
	      {
		best=now;
		bestPar=defaultEndAnnRate;
	      }
	    if( print )
	      {
		cout << defaultEndAnnRate << " ";
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
	defaultEndAnnRate=1/10000.0;
	return bestPar;
      }
      break;
    case 10: 
      {
	double bestPar=-1,best=1e100;
	
	if( print )
	  cout << "#SA-optimizeValues: defaultMultiple " << 8 << endl;
	for(int i=1;i<=6;i++)
	  {
	    StatVar end,laufzeit,init;
	    double now;
	    defaultMultiple = i;
	    solveProblem(0,p,proParameter,optimierungsschritte,SA_OPT,now,end,
			 laufzeit,init);
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
      cerr << "Error: wrong parameter-type in SAOptimization::optimizeValue ("
	   << typ << ")\n";
      exit(1);
    }
	return 1e100;
}



