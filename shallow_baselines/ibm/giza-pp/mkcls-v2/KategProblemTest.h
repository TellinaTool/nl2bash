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







#include "KategProblem.h"


KategProblem &makRandom(int ANZ_WORD,int ANZ_CLS,int initialisierung,
			int auswertung,int nachbarschaft,float relInit=0.1);



KategProblem *fromKModel(const char *str,int maxClass,int initialisierung,
			 int auswertung,int nachbarschaft,int minWordFrequency);


KategProblem *fromNgrFile(const char *str,int maxClass,int initialisierung,
			 int auswertung,int nachbarschaft,int minWordFrequency);

void writeClasses(Array<Kategory> &katOfWord,KategProblem &problem,ostream &to);



int fromCatFile(KategProblem *p,const char *s,bool verb=1);



KategProblem *izrOptimization(KategProblem &p,int minN,int firstN,
double clockForOneRed,double maxClock,int verfahren);



void KategProblemSetParameters(KategProblem &p);


