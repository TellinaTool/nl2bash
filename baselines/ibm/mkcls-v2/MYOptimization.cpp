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




#include "MYOptimization.h"

MYOptimization::MYOptimization(Problem &p,int m) 
: IterOptimization(p,m),acceptFlagsNumber(0),acceptions(0),total(0)
{
}
MYOptimization::MYOptimization(MYOptimization &o)
: IterOptimization(o),acceptFlagsNumber(0),acceptions(0),total(0)
{
}
short MYOptimization::accept(double delta)
	{
	int doIt;
	int verbesserung = delta<0;
  	if( delta < 0 )
    	doIt=1;
  	else
    	{
		if(total>=NUMBER_OF_ACCEPTIONS)
			{
		 	double prob = acceptions/(float)(NUMBER_OF_ACCEPTIONS);
			double zuf = zufall01();
			
			doIt=zuf<prob;
			}
		else
			doIt=0;
		}
	if( total>=NUMBER_OF_ACCEPTIONS )
		{ 
		if( acceptFlags[acceptFlagsNumber] )
			acceptions--;
		}
	acceptFlags[acceptFlagsNumber]=verbesserung;
	if( verbesserung )
		acceptions++;
	total++;
	acceptFlagsNumber++;
	if(acceptFlagsNumber>=NUMBER_OF_ACCEPTIONS)
		acceptFlagsNumber=0;
	return doIt;
	}
	
short MYOptimization::end() 
	{ 
 	return endFlag>0 && total>NUMBER_OF_ACCEPTIONS && acceptions==0; 
	}
void MYOptimization::abkuehlen()
	{
	}


     
void MYOptimization::makeGraphOutput()
{
  IterOptimization::makeGraphOutput();
  *GraphOutput << acceptions;
}

