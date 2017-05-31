/*

Copyright (C) 1999,2000,2001  Franz Josef Och (RWTH Aachen - Lehrstuhl fuer Informatik VI)

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
#include "MoveSwapMatrix.h"

template<class TRANSPAIR>
MoveSwapMatrix<TRANSPAIR>::MoveSwapMatrix(const TRANSPAIR&_ef, const alignment&_a)
  : alignment(_a), ef(_ef), l(ef.get_l()), m(ef.get_m()), _cmove(l+1, m+1), _cswap(m+1, m+1), 
  delmove(l+1, m+1,0),delswap(m+1, m+1,0),changed(l+2, 0), changedCounter(1), 
  modelnr(_ef.modelnr()),lazyEvaluation(0),centerDeleted(0)
{
  double thisValue=ef.scoreOfAlignmentForChange((*this));
  if( lazyEvaluation==0)
    for(WordIndex j=1;j<=m;j++)updateJ(j, 0,thisValue);
}

template<class TRANSPAIR>
void MoveSwapMatrix<TRANSPAIR>::updateJ(WordIndex j, bool useChanged,double thisValue)
{
  massert( lazyEvaluation==0 );
  for(WordIndex i=0;i<=l;i++)
    if( (useChanged==0||changed[i]!=changedCounter) )
      if( get_al(j)!=i ) 
	_cmove(i, j)=ef.scoreOfMove((*this), i, j,thisValue);
      else
	_cmove(i, j)=1.0;
  for(WordIndex j2=j+1;j2<=m;j2++)
    if( get_al(j)!=get_al(j2) )
      _cswap(j, j2)=ef.scoreOfSwap((*this), j, j2,thisValue);
    else
      _cswap(j, j2)=1.0;
  for(WordIndex j2=1;j2<j;j2++)
    if( get_al(j)!=get_al(j2) )
      _cswap(j2, j)=ef.scoreOfSwap((*this), j2, j,thisValue);
    else
      _cswap(j2, j)=1.0;
}
template<class TRANSPAIR>
void MoveSwapMatrix<TRANSPAIR>::updateI(WordIndex i,double thisValue)
{
  massert( lazyEvaluation==0);
  for(WordIndex j=1;j<=m;j++)
    if( get_al(j)!=i )
      _cmove(i, j)=ef.scoreOfMove((*this), i, j,thisValue);
    else
      _cmove(i, j)=1.0;
}

template<class TRANSPAIR>
void MoveSwapMatrix<TRANSPAIR>::printWrongs()const{
  for(WordIndex i=0;i<=l;i++)
    {
      for(WordIndex j=1;j<=m;j++)
	if( get_al(j)==i)
	  cout << "A";
	else
	  {
	    LogProb real=_cmove(i, j), wanted=ef.scoreOfMove((*this), i, j);
	    if( fabs(1.0-real/wanted)>1e-3 )
	      cout << 'b';
	    else if(fabs(1.0-real/wanted)>1e-10 )
	      cout << 'e';
	    else if(real!=wanted)
	      cout << 'E';
	    else
	      cout << ' ';
	  }
      cout << endl;
    }
  cout << endl;
  for(WordIndex j=1;j<=m;j++)
    {
      for(WordIndex j1=1;j1<=m;j1++)
	if( j1>j )
	  {
	    if( get_al(j)==get_al(j1) )
	      cout << 'A';
	    else 
	      cout << (_cswap(j, j1)==ef.scoreOfSwap((*this), j, j1));
	  }
	else
	  cout << ' ';
      cout << endl;  
    }
  massert(0);
}
template<class TRANSPAIR>
bool MoveSwapMatrix<TRANSPAIR>::isRight()const{
  if( lazyEvaluation ) 
    return 1;
  for(WordIndex i=0;i<=l;i++)
    for(WordIndex j=1;j<=m;j++)
      if( get_al(j)!=i && (!(doubleEqual(_cmove(i, j), ef.scoreOfMove((*this), i, j)))) )
	{
	  cerr << "DIFF: " << i << " " << j << " " << _cmove(i, j) << " " << ef.scoreOfMove((*this), i, j) << endl;
	  return 0;
	}
  for(WordIndex j=1;j<=m;j++)
    for(WordIndex j1=1;j1<=m;j1++)
      if( j1>j&&get_al(j)!=get_al(j1)&&(!doubleEqual(_cswap(j, j1), ef.scoreOfSwap((*this), j, j1))) )
	{
	  cerr << "DIFFERENT: " << j << " " << j1 << " " << _cswap(j, j1) << " " << ef.scoreOfSwap((*this), j, j1) << endl;
	  return 0;
	}
  return 1;
}

template<class TRANSPAIR>
void MoveSwapMatrix<TRANSPAIR>::doMove(WordIndex _i, WordIndex _j)
{
  WordIndex old_i=get_al(_j);
  if( lazyEvaluation )
    set(_j,_i);
  else
    {
      if ( modelnr==5||modelnr==6 )
	{
	  set(_j, _i);
	  double thisValue=ef.scoreOfAlignmentForChange((*this));
	  for(WordIndex j=1;j<=m;j++)updateJ(j, 0,thisValue);
	}
      else if ( modelnr==4 )
	{
	  changedCounter++;
	  for(unsigned int k=prev_cept(old_i);k<=next_cept(old_i);++k)changed[k]=changedCounter;
	  for(unsigned int k=prev_cept(_i);k<=next_cept(_i);++k)changed[k]=changedCounter;
	  set(_j, _i);
	  for(unsigned int k=prev_cept(old_i);k<=next_cept(old_i);++k)changed[k]=changedCounter;
	  for(unsigned int k=prev_cept(_i);k<=next_cept(_i);++k)changed[k]=changedCounter;
	  double thisValue=ef.scoreOfAlignmentForChange((*this));
	  for(unsigned int i=0;i<=l;i++)
	    if(changed[i]==changedCounter)
	      updateI(i,thisValue);
	  for(unsigned int j=1;j<=m;j++)
	    if( changed[get_al(j)]==changedCounter )
	      updateJ(j, 1,thisValue);
	}
      else
	{
	  assert(modelnr==3);
	  set(_j, _i);
	  changedCounter++;
	  double thisValue=ef.scoreOfAlignmentForChange((*this));
	  updateI(old_i,thisValue);
	  changed[old_i]=changedCounter;
	  updateI(_i,thisValue);
	  changed[_i]=changedCounter;
	  for(WordIndex j=1;j<=m;j++)
	    if( get_al(j)==_i || get_al(j)==old_i )
	      updateJ(j, 1,thisValue);
	}
    }
}
template<class TRANSPAIR>
void MoveSwapMatrix<TRANSPAIR>::doSwap(WordIndex _j1, WordIndex _j2)
{
  assert( cswap(_j1, _j2)>1 );
  WordIndex i1=get_al(_j1), i2=get_al(_j2);
  if( lazyEvaluation==1 )
    {
      set(_j1, i2);
      set(_j2, i1);
    }
  else
    {
      if ( modelnr==5||modelnr==6 )
	{
	  set(_j1, i2);
	  set(_j2, i1);
	  double thisValue=ef.scoreOfAlignmentForChange((*this));
	  for(WordIndex j=1;j<=m;j++)updateJ(j, 0,thisValue);
	}
      else if( modelnr==4 )
	{
	  changedCounter++;
	  for(unsigned int k=prev_cept(i1);k<=next_cept(i1);++k)changed[k]=changedCounter;
	  for(unsigned int k=prev_cept(i2);k<=next_cept(i2);++k)changed[k]=changedCounter;
	  set(_j1, i2);
	  set(_j2, i1);
	  double thisValue=ef.scoreOfAlignmentForChange((*this));
	  for(unsigned int i=0;i<=l;i++)
	    if(changed[i]==changedCounter)
	      updateI(i,thisValue);
	  for(unsigned int j=1;j<=m;j++)
	    if( changed[get_al(j)]==changedCounter )
	      updateJ(j, 1,thisValue);
	}
      else
	{
	  assert(modelnr==3);
	  set(_j1, i2);
	  set(_j2, i1);
	  changedCounter++;
	  double thisValue=ef.scoreOfAlignmentForChange((*this));
	  updateI(i1,thisValue);
	  changed[i1]=changedCounter;
	  updateI(i2,thisValue);
	  changed[i2]=changedCounter;
	  updateJ(_j1, 1,thisValue);
	  updateJ(_j2, 1,thisValue);
	}
    }
}

#include "transpair_model3.h"
#include "transpair_model4.h"
#include "transpair_model5.h"
#include "transpair_modelhmm.h"
template class MoveSwapMatrix<transpair_model3>;
template class MoveSwapMatrix<transpair_model4>;
template class MoveSwapMatrix<transpair_model5>;
template class MoveSwapMatrix<transpair_modelhmm>;
