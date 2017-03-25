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
#ifndef transpair_model4_h_fjo_defined
#define transpair_model4_h_fjo_defined
#include "Array2.h"
#include "defs.h"
#include "Vector.h"
#include "NTables.h"
#include "ATables.h"
#include "TTables.h"
#include "alignment.h"
#include "D4Tables.h"
#include "transpair_model3.h"

extern double factorial(int n);

class transpair_model4 : public transpair_model3
{
 private:
  d4model&d4m;
  Array2<double> probSecond;
  Vector<Array2<double> > probFirst;
 public:
  typedef transpair_model3 simpler_transpair_model;
  transpair_model4(const Vector<WordIndex>&es, const Vector<WordIndex>&fs, tmodel<COUNT, PROB>&tTable, amodel<PROB>&aTable, amodel<PROB>&dTable, nmodel<PROB>&nTable, double _p1, double _p0,d4model*_d4m) 
    : transpair_model3(es, fs, tTable, aTable, dTable, nTable, _p1, _p0), 
    d4m(*_d4m),probSecond(m+1,m+1,0.0),probFirst(l+1)
    {
      for(unsigned int j1=1;j1<=m;++j1)
	for(unsigned int j2=1;j2<j1;++j2)
	  {
	    probSecond(j1,j2)=d4m.getProb_bigger(j1,j2,0,d4m.fwordclasses.getClass(get_fs(j1)),l,m);
	  }
      for(unsigned int i=0;i<=l;++i)
	{
	  Array2<double> &pf=probFirst[i]=Array2<double>(m+1,m+1,0.0);
	  for(unsigned int j1=1;j1<=m;++j1)
	    {
	      map<m4_key,d4model::Vpff,compare1 >::const_iterator ci=d4m.getProb_first_iterator(d4m.ewordclasses.getClass(get_es(i)),d4m.fwordclasses.getClass(get_fs(j1)),l,m);
	      for(unsigned int j2=0;j2<=m;++j2)
		{
		  pf(j1,j2)=d4m.getProb_first_withiterator(j1,j2,m,ci);
		  massert(pf(j1,j2)==d4m.getProb_first(j1,j2,d4m.ewordclasses.getClass(get_es(i)),d4m.fwordclasses.getClass(get_fs(j1)),l,m));
		}
	    }
	}
    }
  LogProb prob_of_target_and_alignment_given_source_1(const alignment&al,bool verb)const;
  LogProb scoreOfAlignmentForChange(const alignment&a)const
    {return prob_of_target_and_alignment_given_source(a,2); }  
  LogProb scoreOfMove(const alignment&a, WordIndex new_i, WordIndex j,double thisValue=-1.0)const;
  LogProb scoreOfSwap(const alignment&a, WordIndex j1, WordIndex j2,double thisValue=-1.0)const ;
  LogProb _scoreOfMove(const alignment&a, WordIndex new_i, WordIndex j,double thisValue=-1.0)const;
  LogProb _scoreOfSwap(const alignment&a, WordIndex j1, WordIndex j2,double thisValue=-1.0)const ;
  int modelnr()const{return 4;}
  LogProb prob_of_target_and_alignment_given_source(const alignment&al, short distortionType=3,bool verb=0)const;
  void computeScores(const alignment&al,vector<double>&d)const;
};
#endif
