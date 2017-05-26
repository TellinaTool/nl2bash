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



#include "IterOptimization.h"
#include "ProblemTest.h"

ostream *GraphOutput; 


  
IterOptimization::IterOptimization(Problem& p,int m) 
  : maxNonBetterIterations(0),problem(p),maxStep(m),initialisiert(0)
{
}



IterOptimization::IterOptimization(IterOptimization& o) : Optimization(),problem(o.problem)
{
  maxNonBetterIterations=o.maxNonBetterIterations;
  curValue = o.curValue;
  bestStep = o.bestStep;
  bestValue = o.bestValue;
  maxStep = o.maxStep;
  initialisiert = o.initialisiert;
  endFlag = o.endFlag;
  endFlag2 = o.endFlag2;
}


     
double IterOptimization::minimize(int steps)
{
  if( !initialisiert )
    zInitialize();
  
  if( steps==0 )
    return curValue;
  
  int t=0;
  int every=(steps<0)?10000:(steps/1000+1);
  
  do
    {
      curStep++; 
      t++;
      if(verboseMode&&(curStep%1000==0))
	{
	  if(steps>0)
	    cout << "Processed: " << 100.0*(curStep/(double)max(maxStep,1)) << " percent. (IterOptimization run) " 
		 << curValue << " max:" << maxStep << " " << steps << "            \r";
	  else
	    cout << "In step:" << curStep << " currentValue: " << curValue 
		 << " bestValue: " << bestValue-curValue << " " << curStep-bestStep << ".           \r";
	  cout.flush();
	}
      
      
      ProblemChange *change= &(problem.change());
      
      
      double delta=problem.valueChange(*change);
      
      
      abkuehlen();
      
      
      if( accept(delta) )
	{
	  
	  problem.doChange(*change);
	  
	  
	  curValue+=delta;
	  
	  
	  if( curValue<bestValue-1e-10 )
	    {
	      bestValue=curValue;
	      bestStep=curStep;
	      endFlag2=endFlag=0;
	    }
	  
	  if( verboseMode>1 )
	    cout<<"in step: "<<curStep<<" accepted with : "<<delta<<endl;
	}
      
      if(curStep - bestStep>maxNonBetterIterations && maxNonBetterIterations>0)
	endFlag=1;
      if(curStep - bestStep>2*maxNonBetterIterations && maxNonBetterIterations>0)
	endFlag2=1;
      
      
      
      if( GraphOutput&&((curStep%every)==0) )
	{
	  makeGraphOutput();
	  *GraphOutput<<" "<<delta<<endl;
	}
      
      delete change;
    } while( t!=steps && (!end()) && (!problem.endCriterion()) );
  
  if( GraphOutput)
    {
      makeGraphOutput();
      *GraphOutput<<endl;
    }
  return curValue;
}


void IterOptimization::zInitialize() 
{
  initialisiert=1;
  bestValue=curValue=problem.value();
  maxNonBetterIterations=problem.maxNonBetterIterations();
  bestStep=curStep=0;
  endFlag2=endFlag=0;
}


void IterOptimization::makeGraphOutput()
{
  
  *GraphOutput << curStep << " " <<curValue << " ";
}


double IterOptimizationOptimizeParameter(Problem &p,
					 double &parameter,double min,double max,
					 int nRun,int nPar,int verfahren,
					 double &bv)
{
  if( nPar<=0 )
    return (max+min)/2;
  
  StatVar end1,time1,init1;
  StatVar end2,time2,init2;
  double mean1,mean2;
  double par1,par2;

  parameter = par1 = min + (max-min)/3;
  solveProblem(0,p,nRun,-1,verfahren,mean1,end1,time1,init1);
  cout << parameter << " " << mean1 << " " << end1.quantil(0.0) << " " << end1.quantil(1.0) << endl;

  parameter = par2 = min + 2*(max-min)/3;
  solveProblem(0,p,nRun,-1,verfahren,mean2,end2,time2,init2);
  cout << parameter << " " << mean2 << " " << end2.quantil(0.0) << " " << end2.quantil(1.0) << endl;
  
  double bestPar,bestVal;
  if(mean1<mean2)
    {
      bestVal = mean1;
      bestPar=IterOptimizationOptimizeParameter(p,parameter,min,min+2*(max-min)/3,nRun,nPar-2,verfahren,bestVal);
    }
  else
    {
      bestVal = mean2;
      bestPar=IterOptimizationOptimizeParameter(p,parameter,min+(max-min)/3,max,nRun,nPar-2,verfahren,bestVal);
    }
  if( mean1<bestVal&&mean1<=mean2 )
    {
      bv = mean1;
      return par1;
    }
  else if(mean2<bestVal && mean2<=mean1)
    {
      bv = mean2;
      return par2;
    }
  else
    {
      bv = bestVal;
      return bestPar;
    }
}
