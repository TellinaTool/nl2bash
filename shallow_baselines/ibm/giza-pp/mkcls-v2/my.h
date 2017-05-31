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



#ifndef HEADER_my_DEFINED
#define HEADER_my_DEFINED

#define over_array(a,i) for(i=(a).low();i<=(a).high();i++)
#define backwards_array(a,i) for(i=(a).high();i>=(a).low();i--)
#define over_arr(a,i) for(int i=(a).low();i<=(a).high();i++)
#define over_arrMAX(a,i,max) for(int i=(a).low();i<=min((a).high(),max-1);i++)
#define backwards_arr(a,i) for(int i=(a).high();i>=(a).low();i--)

extern double n1mult,n2mult,n3mult;

inline double realProb(int n1,int n2)
{
  massert(n1<=n2);
  iassert(n1>=0&&n2>0);
  if(n2==0)n2=1;
  return ((double)n1)/(double)n2;
}

inline double verfProb(int n1,int n2)
{
  double prob = realProb(n1,n2);
  if( n1==1 )return prob*n1mult;
  else if( n1==2 )return prob*n2mult;
  else if( n1==3 )return prob*n3mult;
  else return prob;
}

#endif
