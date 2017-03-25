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







#ifndef PROBLEMCHANGE
#define PROBLEMCHANGE 
#include <iostream>
#include "general.h"
#include "StatVar.h"

class Optimization;

class ProblemChange

{
	public:
	virtual ~ProblemChange();
	ProblemChange();
};

class Problem {

 private:
  short initialized; 
  int curCompVal;        
  short curCompChange;   
  int maxCompVal;        
  int maxComp;           

  
 protected:
  int curComp;           

 void setValuesFrom(Problem *p);

   virtual int maxDimensionVal(void) ;
  

   virtual int maxDimension(void) ;
  
  
   inline int curDimension(void) { assert(maxComp!=-1);return curComp;}
  

   inline int curDimensionVal(void) { assert(maxComp!=-1);return curCompVal;}
  


   virtual void  _doChange(ProblemChange &c)=0;
  

   virtual int   _change(ProblemChange **p)=0;
  

   virtual void  _undoChange(ProblemChange &c)=0;
  

   virtual void  _initialize(int initialisierung)=0;
  

   virtual double  _value()=0;
  

 public:
   Problem(int maxCompVal=-1,int maxComp=-1,int _initialisierung=0,
		      int _auswertung=0,int _nachbarschaft=0); 

   virtual ~Problem();
  
  
   void doChange(ProblemChange &c);
  

   ProblemChange& change();			
  

   virtual double  value();
  

   virtual double  valueChange(ProblemChange &c);
  

   virtual void  initialize(int a= -23);
  

   inline virtual short endCriterion();	
  

   virtual int   maxNonBetterIterations()=0;
  

   virtual int   expectedNumberOfIterations()=0;
  

   virtual void dumpOn(ostream &strm);
  

   virtual void dumpInfos(ostream &strm);
  

   virtual Problem *makeEqualProblem()=0;
  

   virtual double nicevalue(double vorher=1e100);
  

   virtual StatVar& deviationStatVar(Optimization &s,int anz);
  

   virtual void incrementDirection();
  

  
  
  
  int initialisierung;
  int auswertung;
  int nachbarschaft;
  
  int numberOfFullEvaluations; 
  int numberOfPartEvaluations; 
  int numberOfDoChange;        
                               

 
};

inline short Problem::endCriterion()
{ 
  return 0;
};	

#endif

