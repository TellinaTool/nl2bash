/*

EGYPT Toolkit for Statistical Machine Translation
Written by Yaser Al-Onaizan, Jan Curin, Michael Jahr, Kevin Knight, John Lafferty, Dan Melamed, David Purdy, Franz Och, Noah Smith, and David Yarowsky.

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
/* --------------------------------------------------------------------------*
 *                                                                           *
 * Module :ATables                                                           *
 *                                                                           *
 * Prototypes File: ATables.h                                                *
 *                                                                           *
 * Objective: Defines clases and methods for handling I/O for distortion  &  *
 *            alignment tables.                                              *
 *****************************************************************************/

#ifndef _atables_h
#define _atables_h 1

#include "defs.h"
#include <cassert>
#include <iostream>
#include <algorithm>
#include <functional>
#include <map>
#include <set>
#include "Vector.h"
#include <utility>
#include <fstream>
#include "Array4.h"
#include "myassert.h"
#include "Globals.h"

extern bool CompactADTable;
extern float amodel_smooth_factor;
extern short NoEmptyWord;

/* ------------------- Class Defintions of amodel ---------------------------*/
/* Class Name: amodel:
   Objective: This defines the underlying data structure for distortiont prob.
   and count tables. They are defined as a hash table. Each entry in the hash
   table is the probability (d(j/l,m,i), where j is word target position, i is
   source word position connected to it, m is target sentence length, and l is
   source sentence length) or count collected for it. The  probability and the
   count are represented as log integer probability as 
   defined by the class LogProb .  

  This class is used to represents a Tables (probabiliity) and d (distortion)
  tables and also their corresponding count tables .
  
  *--------------------------------------------------------------------------*/

inline int Mabs(int a)
{
  if(a<0)
    return -a;
  else
    return a;
}

template <class VALTYPE>
class amodel
{
 public:
  Array4<VALTYPE> a;
  bool is_distortion ; 
  WordIndex MaxSentLength;
  bool ignoreL, ignoreM;
  VALTYPE get(WordIndex aj, WordIndex j, WordIndex l, WordIndex m)const
    {
      massert( (!is_distortion) || aj<=m );massert( (!is_distortion) || j<=l );massert( (!is_distortion) || aj!=0 );
      massert( is_distortion    || aj<=l );massert( is_distortion    || j<=m );massert( (is_distortion) || j!=0 );
      massert( l<MaxSentLength );massert( m<MaxSentLength );
      return a.get(aj, j, (CompactADTable&&is_distortion)?MaxSentLength:(l+1),(CompactADTable&&!is_distortion)?MaxSentLength:(m+1));
    }
  static float smooth_factor;
  amodel(bool flag)
    : a(MAX_SENTENCE_LENGTH+1,0.0), is_distortion(flag), MaxSentLength(MAX_SENTENCE_LENGTH)
    {}; 
  VALTYPE&getRef(WordIndex aj, WordIndex j, WordIndex l, WordIndex m)
    {
      massert( (!is_distortion) || aj<=m );massert( (!is_distortion) || j<=l );
      massert( is_distortion    || aj<=l );massert( is_distortion    || j<=m );massert( (is_distortion) || j!=0 );
      massert( l<MaxSentLength );massert( m<MaxSentLength );
      return a(aj, j, (CompactADTable&&is_distortion)?MaxSentLength:(l+1),(CompactADTable&&!is_distortion)?MaxSentLength:(m+1));
    }
  void setValue(WordIndex aj, WordIndex j, WordIndex l, WordIndex m, VALTYPE val)
    {
      getRef(aj, j, l, m)=val;
    }
  VALTYPE getValue(WordIndex aj, WordIndex j, WordIndex l, WordIndex m) const
    {
      if( is_distortion==0 )
	return max(double(PROB_SMOOTH),amodel_smooth_factor/(l+1)+(1.0-amodel_smooth_factor)*get(aj, j, l, m));
      else
	return max(double(PROB_SMOOTH),amodel_smooth_factor/m+(1.0-amodel_smooth_factor)*get(aj, j, l, m));	
    }
  void printTable(const char* filename)const ; 
  template<class COUNT>
  void normalize(amodel<COUNT>& aTable)const
    {
      WordIndex i, j, l, m ;
      COUNT total;
      int nParam=0;
      for(l=0;l<MaxSentLength;l++)
	for(m=0;m<MaxSentLength;m++)
	  {
	    if( CompactADTable && l!=m )
	      continue;
	    unsigned int L=((CompactADTable&&is_distortion)?MaxSentLength:(l+1))-1;
	    unsigned int M=((CompactADTable&&!is_distortion)?MaxSentLength:(m+1))-1;
	    if( is_distortion==0 )
	      for(j=1;j<=M; j++)
		{
		  total=0.0;
		  for(i=0;i<=L;i++)
		    {
		      total+=get(i, j, L, M);
		    }
		  if( total )
		    for(i=0;i<=L;i++)
		      {
			nParam++;
			aTable.getRef(i, j, L, M)=get(i, j, L, M)/total;
			massert(aTable.getRef(i,j,L,M)<=1.0);
			if( NoEmptyWord&&i==0 )
			  aTable.getRef(i,j,L,M)=0;
		      }
		}
	    else
	      for(i=0;i<=L;i++)
		{
		  total=0.0;
		  for(j=1;j<=M;j++)
		    total+=get(j, i, L, M);
		  if( total )
		    for(j=1;j<=M;j++)
		      {
			aTable.getRef(j, i, L, M)=amodel_smooth_factor/M+(1.0-amodel_smooth_factor)*get(j, i, L, M)/total;
			nParam++;
			massert(aTable.getRef(j,i,L,M)<=1.0);
			if( NoEmptyWord&&i==0 )
			  aTable.getRef(j,i,L,M)=0;
		      }
		}
	  }
      cout << "A/D table contains " << nParam << " parameters.\n";
    }

  void readTable(const char *filename); 
  void clear()
    {a.clear();}
};

/* ------------------- End of amodel Class Definitions ----------------------*/

#endif
