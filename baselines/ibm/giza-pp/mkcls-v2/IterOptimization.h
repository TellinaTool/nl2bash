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







#ifndef ITEROPTIMIZATION
#define ITEROPTIMIZATION

#include "Optimization.h"





#define ANZ_VERSCHLECHTERUNGEN 500 

extern ostream *GraphOutput; 
                             

class IterOptimization : public Optimization
	{
  

   private:   
     int maxNonBetterIterations; 
     

   protected:
     Problem &problem;  
     int curStep;	
     double curValue;	
     int bestStep;      
     double bestValue;	
     int maxStep;       
     int initialisiert; 
     short endFlag;     
     short endFlag2;     
       
       


      virtual void makeGraphOutput();
     

      virtual short end()=0;
     

      virtual void  abkuehlen()=0;
     

      virtual short accept(double delta)=0;
     

      virtual void zInitialize();
     

   public:
      IterOptimization(Problem &p,int maxIter=-1);
     

      IterOptimization(IterOptimization &o);
     

      virtual double minimize(int steps=-1);
     

      inline int getCurStep();
     

      inline double getCurrentValue(); 
     

      inline const Problem& getProblem(); 
     

};

double IterOptimizationOptimizeParameter(Problem &p,
			     double &parameter,double min,double max,
			     int nRun,int nPar,int verfahren,double &bv);

inline int IterOptimization::getCurStep() 
{ 
  return curStep;
};
inline double IterOptimization::getCurrentValue() 
{ 
  return curValue; 
}; 
inline const Problem& IterOptimization::getProblem() 
{ 
  return problem; 
}; 

#endif




