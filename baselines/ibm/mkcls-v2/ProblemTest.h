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







#ifndef PROBLEMTEST_H
#define PROBLEMTEST_H

#include "Problem.h"
#include "StatVar.h"
#include <fstream>


enum {TA_OPT, HC_OPT, SA_OPT,RRT_OPT,GDA_OPT,MAX_OPT_NR,MY_OPT };

class IterOptimization;

extern short ProblemTestVerboseMode;

extern ofstream *PrintBestTo,*PrintBestTo2;

double solveProblem(int verbose,Problem &problem,int versuche,
int optimierungsschritte,int verfahren,double &mean,StatVar &endValue,
StatVar &laufzeit,StatVar &initValue,double maxSec= 0,int *iterationsschritte=0);



int compareProblem(const void *p,const void *j);



void multiSolveProblem(Problem &problem,int versuche,int maxSeconds);



IterOptimization *genIterOptimizer(int verfahren,Problem &problem,int maxIter);


void metaOptimization(Problem &p,int nLaeufe,int nPars);

#endif
