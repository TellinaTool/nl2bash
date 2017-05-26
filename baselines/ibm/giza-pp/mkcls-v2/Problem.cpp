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



#include "Problem.h"
#include "Optimization.h"

Problem::~Problem() {}

Problem::Problem(int max,int anz,int _initialisierung,int _auswertung,
	   int _nachbarschaft)
: initialized(0),curCompVal(0),curCompChange(0),maxCompVal(max),maxComp(anz),curComp(0),
  initialisierung(_initialisierung),auswertung(_auswertung),nachbarschaft(_nachbarschaft),
  numberOfFullEvaluations(0),numberOfPartEvaluations(0),numberOfDoChange(0)
{ 
  if( verboseMode>1 )
    cout << "Initialization of Problem: " << maxComp << " " << maxCompVal 
      <<  endl;
}

void Problem::initialize(int i)
{
  curComp=curCompVal=curCompChange=0;
  numberOfFullEvaluations=numberOfPartEvaluations=numberOfDoChange=0;
  initialized=1;
  if( i== -23 )
    _initialize(initialisierung);
  else
    _initialize(i);
  maxComp=maxDimension();
  maxCompVal=maxDimensionVal();
}

void Problem::doChange(ProblemChange &c)
{
  assert (initialized);
  curCompChange=1;
  _doChange(c);
  numberOfDoChange++;	
}

void Problem::incrementDirection()
{
  if( maxCompVal==curCompVal )
    curCompVal=0;
  curCompChange=0;
  curComp=(curComp+1)%maxComp;
}

ProblemChange& Problem::change()
{
  assert( initialized );
  assert( maxCompVal>=curCompVal);

  if( curCompChange||maxCompVal==curCompVal )
    incrementDirection();

  ProblemChange *p;
  int changeFound=_change(&p); 
  curCompVal++;
  if( changeFound==0 )
    return change();  
  else
    return *p;
}
double Problem::value()
{
  numberOfFullEvaluations++;
  if( !initialized )
    initialize();
  return _value();
}

double Problem::valueChange(ProblemChange &x)
{
  numberOfPartEvaluations++;
  assert( initialized );
  double currentValue=value();
  _doChange(x);numberOfDoChange++;
  double newValue=value();
  _undoChange(x);numberOfDoChange++;
  assert( currentValue==value() );
  return newValue-currentValue;
}

void Problem::dumpOn(ostream &strm)
{
  assert( initialized );
  strm << "Problem(" << initialisierung << "," << auswertung << "," 
    << nachbarschaft << ")\n";
  strm << "      #value: " << numberOfFullEvaluations << endl;
  strm << "#valueChange: " << numberOfPartEvaluations << endl;
  strm << "   #doChange: " << numberOfDoChange << endl;
}

StatVar& Problem::deviationStatVar(Optimization &s,int anz)
{
  assert( initialized );
  StatVar &v=*new StatVar;
  double cur=value();
  int howOften=0;
  while( v.getNum()<anz )
    {
      if( howOften++>50000 )
	break;
      double neuer=s.minimize(1);
      if( neuer>cur ) 
	v.addValue(neuer-cur);
      cur=neuer;
      vassert(NULLFLOAT(cur-value()));
    }
  return v;
}

void Problem::dumpInfos(ostream &strm)
{
	strm << "Problem: " << endl;
  assert( initialized );
}


double Problem::nicevalue(double) 
{ 
  return value(); 
}

int Problem::maxDimensionVal(void) {return -1;}
int Problem::maxDimension(void) {return -1;}

ProblemChange::~ProblemChange()
	{
	}
	
ProblemChange::ProblemChange()
	{
	}

void Problem::setValuesFrom(Problem *p)
{
  numberOfFullEvaluations=p->numberOfFullEvaluations;
  numberOfPartEvaluations=p->numberOfPartEvaluations;
  numberOfDoChange=p->numberOfDoChange;
  initialized=p->initialized;
}
