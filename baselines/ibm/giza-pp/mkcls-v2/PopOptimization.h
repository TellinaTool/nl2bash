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







#ifndef POPULATIONOPTIMIZATION
#define POPULATIONOPTIMIZATION

#include "Optimization.h"

typedef struct 
{
  Optimization *opt;
  Problem *prob;
} ProbAndOpt;

bool operator<(const ProbAndOpt&a, const ProbAndOpt&b);
bool operator==(const ProbAndOpt&a, const ProbAndOpt&b);
ostream& operator<<(ostream& , const ProbAndOpt&b);
istream& operator>>(istream& , ProbAndOpt&b);

inline DEFINE_STANDARD_COMPARE(ProbAndOpt)

int compareProbAndOpt(const void *p,const void *j);

class PopOptimization : public Optimization {


   private:
     Array<ProbAndOpt> probandopt; 
       
   protected:
     int initialisiert;          
     Problem *originalProblem;   
											     
											     
											     int verfahren;              
                                 

      virtual void zInitialize();
     

   public:
      PopOptimization(Problem &s,int verf,int anz);
     
     
     virtual ~PopOptimization() {}

      int size();
     
     
      void sort();
     

      virtual Problem& bestProblem()=0;
     

      Problem *problem(int i);
     

      Optimization *optimization(int i);
     

};
#endif
