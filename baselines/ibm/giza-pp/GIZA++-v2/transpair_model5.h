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
#ifndef transpair_model5_h_fjo_defined
#define transpair_model5_h_fjo_defined
#include "Array2.h"
#include "defs.h"
#include "Vector.h"
#include "NTables.h"
#include "ATables.h"
#include "TTables.h"
#include "alignment.h"
#include "D5Tables.h"
#include "transpair_model4.h"

extern double factorial(int n);

inline int vacancies(const Vector<char>&vac,int u)
{
  int n=0;
  const char *i=&(vac[0])+1;
  const char *end=&(vac[0])+u+1;
  while(i<end)
    n+= ((*i++)==0);
  return n;
}

class transpair_model5 : public transpair_model4
{
 private:
  const d5model&d5m;
  bool doModel4Scoring;
 public:
  typedef transpair_model3 simpler_transpair_model;
  mutable map<Vector<PositionIndex>,LogProb> scores[4];
  transpair_model5(const Vector<WordIndex>&es, const Vector<WordIndex>&fs, tmodel<COUNT, PROB>&tTable, 
		   amodel<PROB>&aTable, amodel<PROB>&dTable, nmodel<PROB>&nTable, double _p1, double _p0, 
		   const d5model*_d5m) 
    : transpair_model4(es, fs, tTable, aTable, dTable, nTable, _p1, _p0,&_d5m->d4m),d5m(*_d5m),doModel4Scoring(0) {}
  LogProb scoreOfAlignmentForChange(const alignment&a)const
    {
      if( doModel4Scoring )
	return transpair_model4::prob_of_target_and_alignment_given_source(a,2); 
      else
	return prob_of_target_and_alignment_given_source(a,2); 
    }
  LogProb scoreOfMove(const alignment&a, WordIndex new_i, WordIndex j,double thisValue=-1.0)const;
  LogProb scoreOfSwap(const alignment&a, WordIndex j1, WordIndex j2,double thisValue=-1.0)const ;
  LogProb _scoreOfMove(const alignment&a, WordIndex new_i, WordIndex j,double thisValue=-1.0)const;
  LogProb _scoreOfSwap(const alignment&a, WordIndex j1, WordIndex j2,double thisValue=-1.0)const ;
  int modelnr()const{return 5;}
  LogProb prob_of_target_and_alignment_given_source(const alignment&al, short distortionType=3,bool verb=0)const;
  void computeScores(const alignment&al,vector<double>&d)const;
};
#endif
