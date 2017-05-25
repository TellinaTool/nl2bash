/*

Copyright (C) 2000,2001  Franz Josef Och (RWTH Aachen - Lehrstuhl fuer Informatik VI)

This file is part of GIZA++ ( extension of GIZA ).

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
#include "model3.h"
#include "collCounts.h"

bool makeOneMoveSwap(const alignment&x,const alignment&y,set<OneMoveSwap>&soms)
{
  OneMoveSwap oms;
  oms.type=0;
  int count=0;
  Vector<int> positions(4);
  assert(x.get_m()==y.get_m());
  for(PositionIndex j=1;j<=x.get_m();j++)
    if(x(j)!=y(j))
      {
	if(count==4)
	  return 0;
	positions[count]=j;
	count++;
      }
  assert(count>0);
  if(count==1)
    {
      oms.type=1;
      oms.a=positions[0];
      oms.b=y(positions[0]);
      soms.insert(oms);
      for(unsigned int j=1;j<=x.get_m();++j)
	{
	  if( int(j)!=positions[0]&&y(j)==y(positions[0]))
	    {
	      oms.type=3;
	      oms.a=j;
	      oms.b=x(positions[0]);
	      soms.insert(oms);
	    }
	}
      for(unsigned int j=1;j<=x.get_m();++j)
	{
	  if( int(j)!=positions[0]&&x(j)==x(positions[0]))
	    {
	      oms.type=2;
	      oms.a=positions[0];
	      oms.b=j;
	      if( oms.b<oms.a)swap(oms.b,oms.a);
	      soms.insert(oms);
	    }
	}
      return 1;
    }
  else if(count==2)
    {
      if(x(positions[0])==y(positions[1]) && x(positions[1])==y(positions[0]))
	{
	  oms.type=4;
	  oms.a=positions[0];
	  oms.b=positions[1];
	  soms.insert(oms);
	  for(unsigned int j=1;j<=x.get_m();++j)
	    {
	      if( int(j)!=positions[0]&&y(j)==y(positions[0]))
		{
		  oms.type=2;oms.a=j;oms.b=positions[1];if( oms.b<oms.a)swap(oms.b,oms.a);soms.insert(oms);
		}
	      if( int(j)!=positions[1]&&y(j)==y(positions[1]))
		{
		  oms.type=2;oms.a=j;oms.b=positions[0];if( oms.b<oms.a)swap(oms.b,oms.a);soms.insert(oms);
		}
	    } 
	}
      else if(x(positions[0])==y(positions[1]) )
	{
	  oms.type=3;
	  oms.a=positions[0];
	  oms.b=x(positions[1]);
	  soms.insert(oms);
	  oms.type=2;
	  oms.a=positions[0];
	  oms.b=positions[1];
	  soms.insert(oms);	  
	}
      else if( x(positions[1])==y(positions[0]) )
	{
	  oms.type=3;
	  oms.a=positions[1];
	  oms.b=x(positions[0]);
	  soms.insert(oms);
	  oms.type=2;
	  oms.a=positions[0];
	  oms.b=positions[1];
	  soms.insert(oms);	  
	}
      oms.type=3;
      oms.a=positions[0];
      oms.b=x(positions[0]);
      soms.insert(oms);
      oms.a=positions[1];
      oms.b=x(positions[1]);
      soms.insert(oms);
      return 1;
    }
  else if( count==3 )
    { // three differences and three different numbers
      Vector<int> xx(3),yy(3);
      xx[0]=x(positions[0]);xx[1]=x(positions[1]);xx[2]=x(positions[2]);
      yy[0]=y(positions[0]);yy[1]=y(positions[1]);yy[2]=y(positions[2]);
      sort(xx.begin(),xx.end());
      sort(yy.begin(),yy.end());
      if(xx==yy)
	{
	  oms.type=2;oms.a=positions[0];oms.b=positions[1];soms.insert(oms);
	  oms.type=2;oms.a=positions[0];oms.b=positions[2];soms.insert(oms);
	  oms.type=2;oms.a=positions[1];oms.b=positions[2];soms.insert(oms);
	}
      else
	{
	  //cout << "HERE.\n";
	  if( x(positions[0])==y(positions[1])&&x(positions[1])==y(positions[0]) )
	    { 
	      oms.type=2;oms.a=positions[0];oms.b=positions[1];
	      if( oms.b<oms.a) swap(oms.b,oms.a);
	      soms.insert(oms);
	      oms.type=3;oms.a=positions[2];oms.b=x(positions[2]);soms.insert(oms);
	    }
	  if( x(positions[2])==y(positions[1])&&x(positions[1])==y(positions[2]) )
	    { 
	      oms.type=2;oms.a=positions[2];oms.b=positions[1];
	      if( oms.b<oms.a) swap(oms.b,oms.a);
	      soms.insert(oms);
	      oms.type=3;oms.a=positions[0];oms.b=x(positions[0]);soms.insert(oms);
	    }
	  if( x(positions[0])==y(positions[2])&&x(positions[2])==y(positions[0]) )
	    { 
	      oms.type=2;oms.a=positions[0];oms.b=positions[2];
	      if( oms.b<oms.a) swap(oms.b,oms.a);
	      soms.insert(oms);
	      oms.type=3;oms.a=positions[1];oms.b=x(positions[1]);soms.insert(oms);
	    }
	}
      return 1;
    }
  else if(count==4)
    {
     Vector<int> xx(4),yy(4);
     for(int i=0;i<4;++i)
       {
	 xx[i]=x(positions[i]);
	 yy[i]=y(positions[i]);
       }
      sort(xx.begin(),xx.end());
      sort(yy.begin(),yy.end());
      if(xx==yy)
	{
	  oms.type=2;
	  for(int j1=0;j1<4;j1++)
	    for(int j2=j1+1;j2<4;j2++)
	      {
		if(x(positions[j1])!=x(positions[j2])&&
		   x(positions[j1])==y(positions[j2])&&
		   x(positions[j2])==y(positions[j1]))
		  {
		    oms.type=2;oms.a=positions[j1];oms.b=positions[j2];
		    soms.insert(oms);
		  }
	      }
	}
      return 1;
    }
  else
    return 0;
}
