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







#ifndef MSBOPTIMIZATION
#define MSBOPTIMIZATION 

#include "PopOptimization.h"

class MSBOptimization : public PopOptimization
	{

   protected:
     
     Array<double> percentOfSteps; 
     Array<double> percentOfRun;

     int expectedSteps;     
     short nachMinimierung; 
     
      virtual void zInitialize();
     

   public:
      MSBOptimization(Problem &s,int verf,int anz,Array<double> &pos,
				 Array<double> &por);
     

     virtual ~MSBOptimization(){}

      virtual double minimize(int steps=-1);
     

      static void optimizeValues(Problem &p,int verfahren);
     

      Problem& bestProblem();
     

};
#endif











