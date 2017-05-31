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




#include "GDAOptimization.h"
#include "ProblemTest.h"
#include <cmath>

#define GDAOptimization GDAOptimization
#define IterOptimization IterOptimization

     
     
double GDAOptimization::defaultTemperatur=1e100;


double GDAOptimization::defaultAlpha=0.001;


     
GDAOptimization::GDAOptimization(Problem &p,int m) 
: IterOptimization(p,m) ,temperatur(defaultTemperatur),alpha(defaultAlpha)
{
}

     
GDAOptimization::GDAOptimization(Problem &p,double t,double a,int m) 
: IterOptimization(p,m) ,temperatur(t) ,alpha(a)
{
}

     
GDAOptimization::GDAOptimization(GDAOptimization &o)
: IterOptimization(o)
{
  temperatur = o.temperatur;
  alpha      = o.alpha;
  gdaEndFlag = o.gdaEndFlag;
}

     
void GDAOptimization::zInitialize()
{
  IterOptimization::zInitialize();
  if(temperatur==1e100)
    { 
      double v=problem.value(); 
      
      
      
      
      
      temperatur=v;
    	}
  assert(alpha>=0);
}

short GDAOptimization::accept(double delta)
{
  if(  curValue + delta < temperatur )
    return 1;
  else
    return 0;
}

void  GDAOptimization::abkuehlen()
{
  double newTemperatur =  temperatur - alpha*(temperatur - curValue);
  if( fabs(temperatur - newTemperatur)<1e-30 ) 
    gdaEndFlag=1;
  else
    gdaEndFlag=0;
  temperatur = newTemperatur;
}

short GDAOptimization::end()
{
  return ( endFlag>0 ) && ( gdaEndFlag );
}

void GDAOptimization::makeGraphOutput()
{
  IterOptimization::makeGraphOutput();
  *GraphOutput << temperatur-curValue;
}
	


     
double GDAOptimization::optimizeValue(Problem &p,int proParameter,int numParameter,int typ,
			 int optimierungsschritte,int print)
{
  if(typ!=1)
    {
      cerr << "Error: wrong parameter-type in GDAOptimization::optimizeValue ("
	<< typ << ")\n";
      exit(1);
    }
  else
    {
      double bestPar=-1,best=1e100;
      double now;
      if( print )
	cout << "#GDA-optimizeValues: " << numParameter<<endl;

      
      defaultTemperatur=1e100; 

      for(int i=0;i<=numParameter;i++)
	{
	  StatVar end,laufzeit,init;
	  defaultAlpha = pow(pow(200,1.0/numParameter),i)*0.002;
	  solveProblem(0,p,proParameter,optimierungsschritte,GDA_OPT,now,end,
		       laufzeit,init);
	  if( best>now )
	    {
	      best=now;
	      bestPar=defaultAlpha;
	    }
	  if( print )
	    {
	      cout << defaultAlpha <<" ";
	      cout << end.getMean() << " " << end.quantil(0.2) << " " 
		<< end.quantil(0.79) << "  " << laufzeit.getMean() << " " 
		<< end.quantil(0.0) << " " << end.getSigma() << " " 
		<< end.getSigmaSmaller()<< " "<< end.getSigmaBigger()<< endl;
	    }
	}
      if( print )
	cout << "#Parameter Mittelwert 0.2-Quantil 0.8-Quantil Laufzeit"
	        " Bester Sigma SigmaSmaller SigmaBigger\n";
      defaultAlpha=0.03;
      return bestPar;
    }
	return 1e100;
}

